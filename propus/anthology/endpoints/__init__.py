from propus.anthology.endpoints.certificate import certificate_create_endpoints
from propus.anthology.endpoints.configuration import (
    configuration_create_endpoints,
    configuration_copy_endpoints,
    configuration_read_endpoints,
)
from propus.anthology.endpoints.course import (
    course_change_endpoints,
    course_drop_endpoints,
    course_grade_endpoints,
    course_read_endpoints,
    course_register_endpoints,
    course_reinstate_endpoints,
    course_unregister_endpoints,
)
from propus.anthology.endpoints.enrollment import enrollment_create_endpoints, enrollment_read_endpoints
from propus.anthology.endpoints.student import (
    student_create_endpoints,
    student_read_endpoints,
    student_update_endpoints,
)


end_points = [
    certificate_create_endpoints,
    configuration_create_endpoints,
    configuration_copy_endpoints,
    configuration_read_endpoints,
    course_change_endpoints,
    course_drop_endpoints,
    course_grade_endpoints,
    course_read_endpoints,
    course_register_endpoints,
    course_reinstate_endpoints,
    course_unregister_endpoints,
    enrollment_create_endpoints,
    enrollment_read_endpoints,
    student_create_endpoints,
    student_read_endpoints,
    student_update_endpoints,
]

all_endpoints = dict(d for endpoint_dict in end_points for d in endpoint_dict.items())

# The following assert assures that all endpoint files have unique keys ensuring nothing is lost when merging
assert sum([len(e.keys()) for e in end_points]) == len(all_endpoints), "all keys across endpoints should be unique"
