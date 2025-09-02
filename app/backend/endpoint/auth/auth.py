# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
auth_route = APIRouter(prefix=Cns.AUTH_SESSION.value, tags=[Cns.AUTH.value])


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
