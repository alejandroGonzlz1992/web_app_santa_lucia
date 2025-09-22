# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.schema.service.Checkin import Create_Checkin_Tracker
from app.backend.db_transactions.services.db_checkin import Checkin_Trans_Manager
from app.backend.database.config import Session_Controller


# router
checkin_route = APIRouter(prefix=Cns.CHECKIN_BASE.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()
# serv
serv = Checkin_Trans_Manager()
# error logs
exc_logs = Logs_Manager()


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

    # fetch checkin tracker records
    records = await serv.querying_current_checkin_records(db=db, id_session=user_login.user_role_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records
            }
        }
    )


# GET -> Checkin Register
@checkin_route.get(Cns.CHECKIN_REGISTER.value, response_class=HTMLResponse)
async def getting_app_checkin_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/checkin/checkin.html', context={
            'request': request, 'params': {
                'fg': fg, 'user_session': user_session
            }
        }
    )


# POST -> Checkin Register
@checkin_route.post(Cns.CHECKIN_REGISTER.value, response_class=HTMLResponse)
async def posting_app_checkin_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Checkin_Tracker, Depends(dependency=Create_Checkin_Tracker.formatting)],
) -> HTMLResponse:

    try:
        # register check in mark
        await serv.registering_new_checkin_mark(db=db, schema=model.model_dump(), id_session=user_login.user_role_id)

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        # redirect to endpoint
        return await getting_app_checkin_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_checkin_register_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "marcas", "redirect": "ce", "fg": "_checkin"
            }
        }
    )
