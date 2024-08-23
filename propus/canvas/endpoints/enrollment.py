enrollment_create_endpoints = {
    "create_enrollment_in_section": (
        "/api/v1/sections/<section_id>/enrollments",
        ["<section_id>"],
    ),
}

enrollment_get_endpoints = {
    "list_user_enrollments": ("/api/v1/users/<user_id>/enrollments", ["<user_id>"]),
    "list_section_enrollments": (
        "/api/v1/sections/<section_id>/enrollments",
        ["<section_id>"],
    ),
    "list_course_enrollments": (
        "/api/v1/courses/<course_id>/enrollments",
        ["<course_id>"],
    ),
    "list_students_in_course": (
        "/api/v1/courses/<course_id>/students",
        ["<course_id>"],
    ),
    "get_single_enrollment": ("/api/v1/accounts/1/enrollments/<enrollment_id>", ["<enrollment_id>"]),
}
enrollment_delete_endpoints = {
    "conclude_delete_deactivate_enrollment": (
        "/api/v1/courses/<course_id>/enrollments/<enrollment_id>",
        ["<course_id>", "<enrollment_id>"],
    ),
}

enrollment_update_endpoints = {
    "reactivate_enrollment": (
        "/api/v1/courses/<course_id>/enrollments/<enrollment_id>/reactivate",
        ["<course_id>", "<enrollment_id>"],
    )
}
