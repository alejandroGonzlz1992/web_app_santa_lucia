# import
from fastapi import APIRouter, Request, Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from starlette.responses import Response

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_inability import Inability_Trans_Manager
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.schema.service.Inability import Create_Inability, Update_Inability
from app.backend.database.config import Session_Controller
from app.backend.tooling.bg_tasks import bg_tasks


# router
inability_route = APIRouter(prefix=Cns.URL_INABILITY.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# serv
serv = Inability_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Inability Base
@inability_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_inability_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # query inability records
    results = await serv.query_inability_records(db=db, id_login=user_login.user_id)
    # ->
    records = results["records"]
    logged_in = results["logged_in"]

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records,
                'logged_in': logged_in
            }
        }
    )


# GET -> Inability Register
@inability_route.get(Cns.URL_INABILITY_CREATE.value, response_class=HTMLResponse)
async def getting_app_inability_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Inability Register
@inability_route.post(Cns.URL_INABILITY_CREATE.value, response_class=HTMLResponse)
async def posting_app_inability_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Inability, Depends(dependency=Create_Inability.formatting)],
        background_tasks: BackgroundTasks,
        inability_file: UploadFile = File(...)
) -> HTMLResponse:

    try:
        # cast inability_file in bytes
        in_bytes = await inability_file.read()

        # register new inability | add inability_file object
        await serv.register_new_inability_record(
            db=db, schema=model.model_dump(), file=in_bytes, id_session=user_login.user_role_id)

        # collect, current user's approver
        emails_ = await serv.collecting_subject_and_approver_email(
            db=db, id_session=user_login.user_id, schema=model.model_dump())

        # inability record
        record = await serv.current_inability_record_for_create(db=db, schema=model.model_dump())

        # send email
        background_tasks.add_task(
            bg_tasks.bg_task_send_inability_request, [emails_["sub"], emails_["apr"]], record)

    except IntegrityError:
        db.rollback() # -> db rollback
        await exc_logs.logger_sql_alchemy_integrity_error(exc=IntegrityError) # -> error logs
        # redirect to endpoint
        return await getting_app_inability_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail', exc='_number')

    except SQLAlchemyError:
        db.rollback() # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError) # -> error logs
        # redirect to endpoint
        return await getting_app_inability_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_inability_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "incapacidades", "redirect": "ce", "fg": "_register"
            }
        },
        background=background_tasks
    )


# GET -> Inability Details
@inability_route.get(Cns.URL_INABILITY_DETAIL.value, response_class=HTMLResponse)
async def getting_app_inability_details_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # fetch current inability record
    results = await serv.querying_inability_record_details(db=db, id_login=user_login.user_id, id=id)
    # ->
    record = results["record"]
    logged_in = results["logged_in"]

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'record': record,
                'logged_in': logged_in
            }
        }
    )


# POST -> Inability File
@inability_route.get(Cns.URL_INABILITY_PDF.value, response_class=Response)
async def getting_app_inability_file_download(
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None]
) -> Response:

    # query file and name
    pdf_file = await serv.querying_inability_file_record(db=db, id=id)

    # return
    return Response(
        content=bytes(pdf_file['file']), media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={pdf_file['name']}"}
    )


# GET -> Inability Approval
@inability_route.get(Cns.URL_INABILITY_APPROVAL.value, response_class=HTMLResponse)
async def getting_app_inability_approvals_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/approval.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Inability Approval
@inability_route.post(Cns.URL_INABILITY_UPDATE_POST.value, response_class=HTMLResponse)
async def posting_app_inability_approvals_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Inability, Depends(dependency=Update_Inability.formatting)],
        background_tasks: BackgroundTasks,
) -> HTMLResponse:

    try:
        # update inability status
        await serv.updating_inability_status(db=db, schema=model.model_dump())

        # collect, current user's approver
        emails_ = await serv.collecting_subject_and_approver_email(
            db=db, id_session=user_login.user_id, schema=model.model_dump())

        # inability record
        record = await serv.current_inability_record_for_update(db=db, id=model.id)

        # send email
        background_tasks.add_task(
            bg_tasks.bg_task_send_inability_request, [emails_["sub"], emails_["apr"]], record)

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError) # -> error logs
        # redirect to endpoint
        return await getting_app_inability_approvals_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_inability_approvals_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "incapacidades", "redirect": "ce", "fg": "_update"
            }
        },
        background=background_tasks
    )
