course_drop_endpoints = {
    "fetch_drop_reason": "/ds/odata/StudentCourseStatusChangeReasons",
    "drop_course": "/api/commands/Academics/StudentCourse/DropCourse",
}

course_grade_endpoints = {
    "post_final_grade": "/api/commands/Academics/StudentCourse/PostFinalGrade",
    "fetch_grade": "/ds/odata/GradeScaleLetterGrades",
}

course_read_endpoints = {
    "fetch_all_courses": "/ds/odata/Courses",
    "fetch_course_for_enrollment": (
        "/api/course-registration/students/<student_id>/student-enrollment-periods/<enrollment_id>/student-courses",
        ["<student_id>", "<enrollment_id>"],
    ),
    "fetch_course": "/api/commands/Academics/StudentCourse/get",
    "fetch_term_for_courses": (
        "/ds/campusnexus/Terms/CampusNexus.GetStudentCourseRegistrationTermListCustom(campusId=<campus_id>,"
        + "courseIds='<course_ids>')?$select=<fields_to_return>&%24format=json&%24count=true&%24orderby=TermCode",
        ["<campus_id>", "<course_ids>", "<fields_to_return>"],
    ),
    "fetch_classes_for_courses": (
        "/ds/campusnexus/ClassSections/CampusNexus.GetStudentCourseRegistrationClassScheduleList(campusId=<campus_id>,"
        "termId=<term_id>,courseIds='<course_ids>',isCrossReferenceCourse=false,studentId=<student_id>,"
        "crossRefCourseId=0, isTransferSection = false)?$select=<fields_to_return>&$orderby=CourseName,SectionCode",
        ["<campus_id>", "<term_id>", "<course_ids>", "<student_id>", "<fields_to_return>"],
    ),
    "course_search": "/ds/odata/StudentCourses",
}

course_register_endpoints = {
    "add_new_course": "/api/commands/Academics/StudentCourse/saveNew",
    "register_course": "/api/commands/Academics/StudentCourse/savestudentcourse",
    "add_attendance": "/api/commands/Academics/Attendance/PostExternshipOnlineHours",
}

course_reinstate_endpoints = {
    "reinstate_course": "/api/commands/Academics/StudentCourse/ReinstateCourse",
}

course_change_endpoints = {"fetch_course_change_reason": "/ds/odata/StudentCourseStatusChangeReasons"}

course_unregister_endpoints = {"unregister_course": "/api/commands/Academics/StudentCourse/UnregisterStudentCourse"}
