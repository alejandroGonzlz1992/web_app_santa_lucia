# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
schedule_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])


# GET -> Schedule Base
@schedule_route.get(Cns.CRUD_SCHEDULE_BASE.value, response_class=HTMLResponse)
async def getting_app_schedule_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/schedule/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Schedule Register
@schedule_route.get(Cns.CRUD_SCHEDULE_CREATE.value, response_class=HTMLResponse)
async def getting_app_schedule_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/schedule/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Schedule Update
@schedule_route.get(Cns.CRUD_SCHEDULE_UPDATE.value, response_class=HTMLResponse)
async def getting_app_schedule_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/schedule/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
