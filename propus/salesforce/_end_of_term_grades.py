import json


@staticmethod
def _fetch_program_enrollment_data(args):
    kwarg_dict = {
        "enrollment_status": "Enrollment_Status__c",
        "program_name": "Program_Name__c",
        "date_of_enrollment": "Date_of_Enrollment__c",
        "contact": "Contact__c",
    }
    return {val: args.get(key) for key, val in kwarg_dict.items() if args.get(key)}


@staticmethod
def _fetch_instructor(course, instructor_id=None):
    course_instructor_map = {
        "BUS500": "0055G000008sii8QAA",
        "BUS501": "0055G000008sii8QAA",
        "BUS520": "0055G000009SBSjQAO",
        "BUS521": "0055G000009SBSjQAO",
        "BUS522": "0055G000009SBSjQAO",
        "MC500": "0053k00000BCncAAAT",
        "HC501": "0053k00000BCncAAAT",
        "HC502": "0053k00000BCncAAAT",
        "IT500": "0053k00000AtV4PAAV",
        "IT510": "0053k00000BCgfwAAD",
        "IT520": "0053k00000AtJBpAAN",
        "IT525": "0053k00000AtJBpAAN",
        "IT532": "0055G000009SBSoQAO",
        "IT533": "0055G000009SBSoQAO",
        "WF500": "0053k00000BCgg1AAD",
    }
    return instructor_id if instructor_id else course_instructor_map.get(course)


@staticmethod
def _format_course_name(course):
    course_name_map = {
        "BUS500": "BUS500 - Introduction to Structured Data",
        "BUS501": "BUS501 - Application of Structured Data",
        "BUS520": "BUS520 - Project Management Foundations",
        "BUS521": "BUS521 - Project Management Fundamentals",
        "BUS522": "BUS522 - Project Plan Development",
        "HC501": "HC501 - Equitable Health Impacts: DEI - Part 1",
        "HC502": "HC502 - Equitable Health Impacts: DEI - Part 2",
        "MC500": "MC500 - Medical Coding for Professional Services",
        "IT500": "IT500 - Introduction to Information Technology Support",
        "IT510": "IT510 - Introduction to Cybersecurity",
        "IT520": "IT520 - Customer Relationship Management (CRM) Technology",
        "IT525": "IT525 - Customer Relationship Management (CRM) Platform Administration",
        "IT532": "IT532 - Introduction to Networks",
        "IT533": "IT533 - Introduction to Networks Virtual Lab",
        "WF500": "WF500 - College and Career Essential Skills",
    }
    return course_name_map.get(course)


def create_end_of_term_grade(self, course, ccc_id, sf_id, term_id, term_name, instructor_id=None):
    """
    Create a new end of term grade record on Salesforce.

    Args:
        course_id (str): The ID of the course associated with the grade.
        student_id (str): The ID of the student receiving the grade.
        grade (str): The letter grade (e.g. 'A', 'B', 'C').
        term (str): The academic term (e.g. 'Fall 2022').
        instructor_id (str): The ID of the instructor assigning the grade.

    Returns:
        The Salesforce JSON Response

    Raises:
        FailedRequest: If the API request to create the record fails.
        MissingElement: If required fields are missing from the request.
    """

    payload = {
        "Course__c": self._format_course_name(course),
        "Instructor__c": self._fetch_instructor(course, instructor_id),
        "Name": f"{ccc_id}-{course}-{term_name}",
        "Status__c": "NOT GRADED",
        "Student__c": sf_id,
        "Term__c": term_id,
    }
    url = self._get_endpoint("create_end_of_term_grade")
    return self.make_request(url, data=json.dumps(payload), req_type="post")


def update_end_of_term_grade(self, grade_id, lookup_student=True, **kwargs):
    """
    Update an end of term grade record on Salesforce.

    Args:
        grade_id (str): The ID of the grade record to update.
        kwargs (dict): The updated field values to set on the grade record.
            Expected keys are 'Course__c', 'Instructor__c' and any other
            grade fields.

    Returns:
        None

    Raises:
        FailedRequest: If the API request fails with status 400
        TooManyRequests: If the API rate limit is exceeded
        MissingElement: If the grade record is not found
        MethodNotAllowed: For unsupported HTTP methods
    """
    payload = kwargs
    if "Course__c" in payload:
        payload["Course__c"] = self._format_course_name(payload["Course__c"])
    if "Instructor__c" in payload and lookup_student:
        payload["Instructor__c"] = self._fetch_instructor(payload["Course__c"], payload["Instructor__c"])
    url = self._get_endpoint("update_end_of_term_grade", {"<grade_id>": grade_id})
    self.make_request(url, data=json.dumps(payload), req_type="patch")


def delete_end_of_term_grade(self, grade_id):
    """
    Delete an end of term grade record on Salesforce.

    Args:
        grade_id (str): The ID of the grade record to update.
    Returns:
        None

    Raises:
        FailedRequest: If the API request fails with status 400
        TooManyRequests: If the API rate limit is exceeded
        MissingElement: If the grade record is not found
        MethodNotAllowed: For unsupported HTTP methods
    """
    url = self._get_endpoint("delete_end_of_term_grade", {"<grade_id>": grade_id})
    self.make_request(url, req_type="delete")
