assignment_get_endpoints = {
    "get_course_assignments": ("/api/v1/courses/<course_id>/assignments", ["<course_id>"]),
    "get_assignment": ("/api/v1/courses/<course_id>/assignments/<assignment_id>", ["<course_id>", "<assignment_id>"]),
}

assignment_group_get_endpoints = {
    "get_course_assignment_groups": ("/api/v1/courses/<course_id>/assignment_groups", ["<course_id>"]),
    "get_assignment_group": (
        "/api/v1/courses/<course_id>/assignment_groups/<assignment_group_id>",
        ["<course_id>", "<assignment_group_id>"],
    ),
}
