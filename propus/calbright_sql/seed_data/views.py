student_info_view = """
CREATE VIEW student_info AS
  SELECT
     s.ccc_id,
     u.first_name,
    u.middle_name,
    u.last_name,
    u.preferred_first_name,
    u.preferred_last_name,
    l.status,
    u.phone_number,
    s.mobile_number,
    s.home_phone_number,
    u.calbright_email,
    u.personal_email,
    sal.salutation,
    suf.suffix,
    g.gender,
    p.pronoun,
    a.address1,
    a.address2,
    a.city,
    a.state,
    a.zip,
    a.county,
    a.country
   FROM student s
     JOIN "user" u ON u.ccc_id::text = s.ccc_id::text
     LEFT JOIN gender g ON g.id = u.gender_id
     LEFT JOIN pronoun p ON p.id = u.pronoun_id
     LEFT JOIN salutation sal ON sal.id = u.salutation_id
     LEFT JOIN suffix suf ON suf.id = u.suffix_id
     JOIN learner_status l ON l.id = u.learner_status_id
     LEFT JOIN student_address sa ON sa.student_id = s.ccc_id AND current=True AND valid=True
     LEFT JOIN address a ON a.id = sa.address_id;
"""

student_enrollment_view = """
CREATE VIEW student_enrollment AS
    SELECT e.ccc_id as ccc_id,
        e.id AS enrollment_id,
        p.short_name as program,
        e.enrollment_date as enrollment_date,
        es.status AS enrollment_status,
        e.drop_date as enrollment_drop_date,
        e.completion_date as enrollment_completion_date,
        e.withdrawn_date as enrollment_withdrawn_date,
        ect.id AS enrollment_course_id,
        c.course_code AS course,
        t.term_name AS term,
        concat(ui.first_name, ' ', ui.last_name) AS instructor,
        g.grade AS grade,
        ect.grade_status AS grade_status,
        concat(uc.first_name, ' ', uc.last_name) AS concat,
        ect.certified_date AS grade_certified_date,
        ect.withdraw_date AS course_withdraw_date,
        ect.drop_date AS course_drop_date,
        ect.grade_date AS course_grade_date
    FROM enrollment e
        JOIN program_version pv ON pv.id = e.program_version_id
        JOIN program p ON p.id = pv.program_id
        JOIN enrollment_status es ON es.id = e.enrollment_status_id
        JOIN enrollment_course_term ect ON ect.enrollment_id = e.id
        JOIN course_version cv ON ect.course_version_id = cv.id
        JOIN course c ON cv.course_id = c.id
        JOIN term t ON t.id = ect.term_id
        LEFT JOIN grade g ON g.id = ect.grade_id
        LEFT JOIN "user" ui ON ui.staff_id = ect.instructor_id
        LEFT JOIN "user" uc ON uc.staff_id = ect.certified_by_id
    ORDER BY e.ccc_id, e.enrollment_date;
"""

progress_by_course_view = """
CREATE VIEW progress_by_course AS
SELECT enrollment.Id        AS enrollment_id,
       course_version.course_id,
       COUNT(competency.id) AS competencies,
       SUM(CASE
               WHEN assessment_submission.status = 'passed' AND assessment_type = 'summative' THEN 1
               ELSE 0 END)  AS competencies_passed,
       CAST(SUM(CASE
                    WHEN assessment_submission.status = 'passed' AND assessment_type = 'summative' THEN 1
                    ELSE 0 END) AS DECIMAL) /
       COUNT(competency.id) AS progress
FROM enrollment
         JOIN program_version ON program_version.Id = enrollment.program_version_id
         JOIN program ON program_version.program_id = program.Id
         JOIN program_version_course ON program_version_course.program_version_id = program_version.Id
         JOIN course_version ON program_version_course.course_version_id = course_version.Id
         JOIN competency
              ON course_version.id = competency.course_version_id
                  AND competency.competency_type = 'competency'
                  AND competency.is_active = True
                  AND competency.lms = 'canvas'
         LEFT JOIN assessment ON competency.id = assessment.competency_id
                  AND assessment_type = 'summative'
         LEFT JOIN assessment_submission ON assessment.id = assessment_submission.assessment_id
                  AND enrollment.id = assessment_submission.enrollment_id
GROUP BY enrollment.Id, course_Version.course_id;
"""

progress_by_enrollment_view = """
CREATE VIEW progress_by_enrollment AS
SELECT enrollment.Id        AS enrollment_id,
       COUNT(competency.id) AS competencies,
       SUM(CASE
               WHEN assessment_submission.status = 'passed' AND assessment_type = 'summative' THEN 1
               ELSE 0 END)  AS competencies_passed,
       CAST(SUM(CASE
                    WHEN assessment_submission.status = 'passed' AND assessment_type = 'summative' THEN 1
                    ELSE 0 END) AS DECIMAL) /
       COUNT(competency.id) AS progress
FROM enrollment
         JOIN program_version ON program_version.Id = enrollment.program_version_id
         JOIN program ON program_version.program_id = program.Id
         JOIN program_version_course ON program_version_course.program_version_id = program_version.Id
         JOIN course_version ON program_version_course.course_version_id = course_version.Id
         JOIN competency
              ON course_version.id = competency.course_version_id
                  AND competency.competency_type = 'competency'
                  AND competency.is_active = True
                  AND competency.lms = 'canvas'
         LEFT JOIN assessment ON competency.id = assessment.competency_id
                  AND assessment_type = 'summative'
         LEFT JOIN assessment_submission ON assessment.id = assessment_submission.assessment_id
                  AND enrollment.id = assessment_submission.enrollment_id
GROUP BY enrollment.Id
"""
