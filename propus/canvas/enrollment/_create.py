import datetime
import json
from typing import Literal, Union, Optional


async def create_enrollment(
    self,
    section_id: Union[str, int],
    user_id: Union[str, int],
    enrollment_type: Literal[
        "StudentEnrollment",
        "TeacherEnrollment",
        "TaEnrollment",
        "ObserverEnrollment",
        "DesignerEnrollment",
    ],
    start_at: Optional[datetime.datetime] = None,
    end_at: Optional[datetime.datetime] = None,
    role_id: Optional[int] = None,
    enrollment_state: Optional[Literal["active", "invited", "inactive"]] = "active",
    limit_privileges_to_course_section: Optional[bool] = None,
    notify: bool = False,
    self_enrollment_code: Optional[str] = None,
    self_enrolled: bool = False,
    associated_user_id: Optional[Union[str, int]] = None,
) -> dict:
    """
    Create an enrollment for a user in a section
    :param self:
    :param section_id: The section id
    :param user_id: The user id
    :param enrollment_type: Enroll the user as a student, teacher, TA, observer, or designer. If no value is given,
        the type will be inferred by enrollment if supplied, otherwise ‘StudentEnrollment’ will be used.
    :param start_at: The start time of the enrollment, in ISO8601 format. e.g. 2012-04-18T23:08:51Z
    :param end_at: The end time of the enrollment, in ISO8601 format. e.g. 2012-04-18T23:08:51Z
    :param role_id: Assigns a custom course-level role to the user.
    :param enrollment_state: If set to ‘active,’ student will be immediately enrolled in the course.
        Otherwise they will be required to accept a course invitation. Default is ‘invited.’.
        If set to ‘inactive’, student will be listed in the course roster for teachers, but will not be able to
        participate in the course until their enrollment is activated.
    :param limit_privileges_to_course_section: If set, the enrollment will only allow the user to see and interact
        with users enrolled in the section given by course_section_id.
        - For teachers and TAs, this includes grading privileges.
        - Section-limited students will not see any users (including teachers and TAs) not enrolled in their sections.
        - Users may have other enrollments that grant privileges to multiple sections in the same course.
    :param notify: If true, a notification will be sent to the enrolled user. Notifications are not sent by default.
    :param self_enrollment_code: If the current user is not allowed to manage enrollments in this course,
        but the course allows self-enrollment, the user can self- enroll as a student in the default section
        by passing in a valid code. When self-enrolling, the user_id must be ‘self’. The enrollment_state will be
        set to ‘active’ and all other arguments will be ignored.
    :param self_enrolled: If true, marks the enrollment as a self-enrollment, which gives students the ability
        to drop the course if desired. Defaults to false.
    :param associated_user_id: For an observer enrollment, the ID of a student to observe.
        This is a one-off operation; to automatically observe all a student’s enrollments (for example, as a parent),
        please use the User Observees API.
    :return: The created enrollment object
    """
    payload = {
        "enrollment": {
            "user_id": user_id,
            "type": enrollment_type,
            "notify": notify,
            "self_enrolled": self_enrolled,
        }
    }

    if start_at is not None:
        payload["enrollment"]["start_at"] = start_at.isoformat()
    if end_at is not None:
        payload["enrollment"]["end_at"] = end_at.isoformat()
    if role_id is not None:
        payload["enrollment"]["role_id"] = role_id
    if enrollment_state is not None:
        payload["enrollment"]["enrollment_state"] = enrollment_state
    if limit_privileges_to_course_section is not None:
        payload["enrollment"]["limit_privileges_to_course_section"] = limit_privileges_to_course_section
    if self_enrollment_code is not None:
        payload["enrollment"]["self_enrollment_code"] = self_enrollment_code
    if associated_user_id is not None:
        payload["enrollment"]["associated_user_id"] = associated_user_id

    return self.make_request(
        req_type="post",
        url=self._get_endpoint("create_enrollment_in_section", {"<section_id>": section_id}),
        data=json.dumps(payload),
    )
