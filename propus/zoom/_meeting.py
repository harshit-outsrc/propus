from typing import AnyStr, Dict

# _meeting.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RestAPIClient class.
# These functions are loaded in the __init__.py file


def fetch_meeting(self, meeting_id: AnyStr) -> Dict:
    """Retrieve the given meeting's details.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meeting

    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="meeting", params={"{meetingId}": meeting_id})


def fetch_meeting_invitation(self, meeting_id):
    """Retrieve the meeting invitation note for a specific meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingInvitation

    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="meeting_invitation", params={"{meetingId}": meeting_id})


def fetch_meeting_polls(self, meeting_id):
    """Polls allow the meeting host to survey attendees. List all polls of a meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingPolls
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="meeting_polls", params={"{meetingId}": meeting_id})


def fetch_past_meeting_details(self, meeting_id):
    """Get information about a past meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingDetails
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="past_meeting_details", params={"{meetingId}": meeting_id})


def fetch_past_meeting_instances(self, meeting_id):
    """Return a list of past meeting instances.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetings
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="past_meeting_instances", params={"{meetingId}": meeting_id})


def fetch_past_meeting_participants(self, meeting_id):
    """Retrieve information on participants from a past meeting.
    Note the API doesn't return results if there's only one participant in a meeting.
    Documentation:
        https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingParticipants
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_bulk_data_by_endpoint(endpoint="past_meeting_participants", params={"{meetingId}": meeting_id})


def fetch_past_meeting_polls(self, meeting_id):
    """Polls allow the meeting host to survey attendees. List poll results of a meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingPolls
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="past_meeting_polls", params={"{meetingId}": meeting_id})


def fetch_past_meeting_qa(self, meeting_id):
    """The question & answer (Q&A) feature for Zoom Meetings lets attendees ask questions during a meeting
    and lets the other attendees answer those questions.
    List Q&A of a specific meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingQA
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="past_meeting_qa", params={"{meetingId}": meeting_id})


def fetch_poll(self, meeting_id, poll_id):
    """Polls allow the meeting host to survey attendees. Retrieve information about a specific meeting poll.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollGet
    Arguments:
        meeting_id (AnyStr): Meeting ID
        pool_id (AnyStr): Poll ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="poll", params={"{meetingId}": meeting_id, "{pollId}": poll_id})


def fetch_polls(self, meeting_id):
    """Polls allow the meeting host to survey attendees. List all polls of a meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingPolls
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_bulk_data_by_endpoint(endpoint="polls", params={"{meetingId}": meeting_id})


def fetch_registrant(self, meeting_id, registrant_id):
    """Retrieve details on a specific user who has registered for the meeting.
    A host or a user with administrative permissions can require registration for Zoom meetings.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantGet
    Arguments:
        meeting_id (AnyStr): Meeting ID
        registrant_id (AnyStr): Registrant ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(
        endpoint="registrant", params={"{meetingId}": meeting_id, "{registrantId}": registrant_id}
    )


def fetch_registrants(self, meeting_id):
    """A host or a user with admin permission can require registration for a Zoom meeting.
    List users that have registered for a meeting.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrants
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_bulk_data_by_endpoint(endpoint="registrants", params={"{meetingId}": meeting_id})


def fetch_registration_questions(self, meeting_id):
    """List registration questions that will be displayed to users while registering for a meeting.
    Documentation:
        https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantsQuestionsGet
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="registration_questions", params={"{meetingId}": meeting_id})


def fetch_survey(self, meeting_id):
    """Display information about a meeting survey. Prerequisites: * The host has a Pro license.
    * The Meeting Survey feature is enabled on the host's account. * The meeting must be a scheduled meeting.
    Instant meetings do not have survey features enabled.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyGet
    Arguments:
        meeting_id (AnyStr): Meeting ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="survey", params={"{meetingId}": meeting_id})
