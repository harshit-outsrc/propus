from datetime import datetime
import json
import unittest
from unittest.mock import MagicMock, Mock

from propus.anthology import Anthology


class BaseAnthologyTests(unittest.TestCase):
    def setUp(self) -> None:
        url = "https://anthology.student.1234567890.com"
        self.url = "https://anthology.student.1234567890.com"
        self.application_key = "Authorization some_testing_jwt!"
        self.anthology = Anthology(url=url, application_key=self.application_key)
        self.test_name = None
        self.req_mock = MagicMock()
        self.req_mock.get = Mock(side_effect=self.get_request)
        self.req_mock.post = Mock(side_effect=self.post_request)
        self.anthology.requests_service = self.req_mock
        self.expected_response = {"payload": {"data": "successful call"}}
        self.iteration = None
        self.test_key = None

        self.test_data = {
            "course_id": "calbright_1234",
            "student_id": "12345678",
            "enrollment_id": "4123415",
            "student_number": "XF12345",
            "first_name": "Johnny",
            "last_name": "Appleseed",
            "student_enrollment_id": 12345,
            "notes": "These are the notes",
            "YYYYY/MM/DD": "2020/02/02",
            "YYYYY/MM/DD_2": "2023/01/03",
            "degree_id": 4321,
            "grade": "EXCELLENT",
            "date_completed": "2023-01-04",
            "status_id": 88,
        }

        self._url_mapping = {
            "course_by_id": f"{url}/api/commands/Academics/StudentCourse/get",
            "fetch_class_terms": f"{url}/ds/campusnexus/Terms/CampusNexus.GetStudentCourseRegistrationTermListCustom(campusId=5,courseIds='1,2,3')?$select=TermName,TermCode,Id,TermStartDate,TermEndDate,CodeAndName&%24format=json&%24count=true&%24orderby=TermCode",  # noqa:E501
            "fetch_student_classes": f"{url}/ds/campusnexus/ClassSections/CampusNexus.GetStudentCourseRegistrationClassScheduleList(campusId=5,termId=4321,courseIds='1,2,3',isCrossReferenceCourse=false,studentId=1234,crossRefCourseId=0, isTransferSection = false)?$select=Id,CourseCode,CourseName,SectionCode,SectionName,CourseId,CampusId,StartDate,EndDate,IsActive,DeliveryMethodName,InstructorName&$orderby=CourseName,SectionCode",  # noqa:E501
            "fetch_all_courses": f'{url}/api/course-registration/students/{self.test_data.get("student_id")}/student-enrollment-periods/{self.test_data.get("enrollment_id")}/student-courses',
            "billing_method": f"{url}/ds/campusnexus/BillingMethods?$filter=Id eq 1",
            "catalog_year": f"{url}/ds/campusnexus/ProgramVersions/CampusNexus.GetAreaOfStudyCatalogList(programVersionId=123)?&$format=json&$count=true&$filter=IsMapped eq true and IsActive eq true or(Id eq 123 and IsActive eq false)&$orderby=Name",
            "grade_level": f"{url}/ds/campusnexus/GradeLevels?&$format=json&$count=true&$filter=IsActive eq true&$orderby=Name",
            "program": f"{url}/ds/campusnexus/Programs/CampusNexus.GetEnrollmentProgramList(campusId=5,degreeProgram=0)?&$format=json&$filter=IsActive eq true or (Id eq 0)&$orderby=Name",
            "program_version": f"{url}/ds/campusnexus/ProgramVersions/CampusNexus.GetEnrollmentProgramVersions(campusId=5)?&$format=json&$count=true&$filter=ProgramId eq 123 and IsActive eq true and IsDegreeProgram eq false or (Id eq 0)&$orderby=Name",
            "shift": f"{url}/ds/campusnexus/Shifts?$select=Id,Code,Name,IsActive&$format=json&$count=true&$filter=CampusGroup/CampusList/any(cl:cl/CampusId eq 5) and IsActive eq true&$orderby=Name",
            "start_dates": f"{url}/ds/campusnexus/SchoolStartDates/CampusNexus.GetEnrollmentSchoolStartDates(campusId=5,programVersionId=123)?&$format=json&$count=true&$filter=IsActive eq true&$orderby=StartDate desc",
            "student_by_id": f"{url}/api/commands/Common/Student/get",
            "student_search": f"{url}/ds/campusnexus/Students?%24filter=FirstName eq '{self.test_data.get('first_name')}' and LastName eq '{self.test_data.get('last_name')}' and StudentNumber eq '{self.test_data.get('student_number')}'",
            "add_new_course": f"{url}/api/commands/Academics/StudentCourse/saveNew",
            "register_course": f"{url}/api/commands/Academics/StudentCourse/savestudentcourse",
            "add_attendance": f"{url}/api/commands/Academics/Attendance/PostExternshipOnlineHours",
            "create_certificate_all_fields": f"{url}/api/commands/Academics/StudentEnrollmentPeriodDegree/SaveNew",
            "create_certificate_min_fields": f"{url}/api/commands/Academics/StudentEnrollmentPeriodDegree/SaveNew",
            "post_grades_1": f"{url}/api/commands/Academics/StudentCourse/get",
            "post_grades_2": f"{url}/api/commands/Academics/StudentCourse/PostFinalGrade",
            "update_error_a_1": f"{url}/api/commands/Common/Student/get",
            "update_error_b_1": f"{url}/api/commands/Common/Student/get",
            "update_student_1": f"{url}/api/commands/Common/Student/get",
            "update_student_2": f"{url}/api/commands/Common/Student/Save",
            "get_ethnicities": f"{url}/ds/odata/Ethnicities?$filter=IsActive%20eq%20true&$select=Id,Name",
            "update_student_status": f"{url}/api/commands/Academics/StudentEnrollmentPeriod/EnrollmentStatusChange",
            "get_academic_terms": f"{url}/ds/odata/Terms?$orderby=StartDate&$select=Code,StartDate,EndDate,AddDropDate,Id",
            "term_create": f"{url}/api/commands/Academics/Term/SaveNew",
            "start_date_create": f"{url}/api/commands/Academics/ShiftSchoolStartDate/SaveNew",
            "get_genders": f"{url}/ds/odata/Genders?$filter=IsActive%20eq%20true&$select=Id,Name",
            "drop_course": f"{url}/api/commands/Academics/StudentCourse/DropCourse",
            "fetch_drop_reason": f"{url}/ds/campusnexus/StudentCourseStatusChangeReasons?$filter=IsForDrop%20eq%20true%20and%20IsActive%20eq%20true%20and%20CampusGroup/CampusList/any(c:%20c/CampusId%20eq%205)&$count=true",
            "reinstate_course": f"{url}/api/commands/Academics/StudentCourse/ReinstateCourse",
            "fetch_drop_letter_grades": f"{url}/ds/campusnexus/GradeScaleLetterGrades/CampusNexus.GetGradeScaleLetterGradeListByCriteria(gradeScaleId=1,isAuditGrade=false,isPassFail=false,isIncludeInactive=false,appendGradeCode='',isReturnAll=false)?$select=Id,Code&$filter=IsDropGrade%20eq%20true%20&$orderby=Code",
            "unregister_course": f"{url}/api/commands/Academics/StudentCourse/UnregisterStudentCourse",
            "fetch_unregister_reason": f"{url}/ds/campusnexus/StudentCourseStatusChangeReasons?$filter=IsForUnregister%20eq%20true%20and%20IsActive%20eq%20true%20and%20CampusGroup/CampusList/any(c:%20c/CampusId%20eq%205)",
        }

        self.expected_data = {
            "course_by_id": {"payload": {"id": self.test_data.get("course_id")}},
            "student_by_id": {"payload": {"id": self.test_data.get("student_id")}},
            "add_new_course": {
                "payload": {
                    "CampusId": 5,
                    "ClassSectionId": 2585,
                    "CourseId": 2,
                    "CourseName": "College and Career Essential Skills - Non Credit",
                    "CreatedDateTime": "2024-07-18T00:00:00",
                    "EndDate": "2024-04-22T00:00:00",
                    "IsPassFail": 1,
                    "LetterGrade": "",
                    "ModFlag": "A",
                    "Note": "Created via API",
                    "RetakeFeeWaived": "0",
                    "RetakeOverride": False,
                    "RosterFlag": "",
                    "StartDate": "2023-10-24T00:00:00",
                    "Status": "F",
                    "StudentEnrollmentPeriodId": 10320,
                    "StudentId": 9367,
                    "TermId": 175,
                }
            },
            "register_course": {
                "payload": {
                    "StudentCourseId": 12345,
                    "StudentEnrollmentPeriodId": 876432,
                    "CampusId": 5,
                    "ClassSectionId": 3425,
                    "CourseId": 6,
                    "TermId": 836,
                    "Hours": 10,
                    "Comments": "Registered Via API",
                    "Credits": 0,
                    "Action": 2,
                    "AllowOverrideRegistrationHold": True,
                    "IsAllowedToOverrideLockedTermSequence": True,
                    "IsAllowedPostCourseStartDateRegistration": True,
                    "Description": "",
                    "StartDate": "01/10/2020",
                    "EndDate": "06/10/2020",
                    "RetakeID": 0,
                    "ReturnCode": 0,
                    "IsPassFail": 1,
                    "RetakeFee": "O",
                    "IsAddDropPeriodClassSectionAllowed": True,
                    "IsAllowedToOverrideClosedTerm": True,
                    "IsAllowedToOverrideRegistrationGroup": True,
                    "IsPreCoRequisiteValidationSkipped": True,
                }
            },
            "add_attendance": {
                "payload": {
                    "StudentId": 98753,
                    "ClassSectionId": 8364,
                    "StartDate": "03-01-2023",
                    "EndDate": "04-01-2023",
                    "AllowClosedTerm": True,
                    "IsPostExternshipOnline": True,
                    "Entity": {
                        "Id": -1,
                        "ClassSectionMeetingDateId": 0,
                        "AttendanceDate": f'{datetime.now().strftime("%Y-%m-%d")}T00:00:00.000',
                        "Attended": 54,
                        "Absent": 0,
                        "Status": "A",
                        "AttendedStatus": "A",
                        "Type": "O",
                        "UnitType": "M",
                        "Note": "",
                        "StudentCourseId": 987,
                        "StudentEnrollmentPeriodId": 3746,
                        "EntityState": 0,
                    },
                }
            },
            "create_certificate_all_fields": {
                "payload": {
                    "id": -1,
                    "awardedDate": "2020/02/02 00:00:00",
                    "degreeId": 4321,
                    "note": "These are the notes",
                    "studentEnrollmentPeriodId": 12345,
                }
            },
            "create_certificate_min_fields": {
                "payload": {
                    "id": -1,
                    "awardedDate": f"{datetime.now().strftime('%Y/%m/%d')} 00:00:00",
                    "degreeId": 5,
                    "note": "These are the notes",
                    "studentEnrollmentPeriodId": 12345,
                }
            },
            "post_grades_2": {
                "payload": {
                    "PostFinalGradeForExistingGrade": False,
                    "AllowOverrideExpectedDeadlineDate": True,
                    "CampusId": 5,
                    "StudentCourse": {
                        "studentEnrollmentDpaCourseCategoryId": 13858,
                        "campusId": 5,
                        "id": 6970,
                        "academicYear": 0,
                        "classSectionId": 1879,
                        "clockHours": 30,
                        "clockHoursAttempted": 0,
                        "clockHoursEarned": 0,
                        "consecutiveMinutesAbsent": 0,
                        "cost": 0,
                        "courseId": 6,
                        "courseName": "Customer Relationship Management (CRM) Technology - Non Credit",
                        "createdDateTime": "2023/04/04 18:14:23",
                        "creditHours": 0,
                        "creditHoursAttempted": 0,
                        "creditHoursEarned": 0,
                        "enrollmentStatusClockHours": 0,
                        "enrollmentStatusCreditHours": 0,
                        "expectedEndDate": "2023/06/27 00:00:00",
                        "gradePoints": 0,
                        "gradeScaleId": 1,
                        "lda": "2023/04/04 00:00:00",
                        "letterGrade": "EXCELLENT",
                        "lmsExtractStatus": "R",
                        "makeUpMinutes": 0,
                        "minutesAbsent": 0,
                        "minutesAttended": 60,
                        "modFlag": "A",
                        "note": "Registered Via API",
                        "outsideCourseWorkHours": 0,
                        "payStatus": "Y",
                        "previousStatus": "C",
                        "requiredCourseId": 66,
                        "retakeFeeWaived": "O",
                        "startDate": "2022/12/27 00:00:00",
                        "status": "P",
                        "studentEnrollmentPeriodId": 2625,
                        "studentId": 17602,
                        "termId": 132,
                        "transferTypeId": 1,
                        "isPassFail": True,
                    },
                }
            },
            "update_student_status": {
                "payload": {
                    "StudentEnrollmentPeriodId": "4123415",
                    "NewSchoolStatusId": 88,
                    "EffectiveDate": "2020/02/02",
                    "LastAttendedDate": "2023/01/03",
                    "Note": "These are the notes",
                }
            },
            "term_create": {
                "payload": {
                    "id": -1,
                    "addDropDate": "2023/02/16 00:00:00",
                    "campusIdList": [5],
                    "code": "2022-23-TERM-01",
                    "startDate": "2023/01/17 00:00:00",
                    "endDate": "2023/07/17 00:00:00",
                    "isActive": True,
                    "name": "2022-23-TERM-01",
                    "shiftId": 0,
                    "termUsage": 4,
                    "sendCourseSectionDataToLms": True,
                    "sendInstructorAssignmentsToLms": True,
                    "sendStudentRegistrationDataToLms": True,
                }
            },
            "start_date_create": {
                "payload": {
                    "id": -1,
                    "campusGroupId": 0,
                    "code": "2022-23-TERM-01",
                    "isActive": True,
                    "name": "2022-23-TERM-01",
                    "shiftId": 0,
                    "startDate": "2023/01/17 00:00:00",
                    "campusGroup": {
                        "id": 9173,
                        "code": "K~990",
                        "isActive": True,
                        "name": "K~990",
                        "type": "K",
                        "campusList": [
                            {
                                "id": 9745,
                                "campusGroupId": 9173,
                                "campusId": 5,
                                "isCampusActive": True,
                            }
                        ],
                    },
                }
            },
            "drop_course": {
                "payload": {
                    "StudentEnrollmentScheduleId": 12345,
                    "DropDate": "2023/11/08 09:38:52",
                    "DropReasonId": 3425,
                    "AllowLdwOverride": True,
                    "LetterGrade": "PASS!",
                }
            },
            "reinstate_course": {"payload": {"StudentCourseId": 12345}},
            "unregister_course": {
                "payload": {
                    "IsUnregisterCall": True,
                    "IsMultipleUnregisterEnabled": True,
                    "StudentCourseId": 12345,
                    "Comments": "SOME REASON TO UNREGISTER",
                    "Description": "This is the full description!",
                }
            },
        }

        self.real_response = {
            "post_grades_1": {
                "payload": {
                    "data": {
                        "transcripNote": None,
                        "isCrsg": False,
                        "studentEnrollmentPeriodIdList": None,
                        "studentEnrollmentDpaCourseCategoryId": 13858,
                        "campusId": 5,
                        "studentTransferCreditMultipleCourseAssociationId": None,
                        "studentTransferCreditMultipleId": None,
                        "id": 6970,
                        "academicYear": 0,
                        "adEnrollRegistrationId": None,
                        "advisedDate": None,
                        "appealType": None,
                        "auditEffectiveDate": None,
                        "averageBestOfPercentFinal": None,
                        "billedDate": None,
                        "classSectionId": 1879,
                        "clockHours": 30,
                        "clockHoursAttempted": 0,
                        "clockHoursEarned": 0,
                        "collegeId": None,
                        "consecutiveMinutesAbsent": 0,
                        "cost": 0,
                        "courseAddedFrom": None,
                        "courseFeeScheduleId": None,
                        "courseId": 6,
                        "courseName": "Customer Relationship Management (CRM) Technology - Non Credit",
                        "createdDateTime": "2023/04/04 18:14:23",
                        "creditHours": 0,
                        "creditHoursAttempted": 0,
                        "creditHoursEarned": 0,
                        "crossReferenceCourseId": None,
                        "dateReqMet": None,
                        "dependentClassSectionId": None,
                        "dropDate": None,
                        "endDate": "2023/04/06 00:00:00",
                        "enrollmentStatusClockHours": 0,
                        "enrollmentStatusCreditHours": 0,
                        "examRegistrationComments": None,
                        "examStatus": None,
                        "expectedDeadlineDate": None,
                        "expectedEndDate": "2023/06/27 00:00:00",
                        "facultyPostedLda": None,
                        "faStudentAyPaymentPeriodId": None,
                        "finalGradeReasonId": None,
                        "gradePoints": 0,
                        "gradePostedDate": "2023/04/06 14:01:51",
                        "gradeScaleId": 1,
                        "highSchoolId": None,
                        "include": False,
                        "incompleteGradeNote": None,
                        "inProgressGrade": None,
                        "isAfterAddDrop": True,
                        "isAuditCourse": False,
                        "isAutoDrop": False,
                        "isCostScheduled": False,
                        "isCourseRefundPolicyUsed": False,
                        "isCrossReferencedCourse": None,
                        "isEnrollmentAdjusted": False,
                        "isExtended": False,
                        "isExtensionBilled": None,
                        "isFromPortal": None,
                        "isGlobalCumulativeIncluded": True,
                        "isHalfTicketGenerated": None,
                        "isIncludedInGpaCalc": False,
                        "isIncompleteGradeReplaced": False,
                        "isOnlyRateScheduleUsed": False,
                        "isPassFail": False,
                        "isSpecialExam": None,
                        "isStudentDegreePathwayCourse": False,
                        "isSubstitute": False,
                        "isTransferCredit": True,
                        "lastModifiedDateTime": "2023/04/06 14:01:51",
                        "lastModifiedUserId": 95,
                        "lda": "2023/04/04 00:00:00",
                        "letterGrade": "CPL",
                        "lmsExtractStatus": "R",
                        "makeUpMinutes": 0,
                        "midTermGradeNote": None,
                        "midTermGradePostedDate": None,
                        "midTermLetterGrade": None,
                        "midTermNumericGrade": None,
                        "minutesAbsent": 0,
                        "minutesAttended": 60,
                        "modFlag": "A",
                        "note": "Registered Via API",
                        "numericGrade": None,
                        "outsideCourseWorkHours": 0,
                        "overrideCourseProgression": None,
                        "payStatus": "Y",
                        "previousStatus": "C",
                        "qualityPoints": None,
                        "requiredCourseId": 66,
                        "retakeFeeWaived": "O",
                        "retakeFlag": None,
                        "retakeOverride": False,
                        "retakeTiv2CredEarnValue": None,
                        "retakeTiv2CredEarnZeroed": False,
                        "revenueReferenceNumber": None,
                        "rosterFlag": None,
                        "rowVersion": "AAAAAABi0q4=",
                        "speed": None,
                        "startDate": "2022/12/27 00:00:00",
                        "status": "P",
                        "studentEnrollmentPeriodId": 2625,
                        "studentId": 17602,
                        "studentTransferCreditId": None,
                        "substituteCourseId": None,
                        "supplementaryStatus": None,
                        "termId": 132,
                        "testingScheduleId": None,
                        "transcriptNote": None,
                        "transferredCourseCode": None,
                        "transferredCourseDescrip": None,
                        "transferTypeId": 1,
                        "originalState": "H4sIAAAAAAAEAM1bUW8aORD+K4inu4fAAmnSoiQSoaGNLiR7QNPrvU3WA/HVa29tL+nerz97gSRN2FbE9mURElIWPJ9nxjPzzThHAymhuJr/gcU1sByv5kpLyhfAi1mRYeN7yrg6bt5qnfXbbZXcYgqqldJECiXmupWItN2Nol67E7WnKCkw+i9oKni7XFg1Vyv06f0ad3d3rbteS8iF/WGn/df4Ylouu0e50sATbJ4cVcApH5yck6O2/Twqv9KgfW0eHTehT7neyINfy2ueHLw7jI7a5Son5ZKVMqvBDBIgaPTxBUFWwMq5oguO5LTQuBM+d3DkjEvB2AQX1DwuDfNMe5yy46aWOTbbDoKWVCF5DxpDrJ4Tqs/mc0w0XWIgIaeUsWA7GDJQamrxbzHAS9238/bwnauHDJlIvn4UuVQVoAgmNAW2E7Be1IqcffcB2UBrTDONVXp7CUS/CM9A8vrBMwcfFxjkvA8FV5jk9jiOKc81qsGNQq59qsB9/8orHmMSH0Yx7oIDQpCMpEiDmMZKGCFa4CRnoRzASvGXif3o9RLSp9F7g2j1m51ADXOlRYqyMUFWpk51S7PGGDgsMDXO3vhtOBn/3phhcssFE4uisde4FLwxlGjylfOOJJpcVCakGa3cFlk/3mlj3ajb24v2zXvWedvv7Pe7vdZ+1POA2OzbdzLxEgofkNU2mTxArGc2MQW/muAcJZoSveL4+4gs1uEn+G2MT4O3l8UxQ07M2f1pQeZFkhRZoGLyjG8rU/1EhINZFPXLt6vDrJiHjZNTDTpXQSpNP0n5GdRggcwD1u+Z8VqTFxAIozwUG9qICeZrB3vdQ2++NoIkZ7qITcWH5IJAAIWMYKpzGzkGRQyF9ZUYJRUkSPAYUQ7sgwRiIiGoQBGqXD8WplSrW7peI1N6Kx/3FehM3RN1+m86rf03XgBPE9hSbL+Y3Lti+kgXt2YxIVgQ7znnCTPnoWK3N0YsAt9px3NgCl13bWCJNGOosbTJpQgSHc95LMVColKllBAS1GCuURqiaAsJj1q2uJyVrMqO3KoIrJ0HGHBaeNaaJ2S2JbGh5VWB4lXhWYOaIj/nJBaMJsUnVUucP3ARstUP/RzCh8pwQP7JVTVtfEVtnH3XltPUFZkyDGvVWw9ioQ9M3AAb5mluezRLXOcln9rwEzI3wM75hwyGwJL62etJ8pxgxiCpo2NdcVZMTPm3iaX1DFMxKDUCyuqHbE1l3qOpYTAGfXsHRV2z+TS/UZrqvJIHvCK2mQSuTBradHxrFXIuQOmxIHROA3eRvVKpx6jNsZbeCNU7d2jPGgu+uvC++iAXqA1p2MZJXMYg8YUzrtTWAhKSdYPNH7iJK7QxfMVP2XqI6cnVnO04pmSGMg1JYR+LqGy1eBRU7ZoehVzmKUqahJPy61H3K/jKCpT+KQvYeSDrjkuQEYOFv6M+cEW05SS5RJ7yTpWhoKRxTaExiM+d8YX13qtcK0rWo7vPQgYZxrjq4GqJUt6j3HTZDIUMoJAYCt/p6Ivr/mOJSypy5RvY0BXYnzkwakcsW+YFPowxwW85lZtmjr+LJc43SyaoTYkwQvwMdFkZX19gkitPyJ4HWT/2sItvjmPdqNcK3Ywuu5Z62QsT5XeD6eGxpL9Rivq1Gya4RJ7jfVfUJJMbfHoj2YtCbLEoQ3mduLtGuSXe3+sXFB7sn1IOstiteihfpzT6tn/squtphkG6mSboSx1g4tnd63R9jtt9J6fYHVDZz3ro1lfM5l+aRboHXefuwRqjvwHx4UHU9QTqxz5WkHnxQxsv4N0xywH9KbjnrN5Sr4mkmQ7E4jeGuy+chiIId3gm5z2W+wooyv7lf71N0f75v0Kd/AerDAvbKzUAAA==",
                        "secureState": "H4sIAAAAAAAEAD3MQQrCMBAAwK9I7mZTeysqeFbpoSJel5C0C01Ssisxvl6s4ANm9qecsfb+7Ood56frPUumOGKst7q4zSvMkQ9qElk6ALaTC8g6kM2JkxdtU4CdMS00BgaXCWd6o1CKsMasfkNH/6OUokurUx6/sIHH9TKs7ZYiC0brFBw/juQnSpcAAAA=",
                        "extendedProperties": [],
                        "entityState": 3,
                    },
                    "count": 1,
                },
                "notifications": [],
                "hasError": False,
                "hasFault": False,
                "hasWarning": False,
                "hasValidationError": False,
                "hasValidationWarning": False,
                "hasValidationInformation": False,
                "hasSecurityError": False,
            },
            "update_student_1": {"payload": {"data": {"student_id": self.test_data.get("student_id")}}},
        }

    def get_request(self, url, headers):
        self.test_key = f"{self.test_name}_{self.iteration}" if self.iteration is not None else self.test_name
        return self.fetch_response(url, headers)

    def fetch_response(self, url, headers):
        self.assertEqual(headers.get("Authorization"), self.application_key)
        expected_url = self._url_mapping.get(self.test_key)
        expected_resp = self.expected_response
        if self.iteration is not None:
            self.iteration += 1
            if self.real_response.get(self.test_key) is not None:
                expected_resp = self.real_response.get(self.test_key)
        self.assertEqual(url, expected_url)
        response = MagicMock()
        response.status_code = 200
        response.json = Mock(side_effect=lambda: expected_resp)
        return response

    def post_request(self, url, data, headers):
        self.test_key = f"{self.test_name}_{self.iteration}" if self.iteration is not None else self.test_name
        response = self.fetch_response(url, headers)
        if self.expected_data.get(self.test_key):
            json_data = json.loads(data)
            if self.test_key == "post_grades_2":
                del json_data.get("payload").get("StudentCourse")["gradePostedDate"]
                del json_data.get("payload").get("StudentCourse")["endDate"]
            self.assertEqual(json_data, self.expected_data.get(self.test_key))
        return response
