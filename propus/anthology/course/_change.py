from typing import Dict


async def fetch_course_change_reason(self, filters: Dict = None) -> Dict:
    """
    API wrapper to retrieve course change reasons from Anthology

    Args:
        filters (Dict, optional): Dictionary of possible filters for grade responses. Possible responses are:
            - drop (must be set to True or False)
            - pass_fail (must be set to True or False)
            Defaults to None.

    Returns:
        Dict: direct response from anthology course change reason request
    """
    filter_string = (
        self.format_anthology_filters({f"course_{k}": "true" if v else "false" for k, v in filters.items()})
        if filters
        else ""
    )

    return self.make_request(
        url=self._get_endpoint("fetch_course_change_reason"),
        params={"$filter": filter_string} if filter_string else None,
    )
