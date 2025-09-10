# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.database.config import Session_Controller


# router
checkin_route = APIRouter(prefix=Cns.CHECKIN_BASE.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()


# GET -> Checkin Base
@checkin_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_checkin_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# GET -> Checkin Register
@checkin_route.get(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def getting_app_checkin_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/checkin.html', context={
            'request': request, 'params': {
                'default': 'default', 'user_session': user_session
            }
        }
    )
