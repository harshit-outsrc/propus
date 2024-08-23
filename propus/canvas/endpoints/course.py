course_create_endpoints = {
    "create_course": ("/api/v1/accounts/<account_id>/courses", ["<account_id>"]),
}

course_update_endpoints = {
    "update_course": (
        "/api/v1/courses/<course_id>",
        ["<course_id>"],
    ),
    "update_course_settings": (
        "/api/v1/courses/<course_id>/settings",
        ["<course_id>"],
    ),
}

course_get_endpoints = {
    "get_course": ("/api/v1/courses/<course_id>", ["<course_id>"]),
}

course_delete_or_conclude_endpoints = {
    "delete_or_conclude_course": ("/api/v1/courses/<course_id>", ["<course_id>"]),
}

section_create_endpoints = {
    "create_section": ("/api/v1/courses/<course_id>/sections", ["<course_id>"]),
}

section_get_endpoints = {
    "get_section": (
        "/api/v1/courses/<course_id>/sections/<section_id>",
        ["<course_id>", "<section_id>"],
    ),
}
section_update_endpoints = {
    "update_section": ("/api/v1/sections/<section_id>", ["<section_id>"]),
}
section_delete_endpoints = {
    "delete_section": ("/api/v1/sections/<section_id>", ["<section_id>"]),
}
