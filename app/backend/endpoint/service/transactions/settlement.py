# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union
from datetime import date
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.schema.trans.settlement import Update_Settlement_Record
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.db_transactions.transactions.db_settlement import Settlement_Trans_Manager
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
    results = await serv.query_settlement_records(db=db, id_login=user_login.user_id)
    # ->
    records = results["records"]
    logged_in = results["logged_in"]

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records,
                'logged_in': logged_in
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

    # query specific settlement record
    record = await serv.query_specific_settlement_records(db=db, id_record=id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'record': record
            }
        }
    )


# GET -> Settlement Details PDF
@settlement_route.get(Cns.URL_SETTLEMENT_DETAILS_PDF.value, response_class=FileResponse)
async def posting_app_settlement_details_pdf_endpoint(
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None]
) -> FileResponse:

    # query records
    records = await serv.query_specific_settlement_records(db=db, id_record=id)
    # test the return dict
    to_dict = await serv.fetching_query_rows_into_dict(record=records, today_=date.today())
    # blueprint file path
    blueprint_file_path = Path(__file__).resolve().parents[3] / "tooling/docs/settlement_docs.docx"
    # file name
    pdf_file_name = f'liquidacion_{records._ident}_{records._emp_name}_{records._emp_lastname}.pdf'

    # convert to PDF
    pdf_path = await serv.converting_docx_to_pdf_file_libreoffice(
        temp_path=blueprint_file_path, context=to_dict, out_stem=pdf_file_name)

    return FileResponse(
        path=str(pdf_path), media_type="application/pdf", filename=pdf_file_name)


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


# POST -> Settlement Adjustments
@settlement_route.post(Cns.URL_SETTLEMENT_ADJUST_POST.value, response_class=HTMLResponse)
async def posting_app_settlement_adjust_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Settlement_Record, Depends(Update_Settlement_Record.formatting)],
) -> HTMLResponse:

    try:
        # update record
        await serv.updating_settlement_record(db=db, schema=model.model_dump())

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        # redirect to endpoint
        return await getting_app_settlement_adjust_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_settlement_adjust_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "liquidaciones", "redirect": "ce", "fg": "_update"
            }
        }
    )
