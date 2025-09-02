# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
checkin_route = APIRouter(prefix=Cns.CHECKIN_BASE.value, tags=[Cns.SERV.value])


# GET -> Checkin Base
@checkin_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_checkin_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Checkin Register
@checkin_route.get(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def getting_app_checkin_register_endpoint(
        request: Request
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/checkin.html', context={
            'request': request, 'params': {
                'default': 'default'
            }
        }
    )
