import datetime
import json
from typing import Union, Optional
from propus.canvas.term import TermOverride


async def update_term(
    self,
    account_id: Union[str, int],
    term_id: Union[str, int],
    name: Optional[str] = None,
    start_at: Optional[datetime.datetime] = None,
    end_at: Optional[datetime.datetime] = None,
    sis_term_id: Optional[str] = None,
    overrides: Optional[list[TermOverride]] = None,
) -> dict:
    """
    Update a term
    :param self:
    :param account_id: The ID of the account to create the term in
    :param term_id: The ID of the term to update
    :param name: The name of the term
    :param start_at: The start date of the term
    :param end_at: The end date of the term
    :param sis_term_id: The SIS ID of the term
    :param overrides: The overrides for the term. This is passed as a list of dictionaries with the following keys:
        - override_enrollment_type: str - The type of enrollment to override - options are "StudentEnrollment",
        "TeacherEnrollment", "TaEnrollment", "DesignerEnrollment",
        - override_start_at: datetime.datetime - The start date for the override
        - override_end_at: datetime.datetime - The end date for the override
    :return: The created term
    """
    payload = {"enrollment_term": {}}

    if name is not None:
        payload["enrollment_term"]["name"] = name
    if start_at is not None:
        payload["enrollment_term"]["start_at"] = start_at.isoformat()
    if end_at is not None:
        payload["enrollment_term"]["end_at"] = end_at.isoformat()
    if sis_term_id is not None:
        payload["enrollment_term"]["sis_term_id"] = sis_term_id

    if overrides:
        payload["enrollment_term"]["overrides"] = {}
        for override in overrides:
            payload["enrollment_term"]["overrides"][override.override_enrollment_type] = {}
            if override.override_start_at:
                payload["enrollment_term"]["overrides"][override.override_enrollment_type][
                    "start_at"
                ] = override.override_start_at.isoformat()

            if override.override_end_at:
                payload["enrollment_term"]["overrides"][override.override_enrollment_type][
                    "end_at"
                ] = override.override_end_at.isoformat()

    return self.make_request(
        req_type="put",
        url=self._get_endpoint("update_term", {"<account_id>": account_id, "<term_id>": term_id}),
        data=json.dumps(payload),
    )
