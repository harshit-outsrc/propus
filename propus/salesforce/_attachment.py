import json


def fetch_attachment(self, attachment_id):
    url = self._get_endpoint("fetch_attachment", {"<attachment_id>": attachment_id})
    return self.make_request(url)


def create_attachment(self, parent_id, base64_encoded_file, extension, file_name):
    url = self._get_endpoint("create_attachment")
    return self.make_request(
        url=url,
        req_type="post",
        data=json.dumps(
            {"ParentId": parent_id, "Name": file_name, "ContentType": extension, "Body": base64_encoded_file}
        ),
    )
