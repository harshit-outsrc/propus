user_create_endpoints = {
    "create_user": ("/api/v1/accounts/<account_id>/users", ["<account_id>"]),
}

user_get_endpoints = {
    "get_user": ("/api/v1/users/<user_id>", ["<user_id>"]),
    "get_user_profile": ("/api/v1/users/<user_id>/profile", ["<user_id>"]),
    "list_users_in_account": ("/api/v1/accounts/<account_id>/users", ["<account_id>"]),
    "get_user_page_views": ("/api/v1/users/<user_id>/page_views", ["<user_id>"]),
}

user_update_endpoints = {
    "update_user": ("/api/v1/users/<user_id>", ["<user_id>"]),
}
