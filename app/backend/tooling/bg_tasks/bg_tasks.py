# import
import logging
from typing import Literal, Union

# local import
from app.backend.tooling.emailing.settings.email_setting import Email_Manager
from app.backend.db_transactions.transactions.db_settlement import Settlement_Trans_Manager


# logger
logger = logging.getLogger(__name__)
# email
emailing = Email_Manager()
# serv
serv = Settlement_Trans_Manager()

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


# send evaluation results
async def bg_task_send_evaluation_results(
        rec: list[str], subject: object, audience: Literal["_employee", "_supervisor"]) -> None:

    try:
        # build email content
        msg = await emailing.send_evaluation_results(rec=rec, subject=subject, audience=audience)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=rec, msg=msg)

        # logs
        logger.info("[BG] Evaluation Results notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Evaluation Results notification email to recipients: {e}')


# send permission request extra hours
async def bg_task_send_permission_extra_hour_requests(recipients: Union[list[str], str], record: object) -> None:

    try:
        # build email content
        msg = await emailing.send_extra_hours_request_notification(record=record, rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Permission Extra Hours Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Permission Extra Hours notification email to recipients: {e}')


# send permission update request extra hours
async def bg_task_send_permission_extra_hour_update_request(recipients: Union[list[str], str], record: object) -> None:

    try:
        # build email content
        msg = await emailing.send_extra_hours_update_request_notification(record=record, rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Permission Extra Hours Update Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Update Permission Extra Hours notification email to recipients: {e}')


# send permission request vacations
async def bg_task_send_permission_vacations_requests(recipients: Union[list[str], str], record: object) -> None:

    try:
        # build email content
        msg = await emailing.send_vacations_request_notification(record=record, rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Permission Vacation Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Permission Vacation notification email to recipients: {e}')


# send permission update request vacations
async def bg_task_send_permission_vacations_update_request(recipients: Union[list[str], str], record: object) -> None:
    try:
        # build email content
        msg = await emailing.send_vacations_update_request_notification(record=record, rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Permission Vacations Update Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Update Permission Vacations notification email to recipients: {e}')


# send inability request
async def bg_task_send_inability_request(recipients: Union[list[str], str], record: object) -> None:
    try:
        # build email content
        msg = await emailing.send_inability_request_notification(record=record, rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Inability Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Inability Request notification email to recipients: {e}')


# send report attachment request
async def bg_task_send_report_attachment_request(
        recipients: Union[list[str], str], schema: object, xlsx_data: dict) -> None:
    try:
        # build email content
        msg = await emailing.send_report_request_as_attachment(rec=recipients, schema=schema, attach=xlsx_data)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Report Request notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Report Request notification email to recipients: {e}')


# send payroll report request
async def bg_task_send_payroll_report_request(recipients: Union[list[str], str]) -> None:

    try:
        # build email content
        msg = await emailing.send_payroll_report_notification(rec=recipients)

        # authenticate with gmail server and deliver
        await emailing.authenticate_with_server(rec=recipients, msg=msg)

        # logs
        logger.info("[BG] Report PDF notification email queued/sent to recipients")

    except Exception as e:
        logger.exception(f'[BG]: Failed sending Report PDF notification email to recipients: {e}')
