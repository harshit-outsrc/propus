def _fetch_and_format_data(self, url):
    resp = self.requests_service.get(url=url, headers=self.fetch_get_headers())

    return self.return_response(resp)
