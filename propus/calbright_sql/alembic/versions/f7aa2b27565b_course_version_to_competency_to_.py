"""Course Version to Competency to Assessment changes

Revision ID: f7aa2b27565b
Revises: cd59dfd1cc74
Create Date: 2024-06-14 12:59:57.662578

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.session import Session

from propus.calbright_sql.competency import Competency
from propus.calbright_sql.course_version import CourseVersion
from propus.strut import Strut
from propus.aws.ssm import AWS_SSM
from propus.calbright_sql.seed_data.competency import COMPETENTCY_TO_COURSE_VERSION, TRAILHEAD_DATA

from propus.calbright_sql.enrollment import LMS

# revision identifiers, used by Alembic.
revision = "f7aa2b27565b"
down_revision = "cd59dfd1cc74"
branch_labels = None
depends_on = None


def fetch_strut_competencies(strut):
    return [
        {
            "lms": LMS.strut,
            "lms_id": str(c.get("id")),
            "state": c.get("state"),
            "description": c.get("description"),
            "competency_name": c.get("title"),
        }
        for c in strut.fetch_competencies(start=0, shallow=False)
        if c.get("state") in ["retired", "published"]
    ]


def seed_competency_data(session, strut):
    course_versions = {
        f"{cv.course.course_code}_{int(cv.version_id)}": cv.id
        for cv in session.execute(select(CourseVersion)).scalars().all()
    }

    competency_seed_data = fetch_strut_competencies(strut)
    for lms_id, competency in TRAILHEAD_DATA.items():
        competency_seed_data.append(
            {
                "lms": LMS.trailhead,
                "lms_id": lms_id,
                "competency_name": competency.get("name"),
                "course_version_id": course_versions.get(competency.get("course_version")),
            }
        )
    for competency in competency_seed_data:
        if not competency.get("course_version_competency") and not COMPETENTCY_TO_COURSE_VERSION.get(
            competency.get("lms_id")
        ):
            continue
        competency["course_version_id"] = course_versions.get(
            COMPETENTCY_TO_COURSE_VERSION.get(competency.get("lms_id"))
        )

        session.add(Competency(**competency))
    session.commit()


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    # Delete everything from competency table as we will be re-seeding it
    session.execute(text("DELETE FROM course_version_competency WHERE id IS NOT null"))
    session.execute(text("DELETE FROM pace_timeline_week WHERE id IS NOT null"))
    session.execute(text("DELETE FROM competency WHERE id IS NOT null"))
    session.commit()
    sa.Enum("summative", "formative", "final_grade", name="assessmenttype").create(op.get_bind())
    op.drop_index("ix_course_version_competency_competency_id", table_name="course_version_competency")
    op.drop_index("ix_course_version_competency_course_version_id", table_name="course_version_competency")
    op.drop_index("ix_course_version_competency_id", table_name="course_version_competency")
    op.drop_table("course_version_competency")
    op.drop_index("ix_competency_assessment_assessment_id", table_name="competency_assessment")
    op.drop_index("ix_competency_assessment_competency_id", table_name="competency_assessment")
    op.drop_index("ix_competency_assessment_id", table_name="competency_assessment")
    op.drop_table("competency_assessment")
    op.add_column("assessment", sa.Column("competency_id", sa.UUID(), nullable=False))
    op.add_column(
        "assessment",
        sa.Column(
            "assessment_type",
            postgresql.ENUM("summative", "formative", "final_grade", name="assessmenttype", create_type=False),
            nullable=False,
        ),
    )
    op.drop_constraint("assessment_name_key", "assessment", type_="unique")
    op.create_index(op.f("ix_assessment_competency_id"), "assessment", ["competency_id"], unique=False)
    op.create_foreign_key(None, "assessment", "competency", ["competency_id"], ["id"])
    op.drop_column("assessment", "type")
    op.add_column("competency", sa.Column("course_version_id", sa.UUID(), nullable=False))
    op.add_column(
        "competency",
        sa.Column(
            "lms", postgresql.ENUM("strut", "trailhead", "canvas", name="lms", create_type=False), nullable=False
        ),
    )
    op.alter_column(
        "competency", "lms_id", existing_type=sa.INTEGER(), type_=sa.VARCHAR(length=50), existing_nullable=True
    )
    op.drop_index("ix_competency_salesforce_id", table_name="competency")
    op.create_index(op.f("ix_competency_course_version_id"), "competency", ["course_version_id"], unique=False)
    op.create_foreign_key(None, "competency", "course_version", ["course_version_id"], ["id"])
    op.drop_column("competency", "salesforce_id")
    seed_competency_data(session, Strut(AWS_SSM.build("us-west-2").get_param("strut")))


def downgrade() -> None:
    op.add_column("competency", sa.Column("salesforce_id", sa.VARCHAR(length=25), autoincrement=False, nullable=True))
    op.drop_constraint(None, "competency", type_="foreignkey")
    op.drop_index(op.f("ix_competency_course_version_id"), table_name="competency")
    op.create_index("ix_competency_salesforce_id", "competency", ["salesforce_id"], unique=True)
    op.alter_column(
        "competency", "lms_id", existing_type=sa.VARCHAR(length=50), type_=sa.INTEGER(), existing_nullable=True
    )
    op.drop_column("competency", "lms")
    op.drop_column("competency", "course_version_id")
    op.add_column("assessment", sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, "assessment", type_="foreignkey")
    op.drop_index(op.f("ix_assessment_competency_id"), table_name="assessment")
    op.create_unique_constraint("assessment_name_key", "assessment", ["name"])
    op.drop_column("assessment", "assessment_type")
    op.drop_column("assessment", "competency_id")
    op.create_table(
        "competency_assessment",
        sa.Column("competency_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("assessment_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid_generate_v4()"), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessment.id"], name="competency_assessment_assessment_id_fkey"),
        sa.ForeignKeyConstraint(["competency_id"], ["competency.id"], name="competency_assessment_competency_id_fkey"),
        sa.PrimaryKeyConstraint("competency_id", "assessment_id", "id", name="competency_assessment_pkey"),
    )
    op.create_index("ix_competency_assessment_id", "competency_assessment", ["id"], unique=False)
    op.create_index("ix_competency_assessment_competency_id", "competency_assessment", ["competency_id"], unique=False)
    op.create_index("ix_competency_assessment_assessment_id", "competency_assessment", ["assessment_id"], unique=False)
    op.create_table(
        "course_version_competency",
        sa.Column("course_version_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("competency_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("id", sa.UUID(), server_default=sa.text("uuid_generate_v4()"), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.Column(
            "modified_at", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["competency_id"], ["competency.id"], name="course_version_competency_competency_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["course_version_id"], ["course_version.id"], name="course_version_competency_course_version_id_fkey"
        ),
        sa.PrimaryKeyConstraint("course_version_id", "competency_id", "id", name="course_version_competency_pkey"),
    )
    op.create_index("ix_course_version_competency_id", "course_version_competency", ["id"], unique=False)
    op.create_index(
        "ix_course_version_competency_course_version_id",
        "course_version_competency",
        ["course_version_id"],
        unique=False,
    )
    op.create_index(
        "ix_course_version_competency_competency_id", "course_version_competency", ["competency_id"], unique=False
    )
    sa.Enum("summative", "formative", "final_grade", name="assessmenttype").drop(op.get_bind())
