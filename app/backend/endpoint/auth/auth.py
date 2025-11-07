# import
from logging import getLogger
from fastapi import APIRouter, Request, Depends, HTTPException, status, BackgroundTasks, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.env import env
from app.backend.tooling.setting.security import (verifying_hash_password, loading_payload_data,
                                                  generating_access_token, Privilege_Access_As_User_Exception,
                                                  Privilege_Access_As_Admin_Exception, User_Inactive_Status_Exception,
                                                  Temporary_Invalid_Password_Exception)
from app.backend.schema.auth.Login import User_Login, Restore_Password
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.tooling.bg_tasks import bg_tasks

# router
auth_route = APIRouter(prefix=Cns.AUTH_SESSION.value, tags=[Cns.AUTH.value])
# transactions
trans = Auth_Manager()
# logger error
logger = getLogger(__name__)


# GET -> User Login
@auth_route.get(Cns.AUTH_USER_LOGIN.value, response_class=HTMLResponse)
async def getting_app_user_login_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'auth/user.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Use Login
@auth_route.post(Cns.AUTH_USER_LOGIN.value, response_class=RedirectResponse)
async def posting_app_user_login_endpoint(
        request: Request,
        db: Annotated[Session, Depends(Session_Controller)],
        model: Annotated[User_Login, Depends(User_Login.formatting)],
) -> RedirectResponse:

    try:
        # validate credentials and password
        entity = await trans.getting_credentials_login(db=db, model=model.model_dump())

        # load payload data
        payload = loading_payload_data(record=entity)

        # validate role type
        if payload["role_type"] == Cns.LABEL_ADMIN.value:
            raise Privilege_Access_As_Admin_Exception("Acceso con privilegios incorrectos.")

        # validate credentials
        if not verifying_hash_password(plain=model.password_login_field, hash_password=entity.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

        # validate if user is active
        if not entity.user_roles[0].status:
            raise User_Inactive_Status_Exception("Usuario en estado inactivo.")

    except User_Inactive_Status_Exception:
        return await getting_app_user_login_endpoint(request=request, fg='_inactive')

    except Privilege_Access_As_Admin_Exception:
        return await getting_app_admin_login_endpoint(request=request, fg='_redirect')

    except HTTPException:
        db.rollback() # rollback transactions
        return await getting_app_user_login_endpoint(request=request, fg='_fail', exc='_raise')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await trans.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_login_endpoint(request=request, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await trans.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_login_endpoint(request=request, fg='_ops_error')

    # redirect based on is_temp field
    if await trans.validating_is_temp_password(db=db, payload=payload):
        # response
        resp = RedirectResponse(url=Cns.URL_REDIRECT_TO_PASSWORD_RESTORE.value, status_code=status.HTTP_303_SEE_OTHER)

        # return
        return resp
    else:
        # generate jwt token
        token = generating_access_token(data=payload, expires_delta=env.tkn_expire)
        # response
        resp = RedirectResponse(url=Cns.ROOT.value, status_code=status.HTTP_303_SEE_OTHER)
        # set up token for frontend
        resp.set_cookie(key='access_token', value=token, httponly=True, secure=False, path='/')

        # return
        return resp


# GET -> Admin Login
@auth_route.get(Cns.AUTH_ADMIN_LOGIN.value, response_class=HTMLResponse)
async def getting_app_admin_login_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'auth/admin.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Admin Login
@auth_route.post(Cns.AUTH_ADMIN_LOGIN.value, response_class=RedirectResponse)
async def posting_app_admin_login_endpoint(
        request: Request,
        db: Annotated[Session, Depends(Session_Controller)],
        model: Annotated[User_Login, Depends(User_Login.formatting)],
) -> RedirectResponse:

    try:
        # validate credentials and password
        entity = await trans.getting_credentials_login(db=db, model=model.model_dump())

        # load payload data
        payload = loading_payload_data(record=entity)

        # validate role type
        if payload["role_type"] != Cns.LABEL_ADMIN.value:
            raise Privilege_Access_As_User_Exception("Acceso con privilegios incorrectos.")

        # validate credentials
        if not verifying_hash_password(plain=model.password_login_field, hash_password=entity.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

        # validate if user is active
        if not entity.user_roles[0].status:
            raise User_Inactive_Status_Exception("Usuario en estado inactivo.")

    except User_Inactive_Status_Exception:
        return await getting_app_admin_login_endpoint(request=request, fg='_inactive')

    except Privilege_Access_As_User_Exception:
        return await getting_app_user_login_endpoint(request=request, fg='_redirect')

    except HTTPException:
        db.rollback() # rollback transactions
        return await getting_app_admin_login_endpoint(request=request, fg='_fail', exc='_raise')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await trans.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_admin_login_endpoint(request=request, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await trans.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_admin_login_endpoint(request=request, fg='_ops_error')

    # redirect based on is_temp field
    if await trans.validating_is_temp_password(db=db, payload=payload):
        # response
        resp = RedirectResponse(url=Cns.URL_REDIRECT_TO_PASSWORD_RESTORE.value, status_code=status.HTTP_303_SEE_OTHER)

        # return
        return resp
    else:
        # generate jwt token
        token = generating_access_token(data=payload, expires_delta=env.tkn_expire)
        # response
        resp = RedirectResponse(url=Cns.ROOT.value, status_code=status.HTTP_303_SEE_OTHER)
        # set up token for frontend
        resp.set_cookie(key='access_token', value=token, httponly=True, samesite='lax', secure=False, path='/')

        # return
        return resp


# GET -> Password Recover
@auth_route.get(Cns.AUTH_PASSWORD_RECOVER.value, response_class=HTMLResponse)
async def getting_app_password_recover_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'auth/recover.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Password Recover
@auth_route.post(Cns.AUTH_PASSWORD_RECOVER.value, response_class=HTMLResponse)
async def posting_app_password_recover_endpoint(
        request: Request,
        db: Annotated[Session, Depends(Session_Controller)],
        email_recover_field: Annotated[str, Form(...)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        # query entity
        record = await trans.user_current_password_recover(db=db, input_email=email_recover_field)

        # update db model records
        await trans.updating_temp_password_field(db=db, entity=record)

        # background task
        background_tasks.add_task(
            bg_tasks.bg_task_temp_password_confirmation, record['email'], record['temp_password'])

    except HTTPException as http:
        logger.error(f' [http_exception] -> A http exception has been raised. \n Details: {http.detail}')
        return await getting_app_password_recover_endpoint(request=request, fg='_fail')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'auth/user.html', context={
            'request': request, 'params': {
                'fg': '_reset', 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Password Restore
@auth_route.get(Cns.AUTH_PASSWORD_RESTORE.value, response_class=HTMLResponse)
async def getting_app_password_restore_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'auth/restore.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Password Restore
@auth_route.post(Cns.AUTH_PASSWORD_RESTORE.value, response_class=RedirectResponse)
async def posting_app_password_restore_endpoint(
        request: Request,
        db: Annotated[Session, Depends(Session_Controller)],
        model: Annotated[Restore_Password, Depends(Restore_Password.formatting)],
        background_tasks: BackgroundTasks,
) -> RedirectResponse:

    try:
        # query current entity
        entity = await trans.user_restore_entity(db=db, model=model.model_dump())

        # validate password
        if not verifying_hash_password(plain=model.temp_password_field, hash_password=entity._temp):
            raise Temporary_Invalid_Password_Exception('Invalid Temporal Password')

        # update record in db
        await trans.user_updating_new_password(db=db, id=entity._id, model=model.model_dump())

        # send confirmation email
        background_tasks.add_task(bg_tasks.bg_task_new_password_confirmation, entity._email.strip().lower())

    except HTTPException as http:
        logger.error(f' [http_exception] -> A http exception has been raised. \n Details: {http.detail}')
        return await getting_app_password_restore_endpoint(request=request, fg='_fail', exc='_identification')

    except Temporary_Invalid_Password_Exception:
        return await getting_app_password_restore_endpoint(request=request, fg='_fail', exc='_temp_password')

    # response
    resp = RedirectResponse(url=f'{Cns.OAUTH2_SCHEMA_URL.value}?fg=_restore', status_code=status.HTTP_303_SEE_OTHER)
    # return
    return resp
