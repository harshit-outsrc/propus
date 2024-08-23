from sqlalchemy import ForeignKey, text, CheckConstraint, UniqueConstraint, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref

from propus.calbright_sql import Base
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.program_version import ProgramVersion
from propus.helpers.sql_alchemy import update_or_create


class ProgramVersionCourse(Base):
    __tablename__ = "program_version_course"

    # The following id NEEDS to be specified here for the remote_side argument for self reference
    id = mapped_column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, index=True)

    program_version_id = mapped_column(UUID, ForeignKey("program_version.id"), index=True, nullable=False)
    program_version = relationship(
        "ProgramVersion",
        backref="program_course_version",
        primaryjoin=program_version_id == ProgramVersion.id,
    )

    course_version_id = mapped_column(UUID, ForeignKey("course_version.id"), index=True, nullable=False)
    course_version = relationship(
        "CourseVersion",
        backref="course_program_version",
        primaryjoin=course_version_id == CourseVersion.id,
    )

    next_program_version_course_id = mapped_column(
        UUID, ForeignKey("program_version_course.id", name="next_program_version_course_id"), index=True
    )
    next_program_version_course_record = relationship(
        "ProgramVersionCourse",
        backref=backref("next_program_version_course"),
        remote_side=[id],
    )

    is_first_course_in_program = mapped_column(BOOLEAN, default=False)

    __table_args__ = (
        UniqueConstraint("program_version_id", "course_version_id", name="uniq_program_course_version"),
        CheckConstraint(
            "(next_program_version_course_id != id)",
            name="is_not_self_referential",
        ),
    )

    def __repr__(self) -> str:
        return f"<ProgramVersionCourse: {self.program_version_id} - {self.course_version_id}>"

    def seed_data(self, session, **kwargs):
        seed_data = {
            "Medical Coding for Physician Services_1.0": ["WF500_1", "MC500_1"],
            "Medical Coding for Physician Services_1.5": [
                "WF500_2",
                "MC500_1",
            ],  # Missing (Math, Read/Write)
            "Medical Coding for Physician Services_2.0": ["WF500_2", "MC500_2"],
            "Medical Coding for Physician Services_3.0": ["WF500_2", "MC500_2"],
            "Medical Coding for Physician Services_4.0": ["WF500_4", "MC500_3"],
            "Medical Coding for Physician Services_5.0": ["WF500_5", "MC500_3"],
            "Introduction to Information Technology Support (A+)_1.0": [
                "WF500_1",
                "IT500_1",
            ],
            "Introduction to Information Technology Support (A+)_1.5": [
                "WF500_2",
                "IT500_2",
            ],  # noqa: E501; Missing (Math, Read/Write)
            "Introduction to Information Technology Support (A+)_2.0": [
                "WF500_3",
                "IT500_3",
            ],  # noqa: E501; Missing (Math, Read/Write)
            "Introduction to Information Technology Support (A+)_3.0": [
                "WF500_3",
                "IT500_3",
            ],
            "Introduction to Information Technology Support (A+)_4.0": [
                "WF500_4",
                "IT500_4",
            ],
            "Introduction to Information Technology Support (A+)_5.0": [
                "WF500_5",
                "IT500_5",
            ],
            "Cybersecurity_1.0": ["WF500_1", "IT510_1"],
            "Cybersecurity_1.5": [
                "WF500_2",
                "IT510_2",
            ],  # Missing (Math, Read/Write)
            "Cybersecurity_2.0": [
                "WF500_3",
                "IT510_3",
            ],  # Missing (Math, Read/Write)
            "Cybersecurity_3.0": ["WF500_3", "IT510_3"],
            "Cybersecurity_4.0": ["WF500_4", "IT510_5"],
            "Cybersecurity_5.0": ["WF500_5", "IT510_5"],
            "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion_1.0": [
                "HC501_1",
                "HC502_1",
            ],
            "Upskilling for Equitable Health Impacts Diversity, Equity and Inclusion_2.0": [
                "HC501_2",
                "HC502_2",
            ],
            "Introduction to Data Analysis_1.0": ["BUS501_1"],  # Missing BUS500 (Competency 204)
            "Introduction to Data Analysis_2.0": ["BUS500_1"],
            "Introduction to Data Analysis_3.0": ["BUS500_2", "BUS501_2"],
            "Transition to Technology - Customer Relationship Management Platform Administration_1.0": [
                "IT520_1",
                "IT525_1",
            ],  # noqa: E501;
            "Transition to Technology - Customer Relationship Management Platform Administration_2.0": [
                "IT520_2",
                "IT525_2",
            ],  # noqa: E501;
            "Transition to Technology: Introduction to Networks_1.0": ["IT532_1", "IT533_1"],
            "Project Management_1.0": ["BUS520_1", "BUS521_1", "BUS522_1"],
        }

        for program_version in Base.program_version:
            p_id = program_version.id
            key = f"{program_version.program.program_name}_{program_version.version_id}"
            course_versions = seed_data.get(key)
            for cv in course_versions:
                course_version = Base.course_versions.get(cv)
                row = {
                    "program_version_id": p_id,
                    "course_version_id": course_version.id,
                }

                update_or_create(
                    session,
                    ProgramVersionCourse,
                    row,
                    program_version_id=row.get("program_version_id"),
                    course_version_id=row.get("course_version_id"),
                )
        self.session_commit_with_rollback_on_unique(session)
