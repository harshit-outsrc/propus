import os
from setuptools import setup, find_packages


def fetch_dependencies():
    dependencies = ["JSON-log-formatter~=0.5.1"]
    if os.environ.get("NO_DEPENDENCIES"):
        return dependencies

    requests_sevice = "requests>=2.0.0"

    test_dependencies = [
        "coverage>=4.5.1",
        "flake8>=6.0.0",
        "moto[all]>=4.1.0,<5.0",
        "mock-alchemy>=0.2.6",
    ]

    dependency_management = {
        "api_handler": [requests_sevice],
        "anthology": [requests_sevice],
        "aws": ["backoff==1.10", "boto3~=1.14", "botocore~=1.18", "ssm_cache<3.0"],
        "dialpad": [requests_sevice, "python-dialpad>=2.2.2"],
        "geolocator": ["geopy>=2.4.0"],
        "gsuite": ["PyDrive>=1.3.1", "gspread>=5.10.0"],
        "hubspot": [requests_sevice, "hubspot-api-client>=8.2.1"],
        "salesforce": [requests_sevice],
        "sql": [
            "alembic>=1.10.0",
            "psycopg2-binary~=2.8",
            "SQLAlchemy>=2.0.0",
            "alembic-utils>=0.8.2",
            "alembic-postgresql-enum<=2.0.0",
        ],
        "slack": [requests_sevice, "slack_sdk>=3.27.0", "certifi>=2024.6.2"],
        "twilio": [requests_sevice, "twilio>=8.13.0"],
    }

    if os.environ.get("PROPUS"):
        dependencies += list(
            set(
                [
                    d
                    for req in os.environ.get("PROPUS").split(",")
                    for d in dependency_management.get(req)
                    if dependency_management.get(req)
                ]
            )
        )

    if len(dependencies) == 1:
        dependencies += list(set([d for deps in dependency_management.values() for d in deps]))

    if os.environ.get("TESTS") == "True":
        dependencies += test_dependencies
    return dependencies


setup(
    name="propus",
    version="0.0.1",
    description="Calbright Shared Python libraries",
    author="Calbright",
    packages=find_packages(),
    install_requires=fetch_dependencies(),
    python_requires=">=3.9",
)
