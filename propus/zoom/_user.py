# _user.py
# Convenience functions that typically call get_data_by_endpoint, get_bulk_data_by_endpoint,
# or another boilerplate function from the RESTApiClient class.
# These functions are loaded in the __init__.py file


def create_user(self, action="ssoCreate", feature={}, user_info={}):
    """create_user creates a new Zoom user, e.g., for pre-provisioning a user before onboarding.

    Arguments:
        action (enum): The action to take to create the new user.
            Choices are ['create', 'autoCreate', 'custCreate', and 'ssoCreate'].
            Defaults to 'ssoCreate'
        feature (dict): Information about the user's features.
        user_info (dict): Information about the user.

        Example dictionary data to POST:
            {
                "action": "ssoCreate",
                "user_info": {
                    "email": "a.student@calbright.edu",
                    "first_name": "Amazing",
                    "last_name": "Student",
                    "display_name": "Amazing Student",
                    "type": 1,
                    "feature": {
                        "zoom_phone": true,
                        "zoom_one_type": 16
                        },
                    "plan_united_type": "1"
                }
            }

        Example dictionary response:
            {
                "email": "a.student@calbright.edu",
                "first_name": "Amazing",
                "id": "KDcuGIm1QgePTO8WbOqwIQ",
                "last_name": "Student",
                "type": 1
            }
    """
    user_info["feature"] = feature
    data = dict(action=action, user_info=user_info)
    endpoint = self._get_endpoint("users")
    response = self._make_request(endpoint, data=data, req_type="post")

    return response


def fetch_user(self, user_id):
    """View a user's information on a Zoom account.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/user

    Arguments:
        user_id (AnyStr): User ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="user", params={"{userId}": user_id})


def fetch_user_meetings(self, user_id):
    """List a meeting host user's scheduled meetings.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetings

    Arguments:
        user_id (AnyStr): User ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_bulk_data_by_endpoint(endpoint="user_meetings", params={"{userId}": user_id})


def fetch_user_assistants(self, user_id):
    """List a user's assistants.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/userAssistants

    Arguments:
        user_id (AnyStr): User ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="user_assistants", params={"{userId}": user_id})


def fetch_user_schedulers(self, user_id):
    """List all of a user's schedulers.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/userSchedulers

    Arguments:
        user_id (AnyStr): User ID

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="user_schedulers", params={"{userId}": user_id})


def fetch_user_summary(self):
    """Use this API to get a summary of users, including the number and types of users in the account.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/userSummary

    Arguments:
        None

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_data_by_endpoint(endpoint="user_summary")


def fetch_users(self):
    """Retrieve a list your account's users.
    Documentation: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/users

    Arguments:
        None

    Returns:
        data (dict): Data dictionary returned
    """
    return self.get_bulk_data_by_endpoint(endpoint="users")
