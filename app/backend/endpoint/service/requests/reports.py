# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_reports import Reports_Trans_Manager
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.database.config import Session_Controller
from app.backend.schema.service.Reports import Create_Report


# router
reports_route = APIRouter(prefix=Cns.TRANS_REPORT.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# serv
serv = Reports_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Reports Base
@reports_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_reports_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/report/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Reports Base
@reports_route.post(Cns.BASE.value, response_class=HTMLResponse)
async def posting_app_reports_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Report, Depends(Create_Report.formatting)],
) -> HTMLResponse:

    try:
        test = await serv.querying_checking_tracker_report(db=db, schema=model.model_dump())
        print(test)

    except SQLAlchemyError:
        db.rollback() # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError) # -> error logs
        # redirect to endpoint
        return await getting_app_reports_base_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_reports_base_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "reportes", "redirect": "ce", "fg": "_generate"
            }
        }
    )