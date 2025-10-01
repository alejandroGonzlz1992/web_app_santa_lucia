# import
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from watchfiles import awatch

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_reports import Reports_Trans_Manager
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.database.config import Session_Controller
from app.backend.schema.service.Reports import Create_Report
from app.backend.tooling.bg_tasks import bg_tasks


# router
reports_route = APIRouter(prefix=Cns.TRANS_REPORT.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# serv
serv = Reports_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Reports Base
@reports_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_reports_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/report/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Reports Base
@reports_route.post(Cns.BASE.value, response_class=HTMLResponse)
async def posting_app_reports_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Report, Depends(Create_Report.formatting)],
        background_tasks: BackgroundTasks,
) -> HTMLResponse:

    try:
        # records
        data_frame = await serv.reports_query_manager(db=db, schema=model.model_dump())

        # recipient
        to_email = await serv.getting_current_recipient(db=db, id_session=user_login.user_role_id)

        # excel file
        if model.report_deliver == "download":
            # return
            return await serv.downloadable_file_browser(
                df=data_frame, name=model.report_name_field)

        elif model.report_deliver == "email":
            # attachment
            file_attach = await serv.attachment_for_email_delivery(df=data_frame, name=model.report_name_field)
            # background task
            background_tasks.add_task(
                bg_tasks.bg_task_send_report_attachment_request, to_email._email, model.model_dump(), file_attach)

    except SQLAlchemyError:
        db.rollback() # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError) # -> error logs
        # redirect to endpoint
        return await getting_app_reports_base_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_reports_base_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "reportes", "redirect": "ce", "fg": "_generate"
            }
        },
        background=background_tasks
    )