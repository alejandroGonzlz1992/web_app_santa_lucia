# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
profile_route = APIRouter(prefix=Cns.PROFILE_BASE.value, tags=[Cns.SERV.value])


# GET -> Profile Base
@profile_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_profile_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Profile Address
@profile_route.get(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def getting_app_profile_address_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/address.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Profile Password
@profile_route.get(Cns.PROFILE_PASSWORD.value, response_class=HTMLResponse)
async def getting_app_profile_password_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/password.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Profile Vacations
@profile_route.get(Cns.PROFILE_VACATIONS.value, response_class=HTMLResponse)
async def getting_app_profile_vacation_endpoint(
        request: Request
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/vacations.html', context={
            'request': request, 'params': {
                'default': 'default'
            }
        }
    )


# GET -> Profile Extra Hours
@profile_route.get(Cns.PROFILE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def getting_app_profile_extra_hours_endpoint(
        request: Request
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/extra_hours.html', context={
            'request': request, 'params': {
                'default': 'default'
            }
        }
    )
