# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_records import Db_Crud_Request
from app.backend.schema.crud.entities.Roles import Create_Role, Update_Role


# router
roles_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])



# GET -> Roles Base
@roles_route.get(Cns.CRUD_ROLE_BASE.value, response_class=HTMLResponse)
async def getting_app_roles_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Roles Register
@roles_route.get(Cns.CRUD_ROLE_CREATE.value, response_class=HTMLResponse)
async def getting_app_roles_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Roles Update
@roles_route.get(Cns.CRUD_ROLE_UPDATE.value, response_class=HTMLResponse)
async def getting_app_roles_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/entities/role/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
