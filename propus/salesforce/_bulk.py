from time import sleep
from typing import AnyStr
from propus.helpers.etl import clean_null_bytes
from propus.salesforce.exceptions import SalesforceJobFailed, SalesforceOperationError
import csv
import json
import io


def _create_query_job(
    self,
    soql_query: AnyStr,
    operation: AnyStr = "query",
    contentType: AnyStr = "CSV",
    columnDelimiter: AnyStr = "COMMA",
    lineEnding: AnyStr = "LF",
):
    """Creates a bulk query job based on Bulk API 2.0
    Docs: https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/bulk_api_2_0.htm

    Args:
        soql_query (AnyStr): Select SOQL Query used for creating the job to fetch the data
        operation (AnyStr, optional): Operation used for the job, query and queryAll(deleted and archived records)
            are allowed. Defaults to "query".
        contentType (AnyStr, optional): Only Supports CSV currently. Defaults to CSV.
        columnDelimiter (AnyStr, optional): BACKQUOTED, CARET, COMMA, PIPE, SEMICOLON, and TAB are allowed.
            Defaults to COMMA.
        lineEnding (AnyStr, optional): LF and CRLF are allowed. Defaults to LF.

    Returns:
        Dict: Response with Job ID created from Salesforce
    """

    payload = {
        "operation": operation,
        "query": soql_query,
        "contentType": contentType,
        "columnDelimiter": columnDelimiter,
        "lineEnding": lineEnding,
    }

    url = self._get_endpoint("create_bulk_query_job")
    return self.make_request(url, data=json.dumps(payload), req_type="post")


def _abort_query_job(self, job_id: AnyStr):
    """To abort a job, you must be the job’s creator or have the Manage Data Integrations permission.
    You can only abort jobs that are in the following states:
        - UploadComplete
        - InProgress

    Args:
        job_id (AnyStr): Job ID that is being Aborted.

    Returns:
        Dict: Response with Job ID aborted on Salesforce
    """
    payload = {"state": "Aborted"}

    url = self._get_endpoint("query_bulk_job", {"<sf_jobid>": job_id})

    return self.make_request(url, data=json.dumps(payload), req_type="patch")


def _delete_query_job(self, job_id: AnyStr):
    """You can only delete jobs that are in the following states:
        - JobComplete
        - Aborted
        - Failed

    Args:
        job_id (AnyStr): Job ID that is being deleted.

    Returns:
        Response with "204 No Content" from Salesforce
    """

    url = self._get_endpoint("query_bulk_job", {"<sf_jobid>": job_id})

    return self.make_request(url, req_type="delete")


def _get_query_job(self, job_id: AnyStr):
    """Get information about a job query

    Args:
        job_id (AnyStr): Job ID requested information on.

    Returns:
        Dict: Response with Job data and state on Salesforce
    """

    url = self._get_endpoint("query_bulk_job", {"<sf_jobid>": job_id})

    return self.make_request(url, req_type="get")


def _get_query_job_results(self, job_id: AnyStr, locator: AnyStr = None, max_records: int = None):
    """Get results from a query job that has the state of JobComplete

    Args:
        job_id (AnyStr): Job ID for the requested results.
        locator (AnyStr, optional): string that identifies a specific set of query results. Locator string for next
            set of results in the response of each request. Defaults to None since the first request will be the
            first set of results.
        max_records (int, optional): Maximum number of records to retrieve per set of results for the query. Large
            results may experience timeouts. Defaults to None since the server uses a default value base on the
            service if not specified.

    Returns:
        Dict: Response from Salesforce contains Locator for next set, Number of Records in results request
            followed by record format of job creation. Default is CSV format with COMMA.
    """

    url = self._get_endpoint("query_bulk_job_results", {"<sf_jobid>": job_id})
    adj_headers = self.headers["get"]
    adj_headers["accept"] = "text/csv"

    parameters = {}

    if locator is not None:
        parameters["locator"] = locator

    if max_records is not None:
        parameters["maxRecords"] = max_records
    job_results = self.make_request(url, headers=adj_headers, req_type="get", params=parameters)

    locator = (
        job_results.headers.get("Sforce-Locator", "") if job_results.headers.get("Sforce-Locator", "") != "null" else ""
    )

    number_of_records = int(job_results.headers.get("Sforce-NumberOfRecords"))

    return {
        "locator": locator,
        "number_of_records": number_of_records,
        "records": clean_null_bytes(job_results.text),
    }


def _bulk_query_results(self, job_id, max_records: int = None):
    """Yields a generator from query results to process large amounts of data into dict or file

    Args:
        job_id (AnyStr): job id of the results that are being queried
        max_records (int, optional): Default is None, letting API determine or defining the batch size of records

    Yields:
        Generator[str, None, None]: Data returned from query operations
    """

    locator = "START"
    while locator:
        if locator == "START":
            locator = None
        results = self._get_query_job_results(job_id, locator, max_records)
        locator = results.get("locator")
        yield results.get("records")


def get_dict_from_bulk_query_results(csv_data):
    """Function processes CSV data from a generator that grabs results from bulk api 2.0 jobs and returns a list of
        dict values using csv.DictReader.

    Args:
        csv_data (Generator[str, None, None]): document data returned from bulk api 2.0 results

    Returns:
        List[Dict]: Returns a list of dict values
    """
    all_results = []
    for data in csv_data:
        all_results += list(csv.DictReader(io.StringIO(data)))
    return all_results


def bulk_custom_query_operation(
    self,
    soql_query: AnyStr,
    wait=5,
    max_tries=1,
    query_all=False,
    max_records: int = None,
    dict_format=True,
):
    """This function rolls up the use for creating, waiting, processing the job results and finally clean up for
        Bulk API 2.0. This function is not lambda safe as it could result in major delays/time increases.

        Bulk API 2.0 doesn’t support SOQL queries that include any of these items:
        - GROUP BY, LIMIT, ORDER BY, OFFSET, or TYPEOF clauses.
            Don’t use ORDER BY or LIMIT, as they disable PKChunking for the query. With PKChunking disabled, the
            query takes longer to execute, and potentially results in query timeouts. If ORDER BY or LIMIT is used,
            and you experience query time outs, then remove the ORDER BY or LIMIT clause before any subsequent
            troubleshooting.

        - Aggregate Functions such as COUNT().
        - Date functions in GROUP BY clauses. (Date functions in WHERE clauses are supported.)
        - Compound address fields or compound geolocation fields. (Instead, query the individual components of
            compound fields.)
        - Parent-to-child relationship queries. (Child-to-parent relationship queries are supported.)

    Args:
        soql_query (AnyStr): SOQL Select Query to use for bulk query
        wait (int, optional): Time periods to wait for checking if the query job has finished. Defaults to 5.
        max_tries (int, optional): _description_. Defaults to 1.
        query_all (bool, optional): If True, includes migrated/archived/deleted records. Defaults to False.
        max_records (int, optional): Record batch size returned when grabbing results. Defaults to None.
        dict_format (bool, optional): _description_. Defaults to True.

    Raises:
        Exception: Failed Bulk Query returning state and records processed

    Returns:
        List[Dict]: Returns a dictionary list of records from the query results if dict_format is set
            or
        Generator[str, None, None]: Returns a CSV document data
    """

    if query_all:
        job = self._create_query_job(soql_query, operation="queryAll")
    else:
        job = self._create_query_job(soql_query)

    job_status = self._get_query_job(job.get("id"))

    # UploadComplete, InProgress, Aborted, JobComplete, Failed
    while job_status.get("state") not in ["JobComplete", "Failed", "Aborted"] and max_tries > 0:  # noqa: W503
        self.logger.info(
            f"Waiting for job to complete for {wait} seconds, will retry {max_tries} times. "
            f"Job Status: {job_status.get('id')} - {job_status.get('state')}"
        )
        sleep(wait)
        wait *= 2
        max_tries -= 1
        job_status = self._get_query_job(job.get("id"))

    if job_status.get("state") == "Failed":
        raise SalesforceJobFailed(
            job_status.get("id"),
            job_status.get("state"),
            job_status.get("numberRecordsProcessed"),
        )
    elif job_status.get("state") != "JobComplete" and max_tries == 0:
        raise SalesforceOperationError(
            f"Job ID: {job_status.get('id')} - {job_status.get('state')}, maximum retries met without job finishing."
        )

    results = self._bulk_query_results(job.get("id"), max_records)

    if dict_format:
        results = get_dict_from_bulk_query_results(results)

    self._delete_query_job(job.get("id"))

    return results
