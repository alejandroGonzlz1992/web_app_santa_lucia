# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.services.db_permission import Permission_Trans_Manager


# router
permission_route = APIRouter(prefix=Cns.URL_PERMISSION.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()
# serv
serv = Permission_Trans_Manager()


# GET -> Permission Base
@permission_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_permission_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)]
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/index.html', context={
            'request': request, 'params': {
                'default': 'default', 'user_session': user_session
            }
        }
    )


# GET -> Extra Hours Menu
@permission_route.get(Cns.URL_PERMISSION_EXTRA_HOURS_MAIN.value, response_class=HTMLResponse)
async def getting_app_permission_extra_hours_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # fetch request extra hours info

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/permission/extra_hours/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )
