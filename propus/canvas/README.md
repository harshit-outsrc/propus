# Canvas Propus Modules
This module contains a set of functions to interact with the Instructure Canvas REST API.

The modules include:
- [`user`](#user) - Functions to interact with the Canvas User API. Includes creating, reading, and updating users.
- [`course`](#course) - Functions to interact with the Canvas Course API. Includes creating, reading, updating, and deleting/concluding courses.
- [`enrollment`](#enrollment) - Functions to interact with the Canvas Enrollment API. Includes creating, reading, reactivating, and deleting/concluding enrollments.
- [`submission`](#submission) - Functions to interact with the Canvas Submission API. Includes listing submissions by course/section for single/multiple assignments, getting a submission summary by course/section, and getting missing submissions for a user.
- [`term`](#term) - Functions to interact with the Canvas Term API. Includes creating, reading, updating, and deleting terms.

There are also some helper functions which use some other services, such as Postgres:
- [`create_canvas_user`](#create-a-canvas-user) - Creates a user in Canvas and stores the user ID in a Postgres database.]
Requirements:
A SSM parameter store with the following parameters:
```python
{
    "token": "Bearer [token]", # Canvas API token
    "base_url": "https://calbright-dev.instructure.com", # Canvas base URL
    "auth_providers": {"okta": 105, "google": 105}, # Canvas auth provider IDs - expects okta + google as keys
}
```

You can instantiate the module as follows:
```python
ssm = AWS_SSM.build("us-west-2")
creds = ssm.get_param("canvas.dev.token", param_type="json")
canvas = Canvas(base_url=creds["base_url"], application_key=creds["token"], auth_providers=creds["auth_providers"])
```
The following examples all assume that you have instantiated the module as shown above.

## User
Example: Create a user [student]
```python
student_user = asyncio.run(
    canvas.create_user(
        user_type="student",
        first_name="Testers",
        last_name="McTesterson VII",
        email_address="testeroni124557465asd7@calbright.org",
        sis_user_id="testeroniii",
    )
)
print(student_user)
```

Example:  Get a single user
```python
user = asyncio.run(canvas.get_user(user_id=110))
print(user)
```

Example:  Get a single user's profile
```python
user_profile = asyncio.run(canvas.get_user_profile(user_id=110))
print(user_profile)
```

Example:  Get the user list for an account
```python
user_list = asyncio.run(canvas.list_users_in_account(account_id=1))
print(user_list)
```

Example: Update a user
```python
updated_user = asyncio.run(
    canvas.update_user(
        user_id=110,
        first_name="Testeroniiiii",
        last_name="McTestersons VI",
        email="myNewCoolEmail132445@calbright.org",
        time_zone="America/New_York",
        locale="sp",
        title="Thin Mint Eater Extaordinaire",
        bio="I can eat 100000 thin mints in a single sitting",
        pronouns="they/them",
    )
)
print(updated_user)
```

Example:  Get the page views for a user
```python
page_views = asyncio.run(
    canvas.get_user_page_views(
        user_id=104,
        start_time=datetime.datetime(2024, 3, 6),
        end_time=datetime.datetime(2024, 3, 7),
    )
)
print(page_views)
```
## Course

Example: Create a course (simple)
```python
created_course = asyncio.run(
    canvas.create_course(
        account_id=1,
        course_name="Test Course Propus 4",
        course_code="TEST-104",
        term_id=1,
        sis_course_id="TEST-104",
    )
)
print(created_course)
```

Example: Create a course (expanded)
```python
created_course = asyncio.run(
    canvas.create_course(
        account_id=1,
        course_name="Test Course Propus 2",
        course_code="TEST-102",
        term_id=1,
        sis_course_id="TEST-102",
        start_at=datetime.datetime(2024, 3, 15),
        end_at=datetime.datetime(2024, 6, 15),
        license="private",
        is_public=False,
        is_public_to_auth_users=False,
        public_syallbus=False,
        public_syllabus_to_auth=False,
        public_description="This is the public course description for TEST-102: Test Course Propus 2",
        allow_student_wiki_edits=False,
        allow_wiki_comments=False,
        allow_student_forum_attachments=True,
        open_enrollment=False,
        self_enrollment=False,
        restrict_enrollments_to_course_dates=True,
        integration_id="TEST-102-INT",
        hide_final_grades=False,
        apply_assignment_group_weights=True,
        time_zone="America/New_York",
        default_view="modules",
        syllabus_body="This is your course. Learning outcomes include: eating thin mints and other girl scout cookies.",
        grading_standard_id=1,
        grade_passback_setting="disabled",
        course_format="blended",
        offer=True,
        enroll_me=True,
        enable_sis_reactivation=False,
    )
)
print(created_course)
```

Example: Create a course section
```python
created_section = asyncio.run(
    canvas.create_section(
        course_id=110,
        name="Test Section 1 Propusss",
        sis_section_id="TEST-102-SEC-1212",
        integration_id="TEST-102-SEC-1212-INT",
        start_at=datetime.datetime(2024, 3, 17),
        end_at=datetime.datetime(2024, 6, 17),
        restrict_enrollments_to_section_dates=True,
        enable_sis_reactivation=False,
    )
)
print(created_section)
```

Example: get a single course
```python
course = asyncio.run(canvas.get_course(course_id=106))
print(course)
```

Example: get a single section
```python
section = asyncio.run(canvas.get_section(course_id=106, section_id=2))
print(section)
```

Example: Update a course's settings
```python
updated_course_settings = asyncio.run(
    canvas.update_course_settings(
        course_id=106,
        hide_final_grades=True,
        lock_all_announcements=True,
        default_due_time=datetime.time(7, 29, 59).strftime("%H:%M:%S"),
    )
)
print(updated_course_settings)
```

Example: Update a course
```python
updated_course = asyncio.run(
    canvas.update_course(
        course_id=106,
        sis_course_id="TEST-102-UPDATED",
        name="Test Course Propus 2 - Updated",
        course_code="TEST-102-UPDATED",
        integration_id="TEST-102-UPDATED-INT",
        storage_quota_mb=1400,
        default_view="assignments",
    )
)
print(updated_course)
```

Example: Update a section
```python
updated_section = asyncio.run(
    canvas.update_section(
        section_id=5,
        name="Test Section 3 Propus 2 - Updated",
        sis_section_id="TEST-102-SEC-3-UPDATED",
        integration_id="TEST-102-SEC-3-UPDATED-INT",
        start_at=datetime.datetime(2024, 4, 19),
        end_at=datetime.datetime(2024, 5, 19),
        restrict_enrollments_to_section_dates=True,
    )
)
print(updated_section)
```

Example: Delete a course
```python
deleted_course_status = asyncio.run(
    canvas.delete_or_conclude_course(course_id=108, event="delete")
)
print(deleted_course_status)
```

Example: Conclude a course
```python
concluded_course_status = asyncio.run(
    canvas.delete_or_conclude_course(course_id=110, event="conclude")
)
print(concluded_course_status)
```

Example: Delete a section
```python
deleted_section = asyncio.run(canvas.delete_section(section_id=8))
print(deleted_section)
```
## Enrollment
Example: Create an enrollment
```python
created_enrollment = asyncio.run(
    canvas.create_enrollment(
        section_id=4,
        user_id=106,
        enrollment_type="StudentEnrollment",
        limit_privileges_to_course_section=True,
        notify=True,
        start_at=datetime.datetime(2024, 4, 18),
        end_at=datetime.datetime(2024, 6, 19),
    )
)
print(created_enrollment)
```

Example: List enrollments for a user
```python
user_enrollments = asyncio.run(
    canvas.list_enrollments(object_type="user", object_id=106, sis_course_id="TEST-101")
)
print(user_enrollments)
```

Example: List enrollments for a section
```python
section_enrollments = asyncio.run(
    canvas.list_enrollments(
        object_type="section",
        object_id=4,
    )
)
print(section_enrollments)
```

Example: List enrollments for a course
```python
course_enrollments = asyncio.run(
    canvas.list_enrollments(
        object_type="course", object_id=105, include=["uuid", "avatar_url"]
    )
)
print(course_enrollments)
```

Example: List students in a course
```python
students_in_course = asyncio.run(canvas.list_students_in_course(course_id=105))
print(students_in_course)
```

Example: Deactivate an enrollment
```python
deactivated_enrollment = asyncio.run(
    canvas.conclude_delete_deactivate_enrollment(
        course_id=105, enrollment_id=8, task="deactivate"
    )
)
print(deactivated_enrollment)
```

Example: Reactivate an enrollment
```python
reactivated_enrollment = asyncio.run(
    canvas.reactivate_enrollment(course_id=105, enrollment_id=8)
)
print(reactivated_enrollment)
```

Example delete an enrollment
```python
deleted_enrollment = asyncio.run(
    canvas.conclude_delete_deactivate_enrollment(
        course_id=105, enrollment_id=8, task="delete"
    )
)
print(deleted_enrollment)
```

Example: Get a single enrollment
```python
enrollment = asyncio.run(canvas.get_single_enrollment(enrollment_id=8))
print(enrollment)
```

## Submission

Example: List assignment submissions for a single assignment by course
```python
course_single_assignment_submissions = asyncio.run(
    canvas.list_assignment_submissions_for_single_assignment(
        object_type="course",
        object_id=106,
        assignment_id=121,
        include=["submission_history", "submission_comments", "user"],
    )
)
print(course_single_assignment_submissions)
```

Example: List assignment submissions for a single assignment by section
```python
section_single_assignment_submissions = asyncio.run(
    canvas.list_assignment_submissions_for_single_assignment(
        object_type="section",
        object_id=2,
        assignment_id=121,
        include=["visibility", "rubric_assessment", "read_status"],
    )
)
print(section_single_assignment_submissions)
```

Example: List assignment submissions for multiple assignments by course
```python
course_multiple_assignments_submissions = asyncio.run(
    canvas.list_assignment_submissions_for_multiple_assignments(
        object_type="course",
        object_id=106,
        workflow_state="submitted",
        submitted_since=datetime.datetime(2024, 3, 12),
    )
)
print(course_multiple_assignments_submissions)
```

Example: List assignment submissions for multiple assignments by section
```python
section_multiple_assignments_submissions = asyncio.run(
    canvas.list_assignment_submissions_for_multiple_assignments(
        object_type="section",
        object_id=2,
        enrollment_state="active",
        order="id",
        order_direction="ascending",
        include=["total_scores", "submission_comments", "visibility"],
    )
)
print(section_multiple_assignments_submissions)
```

Example: Get a single submission by course and user
```python
single_submission_by_course = asyncio.run(
    canvas.get_single_submission(
        object_type="course",
        object_id=106,
        assignment_id=121,
        user_id=109,
        include=["submission_comments", "rubric_assessment"],
    )
)
print(single_submission_by_course)
```

Example: Get a single submission by section and user
```python
single_submission_by_section = asyncio.run(
    canvas.get_single_submission(
        object_type="section",
        object_id=2,
        assignment_id=121,
        user_id=109,
        include=["visibility", "submission_history", "read_status"],
    )
)
print(single_submission_by_section)
```

Example: Get submission summary by course
```python
course_assignment_submission_summary = asyncio.run(
    canvas.get_submission_summary(
        object_type="course",
        object_id=106,
        assignment_id=121,
    )
)
print(course_assignment_submission_summary)
```

Example: Get submission summary by section
```python
section_assignment_submission_summary = asyncio.run(
    canvas.get_submission_summary(
        object_type="section",
        object_id=2,
        assignment_id=121,
    )
)
print(section_assignment_submission_summary)
```

Example: List missing submissions for user
```python
missing_submissions = asyncio.run(
    canvas.list_missing_submissions_for_user(
        user_id=109, include=["course", "planner_overrides"]
    )
)
print(missing_submissions)
```

## Term

Example: Create a term
```python
from propus.canvas.term import TermOverride

term_overrides = [
    TermOverride(
        override_enrollment_type="TeacherEnrollment",
        override_start_at=datetime.datetime(2024, 4, 1),
        override_end_at=datetime.datetime(2024, 5, 1),
    ),
    TermOverride(
        override_enrollment_type="StudentEnrollment",
        override_start_at=datetime.datetime(2024, 4, 1),
    ),
]
created_term = asyncio.run(
    canvas.create_term(
        account_id=1,
        name="Test Term 4",
        start_at=datetime.datetime(2024, 4, 1),
        end_at=datetime.datetime(2024, 6, 1),
        sis_term_id="TEST-TERM-4",
        overrides=term_overrides,
    )
)
print(created_term)
```

Example: Get a term
```python
term = asyncio.run(canvas.get_term(account_id=1, term_id=102))
print(term)
```

Example: Get a list of terms
```python
list_of_terms = asyncio.run(
    canvas.list_terms(
        account_id=1, workflow_state="all", include=["course_count", "overrides"]
    )
)
print(list_of_terms)
```

Example: Update a term
```python
from propus.canvas.term import TermOverride

updated_term_overrides = [
    TermOverride(
        override_enrollment_type="TeacherEnrollment",
        override_start_at=datetime.datetime(2024, 4, 1),
        override_end_at=datetime.datetime(2024, 5, 1),
    ),
    TermOverride(
        override_enrollment_type="StudentEnrollment",
        override_start_at=datetime.datetime(2024, 4, 1),
    ),
]
updated_term = asyncio.run(
    canvas.update_term(
        account_id=1,
        term_id=106,
        name="Test Term 4 - Updated",
        start_at=datetime.datetime(2024, 8, 1),
        end_at=datetime.datetime(2024, 9, 1),
        sis_term_id="TEST-TERM-44-UPDATED",
        overrides=updated_term_overrides,
    )
)
print(updated_term)
```

Example: Delete a term
```python
deleted_term = asyncio.run(canvas.delete_term(account_id=1, term_id=105))
print(deleted_term)
```
## Helper Functions
### Create a Canvas User
Note: Requires the following runtime vars: 
```
DB=calbright_dev; ENV=localhost; PASSWORD=[password]; USER=calbright
```

```python
import os
from propus.calbright_sql.calbright import Calbright
from propus.helpers.canvas import create_canvas_user


calbright_postgres = Calbright.build(
    {
        "db": os.environ.get("DB"),
        "host": "localhost",
        "user": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD"),
    },
    verbose=False,
).session
test_user_data = {
    "first_name": "Tony",
    "last_name": "Pizza",
    "email_address": "tony.pizza@calbright.org",
    "ccc_id": "a1",
}

user_id = create_canvas_user(
    user_type="student",
    first_name=test_user_data["first_name"],
    last_name=test_user_data["last_name"],
    email_address=test_user_data["email_address"],
    sis_user_id=test_user_data["ccc_id"],
    session=calbright_postgres,
    canvas=canvas,
)
print(user_id)
```