from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from propus.calbright_sql import Base
from propus.calbright_sql.enrollment import Enrollment
from propus.calbright_sql.learner_status import LearnerStatus
from propus.calbright_sql.user import User


class WorkflowHistory(Base):
    __tablename__ = "workflow_history"

    # Using user.id here instead of student.ccc_id because a student moves through the workflow before they are an
    # applied student (before ccc_id)
    user_id = mapped_column(UUID, ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="workflow_history_user", primaryjoin=user_id == User.id)

    enrollment_id = mapped_column(UUID, ForeignKey("enrollment.id"), index=True)
    enrollment = relationship("Enrollment", backref="workflow_enrollment", primaryjoin=enrollment_id == Enrollment.id)

    to_status_id = mapped_column(UUID, ForeignKey("learner_status.id"), index=True, nullable=False)
    to_status = relationship(
        "LearnerStatus", backref="workflow_to_status", primaryjoin=to_status_id == LearnerStatus.id
    )

    from_status_id = mapped_column(UUID, ForeignKey("learner_status.id"), index=True)
    from_status = relationship(
        "LearnerStatus", backref="workflow_from_status", primaryjoin=from_status_id == LearnerStatus.id
    )

    salesforce_workflow_id = mapped_column(VARCHAR(25), unique=True, index=True)
