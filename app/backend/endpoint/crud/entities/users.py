# import
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_entities import Crud_Entities_Manager
from app.backend.schema.crud.entities.Users import Create_User, Update_User, User_Status


# router
user_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])
# entities query
entities = Crud_Entities_Manager()


# GET -> Users Base
@user_route.get(Cns.CRUD_USER_BASE.value, response_class=HTMLResponse)
async def getting_app_user_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # rows
    rows = await entities.getting_users_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'rows': rows
            }
        }
    )


# GET -> Users Register
@user_route.get(Cns.CRUD_USER_CREATE.value, response_class=HTMLResponse)
async def getting_app_user_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # current user logged in

    # roles
    roles = await entities.getting_roles_crud_for_users(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'roles': roles
            }
        }
    )


# POST -> Users Register
@user_route.post(Cns.CRUD_USER_CREATE.value, response_class=HTMLResponse)
async def posting_app_user_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[Create_User, Depends(dependency=Create_User.formatting)],
) -> HTMLResponse:

    try:
        # commit to db (user)
        user = await entities.registering_crud_users(db=db, model=model.model_dump())

        # collect the user id
        user_id = user.id_record

        # commit to db (user_role)
        await entities.registering_crud_user_role_entity(db=db, user_id=user_id, model=model.model_dump())

        # enable one-day of vacation per registration date

        # add background tasks -> deliver email instructions

    except IntegrityError as ie:
        db.rollback() # db rollback ops
        # integrity error type
        catch = await entities.identify_error_integrity(catcher=ie)
        return await getting_app_user_register_endpoint(
            request=request, db=db, exc=catch, fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_register_endpoint(
            request=request, db=db, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_register_endpoint(
            request=request, db=db, fg='_ops_error')

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
        id: Annotated[Union[int, str], None],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # roles
    roles = await entities.getting_roles_crud_for_users(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'roles': roles
            }
        }
    )


# POST -> Users Update
@user_route.post(Cns.CRUD_USER_POST.value, response_class=HTMLResponse)
async def posting_app_user_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
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
            request=request, db=db, id=model.id, exc=catch, fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_update_endpoint(
            request=request, db=db, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_update_endpoint(
            request=request, db=db, id=model.id, fg='_ops_error')

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
        id: Annotated[Union[int, str], None],
        exc: Annotated[str, None] = None,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/status.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Users Status Update
@user_route.post(Cns.CRUD_USER_ENABLE_POST.value, response_class=HTMLResponse)
async def posting_app_user_enable_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[User_Status, Depends(dependency=User_Status.formatting)]
) -> HTMLResponse:

    try:
        # commit to db (user_role)
        await entities.updating_crud_user_status(db=db, model=model.model_dump())

    except HTTPException:
        db.rollback() # db rollback ops
        return await getting_app_user_enable_endpoint(
            request=request, db=db, id=model.id, exc='_termination_date', fg='_fail')

    except SQLAlchemyError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op)  # log errors
        return await getting_app_user_enable_endpoint(
            request=request, db=db, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_user_enable_endpoint(
            request=request, db=db, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'usuarios', 'fg': '_status'
            }
        }
    )
