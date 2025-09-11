# import
import random, string, smtplib, ssl
from email import encoders
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from typing import Union, Literal

# local import
from app.backend.tooling.setting.constants import Constants
from app.backend.tooling.emailing.templates import email_templates
from app.backend.tooling.setting.env import env


# email manager
class Email_Manager:

    # init
    def __init__(self):
        self.settings = {"smtp": smtplib, "ssl": ssl}
        self.utils = {"random": random, "string": string}
        self.cns = Constants
        self.key = env.app_key
        self.template = email_templates
        # email builder
        self.builder = {"message": EmailMessage, "multipart": MIMEMultipart, "text": MIMEText,
                        "base": MIMEBase, "application": MIMEApplication, "encoders": encoders}

    # new password confirmation
    async def new_password_confirmation_email(self, rec: str) -> str:
        # header
        msg = self.builder["multipart"]("alternative")
        msg["From"] = self.cns.EMAIL_SANTALUCIA_SENDER.value
        msg["To"] = rec
        msg["Subject"] = self.cns.SUBJECT_EMAIL_NEW_PASSWORD_CONFIRM.value

        # html template
        content = self.builder["text"](
            self.template.html_new_password_confirmation_temp(login_url=self.cns.EMAIL_TO_LOGIN_SESSION.value), "html")

        # attach content
        msg.attach(content)

        # return msg as string
        return msg.as_string()

    # temp password confirmation
    async def temp_password_confirmation_email(self, rec: str, password: str) -> str:
        # header
        msg = self.builder["multipart"]("alternative")
        msg["From"] = self.cns.EMAIL_SANTALUCIA_SENDER.value
        msg["To"] = rec
        msg["Subject"] = self.cns.SUBJECT_EMAIL_TEMP_PASSWORD_CONFIRM.value

        # html template
        content = self.builder["text"](
            self.template.html_temp_password_sending(temp=password), "html")

        # attach content
        msg.attach(content)

        # return msg as string
        return msg.as_string()

    # authenticate with gmail server
    async def authenticate_with_server(self, rec: Union[str, list[str]], msg: Union[EmailMessage, str]) -> None:
        context = self.settings["ssl"].create_default_context()
        sender = self.cns.EMAIL_SANTALUCIA_SENDER.value

        # normalize recipients: either list[rec] or rec
        recipients = [rec] if isinstance(rec, str) else rec

        # new connection with gmail server on each call
        with self.settings["smtp"].SMTP_SSL(
                'smtp.gmail.com', 465, context=context, timeout=30) as gmail_server:
            # ehlo | authenticate
            gmail_server.ehlo()
            gmail_server.login(sender, self.key)

            if isinstance(msg, EmailMessage):
                if not msg.get("From"):
                    msg["From"] = sender

                if not msg.get("To"):
                    msg["To"] = ", ".join(recipients)

                # send email
                gmail_server.send_message(msg, from_addr=sender, to_addrs=recipients)

            else:
                # when passing a raw string as email content
                gmail_server.sendmail(sender, recipients, msg)

    # temp password confirmation with url_login
    async def temp_password_confirmation_with_url_login(self, rec: str, password: str) -> str:
        # header
        msg = self.builder["multipart"]("alternative")
        msg["From"] = self.cns.EMAIL_SANTALUCIA_SENDER.value
        msg["To"] = rec
        msg["Subject"] = self.cns.SUBJECT_EMAIL_TEMP_PASSWORD_FIRST_SIGNIN.value

        # html template
        content = self.builder["text"](
            self.template.html_temp_password_with_url_sending(
                temp=password, login_url=self.cns.EMAIL_TO_LOGIN_SESSION.value), "html")

        # attach content
        msg.attach(content)

        # return msg as string
        return msg.as_string()

    # evaluation enable status
    async def send_evaluation_enable_notification(
            self, rec: dict[list], audience: Literal["employee", "supervisor"]) -> str:
        # header
        msg = self.builder["multipart"]("alternative")
        msg["From"] = self.cns.EMAIL_SANTALUCIA_SENDER.value

        if audience == "employee":
            recipients = rec["employees"]
            msg["Subject"] = self.cns.SUBJECT_EVALUATION_ENABLE_SUPERVISOR.value

            # html template
            content = self.builder["text"](
                self.template.html_evaluation_activate_with_url_sending(
                    type_of="supervisor", login_url=self.cns.EMAIL_TO_LOGIN_SESSION.value), "html")

            # attach content
            msg.attach(content)
            # to
            msg["To"] = ", ".join(recipients)

        elif audience == "supervisor":
            recipients = rec["supervisors"]
            msg["Subject"] = self.cns.SUBJECT_EVALUATION_ENABLE_EMPLOYEE.value

            # html template
            content = self.builder["text"](
                self.template.html_evaluation_activate_with_url_sending(
                    type_of="empleado", login_url=self.cns.EMAIL_TO_LOGIN_SESSION.value), "html")

            # attach content
            msg.attach(content)
            # to
            msg["To"] = ", ".join(recipients)

        # return
        return msg.as_string()
