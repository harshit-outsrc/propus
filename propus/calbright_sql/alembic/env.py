import os
import sys

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic_utils.replaceable_entity import register_entities
import alembic_postgresql_enum

from propus.calbright_sql import Base

from propus.calbright_sql.replaceable_objects.trigger_functions import (
    invoke_trigger_system_lambda,
)

from propus.calbright_sql.replaceable_objects.triggers import (
    new_ccc_application_trigger,
    new_enrollment_trigger,
    new_certificate_trigger,
    update_create_grade_trigger,
    update_student_demographic_trigger,
)

from propus.calbright_sql.replaceable_objects.db_extensions import (
    create_uuid_ossp,
    create_aws_commons,
    create_aws_lambda,
    # create_plpgsql,
)

# Add all models here for easy access
from propus.calbright_sql.security_asn import ASN
from propus.calbright_sql.address import Address
from propus.calbright_sql.alembic_version_history import AlembicVersionHistory
from propus.calbright_sql.assessment import Assessment
from propus.calbright_sql.assessment_submission import AssessmentSubmission
from propus.calbright_sql.ccc_application import CCCApplication
from propus.calbright_sql.competency import Competency
from propus.calbright_sql.course import Course
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.device import Device
from propus.calbright_sql.device_request import DeviceRequest
from propus.calbright_sql.security_domain import Domain
from propus.calbright_sql.ethnicity import Ethnicity
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.enrollment_counselor import EnrollmentCounselor
from propus.calbright_sql.enrollment_prereq import EnrollmentPreReq
from propus.calbright_sql.enrollment_course_term import EnrollmentCourseTerm
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.event import Event
from propus.calbright_sql.expressed_interest import ExpressInterest
from propus.calbright_sql.gender import Gender
from propus.calbright_sql.grade import Grade
from propus.calbright_sql.instructor_course import InstructorCourse
from propus.calbright_sql.learner_status import LearnerStatus
from propus.calbright_sql.pace_timeline_week import PaceTimelineWeek
from propus.calbright_sql.pace_timeline import PaceTimeline
from propus.calbright_sql.preferred_contact_method import PreferredContactMethod
from propus.calbright_sql.preferred_contact_time import PreferredContactTime
from propus.calbright_sql.program import Program
from propus.calbright_sql.program_version import ProgramVersion
from propus.calbright_sql.program_version_course import ProgramVersionCourse
from propus.calbright_sql.prereq_programs import PrereqProgram
from propus.calbright_sql.pronoun import Pronoun
from propus.calbright_sql.salutation import Salutation
from propus.calbright_sql.scheduled_event import ScheduledEvent
from propus.calbright_sql.staff import Staff
from propus.calbright_sql.student import Student
from propus.calbright_sql.student_address import StudentAddress
from propus.calbright_sql.student_ethnicity import StudentEthnicity
from propus.calbright_sql.student_event import StudentEvent
from propus.calbright_sql.student_form import StudentForm
from propus.calbright_sql.student_contact_method import StudentContactMethod
from propus.calbright_sql.student_contact_time import StudentContactTime
from propus.calbright_sql.suffix import Suffix
from propus.calbright_sql.term import Term
from propus.calbright_sql.workflow_history import WorkflowHistory
from propus.calbright_sql.user_lms import UserLms
from propus.calbright_sql.user_note import UserNote
from propus.calbright_sql.user import User


def set_registered_entities():
    """
    Set register entities for non-local environments since the functions and extensions are meant for an RDS context
    """
    register_entities(
        [
            # PSQL Functions
            invoke_trigger_system_lambda,
            # PSQL Triggers
            new_ccc_application_trigger,
            new_enrollment_trigger,
            new_certificate_trigger,
            update_create_grade_trigger,
            update_student_demographic_trigger,
            # PSQL Extensions
            create_uuid_ossp,
            create_aws_commons,
            create_aws_lambda,
            # create_plpgsql,
        ]
    )


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

env = os.environ.get("ENV")
if env == "localhost":
    db = os.environ.get("DB")
    host = "localhost"
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
elif env == "stage" or env == "prod":
    from propus.aws.ssm import AWS_SSM

    set_registered_entities()
    ssm = AWS_SSM.build("us-west-2")
    creds = ssm.get_param(f"psql.calbright.{env}.write", "json")

    db = creds.get("db")
    host = creds.get("host")
    user = creds.get("user")
    password = creds.get("password")
else:
    print("'ENV' environment variable must be set to 'localhost' or 'stage' prior to calling alembic")
    sys.exit()

config.set_main_option("sqlalchemy.url", f"postgresql://{user}:{password}@{host}/{db}")


def update_history(ctx, step, heads, run_args):
    from sqlalchemy import text

    if step.is_upgrade:
        revision_id = step.up_revision_id
        message = step.up_revision.doc
        ctx.connection.execute(
            text(
                f"""INSERT INTO alembic_version_history (version_number, revision_type, message) VALUES
                    ('{revision_id}', 'upgrade', '{message}')"""
            )
        )
    else:
        revision_id = step.down_revision_ids[0] if len(step.down_revision_ids) else None
        message = f"Downgrade from version: {step.up_revision_id} -> {revision_id}"
        ctx.connection.execute(
            text(
                f"""INSERT INTO alembic_version_history (version_number, revision_type, message) VALUES
                    ('{revision_id}', 'downgrade', '{message}')"""
            )
        )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            on_version_apply=update_history,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
