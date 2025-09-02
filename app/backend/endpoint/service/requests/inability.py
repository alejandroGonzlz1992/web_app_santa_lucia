# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
inability_route = APIRouter(prefix=Cns.URL_INABILITY.value, tags=[Cns.TRANS.value])


# GET -> Inability Base
@inability_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_inability_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Inability Register
@inability_route.get(Cns.URL_INABILITY_CREATE.value, response_class=HTMLResponse)
async def getting_app_inability_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Inability Details
@inability_route.get(Cns.URL_INABILITY_DETAIL.value, response_class=HTMLResponse)
async def getting_app_inability_details_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Inability Approval
@inability_route.get(Cns.URL_INABILITY_APPROVAL.value, response_class=HTMLResponse)
async def getting_app_inability_approvals_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/inability/approval.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )

