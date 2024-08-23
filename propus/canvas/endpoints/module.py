module_get_endpoints = {
    "get_course_modules": ("/api/v1/courses/<course_id>/modules", ["<course_id>"]),
    "get_module": ("/api/v1/courses/<course_id>/modules/<module_id>", ["<course_id>", "<module_id>"]),
    "get_module_items": ("/api/v1/courses/<course_id>/modules/<module_id>/items", ["<course_id>", "<module_id>"]),
    "get_module_item": (
        "/api/v1/courses/<course_id>/modules/<module_id>/items/<module_item_id>",
        ["<course_id>", "<module_id>", "<module_item_id>"],
    ),
}
