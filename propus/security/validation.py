from typing import AnyStr, List
from sqlalchemy import select

from propus.helpers.sql_alchemy import get_or_create
from propus.key_cdn import KeyCDN
from propus.logging_utility import Logging
from propus.calbright_sql.security_asn import ASN
from propus.calbright_sql.security_domain import Domain


logger = Logging.get_logger("security_validation")


def validate_asn(session, ip_address: AnyStr = None) -> ASN:
    """
    Gets or creates ASN from IP address.

    Args:
        session: Sql Alchemy database session
        ip_address (AnyStr): IP address (or host name) to get ASN from

    Returns:
        ASN object
    """
    key_cdn_client = KeyCDN.build()
    asn_response = key_cdn_client.get_geo_json(ip_address)
    asn = asn_response.get("data", {}).get("geo", {}).get("asn")
    if asn:
        security_asn, asn_created = get_or_create(
            session,
            model=ASN,
            asn=asn,
        )
        asn_result = "created" if asn_created else "found"
        logger.info(f"Validation: {security_asn} {asn_result}.")
    else:
        security_asn = None
        logger.info(f"Validation failed: unable to resolve ASN from {ip_address}.")

    return security_asn


def validate_domain(session, domain_string: AnyStr = None) -> Domain:
    """
    Checks if a security domain exists for the domain name or email provided; if not, checks whether
    there is a flagged TLD; if not then a new security domain is created with flag=False

    Args:
        session: Sql Alchemy database session
        domain_string (AnyStr): Email address or domain to validate

    Returns:
        Domain object
    """
    domain_created = False

    if "@" in domain_string:
        domain_name = domain_string.split("@")[1:][0]
    else:
        domain_name = domain_string if not domain_string.startswith(".") else domain_string[1:]
    security_domain = session.execute(select(Domain).filter_by(name=domain_name).limit(1)).scalars().first()

    if not security_domain:
        tld = domain_name if "." not in domain_name else domain_name.split(".")[-1:][0]
        security_domain = session.execute(select(Domain).filter_by(name=tld).limit(1)).scalars().first()
        if not security_domain or not security_domain.flag:
            security_domain, domain_created = get_or_create(
                session,
                model=Domain,
                name=domain_name,
            )

    domain_result = "created" if domain_created else "found"
    logger.info(f"Validation: {security_domain} {domain_result}.")

    return security_domain


def security_validation(session, email: AnyStr = None, ip_address: AnyStr = None) -> List:
    """
    Validates Domain and ASN from email address from CCCApply.
    Replaces / expands upon steps 9 and 15 in https://zapier.com/editor/128028157/published (accessed 2023-06-05)
    Args:
        session: Sql Alchemy database session
        email (AnyStr): Email address / domain to verify
        ip_address (AnyStr): IP address to verify ASN

    Returns:
        List of validated objects
    """
    validated_objects = []
    if email:
        security_domain = validate_domain(session, email)
        if security_domain:
            validated_objects.append(security_domain)

    if ip_address:
        security_asn = validate_asn(session, ip_address)
        if security_asn:
            validated_objects.append(security_asn)

    return validated_objects
