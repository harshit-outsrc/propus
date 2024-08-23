from datetime import datetime
from math import ceil

CURRENT_COURSE_VERSION_MAP = {
    "IT500": "5.0",
    "WF500": "5.0",
    "IT520": "2.0",
    "IT525": "3.0",
    "IT510": "5.0",
    # "BUS500": "2.0",
    # "BUS501": "2.0",
    "BUS500": "3.0",  # TODO: Updated for testing, verify if this will be the correct version...
    "BUS501": "3.0",  # TODO: Updated for testing, verify if this will be the correct version...
    "IT532": "1.0",
    "IT533": "1.0",
    "HC501": "1.0",
    "HC502": "1.0",
    "HC501": "1.0",
    "HC502": "1.0",
    "MC500": "2.0",
    "BUS520": "1.0",
    "BUS521": "1.0",
    "BUS522": "1.0",
}


COURSE_TO_INSTRUCTOR_MAP = {
    "WF500": "ashley@calbright.org",
    "BUS500": "catherine.parker@calbright.org",
    "BUS501": "catherine.parker@calbright.org",
    "BUS520": "ellen.rinker@calbright.org",
    "BUS521": "ellen.rinker@calbright.org",
    "BUS522": "ellen.rinker@calbright.org",
    "MC500": "cindy@calbright.org",
    "HC501": "cindy@calbright.org",
    "HC502": "cindy@calbright.org",
    "IT510": "elizabeth@calbright.org",
    "IT520": "elizabeth@calbright.org",
    "IT525": "elizabeth@calbright.org",
    "IT500": "michael@calbright.org",
}


PROGRAM_TO_COURSE_VERSION_MAP = {
    "IT Support": {"IT500": "5.0", "WF500": "5.0"},
    "Customer Relationship Management": {"IT520": "2.0", "IT525": "3.0"},
    "Cybersecurity": {"IT510": "5.0", "WF500": "5.0"},
    # "Data Analysis": {"BUS500": "2.0", "BUS501": "2.0"},
    "Data Analysis": {"BUS500": "3.0", "BUS501": "3.0"},  # TODO: Updated for testing, verify if correct...
    "T2T Intro to Networks": {"IT532": "1.0", "IT533": "1.0"},
    "HC DEI": {"HC501": "1.0", "HC502": "1.0"},
    "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion": {"HC501": "1.0", "HC502": "1.0"},
    "Medical Coding": {"MC500": "2.0", "WF500": "1.0"},
    "Project Management": {"BUS520": "1.0", "BUS521": "1.0", "BUS522": "1.0"},
}


PROGRAM_SHORT_NAME_TO_SF_API_NAME = {
    "Customer Relationship Management": "T2T CRM Admin",
    "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion": "HC DEI",
}


def format_term_name(start_date: datetime):
    year_start = start_date.year
    if start_date.month <= 6:
        year_start -= 1
    year_start_date = datetime(year_start, 7, 1)
    term_num = ceil(((start_date - year_start_date).days + 1) / 7)
    return f"{year_start}-{str(year_start+1)[2:]}-TERM-{term_num:02}"
