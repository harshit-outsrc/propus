import unittest
from unittest.mock import MagicMock, Mock

from propus.gsuite import Drive


class TestGoogleDrive(unittest.TestCase):
    def setUp(self) -> None:
        google_client = MagicMock()
        google_client.CreateFile = Mock(side_effect=self.create_file)
        self.drive = Drive(google_client)
        self.functions_called = []
        self.file_name = "a.b.pdf"
        self.meta_data = {"file": self.file_name, "date": "today", "a": "b"}
        self.delete_file_meta = {"id": self.file_name}

    def test_upload_file(self):
        self.drive.upload_file(self.file_name, self.meta_data)
        self.assertEqual(self.functions_called, ["create_file", "set_content_file", "upload"])

    def create_file(self, meta_data):
        self.assertTrue(meta_data in [self.meta_data, self.delete_file_meta])
        self.functions_called.append("create_file")
        drive = MagicMock
        drive.SetContentFile = Mock(side_effect=self.set_content_file)
        drive.Upload = Mock(side_effect=self.upload)
        drive.Delete = Mock(side_effect=self.delete)
        return drive

    def set_content_file(self, file_name):
        self.assertEqual(file_name, self.file_name)
        self.functions_called.append("set_content_file")

    def upload(self):
        self.functions_called.append("upload")

    def test_delete_file(self):
        self.drive.delete_file(self.file_name)
        self.assertEqual(self.functions_called, ["create_file", "delete"])

    def delete(self):
        self.functions_called.append("delete")


if __name__ == "__main__":
    unittest.main()
