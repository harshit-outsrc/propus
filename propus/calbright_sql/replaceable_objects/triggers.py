import os
from alembic_utils.pg_trigger import PGTrigger

env = os.environ.get("ENV")

new_ccc_application_trigger = PGTrigger(
    schema="public",
    signature="new_ccc_application_trigger",
    on_entity="ccc_application",
    definition=f"""
    AFTER INSERT ON ccc_application
    FOR EACH ROW
    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                        'new_ccc_application_trigger')
    """,
)

new_enrollment_trigger = PGTrigger(
    schema="public",
    signature="new_enrollment_trigger",
    on_entity="enrollment",
    definition=f"""
    AFTER INSERT ON enrollment
    FOR EACH ROW
    EXECUTE PROCEDURE invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                        'new_enrollment_trigger')
    """,
)

new_certificate_trigger = PGTrigger(
    schema="public",
    signature="new_certificate_trigger",
    on_entity="enrollment",
    definition=f"""
    AFTER INSERT OR UPDATE OF completion_date, enrollment_status_id
    ON enrollment
    FOR EACH ROW
    WHEN (new.completion_date IS NOT NULL and new.enrollment_status_id IS NOT NULL)
    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                        'new_certificate_trigger');
    """,
)

update_create_grade_trigger = PGTrigger(
    schema="public",
    signature="update_create_grade_trigger",
    on_entity="enrollment_course_term",
    definition=f"""
    AFTER UPDATE OF grade_status, grade_id
    ON enrollment_course_term
    FOR EACH ROW
    WHEN (new.grade_id IS NOT NULL and new.grade_status = 'certified' and old.grade_status <> new.grade_status)
    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                        'update_create_grade_trigger');
    """,
)

insert_create_grade_trigger = PGTrigger(
    schema="public",
    signature="insert_create_grade_trigger",
    on_entity="enrollment_course_term",
    definition=f"""
    AFTER INSERT
    ON enrollment_course_term
    FOR EACH ROW
    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                        'update_create_grade_trigger');
    """,
)

update_student_demographic_trigger = PGTrigger(
    schema="public",
    signature="update_student_demographic_trigger",
    on_entity="user",
    definition=f"""
    AFTER UPDATE OF ccc_id, anthology_id, gender_id, pronoun_id, salutation_id, suffix_id, first_name, middle_name,
      last_name, maiden_name, preferred_first_name, preferred_last_name, phone_number, calbright_email, personal_email
    ON user
    FOR EACH ROW
    WHEN (new.ccc_id <> '' AND new.anthology_id IS NOT NULL AND new.staff_id IS NULL)
    EXECUTE FUNCTION invoke_trigger_system_lambda('psql-trigger-handler-{env}-lambda', 'us-west-2',
                                                     'update_student_demographic_trigger');
    """,
)
