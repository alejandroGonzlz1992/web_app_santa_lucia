# import
from fastapi import APIRouter, Request, Depends, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.services.db_permission import Permission_Trans_Manager
from app.backend.schema.service.Permission import Create_Extra_Hours, Create_Vacations, Update_Request
from app.backend.tooling.bg_tasks import bg_tasks
from app.backend.tooling.setting.security import Vacation_Statuses_Exception


# router
permission_route = APIRouter(prefix=Cns.URL_PERMISSION.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()
# serv
serv = Permission_Trans_Manager()


# GET -> Permission Base
@permission_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_permission_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)]
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/index.html', context={
            'request': request, 'params': {
                'default': 'default', 'user_session': user_session
            }
        }
    )


# GET -> Extra Hours Menu
@permission_route.get(Cns.URL_PERMISSION_EXTRA_HOURS_MAIN.value, response_class=HTMLResponse)
async def getting_app_permission_extra_hours_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # extra hour requests record
    results = await serv.querying_extra_hours_details(db=db, id_login=user_login.user_id)
    # -> from results
    records = results["records"]
    logged_in = results["logged_in"]

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/extra_hours/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records,
                'logged_in': logged_in
            }
        }
    )


# GET -> Extra Hours Register
@permission_route.get(Cns.URL_PERMISSION_CREATE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def getting_app_permission_extra_hours_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/extra_hours/register.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Extra Hours Register
@permission_route.post(Cns.URL_PERMISSION_CREATE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def posting_app_permission_extra_hours_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Extra_Hours, Depends(Create_Extra_Hours.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # insert record on db
        current = await serv.registering_extra_hour_record(db=db, model=model.model_dump(), id_session=user_login.user_role_id)
        # collecting emails
        emails_ = await serv.collecting_subject_approver_emails(db=db, id_login=user_login.user_role_id)
        # records
        records = await serv.current_extra_hour_request_record(db=db, id_request=current.id_record)

        # bg tasks
        background_tasks.add_task(
            bg_tasks.bg_task_send_permission_extra_hour_requests, [emails_["user_email"], emails_["approver_email"]],
            records
        )

    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_permission_extra_hours_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_permission_extra_hours_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "solicitudes", "redirect": "ce/horas_extra", "fg": "_register"
            }
        },
        background=background_tasks
    )


# GET -> Extra Hours Update
@permission_route.get(Cns.URL_PERMISSION_UPDATE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def getting_app_permission_extra_hours_update_endpoint(
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
        'service/permission/extra_hours/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Extra Hours Update
@permission_route.post(Cns.URL_PERMISSION_UPDATE_EXTRA_HOURS_POST.value, response_class=HTMLResponse)
async def posting_app_permission_extra_hours_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Request, Depends(Update_Request.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # update record on db
        current = await serv.updating_extra_hour_record(db=db, model=model.model_dump())

        # collecting emails
        emails_ = await serv.collecting_subject_approver_emails(db=db, id_login=current.id_subject)

        # records
        records = await serv.current_extra_hour_request_record(db=db, id_request=model.id)

        if current.status == "Aprobado":
            # add extra hours user
            await serv.registering_user_extra_hours(db=db, model=model.model_dump())

        # bg tasks
        background_tasks.add_task(
            bg_tasks.bg_task_send_permission_extra_hour_update_request,
            [emails_["user_email"], emails_["approver_email"]],
            records)

    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_permission_extra_hours_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_permission_extra_hours_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "solicitudes", "redirect": "ce/horas_extra", "fg": "_update"
            }
        },
        background=background_tasks
    )


# GET -> Vacations Menu
@permission_route.get(Cns.URL_PERMISSION_VACATION_MAIN.value, response_class=HTMLResponse)
async def getting_app_permission_vacations_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # vacations requests record
    results = await serv.querying_vacations_details(db=db, id_login=user_login.user_id)
    # -> from results
    records = results["records"]
    logged_in = results["logged_in"]

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/vacations/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records,
                'logged_in': logged_in
            }
        }
    )


# GET -> Vacations Register
@permission_route.get(Cns.URL_PERMISSION_CREATE_VACATION.value, response_class=HTMLResponse)
async def getting_app_permission_vacations_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/vacations/register.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Vacations Register
@permission_route.post(Cns.URL_PERMISSION_CREATE_VACATION.value, response_class=HTMLResponse)
async def posting_app_permission_vacations_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Vacations, Depends(Create_Vacations.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # validate available days
        await serv.current_vacation_available_record(
            db=db, id_session=user_login.user_role_id, schema=model.model_dump())

        # validate available days vs in_progress
        await serv.validating_vacation_status(
            db=db, id_session=user_login.user_role_id, schema=model.model_dump())

        # insert record on db
        current = await serv.registering_vacations_record(db=db, model=model.model_dump(), id_session=user_login.user_role_id)
        # collecting emails
        emails_ = await serv.collecting_subject_approver_emails(db=db, id_login=user_login.user_role_id)
        # records
        records = await serv.current_vacation_request_record(db=db, id_request=current.id_record)

        # bg tasks
        background_tasks.add_task(
            bg_tasks.bg_task_send_permission_vacations_requests, [emails_["user_email"], emails_["approver_email"]],
            records)

    except Vacation_Statuses_Exception:
        return await getting_app_permission_vacations_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_no_approved_yet')

    except HTTPException:
        db.rollback()  # db rollback
        return await getting_app_permission_vacations_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail_available')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_permission_vacations_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_permission_vacations_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "solicitudes", "redirect": "ce/vacaciones", "fg": "_register"
            }
        },
        background=background_tasks
    )


# GET -> Vacations Update
@permission_route.get(Cns.URL_PERMISSION_UPDATE_VACATION.value, response_class=HTMLResponse)
async def getting_app_permission_vacations_update_endpoint(
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
        'service/permission/vacations/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Vacations Update
@permission_route.post(Cns.URL_PERMISSION_UPDATE_VACATION_POST.value, response_class=HTMLResponse)
async def posting_app_permission_vacations_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Request, Depends(Update_Request.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # update record on db
        current = await serv.updating_vacations_record(db=db, model=model.model_dump())

        # collecting emails
        emails_ = await serv.collecting_subject_approver_emails(db=db, id_login=current.id_subject)

        # records
        records = await serv.current_vacation_request_record(db=db, id_request=model.id)

        if current.status == "Aprobado":
            # update used days
            await serv.updating_used_days_vacations(db=db, record=records)

        # bg tasks
        background_tasks.add_task(
            bg_tasks.bg_task_send_permission_vacations_update_request, [emails_["user_email"], emails_["approver_email"]],
            records)

    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_permission_vacations_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_permission_vacations_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "solicitudes", "redirect": "ce/vacaciones", "fg": "_update"
            }
        },
        background=background_tasks
    )
