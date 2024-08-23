from dataclasses import dataclass
from typing import Literal, Optional
import datetime


@dataclass
class TermOverride:
    override_enrollment_type: Literal[
        "StudentEnrollment",
        "TeacherEnrollment",
        "TaEnrollment",
        "DesignerEnrollment",
    ]
    override_start_at: Optional[datetime.datetime] = None
    override_end_at: Optional[datetime.datetime] = None
