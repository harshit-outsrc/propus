from unittest import TestCase
from unittest.mock import Mock

from mock_alchemy.mocking import AlchemyMagicMock

from propus.security.validation import (
    KeyCDN,
    security_validation,
    validate_asn,
    validate_domain,
)
from propus.calbright_sql.security_asn import ASN
from propus.calbright_sql.security_domain import Domain


class TestSecurityValidation(TestCase):
    def setUp(self) -> None:
        # Test data
        self.ip = "8.8.8.8"
        self.host = "baz.com"
        self.email = "foo.bar@baz.com"
        self.asn = ASN(asn=15169, flag=False)
        self.domain = Domain(name="baz.com", flag=False)
        self.results_dict = {
            "test_validate_ip": {"data": {"geo": {"asn": 15169}}},
            "test_security_validation": {"data": {"geo": {"asn": 15169}}},
            "test_validate_email": self.domain,
        }

        KeyCDN.get_geo_json = Mock(side_effect=self.return_data)

        session = AlchemyMagicMock()
        session.add(self.asn)
        session.add(self.domain)
        session.execute.return_value.scalars.return_value.first.return_value = self.domain
        session.execute.return_value.scalars.return_value.one.return_value = self.asn
        self.session = session

    def return_data(self, host_string):
        return self.results_dict.get(self.test_name, None)

    def test_validate_email(self):
        self.test_name = "test_validate_email"
        self.session.return_value = self.domain
        result = validate_domain(self.session, self.email)
        self.assertEqual(result.name, self.domain.name)
        self.assertEqual(result.flag, self.domain.flag)

    def test_validate_host(self):
        self.test_name = "test_validate_host"
        result = validate_domain(self.session, self.host)
        self.assertEqual(result.name, self.domain.name)
        self.assertEqual(result.flag, self.domain.flag)

    def test_validate_ip(self):
        self.test_name = "test_validate_ip"
        result = validate_asn(self.session, self.ip)
        self.assertEqual(result.asn, self.asn.asn)
        self.assertEqual(result.flag, self.asn.flag)

    def test_security_validation(self):
        self.test_name = "test_security_validation"
        results = security_validation(self.session, self.email, self.ip)
        domain = results[0]
        asn = results[1]
        self.assertEqual(2, len(results))
        self.assertEqual(domain.name, self.domain.name)
        self.assertEqual(domain.flag, self.domain.flag)
        self.assertEqual(asn.asn, self.asn.asn)
        self.assertEqual(asn.flag, self.asn.flag)


if __name__ == "__main__":
    import unittest

    unittest.main()
