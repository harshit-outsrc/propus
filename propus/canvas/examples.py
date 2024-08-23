"""
This file contains examples of how to use the Canvas class to interact with the Canvas API, and is useful
    for development and testing locally.
- It is structured so that there is a '# Example:' comment before each example.
- To use an example, uncomment the example and run the file.
- You may need to uncomment imports at the top which stay commented out to avoid tests getting mad.
- The examples are organized into sections by the Canvas API endpoint they interact with.
- Note that where IDs are needed you should get them from the current state of the Canvas instance you are working with.
"""

from propus.aws.ssm import AWS_SSM
from propus.canvas import Canvas

# import datetime
# import asyncio

ssm = AWS_SSM.build("us-west-2")
creds = ssm.get_param("canvas.dev.token", param_type="json")
canvas = Canvas(base_url=creds["base_url"], application_key=creds["token"], auth_providers=creds["auth_providers"])

# USERS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ USERS
# Example: Create a user [student]
# student_user = asyncio.run(
#     canvas.create_user(
#         user_type="student",
#         first_name="Johnny",
#         last_name="Trampolini",
#         email_address="jt213445646754676216754@calbright.org",
#         sis_user_id="jtrampolini",
#     )
# )
# print(student_user)

# Example:  Get a single user
# user = asyncio.run(canvas.get_user(user_id=110))
# print(user)

# Example:  Get a single user's profile
# user_profile = asyncio.run(canvas.get_user_profile(user_id=110))
# print(user_profile)

# Example:  Get the user list for an account
# user_list = asyncio.run(canvas.list_users_in_account(account_id=1))
# print(user_list)

# Example: Update a user
# updated_user = asyncio.run(
#     canvas.update_user(
#         user_id=110,
#         first_name="Testeroniiiii",
#         last_name="McTestersons VI",
#         email="myNewCoolEmail132445@calbright.org",
#         time_zone="America/New_York",
#         locale="sp",
#         title="Thin Mint Eater Extaordinaire",
#         bio="I can eat 100000 thin mints in a single sitting",
#         pronouns="they/them",
#     )
# )
# print(updated_user)


# Example:  Get the page views for a user
# page_views = asyncio.run(
#     canvas.get_user_page_views(
#         user_id=104,
#         start_time=datetime.datetime(2024, 3, 6),
#         end_time=datetime.datetime(2024, 3, 7),
#     )
# )
# print(page_views)


# COURSES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ COURSES
# Example: Create a course (simple)
# created_course = asyncio.run(
#     canvas.create_course(
#         account_id=1,
#         course_name="Test Course Propus 4",
#         course_code="TEST-104",
#         term_id=1,
#         sis_course_id="TEST-104",
#     )
# )
# print(created_course)


# Example: Create a course (complex)
# created_course = asyncio.run(
#     canvas.create_course(
#         account_id=1,
#         course_name="Test Course Propus 2",
#         course_code="TEST-102",
#         term_id=1,
#         sis_course_id="TEST-102",
#         start_at=datetime.datetime(2024, 3, 15),
#         end_at=datetime.datetime(2024, 6, 15),
#         license="private",
#         is_public=False,
#         is_public_to_auth_users=False,
#         public_syallbus=False,
#         public_syllabus_to_auth=False,
#         public_description="This is the public course description for TEST-102: Test Course Propus 2",
#         allow_student_wiki_edits=False,
#         allow_wiki_comments=False,
#         allow_student_forum_attachments=True,
#         open_enrollment=False,
#         self_enrollment=False,
#         restrict_enrollments_to_course_dates=True,
#         integration_id="TEST-102-INT",
#         hide_final_grades=False,
#         apply_assignment_group_weights=True,
#         time_zone="America/New_York",
#         default_view="modules",
#         syllabus_body="This is your course. Learning outcomes include: eating thin mints and other cookies.",
#         grading_standard_id=1,
#         grade_passback_setting="disabled",
#         course_format="blended",
#         offer=True,
#         enroll_me=True,
#         enable_sis_reactivation=False,
#     )
# )
# print(created_course)

# Example: Create a course section
# created_section = asyncio.run(
#     canvas.create_section(
#         course_id=110,
#         name="Test Section 1 Propusss",
#         sis_section_id="TEST-102-SEC-1212",
#         integration_id="TEST-102-SEC-1212-INT",
#         start_at=datetime.datetime(2024, 3, 17),
#         end_at=datetime.datetime(2024, 6, 17),
#         restrict_enrollments_to_section_dates=True,
#         enable_sis_reactivation=False,
#     )
# )
# print(created_section)

# Example: get a single course
# course = asyncio.run(canvas.get_course(course_id=106))
# print(course)


# Example: get a single section
# section = asyncio.run(canvas.get_section(course_id=106, section_id=2))
# print(section)


# Example: Update a course's settings
# updated_course_settings = asyncio.run(
#     canvas.update_course_settings(
#         course_id=106,
#         hide_final_grades=True,
#         lock_all_announcements=True,
#         default_due_time=datetime.time(7, 29, 59).strftime("%H:%M:%S"),
#     )
# )
# print(updated_course_settings)

# Example: Update a course
# updated_course = asyncio.run(
#     canvas.update_course(
#         course_id=106,
#         sis_course_id="TEST-102-UPDATED",
#         name="Test Course Propus 2 - Updated",
#         course_code="TEST-102-UPDATED",
#         integration_id="TEST-102-UPDATED-INT",
#         storage_quota_mb=1400,
#         default_view="assignments",
#     )
# )
# print(updated_course)

# Example: Update a section
# updated_section = asyncio.run(
#     canvas.update_section(
#         section_id=5,
#         name="Test Section 3 Propus 2 - Updated",
#         sis_section_id="TEST-102-SEC-3-UPDATED",
#         integration_id="TEST-102-SEC-3-UPDATED-INT",
#         start_at=datetime.datetime(2024, 4, 19),
#         end_at=datetime.datetime(2024, 5, 19),
#         restrict_enrollments_to_section_dates=True,
#     )
# )
# print(updated_section)

# Example: Delete a course
# deleted_course_status = asyncio.run(
#     canvas.delete_or_conclude_course(course_id=108, event="delete")
# )
# print(deleted_course_status)

# Example: Conclude a course
# concluded_course_status = asyncio.run(
#     canvas.delete_or_conclude_course(course_id=110, event="conclude")
# )
# print(concluded_course_status)

# Example: Delete a section
# deleted_section = asyncio.run(canvas.delete_section(section_id=8))
# print(deleted_section)


# ENROLLMENTS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ENROLLMENTS
# Example: Create an enrollment
# created_enrollment = asyncio.run(
#     canvas.create_enrollment(
#         section_id=4,
#         user_id=106,
#         enrollment_type="StudentEnrollment",
#         limit_privileges_to_course_section=True,
#         notify=True,
#         start_at=datetime.datetime(2024, 4, 18),
#         end_at=datetime.datetime(2024, 6, 19),
#     )
# )
# print(created_enrollment)


# Example: List enrollments for a user
# user_enrollments = asyncio.run(
#     canvas.list_enrollments(object_type="user", object_id=106, sis_course_id="TEST-101")
# )
# print(user_enrollments)

# Example: List enrollments for a section
# section_enrollments = asyncio.run(
#     canvas.list_enrollments(
#         object_type="section",
#         object_id=4,
#     )
# )
# print(section_enrollments)

# Example: List enrollments for a course
# course_enrollments = asyncio.run(
#     canvas.list_enrollments(
#         object_type="course", object_id=105, include=["uuid", "avatar_url"]
#     )
# )
# print(course_enrollments)

# Example: List students in a course
# students_in_course = asyncio.run(canvas.list_students_in_course(course_id=105))
# print(students_in_course)

# Example: Deactivate an enrollment
# deactivated_enrollment = asyncio.run(
#     canvas.conclude_delete_deactivate_enrollment(
#         course_id=105, enrollment_id=8, task="deactivate"
#     )
# )
# print(deactivated_enrollment)


# Example: Reactivate an enrollment
# reactivated_enrollment = asyncio.run(
#     canvas.reactivate_enrollment(course_id=105, enrollment_id=8)
# )
# print(reactivated_enrollment)

# Example delete an enrollment
# deleted_enrollment = asyncio.run(
#     canvas.conclude_delete_deactivate_enrollment(
#         course_id=105, enrollment_id=8, task="delete"
#     )
# )
# print(deleted_enrollment)

# Example: Get a single enrollment
# enrollment = asyncio.run(canvas.get_single_enrollment(enrollment_id=8))
# print(enrollment)

# TERMS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ TERMS
# Example: Create a term
# from propus.canvas.term import TermOverride
#
# term_overrides = [
#     TermOverride(
#         override_enrollment_type="TeacherEnrollment",
#         override_start_at=datetime.datetime(2024, 4, 1),
#         override_end_at=datetime.datetime(2024, 5, 1),
#     ),
#     TermOverride(
#         override_enrollment_type="StudentEnrollment",
#         override_start_at=datetime.datetime(2024, 4, 1),
#     ),
# ]
# created_term = asyncio.run(
#     canvas.create_term(
#         account_id=1,
#         name="Test Term 4",
#         start_at=datetime.datetime(2024, 4, 1),
#         end_at=datetime.datetime(2024, 6, 1),
#         sis_term_id="TEST-TERM-4",
#         overrides=term_overrides,
#     )
# )
# print(created_term)

# # Example: Get a term
# term = asyncio.run(canvas.get_term(account_id=1, term_id=102))
# print(term)

# # Example: Get a list of terms
# list_of_terms = asyncio.run(
#     canvas.list_terms(
#         account_id=1, workflow_state="all", include=["course_count", "overrides"]
#     )
# )
# print(list_of_terms)

# # Example: Update a term
# from propus.canvas.term import TermOverride
#
# updated_term_overrides = [
#     TermOverride(
#         override_enrollment_type="TeacherEnrollment",
#         override_start_at=datetime.datetime(2024, 4, 1),
#         override_end_at=datetime.datetime(2024, 5, 1),
#     ),
#     TermOverride(
#         override_enrollment_type="StudentEnrollment",
#         override_start_at=datetime.datetime(2024, 4, 1),
#     ),
# ]
# updated_term = asyncio.run(
#     canvas.update_term(
#         account_id=1,
#         term_id=106,
#         name="Test Term 4 - Updated",
#         start_at=datetime.datetime(2024, 8, 1),
#         end_at=datetime.datetime(2024, 9, 1),
#         sis_term_id="TEST-TERM-44-UPDATED",
#         overrides=updated_term_overrides,
#     )
# )
# print(updated_term)
#
# Example: Delete a term
# deleted_term = asyncio.run(canvas.delete_term(account_id=1, term_id=105))
# print(deleted_term)


# SUBMISSIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ SUBMISSIONS
# Example: List assignment submissions for a single assignment by course
# course_single_assignment_submissions = asyncio.run(
#     canvas.list_assignment_submissions_for_single_assignment(
#         object_type="course",
#         object_id=106,
#         assignment_id=121,
#         include=["submission_history", "submission_comments", "user"],
#     )
# )
# print(course_single_assignment_submissions)

# Example: List assignment submissions for a single assignment by section
# section_single_assignment_submissions = asyncio.run(
#     canvas.list_assignment_submissions_for_single_assignment(
#         object_type="section",
#         object_id=2,
#         assignment_id=121,
#         include=["visibility", "rubric_assessment", "read_status"],
#     )
# )
# print(section_single_assignment_submissions)

# Example: List assignment submissions for multiple assignments by course
# course_multiple_assignments_submissions = asyncio.run(
#     canvas.list_assignment_submissions_for_multiple_assignments(
#         object_type="course",
#         object_id=106,
#         workflow_state="submitted",
#         submitted_since=datetime.datetime(2024, 3, 12),
#     )
# )
# print(course_multiple_assignments_submissions)

# Example: List assignment submissions for multiple assignments by section
# section_multiple_assignments_submissions = asyncio.run(
#     canvas.list_assignment_submissions_for_multiple_assignments(
#         object_type="section",
#         object_id=2,
#         enrollment_state="active",
#         order="id",
#         order_direction="ascending",
#         include=["total_scores", "submission_comments", "visibility"],
#     )
# )
# print(section_multiple_assignments_submissions)

# Example: Get a single submission by course and user
# single_submission_by_course = asyncio.run(
#     canvas.get_single_submission(
#         object_type="course",
#         object_id=115,
#         assignment_id=213,
#         user_id=134,
#         # include=["submission_comments", "rubric_assessment"],
#         include=["submission_history"],
#     )
# )
# print(single_submission_by_course)

# Example: Get a single submission by section and user
# single_submission_by_section = asyncio.run(
#     canvas.get_single_submission(
#         object_type="section",
#         object_id=2,
#         assignment_id=121,
#         user_id=109,
#         include=["visibility", "submission_history", "read_status"],
#     )
# )
# print(single_submission_by_section)

# Example: Get submission summary by course
# course_assignment_submission_summary = asyncio.run(
#     canvas.get_submission_summary(
#         object_type="course",
#         object_id=106,
#         assignment_id=121,
#     )
# )
# print(course_assignment_submission_summary)

# Example: Get submission summary by section
# section_assignment_submission_summary = asyncio.run(
#     canvas.get_submission_summary(
#         object_type="section",
#         object_id=2,
#         assignment_id=121,
#     )
# )
# print(section_assignment_submission_summary)

# Example: List missing submissions for user
# missing_submissions = asyncio.run(
#     canvas.list_missing_submissions_for_user(
#         user_id=109, include=["course", "planner_overrides"]
#     )
# )
# print(missing_submissions)

# ASSIGNMENTS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ASSIGNMENTS
# Example: Get all assignments for a course
# course_assignments = asyncio.run(canvas.get_course_assignments(course_id=106))
# print(course_assignments)

# Example: Get all assignments for a course - Expanded
# course_assignments = asyncio.run(
#     canvas.get_course_assignments(
#         course_id=106,
#         include="submission",
#         search_term="test",
#         override_assignment_dates=False,
#         needs_grading_count_by_section=False,
#         # bucket="ungraded",
#         assignment_ids=[130],
#         order_by="name",
#         post_to_sis=False,
#         new_quizzes=True,
#     ),
# )
#
# print(course_assignments)

# Example: Get a single assignment
# assignment = asyncio.run(canvas.get_assignment(course_id=106, assignment_id=121))
# print(assignment)

# Example - Get a single assignment - Expanded
# assignment = asyncio.run(
#     canvas.get_assignment(
#         course_id=106,
#         assignment_id=121,
#         include="submission",
#         override_assignment_dates=True,
#         needs_grading_count_by_section=True,
#         all_dates=True,
#     )
# )
# print(assignment)

# Example: Get all assignment groups for a course
# assignment_groups = asyncio.run(canvas.get_course_assignment_groups(course_id=106))
# print(assignment_groups)
#

# Example - Get all assignment groups for a course - Expanded
# assignment_groups = asyncio.run(
#     canvas.get_course_assignment_groups(
#         course_id=106,
#         include="assignments",
#         assignment_ids=[121],
#         exclude_assignment_submission_types="wiki_page",
#         override_assignment_dates=False,
#         grading_period_id=None,
#         scope_assignments_to_student=False,
#     )
# )
# print(assignment_groups)

# # Example: Get a single assignment group
# assignment_group = asyncio.run(canvas.get_assignment_group(course_id=106, assignment_group_id=112))
# print(assignment_group)

# # Example: Get a single assignment group - Expanded
# assignment_group = asyncio.run(
#     canvas.get_assignment_group(
#         course_id=106,
#         assignment_group_id=112,
#         include="assignments",
#         override_assignment_dates=False,
#         grading_period_id=None,
#     )
# )
# print(assignment_group)

# MODULES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ MODULES
# Example: Get all modules for a course
# course_modules = asyncio.run(canvas.get_course_modules(course_id=115))
# print(course_modules)

# Example: Get all modules for a course - Expanded
# course_modules = asyncio.run(
#     canvas.get_course_modules(
#         course_id=115,
#         include="items",
#         # search_term="test",
#         # student_id=106,
#     )
# )
# print(course_modules)

# HELPER FUNCTIONS  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ HELPER FUNCTIONS
# Example - use the helper function to create a Canvas user and update the database with the Canvas ID
# Note: requires the following ENV runtime vars: DB=calbright_dev; ENV=localhost; PASSWORD=[password]; USER=calbright
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import create_canvas_user
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
# test_user_data = {
#     "first_name": "Tony",
#     "last_name": "Pizza",
#     "email_address": "tony.pizza@calbright.org",
#     "ccc_id": "a1",
# }
#
# user_id = create_canvas_user(
#     user_type="student",
#     first_name=test_user_data["first_name"],
#     last_name=test_user_data["last_name"],
#     email_address=test_user_data["email_address"],
#     sis_user_id=test_user_data["ccc_id"],
#     session=calbright_postgres,
#     canvas=canvas,
# )
# print(user_id)


# ## Example - create initial student enrollment
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import create_initial_course_enrollment
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# test_data = {
#     "ccc_id": "a111",
# }
#
# enrollment_id = create_initial_course_enrollment(ccc_id=test_data["ccc_id"],
#                                                  session=calbright_postgres, canvas=canvas)


# # Example - create course sections that don't exist in Canvas
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import create_course_sections
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# section = create_course_sections(session=calbright_postgres, canvas=canvas)

# # Example - enroll a student in a subsequent course when they pass a summative assignment
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import create_subsequent_course_enrollment
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
# test_data = {"current_course_id": "113", "ccc_id": "a1", "canvas_user_id": "124"}
#
# section = create_subsequent_course_enrollment(
#     current_course_id=test_data["current_course_id"],
#     ccc_id=test_data["ccc_id"],
#     canvas_user_id=test_data["canvas_user_id"],
#     session=calbright_postgres,
#     canvas=canvas,
# )


# # Example - create instructor section enrollments
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import enroll_instructors_in_sections
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# enrollments = enroll_instructors_in_sections(session=calbright_postgres, canvas=canvas)


# # Example - conclude student enrollments (drop / withdrawal)
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.canvas import conclude_student_enrollments
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# test_data = {"ccc_id": "a1"}
#
# concluded_enrollments = conclude_student_enrollments(
#     ccc_id=test_data["ccc_id"], session=calbright_postgres, canvas=canvas
# )

# Example - create course_version_section records (non-Canvas)
# import os
# from propus.calbright_sql.calbright import Calbright
# from propus.helpers.sql_calbright.course_version_sections import create_course_version_section_records
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# create_course_version_section_records(session=calbright_postgres)


# Example - create enrollment_course_term section assignment / load balancing
# import os
# from propus.helpers.sql_calbright.enrollment import assign_enrollment_course_term_sections
# from propus.calbright_sql.calbright import Calbright
# from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm
#
# calbright_postgres = Calbright.build(
#     {
#         "db": os.environ.get("DB"),
#         "host": "localhost",
#         "user": os.environ.get("USER"),
#         "password": os.environ.get("PASSWORD"),
#     },
#     verbose=False,
# ).session
#
# enrollment_course_terms = calbright_postgres.query(EnrollmentCourseTerm).all()
# enrollments = assign_enrollment_course_term_sections(
#     session=calbright_postgres, enrollment_course_term_list=enrollment_course_terms
# )
