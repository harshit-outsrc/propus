import enum
from sqlalchemy import ForeignKey, VARCHAR, Enum
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from propus.calbright_sql import Base
from propus.calbright_sql.program import Program
from propus.calbright_sql.user import User


class LeadSource(enum.Enum):
    calbright_webpage = "Calbright Webpage"
    indirect_organization = "Indirect Organization"
    workforce_board = "Workforce Board"
    social_media = "Social Media"
    web = "Web"
    tv = "TV"
    radio = "Radio"
    event = "Event"
    conference = "Conference"
    employer = "Employer"
    referral = "Referral"
    zoominfo = "Zoominfo"
    flyer = "Flyer"
    dmv = "DMV"
    other = "Other"


class BrowserType(enum.Enum):
    mobile = "Mobile"
    desktop = "Desktop"


class ExpressInterest(Base):
    __tablename__ = "express_interest"

    # Using user.id here instead of student.ccc_id because a student expresses interest before they have applied
    # and retrieved a ccc_id
    user_id = mapped_column(UUID(), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship(
        "User",
        backref=backref("expressed_interest_user", order_by="ExpressInterest.created_at.desc()"),
        primaryjoin=user_id == User.id,
    )

    program_interest_id = mapped_column(UUID(), ForeignKey("program.id"), index=True)
    program_interest = relationship(
        "Program", backref="express_interest_program", primaryjoin=program_interest_id == Program.id
    )

    state_declared = mapped_column(VARCHAR(25))
    browser_type = mapped_column(Enum(BrowserType))
    landing_page = mapped_column(VARCHAR(500))
    lead_source = mapped_column(Enum(LeadSource))
    utm_medium = mapped_column(VARCHAR(100))
    utm_term = mapped_column(VARCHAR(100))
    utm_source = mapped_column(VARCHAR(100))
    utm_content = mapped_column(VARCHAR(200))
    utm_campaign = mapped_column(VARCHAR(150))
    referrer_url = mapped_column(VARCHAR(5000))
    ip_address = mapped_column(VARCHAR(50))
