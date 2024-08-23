from sqlalchemy import create_engine, DDL, text
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, AnyStr


class Calbright:
    _config_string = "postgresql+psycopg2://{user}:{pword}@{host}/{db}"

    def __init__(self, eng):
        super().__init__()
        self.engine = eng
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    @staticmethod
    def build(connection_configs: Dict, verbose: bool = False, connection_args={}):
        """
        build will return a basic configuration with an SQLAlchemy engine intialized

        Args:
            connection_configs (Dict): a dictionary with Database Connection Configs:
                {
                    'db': 'db_name',
                    'host': 'hostname',
                    'user': 'db_user',
                    'password': 'db_password',
                    'poolSize': 10, #Not Required (Default 50)
                    'maxOverflow': 10, #Not Required (Default 50)
                }

        Returns:
            Calbright: Instance of Calbright Sql Class
        """
        engine = create_engine(
            Calbright._config_string.format(
                user=connection_configs.get("user"),
                pword=connection_configs.get("password"),
                host=connection_configs.get("host"),
                db=connection_configs.get("db"),
            ),
            pool_size=connection_configs.get("poolSize", 50),
            max_overflow=connection_configs.get("maxOverflow", 50),
            echo=verbose,
            connect_args=connection_args,
        )
        return Calbright(engine)

    def add_all(self, model_objects: list[object]):
        """
        function used to allow add_all statements using SQLAlchemy session. Given a list of objects based on our ORM
        to add new records.

        Args:
            model_objects (List[SQLalchemy.model]): list of table model being inserted
        """
        try:
            self.session.add_all(model_objects)
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise err

    #  Execute sql file based on the engine (PostgreSQL) and path to file
    def execute_sql_file(self, path):
        """
        function used to execute sql files based on path passed using SQLalchemy DDL function.

        Args:
            path (str): SQL file path str
        """
        try:
            with open(path, encoding="utf8") as file:
                sql = file.read()

            ddl_stmt = DDL(sql)
            self.session.execute(ddl_stmt)
            self.session.commit()

        except Exception as err:
            self.session.rollback()
            raise err

    def execute(self, sql_stmt: AnyStr):
        sql_response = None
        with self.engine.connect() as con:
            resp = con.execute(text(sql_stmt))
            if resp.returns_rows:
                sql_response = [row for row in resp]
            con.commit()
        return sql_response

    def helper_fetch_configurations(self, config_type, key_name):
        table_map = {t.__tablename__: t for t in self.all_models}
        if not table_map:
            return None
        data = {}
        resp = self.session.query(table_map.get(config_type)).all()
        for row in resp:
            r_dict = row.to_dict()
            data[r_dict.get(key_name)] = r_dict
        return data

    # Add all models here for easy access
    from .address import Address
    from .alembic_version_history import AlembicVersionHistory
    from .assessment import Assessment
    from .assessment_submission import AssessmentSubmission
    from .ccc_application import CCCApplication
    from .course import Course
    from .course_version import CourseVersion
    from .student_form import StudentForm
    from .device import Device
    from .device_request import DeviceRequest
    from .ethnicity import Ethnicity
    from .enrollment import Enrollment
    from .enrollment_counselor import EnrollmentCounselor
    from .enrollment_prereq import EnrollmentPreReq
    from .enrollment_course_term import EnrollmentCourseTerm
    from .enrollment_status import EnrollmentStatus
    from .event import Event
    from .expressed_interest import ExpressInterest
    from .gender import Gender
    from .grade import Grade
    from .instructor_course import InstructorCourse
    from .learner_status import LearnerStatus
    from .competency import Competency
    from .pace_timeline_week import PaceTimelineWeek
    from .pace_timeline import PaceTimeline
    from .preferred_contact_method import PreferredContactMethod
    from .preferred_contact_time import PreferredContactTime
    from .program import Program
    from .program_version import ProgramVersion
    from .program_version_course import ProgramVersionCourse
    from .prereq_programs import PrereqProgram
    from .pronoun import Pronoun
    from .salutation import Salutation
    from .scheduled_event import ScheduledEvent
    from .staff import Staff
    from .student import Student
    from .student_address import StudentAddress
    from .student_ethnicity import StudentEthnicity
    from .suffix import Suffix
    from .student_contact_method import StudentContactMethod
    from .student_contact_time import StudentContactTime
    from .term import Term
    from .workflow_history import WorkflowHistory
    from .security_asn import ASN
    from .security_domain import Domain
    from .student_event import StudentEvent
    from .user_note import UserNote
    from .user_lms import UserLms
    from .user import User

    #  Order is important in the following list
    all_models = [
        PreferredContactMethod,
        PreferredContactTime,
        Address,
        Gender,
        Assessment,
        AssessmentSubmission,
        Course,
        EnrollmentStatus,
        Enrollment,
        EnrollmentPreReq,
        EnrollmentCounselor,
        EnrollmentCourseTerm,
        Event,
        ScheduledEvent,
        Term,
        Grade,
        CourseVersion,
        Ethnicity,
        ExpressInterest,
        LearnerStatus,
        Competency,
        Program,
        ProgramVersion,
        PrereqProgram,
        Student,
        Staff,
        User,
        UserNote,
        UserLms,
        InstructorCourse,
        StudentEvent,
        StudentContactMethod,
        Pronoun,
        StudentContactTime,
        ProgramVersionCourse,
        StudentAddress,
        StudentEthnicity,
        WorkflowHistory,
        Salutation,
        Suffix,
        CCCApplication,
        Device,
        DeviceRequest,
        StudentForm,
        ASN,
        Domain,
        PaceTimeline,
        PaceTimelineWeek,
        AlembicVersionHistory,
    ]
