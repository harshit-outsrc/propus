from sqlalchemy import FLOAT, ForeignKey, UniqueConstraint, Enum, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from propus.helpers.sql_alchemy import update_or_create

from propus.calbright_sql import Base
from propus.calbright_sql.course import Course
from propus.calbright_sql.enrollment import LMS


class CourseVersion(Base):
    __tablename__ = "course_version"

    course_id = mapped_column(UUID, ForeignKey("course.id"), index=True, nullable=False)
    course = relationship("Course", backref="course_version_course", primaryjoin=course_id == Course.id)
    version_id = mapped_column(FLOAT, nullable=False)

    lms = mapped_column(Enum(LMS), nullable=True)
    lms_id = mapped_column(VARCHAR(100), index=True, unique=True, nullable=True)

    __table_args__ = (UniqueConstraint("course_id", "version_id", name="uniq_course_version"),)

    def seed_data(self, session, **kwargs):
        course_versions_by_name = {
            "MC500": 3,
            "IT500": 5,
            "IT510": 5,
            "HC501": 2,
            "HC502": 2,
            "WF510": 1,
            "WF500": 5,
            "BUS500": 2,
            "BUS501": 2,
            "IT520": 3,
            "IT525": 3,
            "IT532": 1,
            "IT533": 1,
            "BUS520": 1,
            "BUS521": 1,
            "BUS522": 1,
        }
        course_versions = {}
        for course_id, num_versions in course_versions_by_name.items():
            c_id = Base.course_name_to_id.get(course_id)
            for version in range(1, num_versions + 1):
                row = {"course_id": c_id, "version_id": version}
                record = update_or_create(
                    session,
                    CourseVersion,
                    row,
                    course_id=row.get("course_id"),
                    version_id=row.get("version_id"),
                )
                course_versions[f"{course_id}_{version}"] = record[0]
        self.session_commit_with_rollback_on_unique(session)
        Base.course_versions = course_versions
