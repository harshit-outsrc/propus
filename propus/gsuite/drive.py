from typing import AnyStr, Dict

from propus.logging_utility import Logging


class Drive:
    def __init__(self, client):
        self.client = client
        self.logger = Logging.get_logger("propus/gsuite/drive.py")

    @staticmethod
    def build(auth_source: AnyStr, credentials_file: AnyStr = None, save_creds: bool = False):
        """
        Build method for the Drive class

        Args:
            auth_source (string): Type of authentication source. Options are file or local

            credentials_file (string): if auth_source is set to file then this is the full name of the file

        Returns:
            class(Drive): Class Initialization of Drive
        """
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        gauth = GoogleAuth()

        def auth_from_file(f_name):
            gauth.LoadCredentialsFile(f_name)
            if gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            return gauth

        def local_auth(f_name, save_creds):
            gauth.LocalWebserverAuth()
            if save_creds:
                gauth.SaveCredentialsFile(f_name)
            return gauth

        if auth_source == "file":
            return Drive(GoogleDrive(auth_from_file(credentials_file)))
        return Drive(GoogleDrive(local_auth(credentials_file, save_creds)))

    def upload_file(self, file_name: AnyStr, metadata: Dict):
        """
        This method will upload a file to google drive

        Args:
            file_name (string): filename (should include full path) to be uploaded to google drive
            metadata (dict): Dictionary of all key/value metadata keys.
                - Example: {'title': 'hello.pdf', "parents": [{"id": "1iy6jggaVy71epoDXoYIvMZM9iO7qKgue"}]}
        """
        drive = self.client.CreateFile(metadata)
        drive.SetContentFile(file_name)
        drive.Upload()
        self.logger.info(f"uploaded {file_name} successfully")

    def delete_file(self, file_id):
        drive_file = self.client.CreateFile({"id": file_id})
        drive_file.Delete()  # Permanently delete the file.
