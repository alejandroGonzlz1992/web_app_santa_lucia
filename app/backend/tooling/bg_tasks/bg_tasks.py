# import
import logging
from typing import Literal, Union

# local import
from app.backend.tooling.emailing.settings.email_setting import Email_Manager


# logger
logger = logging.getLogger(__name__)
# email
emailing = Email_Manager()


# send new password confirmation task
async def bg_task_new_password_confirmation(rec: str) -> None:
    try:
        # build email content
        msg = await emailing.new_password_confirmation_email(rec=rec)

        # authenticate with gmail server
        await emailing.authenticate_with_server(rec=rec, msg=msg)

        # log
        logger.info(f" [BG_task] -> New password confirmation email sent to {rec} successfully.")

    except Exception as e:
        # log
        logger.info(f" [BG_task] -> Fail to send New password confirmation email to {rec}. \n Details: {e}")


# send temp password confirmation task
async def bg_task_temp_password_confirmation(rec: str, temp: str) -> None:
    try:
        # build email content
        msg = await emailing.temp_password_confirmation_email(rec=rec, password=temp)

        # authenticate with gmail server
        await emailing.authenticate_with_server(rec=rec, msg=msg)

        # log
        logger.info(f" [BG_task] -> Temporarily password confirmation email sent to {rec} successfully.")

    except Exception as e:
        # log
        logger.info(f" [BG_task] -> Fail to send Temporarily password confirmation email to {rec}. \n Details: {e}")


# send temp password confirmation with url task
async def bg_task_temp_password_url_login_confirmation(rec: str, password: str) -> None:
    try:
        # build email content
        msg = await emailing.temp_password_confirmation_with_url_login(rec=rec, password=password)

        # authenticate with gmail server
        await emailing.authenticate_with_server(rec=rec, msg=msg)

        # log
        logger.info(f" [BG_task] -> Temporarily password confirmation email sent to {rec} successfully.")

    except Exception as e:
        # log
        logger.info(f" [BG_task] -> Fail to send Temporarily password confirmation email to {rec}. \n Details: {e}")


# send evaluation activation to recipients
async def bg_task_send_evaluation_status_recipients(rec: dict[list], audience: Literal["employee", "supervisor"]) -> None:
    try:
        # build email content
        msg = await emailing.send_evaluation_enable_notification(rec=rec, audience=audience)

        # authenticate with gmail server and deliver
        if audience == "employee":
            await emailing.authenticate_with_server(rec=rec["employees"], msg=msg)

        else:
            await emailing.authenticate_with_server(rec=rec["supervisors"], msg=msg)

        # log
        logger.info(f" [BG_task] -> Evaluation notification email sent to recipients successfully.")

    except Exception as e:
        # log
        logger.info(f" [BG_task] -> Fail to send Temporarily password confirmation email to recipients. \n Details: {e}")

