from sqlalchemy import TIMESTAMP, DATE, INTEGER, BOOLEAN, VARCHAR, DECIMAL
from sqlalchemy.orm import mapped_column

from propus.calbright_sql import Base


class CCCApplication(Base):
    __tablename__ = "ccc_application"

    # Additional Fields to determine if the student is flagged or has been processed
    processed_application = mapped_column(BOOLEAN, default=False)
    blocked_application = mapped_column(BOOLEAN, default=False)

    app_id = mapped_column(INTEGER, nullable=False)
    accepted_terms = mapped_column(BOOLEAN, default=False)
    accepted_terms_tstmp = mapped_column(DATE)
    ccc_id = mapped_column(VARCHAR(8), nullable=False, index=True)
    ip_addr_acct_create = mapped_column(VARCHAR(40))
    ip_addr_app_create = mapped_column(VARCHAR(40))
    status = mapped_column(VARCHAR(50))
    college_id = mapped_column(VARCHAR(3))
    term_id = mapped_column(DECIMAL)
    major_id = mapped_column(DECIMAL)
    intended_major = mapped_column(VARCHAR(30))
    edu_goal = mapped_column(VARCHAR(50))
    highest_edu_level = mapped_column(VARCHAR(5))
    consent_indicator = mapped_column(BOOLEAN, default=False)
    app_lang = mapped_column(VARCHAR(2))
    ack_fin_aid = mapped_column(BOOLEAN, default=False)
    fin_aid_ref = mapped_column(BOOLEAN, default=False)
    confirmation = mapped_column(VARCHAR(30))
    streetaddress1 = mapped_column(VARCHAR(50))
    streetaddress2 = mapped_column(VARCHAR(50))
    city = mapped_column(VARCHAR(50))
    postalcode = mapped_column(VARCHAR(20))
    state = mapped_column(VARCHAR(2))
    nonusaprovince = mapped_column(VARCHAR(30))
    country = mapped_column(VARCHAR(2))
    non_us_address = mapped_column(BOOLEAN, default=False)
    address_val_override = mapped_column(BOOLEAN, default=False)
    address_val_over_tstmp = mapped_column(DATE)
    email = mapped_column(VARCHAR(254))
    email_verified = mapped_column(BOOLEAN, default=False)
    email_verified_tstmp = mapped_column(DATE)
    perm_streetaddress1 = mapped_column(VARCHAR(50))
    perm_streetaddress2 = mapped_column(VARCHAR(50))
    perm_city = mapped_column(VARCHAR(50))
    perm_postalcode = mapped_column(VARCHAR(20))
    perm_state = mapped_column(VARCHAR(2))
    perm_nonusaprovince = mapped_column(VARCHAR(30))
    perm_country = mapped_column(VARCHAR(2))
    address_same = mapped_column(BOOLEAN, default=False)
    mainphone = mapped_column(VARCHAR(19))
    phone_verified = mapped_column(BOOLEAN, default=False)
    phone_verified_tstmp = mapped_column(DATE)
    phone_type = mapped_column(VARCHAR(10))
    pref_contact_method = mapped_column(VARCHAR(255))
    enroll_status = mapped_column(VARCHAR(50))
    hs_edu_level = mapped_column(VARCHAR(50))
    hs_comp_date = mapped_column(DATE)
    higher_edu_level = mapped_column(VARCHAR(50))
    higher_comp_date = mapped_column(DATE)
    cahs_graduated = mapped_column(BOOLEAN, default=False)
    cahs_3year = mapped_column(BOOLEAN, default=False)
    hs_name = mapped_column(VARCHAR(30))
    hs_state = mapped_column(VARCHAR(2))
    hs_country = mapped_column(VARCHAR(2))
    hs_cds = mapped_column(VARCHAR(6))
    hs_ceeb = mapped_column(VARCHAR(7))
    hs_not_listed = mapped_column(BOOLEAN, default=False)
    college_count = mapped_column(DECIMAL)
    hs_attendance = mapped_column(DECIMAL)
    coenroll_confirm = mapped_column(BOOLEAN, default=False)
    gender = mapped_column(VARCHAR(50))
    pg_firstname = mapped_column(VARCHAR(50))
    pg_lastname = mapped_column(VARCHAR(50))
    pg_rel = mapped_column(VARCHAR(50))
    pg1_edu = mapped_column(VARCHAR(50))
    pg2_edu = mapped_column(VARCHAR(50))
    pg_edu_mis = mapped_column(VARCHAR(2))
    under19_ind = mapped_column(BOOLEAN, default=False)
    dependent_status = mapped_column(VARCHAR(50))
    race_ethnic = mapped_column(VARCHAR(50))
    hispanic = mapped_column(BOOLEAN)
    race_group = mapped_column(VARCHAR(80))
    race_ethnic_full = mapped_column(VARCHAR(1000))
    ssn = mapped_column(VARCHAR(50))
    birthdate = mapped_column(DATE)
    firstname = mapped_column(VARCHAR(50))
    middlename = mapped_column(VARCHAR(50))
    lastname = mapped_column(VARCHAR(50))
    suffix = mapped_column(VARCHAR(3))
    otherfirstname = mapped_column(VARCHAR(50))
    othermiddlename = mapped_column(VARCHAR(50))
    otherlastname = mapped_column(VARCHAR(50))
    citizenship_status = mapped_column(VARCHAR(50))
    alien_reg_number = mapped_column(VARCHAR(20))
    visa_type = mapped_column(VARCHAR(20))
    no_documents = mapped_column(BOOLEAN, default=False)
    alien_reg_issue_date = mapped_column(DATE)
    alien_reg_expire_date = mapped_column(DATE)
    alien_reg_no_expire = mapped_column(BOOLEAN, default=False)
    military_status = mapped_column(VARCHAR(50))
    military_discharge_date = mapped_column(DATE)
    military_home_state = mapped_column(VARCHAR(2))
    military_home_country = mapped_column(VARCHAR(2))
    military_ca_stationed = mapped_column(BOOLEAN, default=False)
    military_legal_residence = mapped_column(VARCHAR(2))
    ca_res_2_years = mapped_column(BOOLEAN, default=False)
    ca_date_current = mapped_column(DATE)
    ca_not_arrived = mapped_column(BOOLEAN, default=False)
    ca_college_employee = mapped_column(BOOLEAN, default=False)
    ca_school_employee = mapped_column(BOOLEAN, default=False)
    ca_seasonal_ag = mapped_column(BOOLEAN, default=False)
    ca_outside_tax = mapped_column(BOOLEAN)
    ca_outside_tax_year = mapped_column(DATE)
    ca_outside_voted = mapped_column(BOOLEAN)
    ca_outside_voted_year = mapped_column(DATE)
    ca_outside_college = mapped_column(BOOLEAN)
    ca_outside_college_year = mapped_column(DATE)
    ca_outside_lawsuit = mapped_column(BOOLEAN)
    ca_outside_lawsuit_year = mapped_column(DATE)
    res_status = mapped_column(VARCHAR(50))
    res_status_change = mapped_column(BOOLEAN, default=False)
    res_prev_date = mapped_column(DATE)
    adm_ineligible = mapped_column(INTEGER)
    elig_ab540 = mapped_column(BOOLEAN, default=False)
    res_area_a = mapped_column(DECIMAL)
    res_area_b = mapped_column(DECIMAL)
    res_area_c = mapped_column(DECIMAL)
    res_area_d = mapped_column(DECIMAL)
    experience = mapped_column(INTEGER)
    recommend = mapped_column(INTEGER)
    comments = mapped_column(VARCHAR(50))
    comfortable_english = mapped_column(BOOLEAN, default=False)
    financial_assistance = mapped_column(BOOLEAN, default=False)
    tanf_ssi_ga = mapped_column(BOOLEAN, default=False)
    foster_youths = mapped_column(BOOLEAN, default=False)
    academic_counseling = mapped_column(BOOLEAN, default=False)
    basic_skills = mapped_column(BOOLEAN, default=False)
    calworks = mapped_column(BOOLEAN, default=False)
    career_planning = mapped_column(BOOLEAN, default=False)
    child_care = mapped_column(BOOLEAN, default=False)
    counseling_personal = mapped_column(BOOLEAN, default=False)
    dsps = mapped_column(BOOLEAN, default=False)
    eops = mapped_column(BOOLEAN, default=False)
    esl = mapped_column(BOOLEAN, default=False)
    health_services = mapped_column(BOOLEAN, default=False)
    housing_info = mapped_column(BOOLEAN, default=False)
    employment_assistance = mapped_column(BOOLEAN, default=False)
    online_classes = mapped_column(BOOLEAN, default=False)
    reentry_program = mapped_column(BOOLEAN, default=False)
    scholarship_info = mapped_column(BOOLEAN, default=False)
    student_government = mapped_column(BOOLEAN, default=False)
    testing_assessment = mapped_column(BOOLEAN, default=False)
    transfer_info = mapped_column(BOOLEAN, default=False)
    tutoring_services = mapped_column(BOOLEAN, default=False)
    veterans_services = mapped_column(BOOLEAN, default=False)
    col1_ceeb = mapped_column(VARCHAR(7))
    col1_cds = mapped_column(VARCHAR(6))
    col1_not_listed = mapped_column(BOOLEAN, default=False)
    col1_name = mapped_column(VARCHAR(30))
    col1_degree_date = mapped_column(DATE)
    col1_degree_obtained = mapped_column(VARCHAR(50))
    col2_ceeb = mapped_column(VARCHAR(7))
    col2_cds = mapped_column(VARCHAR(6))
    col2_not_listed = mapped_column(BOOLEAN, default=False)
    col2_name = mapped_column(VARCHAR(30))
    col2_degree_date = mapped_column(DATE)
    col2_degree_obtained = mapped_column(VARCHAR(50))
    college_name = mapped_column(VARCHAR(50))
    district_name = mapped_column(VARCHAR(50))
    term_code = mapped_column(VARCHAR(15))
    term_description = mapped_column(VARCHAR(100))
    major_code = mapped_column(VARCHAR(30))
    major_description = mapped_column(VARCHAR(100))
    tstmp_submit = mapped_column(TIMESTAMP)
    tstmp_create = mapped_column(TIMESTAMP)
    tstmp_update = mapped_column(TIMESTAMP)
    ssn_display = mapped_column(VARCHAR(11))
    foster_youth_status = mapped_column(VARCHAR(50))
    foster_youth_preference = mapped_column(BOOLEAN, default=False)
    foster_youth_mis = mapped_column(BOOLEAN, default=False)
    foster_youth_priority = mapped_column(BOOLEAN, default=False)
    tstmp_download = mapped_column(TIMESTAMP)
    address_validation = mapped_column(VARCHAR(50))
    mail_addr_validation_ovr = mapped_column(BOOLEAN, default=False)
    zip4 = mapped_column(VARCHAR(4))
    perm_address_validation = mapped_column(VARCHAR(50))
    perm_zip4 = mapped_column(VARCHAR(4))
    discharge_type = mapped_column(VARCHAR(50))
    college_expelled_summary = mapped_column(BOOLEAN, default=False)
    col1_expelled_status = mapped_column(BOOLEAN, default=False)
    col2_expelled_status = mapped_column(BOOLEAN, default=False)
    rdd = mapped_column(DATE)
    ssn_type = mapped_column(VARCHAR(50))
    military_stationed_ca_ed = mapped_column(BOOLEAN, default=False)
    ip_address = mapped_column(VARCHAR(15))
    campaign1 = mapped_column(VARCHAR(255))
    campaign2 = mapped_column(VARCHAR(255))
    campaign3 = mapped_column(VARCHAR(255))
    orientation_encrypted = mapped_column(VARCHAR(50))
    transgender_encrypted = mapped_column(VARCHAR(50))
    ssn_exception = mapped_column(BOOLEAN, default=False)
    preferred_firstname = mapped_column(VARCHAR(50))
    preferred_name = mapped_column(BOOLEAN, default=False)
    ssn_no = mapped_column(BOOLEAN, default=False)
    grade_point_average = mapped_column(VARCHAR(5))
    highest_english_course = mapped_column(INTEGER)
    highest_english_grade = mapped_column(VARCHAR(2))
    highest_math_course_taken = mapped_column(INTEGER)
    highest_math_taken_grade = mapped_column(VARCHAR(2))
    highest_math_course_passed = mapped_column(INTEGER)
    highest_math_passed_grade = mapped_column(VARCHAR(2))
    hs_cds_full = mapped_column(VARCHAR(14))
    col1_cds_full = mapped_column(VARCHAR(14))
    col2_cds_full = mapped_column(VARCHAR(14))
    ssid = mapped_column(VARCHAR(10))
    no_perm_address_homeless = mapped_column(BOOLEAN, default=False)
    no_mailing_address_homeless = mapped_column(BOOLEAN, default=False)
    term_start = mapped_column(DATE)
    term_end = mapped_column(DATE)
    homeless_youth = mapped_column(BOOLEAN, default=False)
    cip_code = mapped_column(VARCHAR(6))
    major_category = mapped_column(VARCHAR(100))
    mainphoneintl = mapped_column(VARCHAR(25))
    secondphoneintl = mapped_column(VARCHAR(25))
    non_credit = mapped_column(BOOLEAN, default=False)
    fraud_score = mapped_column(INTEGER)
    fraud_status = mapped_column(DECIMAL)
    highest_grade_completed = mapped_column(VARCHAR(2))

    # Supplemental Questions on CCCApply Application that align to the CCCApply Database.
    current_jobs = mapped_column(INTEGER)
    current_job_hours = mapped_column(INTEGER)
    background_has_dependent = mapped_column(BOOLEAN, default=False)
    background_immigrant = mapped_column(BOOLEAN, default=False)
    background_military_veteran = mapped_column(BOOLEAN, default=False)
    background_recent_job_impact = mapped_column(BOOLEAN, default=False)
    background_incarcerated = mapped_column(BOOLEAN, default=False)
    reason_online_program = mapped_column(BOOLEAN, default=False)
    reason_skill_jobs = mapped_column(BOOLEAN, default=False)
    reason_affordable = mapped_column(BOOLEAN, default=False)
    reason_non_traditional_schedule = mapped_column(BOOLEAN, default=False)
    reason_caregiving_responsibilities = mapped_column(BOOLEAN, default=False)
    reason_other = mapped_column(VARCHAR(250))
    available_mornings = mapped_column(BOOLEAN, default=False)
    available_afternoons = mapped_column(BOOLEAN, default=False)
    available_evenings = mapped_column(BOOLEAN, default=False)
    available_weekends = mapped_column(BOOLEAN, default=False)
    contact_email = mapped_column(BOOLEAN, default=False)
    contact_phone_call = mapped_column(BOOLEAN, default=False)
    contact_text_message = mapped_column(BOOLEAN, default=False)
    acceptable_use_policy = mapped_column(BOOLEAN, default=False)
