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
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # current user logged in

    # roles
    roles = await entities.getting_roles_crud_for_users(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD, 'roles': roles
            }
        }
    )


# GET -> Users Update
@user_route.get(Cns.CRUD_USER_UPDATE.value, response_class=HTMLResponse)
async def getting_app_user_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
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


# GET -> Users Status Update
@user_route.get(Cns.CRUD_USER_ENABLE.value, response_class=HTMLResponse)
async def getting_app_user_enable_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/user/status.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
