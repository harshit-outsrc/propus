# Anthology

## Examples
```
import asyncio
from datetime import datetime

from propus.anthology import Anthology
from propus.aws.ssm import AWS_SSM

STUDENT_RECORD = {
    'first_name': 'Calbright',
    'last_name': 'Student',
    'student_number': 'XYN112314',
    'phone_number': '(123) 123-1234',
    'dob': '2001/03/20',
    'email': 'test@test.com'
}

def full_workflow(anthology):
    # Step 1 Create Student (After Signed CSEP)
    STUDENT_RECORD['student_number'] = datetime.now().strftime('%m%d%H%M%S')
    response = asyncio.run(anthology.create_student(**STUDENT_RECORD))
    student_id = response.get("data").get("id")
    print(f'\n\n\nStudent Created Successfully: https://sisclientweb-tst-300915.campusnexus.cloud/#/students/{student_id}')

    # Step 2 Enroll Student in program (After Signed CSEP) < Repeat student would start here
    enrollment = asyncio.run(anthology.create_enrollment(
        student_id=student_id,
        program_id=6,
        program_version_id=10,
        grade_level_id=2,
        start_date='2023-03-10',
        grad_date='2026-03-10',
        catalog_year_id=6,
        version_start_date=827
    ))
    enrollment_id = enrollment.get("data").get("id")
    courses = asyncio.run(anthology.fetch_all_courses(student_id, enrollment_id))
    all_course_data = []
    last_course_id = None
    for course in courses.get('Items'):
        student_course_id = course.get('Entity').get('Id')
        student_enrollment_period = course.get('Entity').get('StudentEnrollmentPeriodId')
        course_id = course.get('Entity').get('CourseId')
        hours = course.get('Entity').get('ClockHours')
        terms = asyncio.run(anthology.fetch_term_for_courses([course_id]))
        last_term = terms.get('value')[-1]
        term_id = last_term.get('Id')
        start_date = last_term.get('TermStartDate')
        end_date = last_term.get('TermEndDate')
        course_data = asyncio.run(anthology.fetch_student_classes(student_id, term_id, course_ids=[course_id]))
        class_section_id = course_data.get('value')[0].get('Id')
        all_course_data.append({
            'student_id': student_id,
            'class_section_id': class_section_id,
            'start_date': start_date,
            'end_date': end_date,
            'student_course_id': student_course_id,
            'student_enrollment_id': student_enrollment_period
        })
        asyncio.run(anthology.register_course(student_course_id, student_enrollment_period, class_section_id, course_id, term_id, hours, start_date, end_date))
        last_course_id = student_course_id
    
    # Step 3: After student has completed first SSA
    for course in all_course_data:
        asyncio.run(anthology.add_attendance(**course))
    asyncio.run(anthology.change_student_status(
        student_enrollment_id=enrollment_id, new_status_id=85,  # Started Program Pathway
        note='Updating Student Status from API to SPP'
    ))

    # Step 4: Drop Student
    asyncio.run(
        anthology.drop_course(
            student_course_id=last_course_id, drop_date="2023/10/26 14:21:58", drop_reason_id=6, letter_grade="X"
        )
    )

    # Step 5: Reinstate Student
    response = asyncio.run(anthology.reinstate_course(student_course_id=last_course_id))

    # Step 6: Student has completed course
    for course in all_course_data:
        asyncio.run(anthology.post_final_grade(course_id=course.get('student_course_id'), letter_grade='CPL'))
    
    asyncio.run(anthology.change_student_status(
        student_enrollment_id=enrollment_id, new_status_id=88,  # Completed
        note='Updating Student Status from API to Completed'
    ))
    
    asyncio.run(anthology.create_certificate(
        student_enrollment_id=enrollment_id,
        notes='This is a certificate added via API! Congratulations'
    ))


if __name__ == '__main__':
    ssm = AWS_SSM.build()
    anthology_creds = ssm.get_param('anthology.test', param_type='json')
    anthology = Anthology(**anthology_creds)
    full_workflow(anthology)
```