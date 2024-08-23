import json
from typing import Dict

from propus.anthology.student._exceptions import InvalidSearchParameters


async def student_by_id(self, student_id: int) -> Dict:
    """
    Query Anthology API by the anthology API

    Args:
        student_id (int): string representation of anthology's ID

    Returns:
        Dict: Student Payload from Anthology. Example:
        {
            "Id": 17557,
            "AcgEligReasonCode": null,
            "AgencyId": 0,
            "AlienNumber": "",
            "ArAccountStatus": "X",
            "ArBalance": 0.0000,
            "ArNextTransactionNumber": 0,
            "AssignedAdmissionsRepId": 2,
            "AthleticIdentifier": null,
            ...
        }
    """
    return self.make_request(
        req_type="post", url=self._get_endpoint("student_by_id"), data=json.dumps({"payload": {"id": student_id}})
    )


def get_filters(arguments):
    available_filters = {"first_name": "str", "last_name": "str", "student_number": "str", "student_number_or": "list"}

    filters = ""
    for f, t in available_filters.items():
        if arguments.get(f):
            if t == "str":
                anthology_key = "".join([a.capitalize() for a in f.split("_")])
                filters += f"{anthology_key} eq '{arguments.get(f)}' and "
            elif t == "list":
                f_list = f.split("_")
                anthology_key = "".join([a.capitalize() for a in f_list[:-1]])
                filters += (
                    "(" + f" {f_list[-1]} ".join([f"{anthology_key} eq '{k}'" for k in arguments.get(f)]) + ") and "
                )
    if filters == "":
        raise InvalidSearchParameters
    return filters[:-5]


async def student_search(self, **kwargs):
    """
    Issues a search against Anthology's search API. All filters passed in will be used as a binary AND argument

    Args:
        [at least one optional argument is required]
        first_name (str): [optional] First name entry
        last_name (str): [optional]  Last name entry
        student_number (str): [optional]  Student Number
        student_number_or (list): [optional]  Student Number OR

    Returns:
         Dict: List of matching Student Records from Anthology. Example:
         {
            "@odata.context": "https://sisclientweb-tst-300915.campusnexus.cloud/ds/campusnexus/$metadata#Students",
            "value": [
                {
                    "Id": 17557,
                    "AcgEligReasonCode": null,
                    "AgencyId": 0,
                    "AlienNumber": "",
                    "ArAccountStatus": "X",
                    "ArBalance": 0.0000,
                    "ArNextTransactionNumber": 0,
                    "AssignedAdmissionsRepId": 2,
                    "AthleticIdentifier": null,
                    ...
                }
            ]
        }
    """
    params = {"$filter": get_filters(kwargs)} if kwargs else None
    return self.make_request(url=self._get_endpoint("student_search"), params=params)
