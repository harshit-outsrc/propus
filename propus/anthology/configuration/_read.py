from typing import AnyStr, Dict


async def fetch_configurations(self, configuration_type: AnyStr, **kwargs) -> Dict:
    """
    Simple configuration retriever from Anthology.

    Args:
        configuration_type (AnySTr): configuration type requested. The following list are possible retrieval types:
            - billing_method
            - catalog_year
            - ethnicity
            - gender
            - grade_level
            - program
            - program_version
            - pronoun
            - school_status
            - shift
            - start_date
            - suffix
            - term
            - title
        kwargs: Any additional arguments needed for the configuration fetching


    Returns:
        dict: Dictionary data of all available billing methods
    """
    if configuration_type in ["program_version", "program", "shift", "start_date"]:
        kwargs["campus_id"] = self._campus_id
    return self.make_request(
        url=self._get_endpoint(configuration_type, parameters={f"<{k}>": v for k, v in kwargs.items()})
    )
