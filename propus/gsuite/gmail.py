from typing import AnyStr

from propus.logging_utility import Logging
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class Gmail:
    def __init__(self, client):
        self.client = client
        self.logger = Logging.get_logger("propus/gsuite/gmail.py")

    @staticmethod
    def build(
        auth_source: AnyStr, credentials_file: AnyStr = None, save_creds: bool = False
    ):
        """
        Build method for the Gmail class

        Args:
            auth_source (string): Type of authentication source. Options are file or local

            credentials_file (string): if auth_source is set to file then this is the full name of the file

        Returns:
            class(Gmail): Class Initialization of Gmail
        """
        from google_auth_oauthlib import GoogleAuth

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
            return Gmail(auth_from_file(credentials_file))
        return Gmail(local_auth(credentials_file, save_creds))

    def send_email(
        self,
        subject: str,
        body: str,
        sender: str,
        recipients: list[str],
        password: str,
        attachment_path: str,
    ):
        log_template = f"""\n
            From {sender} to {recipients}\n
            Subject: {subject}\n
            Attachments: {attachment_path}\n
            \nContent:\n {body}
        """
        try:
            message = MIMEMultipart()
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = ", ".join(recipients)
            text_part = MIMEText(body)
            message.attach(text_part)

            if attachment_path:
                with open(attachment_path, "rb") as attachment:
                    # Add the attachment to the message
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {attachment_path.split('/')[-1]}",
                        message.attach(part),
                    )

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, recipients, message.as_string())
                    self.logger.info("Succesfully sent Gmail message:" + log_template)
        except Exception as e:
            self.logger.error(
                f"Failed attempt to send Gmail message: {e}" + log_template
            )
