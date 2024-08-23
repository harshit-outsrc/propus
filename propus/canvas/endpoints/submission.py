submission_get_endpoints = {
    "list_assignment_submissions_by_course_single_assignment": (
        "/api/v1/courses/<course_id>/assignments/<assignment_id>/submissions",
        ["<course_id>", "<assignment_id>"],
    ),
    "list_assignment_submissions_by_section_single_assignment": (
        "/api/v1/sections/<section_id>/assignments/<assignment_id>/submissions",
        ["<section_id>", "<assignment_id>"],
    ),
    "list_assignment_submissions_by_course_multiple_assignments": (
        "/api/v1/courses/<course_id>/students/submissions",
        ["<course_id>"],
    ),
    "list_assignment_submissions_by_section_multiple_assignments": (
        "/api/v1/sections/<section_id>/students/submissions",
        ["<section_id>"],
    ),
    "get_single_submission_by_course_and_user": (
        "/api/v1/courses/<course_id>/assignments/<assignment_id>/submissions/<user_id>",
        ["<course_id>", "<assignment_id>", "<user_id>"],
    ),
    "get_single_submission_by_section_and_user": (
        "/api/v1/sections/<section_id>/assignments/<assignment_id>/submissions/<user_id>",
        ["<section_id>", "<assignment_id>", "<user_id>"],
    ),
    "get_submission_summary_by_course": (
        "/api/v1/courses/<course_id>/assignments/<assignment_id>/submission_summary",
        ["<course_id>", "<assignment_id>"],
    ),
    "get_submission_summary_by_section": (
        "/api/v1/sections/<section_id>/assignments/<assignment_id>/submission_summary",
        ["<section_id>", "<assignment_id>"],
    ),
    "list_missing_submissions_by_user": (
        "/api/v1/users/<user_id>/missing_submissions",
        ["<user_id>"],
    ),
}
