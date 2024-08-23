import json


async def copy_class_schedule(self, source_term_id: str, target_term_id: str) -> dict:
    """
    Copy one course schedule from a source term to a target term

    Args:
        source_term_id (str): source term id
        target_term_id (str): target term id

    Returns:
        dict: Anthology copy course schedule response
    """
    payload = {
        "CampusId": 5,
        "CopyClassScheduleOption": "ALL",
        "CourseId": 2,
        "ExtendedPropertyList": [
            {"IsExtendedProperty": True, "Name": "XB01 Accounting Method"},
            {"IsExtendedProperty": True, "Name": "XB02 Date First Census"},
            {"IsExtendedProperty": True, "Name": "XB04 Contract Education Code"},
            {"IsExtendedProperty": True, "Name": "XB08 DSPS Special Status"},
            {"IsExtendedProperty": True, "Name": "XB09 Work Based Learning Activities"},
            {"IsExtendedProperty": True, "Name": "XB10 CVU/CVC Status"},
            {"IsExtendedProperty": True, "Name": "XB12 Instructional Material Cost"},
            {"IsExtendedProperty": True, "Name": "Census Date"},
        ],
        "Id": 0,
        "IsCopyAttendanceRules": True,
        "IsCopyBookList": True,
        "IsCopyCourseFeeSchedule": True,
        "IsCopyCourseSharingCampuses": True,
        "IsCopyDays": True,
        "IsCopyDocuments": True,
        "IsCopyGradeBook": True,
        "IsCopyHideFaculty": True,
        "IsCopyHideLocation": True,
        "IsCopyInstructor": True,
        "IsCopyLmsVendor": False,
        "IsCopyMaxCourseSections": True,
        "IsCopyRegistrationRelationships": True,
        "IsCopyRooms": True,
        "IsCopySecondaryInstructor": True,
        "IsCopySelectedOnlyAndCrossList": True,
        "IsCopyTimes": True,
        "IsCopyWaitList": True,
        "IsCrossList": True,
        "IsInstructorAttributes": True,
        "IsOnlyValidation": False,
        "IsSecondSecondaryCode": True,
        "isValidationMessageDisplayed": False,
        "IsVariableCredits": True,
        "NewSectionCode": "",
        "SourceTermId": source_term_id,
        "TargetTermID": target_term_id,
    }

    return self.make_request(
        req_type="post", url=self._get_endpoint("copy_class_schedule"), data=json.dumps({"payload": payload})
    )
