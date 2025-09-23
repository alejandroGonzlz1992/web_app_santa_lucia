# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_profile import Profile_Trans_Manager
from app.backend.database.config import Session_Controller


# router
profile_route = APIRouter(prefix=Cns.PROFILE_BASE.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()
# serv
serv = Profile_Trans_Manager()


# GET -> Profile Base
@profile_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_profile_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# GET -> Profile Address
@profile_route.get(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def getting_app_profile_address_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # fetch province, canton, and district records
    address = await serv.querying_province_canton_and_districts(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/address.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, "address": address
            }
        }
    )


# GET -> Profile Password
@profile_route.get(Cns.PROFILE_PASSWORD.value, response_class=HTMLResponse)
async def getting_app_profile_password_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/password.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# GET -> Profile Vacations
@profile_route.get(Cns.PROFILE_VACATIONS.value, response_class=HTMLResponse)
async def getting_app_profile_vacation_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/vacations.html', context={
            'request': request, 'params': {
                'default': 'default', 'user_session': user_session
            }
        }
    )


# GET -> Profile Extra Hours
@profile_route.get(Cns.PROFILE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def getting_app_profile_extra_hours_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/extra_hours.html', context={
            'request': request, 'params': {
                'default': 'default', 'user_session': user_session
            }
        }
    )
