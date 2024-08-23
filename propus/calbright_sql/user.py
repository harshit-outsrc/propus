from sqlalchemy import ForeignKey, VARCHAR, UUID, INTEGER, CheckConstraint, BOOLEAN, text
from sqlalchemy.orm import mapped_column, relationship, backref

from propus.calbright_sql import Base
from propus.calbright_sql.gender import Gender
from propus.calbright_sql.pronoun import Pronoun
from propus.calbright_sql.salutation import Salutation
from propus.calbright_sql.suffix import Suffix
from propus.calbright_sql.learner_status import LearnerStatus
from propus.calbright_sql.program import Program


class User(Base):
    __tablename__ = "user"
    # The following id NEEDS to be specified here for the remote_side argument for self reference `merged_parent_record`
    id = mapped_column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True)

    staff_id = mapped_column(UUID, ForeignKey("staff.id"), index=True)
    staff = relationship("Staff", back_populates="user")

    ccc_id = mapped_column(VARCHAR(12), ForeignKey("student.ccc_id"), index=True, unique=True)
    student = relationship("Student", back_populates="user")

    salesforce_id = mapped_column(VARCHAR(25), unique=True, index=True)
    anthology_id = mapped_column(INTEGER, unique=True, index=True)

    gender_id = mapped_column(UUID(), ForeignKey("gender.id"), index=True)
    gender = relationship("Gender", backref="user_gender", primaryjoin=gender_id == Gender.id)

    pronoun_id = mapped_column(UUID(), ForeignKey("pronoun.id"), index=True)
    pronoun = relationship("Pronoun", backref="user_pronoun", primaryjoin=pronoun_id == Pronoun.id)

    salutation_id = mapped_column(UUID(), ForeignKey("salutation.id"), index=True)
    salutation = relationship("Salutation", backref="user_salutation", primaryjoin=salutation_id == Salutation.id)

    suffix_id = mapped_column(UUID(), ForeignKey("suffix.id"), index=True)
    suffix = relationship("Suffix", backref="user_suffix", primaryjoin=suffix_id == Suffix.id)

    intended_program_id = mapped_column(UUID, ForeignKey("program.id"), nullable=True)
    intended_program = relationship(
        "Program", backref="intended_program", primaryjoin=intended_program_id == Program.id
    )

    first_name = mapped_column(VARCHAR(50), nullable=False, index=True)
    middle_name = mapped_column(VARCHAR(50))
    last_name = mapped_column(VARCHAR(50), nullable=False, index=True)
    maiden_name = mapped_column(VARCHAR(50), index=True)

    preferred_first_name = mapped_column(VARCHAR(100))
    preferred_last_name = mapped_column(VARCHAR(100))

    phone_number = mapped_column(VARCHAR(10), index=True)
    slack_id = mapped_column(VARCHAR(25), index=True)
    calbright_email = mapped_column(VARCHAR(100), index=True, unique=True)
    personal_email = mapped_column(VARCHAR(100), index=True)
    profile_image = mapped_column(VARCHAR(250))

    call_opt_out = mapped_column(BOOLEAN, default=False)
    sms_opt_out = mapped_column(BOOLEAN, default=False)

    is_test_user = mapped_column(BOOLEAN, default=False)

    is_duplicate_record = mapped_column(BOOLEAN, default=False)
    merged_user_id = mapped_column(UUID, ForeignKey("user.id", name="merged_user_id"), index=True)
    merged_parent_record = relationship("User", backref=backref("merged_parent"), remote_side=[id])

    learner_status_id = mapped_column(UUID(), ForeignKey("learner_status.id"), index=True)
    learner_status = relationship(
        "LearnerStatus", backref="user_interest_status", primaryjoin=learner_status_id == LearnerStatus.id
    )

    # The Following Fields are for Duplicate Student

    __table_args__ = (
        CheckConstraint(
            "learner_status_id IS NOT NULL OR (staff_id IS NOT NULL AND learner_status_id IS NULL)",
            name="learner_status_not_null",
        ),
        CheckConstraint(
            "ccc_id IS NOT NULL OR staff_id IS NOT NULL or salesforce_id IS NOT NULL", name="is_student_or_staff"
        ),
        CheckConstraint(
            "(is_duplicate_record IS true AND merged_user_id IS NOT NULL) or "
            "(is_duplicate_record IS false AND merged_user_id IS NULL)",
            name="is_merged_or_unique",
        ),
    )

    @staticmethod
    def seed_data(self, session, **kwargs):
        from propus.calbright_sql.seed_data.staff_ingestion import ingest_staff_data

        ingest_staff_data(session)
        self.session_commit_with_rollback_on_unique(session)
