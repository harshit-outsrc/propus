term_create_endpoints = {
    "create_term": (
        "/api/v1/accounts/<account_id>/terms",
        ["<account_id>"],
    ),
}

term_update_endpoints = {
    "update_term": (
        "/api/v1/accounts/<account_id>/terms/<term_id>",
        ["<account_id>", "<term_id>"],
    ),
}

term_get_endpoints = {
    "get_term": (
        "/api/v1/accounts/<account_id>/terms/<term_id>",
        ["<account_id>", "<term_id>"],
    ),
    "list_terms": (
        "/api/v1/accounts/<account_id>/terms",
        ["<account_id>"],
    ),
}

term_delete_endpoints = {
    "delete_term": (
        "/api/v1/accounts/<account_id>/terms/<term_id>",
        ["<account_id>", "<term_id>"],
    ),
}
