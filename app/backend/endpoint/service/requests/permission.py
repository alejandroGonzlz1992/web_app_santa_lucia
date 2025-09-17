# import
from fastapi import APIRouter, Request, Depends, BackgroundTasks
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
from app.backend.schema.service.Permission import Create_Extra_Hours


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
    records = await serv.querying_extra_hours_details(db=db, id_login=user_login.user_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/extra_hours/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records
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


    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        return await posting_app_permission_extra_hours_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await posting_app_permission_extra_hours_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "solicitudes", "redirect": "ce/horas_extra", "fg": "_register"
            }
        },
        # background=background_tasks
    )
