student_create_endpoints = {"create_student": "/api/commands/Common/Student/SaveNew"}

student_read_endpoints = {
    "student_by_id": "/api/commands/Common/Student/get",
    "student_search": "/ds/odata/Students",
}

student_update_endpoints = {
    "update_student": "/api/commands/Common/Student/Save",
    "change_student_status": "/api/commands/Academics/StudentEnrollmentPeriod/EnrollmentStatusChange",
}
