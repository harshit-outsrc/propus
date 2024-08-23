from propus.canvas.endpoints.assignment import assignment_get_endpoints, assignment_group_get_endpoints

from propus.canvas.endpoints.course import (
    course_create_endpoints,
    course_update_endpoints,
    course_get_endpoints,
    section_create_endpoints,
    section_get_endpoints,
    section_update_endpoints,
    section_delete_endpoints,
    course_delete_or_conclude_endpoints,
)

from propus.canvas.endpoints.enrollment import (
    enrollment_create_endpoints,
    enrollment_get_endpoints,
    enrollment_delete_endpoints,
    enrollment_update_endpoints,
)

from propus.canvas.endpoints.module import module_get_endpoints

from propus.canvas.endpoints.submission import submission_get_endpoints

from propus.canvas.endpoints.term import (
    term_create_endpoints,
    term_update_endpoints,
    term_get_endpoints,
    term_delete_endpoints,
)

from propus.canvas.endpoints.users import (
    user_create_endpoints,
    user_get_endpoints,
    user_update_endpoints,
)


endpoints = [
    # assignment
    assignment_get_endpoints,
    assignment_group_get_endpoints,
    # course
    course_create_endpoints,
    course_update_endpoints,
    course_get_endpoints,
    section_create_endpoints,
    section_get_endpoints,
    section_update_endpoints,
    section_delete_endpoints,
    course_delete_or_conclude_endpoints,
    # enrollment
    enrollment_create_endpoints,
    enrollment_get_endpoints,
    enrollment_delete_endpoints,
    enrollment_update_endpoints,
    # module
    module_get_endpoints,
    # user
    user_create_endpoints,
    user_get_endpoints,
    user_update_endpoints,
    # term
    term_create_endpoints,
    term_update_endpoints,
    term_get_endpoints,
    term_delete_endpoints,
    # submission
    submission_get_endpoints,
]


all_endpoints = dict(d for endpoint_dict in endpoints for d in endpoint_dict.items())
