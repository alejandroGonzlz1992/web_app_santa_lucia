# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.transactions.db_settlement import Settlement_Trans_Manager
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.database.config import Session_Controller


# router
settlement_route = APIRouter(prefix=Cns.URL_SETTLEMENT.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# serv
serv = Settlement_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Settlement Base
@settlement_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_settlement_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # query inability records
    records = await serv.query_settlement_records(db=db, id_session=user_login.user_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records
            }
        }
    )


# GET -> Settlement Details
@settlement_route.get(Cns.URL_SETTLEMENT_DETAILS.value, response_class=HTMLResponse)
async def getting_app_settlement_details_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# GET -> Settlement Adjustments
@settlement_route.get(Cns.URL_SETTLEMENT_ADJUST.value, response_class=HTMLResponse)
async def getting_app_settlement_adjust_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/adjust.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )
