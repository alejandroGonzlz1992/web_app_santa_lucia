# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
permission_route = APIRouter(prefix=Cns.URL_PERMISSION.value, tags=[Cns.SERV.value])


# GET -> Permission Base
@permission_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_permission_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Permission Extra Hours
@permission_route.get(Cns.URL_PERMISSION_CREATE_HOUR.value, response_class=HTMLResponse)
async def getting_app_permission_extra_hour_create_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/extra_hours.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Permission Vacations
@permission_route.get(Cns.URL_PERMISSION_CREATE_VACATION.value, response_class=HTMLResponse)
async def getting_app_permission_vacation_create_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/vacations.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Permission Approvals
@permission_route.get(Cns.URL_PERMISSION_APPROVALS.value, response_class=HTMLResponse)
async def getting_app_permission_approvals_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/approvals.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Permission Approvals Update
@permission_route.get(Cns.URL_PERMISSION_APPROVALS_UPDATE.value, response_class=HTMLResponse)
async def getting_app_permission_approvals_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
