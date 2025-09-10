# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_entities import Crud_Entities_Manager
from app.backend.schema.crud.entities.Roles import Create_Role, Update_Role
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager


# router
roles_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])
# entities query
entities = Crud_Entities_Manager()
# trans
trans = Auth_Manager()


# GET -> Roles Base
@roles_route.get(Cns.CRUD_ROLE_BASE.value, response_class=HTMLResponse)
async def getting_app_roles_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # rows
    rows = await entities.getting_roles_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'rows': rows, 'user_session': user_session
            }
        }
    )


# GET -> Roles Register
@roles_route.get(Cns.CRUD_ROLE_CREATE.value, response_class=HTMLResponse)
async def getting_app_roles_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # departments
    departments = await entities.getting_departments_crud_rows(db=db)

    # schedules
    schedules = await entities.getting_schedule_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'departments': departments, 'schedules': schedules,
                'user_session': user_session
            }
        }
    )


# POST -> Roles Register
@roles_route.post(Cns.CRUD_ROLE_CREATE.value, response_class=HTMLResponse)
async def posting_app_roles_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Role, Depends(dependency=Create_Role.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await entities.registering_crud_role(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_roles_register_endpoint(
            request=request, user_login=user_login, db=db, fg='_orm_error')

    except OperationalError as op:
        db.rollback() # db rollback ops
        await entities.logger_sql_alchemy_ops_error(exception=op) # log errors
        return await getting_app_roles_register_endpoint(
            request=request, user_login=user_login, db=db, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'roles', 'fg': '_create'
            }
        }
    )


# GET -> Roles Update
@roles_route.get(Cns.CRUD_ROLE_UPDATE.value, response_class=HTMLResponse)
async def getting_app_roles_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # departments
    departments = await entities.getting_departments_crud_rows(db=db)

    # schedules
    schedules = await entities.getting_schedule_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'departments': departments, 'schedules': schedules,
                'user_session': user_session
            }
        }
    )


# POST -> Roles Update
@roles_route.post(Cns.CRUD_ROLE_POST.value, response_class=HTMLResponse)
async def posting_app_roles_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Role, Depends(dependency=Update_Role.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await entities.updating_crud_role(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await entities.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_roles_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError as op:
        db.rollback() # db rollback ops

        await entities.logger_sql_alchemy_ops_error(exception=op) # log errors
        return await getting_app_roles_update_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'roles', 'fg': '_update'
            }
        }
    )
