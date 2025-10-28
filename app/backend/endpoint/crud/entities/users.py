# import
from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_entities import Crud_Entities_Manager
from app.backend.schema.crud.entities.Users import Create_User, Update_User, User_Status
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.tooling.setting.security import User_Active_Status_Exception, User_Inactive_Status_Exception
from app.backend.tooling.bg_tasks import bg_tasks


# router
user_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])
# entities query
entities = Crud_Entities_Manager()
# trans
trans = Auth_Manager()


# GET -> Users Base
@user_route.get(Cns.CRUD_USER_BASE.value, response_class=HTMLResponse)
async def getting_app_user_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # rows
    rows = await entities.getting_users_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'rows': rows, 'user_session': user_session
            }
        }
    )


# GET -> Users Register
@user_route.get(Cns.CRUD_USER_CREATE.value, response_class=HTMLResponse)
async def getting_app_user_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)
    # roles
    roles = await entities.getting_roles_crud_for_users(db=db)
    # management
    management = await entities.getting_users_jefaturas_crud(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'roles': roles, 'user_session': user_session,
                'management': management
            }
        }
    )


# POST -> Users Register
@user_route.post(Cns.CRUD_USER_CREATE.value, response_class=HTMLResponse)
async def posting_app_user_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_User, Depends(dependency=Create_User.formatting)],
        background_tasks: BackgroundTasks,
) -> HTMLResponse:

    try:
        # commit to db (user)
        user = await entities.registering_crud_users(db=db, model=model.model_dump())

        # collect the user id
        user_id = user["user"].id_record

        # commit to db (user_role)
        await entities.registering_crud_user_role_entity(db=db, user_id=user_id, model=model.model_dump())

        # enable one-day of vacation per registration date
        await entities.fetching_vacation_days(db=db, user_id=user_id)

        # add background tasks -> deliver email instructions
        background_tasks.add_task(
            bg_tasks.bg_task_temp_password_url_login_confirmation, user["user"].email, user["temp"])

    except IntegrityError as ie:
        db.rollback() # db rollback ops
        # integrity error type
        catch = await entities.identify_error_integrity(catcher=ie)
        return await getting_app_user_register_endpoint(
            request=request, db=db, user_login=user_login, exc=catch, fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'usuarios', 'fg': '_create'
            }
        }
    )


# GET -> Users Update
@user_route.get(Cns.CRUD_USER_UPDATE.value, response_class=HTMLResponse)
async def getting_app_user_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # roles
    roles = await entities.getting_roles_crud_for_users(db=db)

    # management
    management = await entities.getting_users_jefaturas_crud(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'roles': roles, 'user_session': user_session,
                "management": management
            }
        }
    )


# POST -> Users Update
@user_route.post(Cns.CRUD_USER_POST.value, response_class=HTMLResponse)
async def posting_app_user_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_User, Depends(dependency=Update_User.formatting)]
) -> HTMLResponse:

    try:
        # commit to db (user)
        await entities.updating_crud_users(db=db, model=model.model_dump())

        # commit to db (user_role)
        await entities.updating_crud_user_role_entity(db=db, model=model.model_dump())

    except IntegrityError as ie:
        db.rollback()  # db rollback ops
        await entities.logger_sql_integrity_error(exception=ie)
        # integrity error type
        catch = await entities.identify_error_integrity(catcher=ie)
        return await getting_app_user_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, exc=catch, fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'usuarios', 'fg': '_update'
            }
        }
    )


# GET -> Users Status Update
@user_route.get(Cns.CRUD_USER_ENABLE.value, response_class=HTMLResponse)
async def getting_app_user_enable_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/status.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Users Status Update
@user_route.post(Cns.CRUD_USER_ENABLE_POST.value, response_class=HTMLResponse)
async def posting_app_user_enable_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[User_Status, Depends(dependency=User_Status.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # commit to db (user_role)
        record = await entities.querying_user_status_entity(db=db, model=model.model_dump())

        if record._status and model.user_status:
            raise User_Active_Status_Exception('User is already as active status')

        elif not record._status and not model.user_status:
            raise User_Inactive_Status_Exception('User is already as inactive status')

        # update record on db
        to_deliver = await entities.updating_user_status(db=db, record=record, model=model.model_dump())

        if to_deliver["flag"]:
            # background task
            background_tasks.add_task(
                bg_tasks.bg_task_temp_password_url_login_confirmation, record._email, to_deliver["temp"])

    except HTTPException:
        db.rollback() # db rollback ops
        return await getting_app_user_enable_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, exc='_termination_date', fg='_fail')

    except User_Inactive_Status_Exception:
        db.rollback() # db rollback ops
        return await getting_app_user_enable_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, exc='_as_inactive', fg='_fail')

    except User_Active_Status_Exception:
        db.rollback() # db rollback ops
        return await getting_app_user_enable_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, exc='_as_active', fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_enable_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_enable_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return flag
    flag = '_active' if bool(model.user_status) else '_inactive'

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'usuarios', 'fg': flag
            }
        }
    )
