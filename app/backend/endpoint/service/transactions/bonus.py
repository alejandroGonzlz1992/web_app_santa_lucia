# import
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from pathlib import Path
from datetime import date

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.transactions.db_bonus import Bonus_Trans_Manager
from app.backend.schema.trans.bonus import Update_Bonus_Record, Generate_Bonus_Record
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.database.config import Session_Controller
from app.backend.tooling.setting.security import Bonus_Quota_Already_Exception


# router
bonus_route = APIRouter(prefix=Cns.URL_BONUS.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# serv
serv = Bonus_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Bonus Base
@bonus_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_bonus_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # query bonus records
    records = await serv.query_bonus_records(db=db, id_session=user_login.user_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/bonus/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'records': records,
                'role': user_login.role_type
            }
        }
    )


# GET -> Bonus Generate
@bonus_route.get(Cns.URL_BONUS_GENERATE.value, response_class=HTMLResponse)
async def getting_app_bonus_generate_endpoint(
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
        'service/payroll/bonus/generate.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session,
                'periods': Cns.BONUS_PERIODS.value
            }
        }
    )


# POST -> Bonus Generate
@bonus_route.post(Cns.URL_BONUS_GENERATE.value, response_class=HTMLResponse)
async def posting_app_bonus_generate_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Generate_Bonus_Record, Depends(dependency=Generate_Bonus_Record.formatting)]
) -> HTMLResponse:

    try:
        # collecting all users
        users = await serv.querying_users_bonus_records(db=db)
        # validating period selected
        await serv.validating_bonus_periods(db=db, schema=model.model_dump())

        # bonus calculation
        record = await serv.generating_bonus_calculations(db=db, users=users, schema=model.model_dump())

    except Bonus_Quota_Already_Exception:
        return await getting_app_bonus_generate_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail', exc='_duplicate')

    except HTTPException as http:
        db.rollback() # -> db rollback
        print(f'Error HTTPException: {http}')
        return await getting_app_bonus_generate_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail', exc='_not_start')

    except SQLAlchemyError as op:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        return await getting_app_bonus_generate_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError as op:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        return await getting_app_bonus_generate_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'aguinaldos', 'redirect': 'ce', 'fg': '_update'
            }
        }
    )


# GET -> Bonus Details
@bonus_route.get(Cns.URL_BONUS_DETAILS.value, response_class=HTMLResponse)
async def getting_app_bonus_details_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # query specific bonus record
    record = await serv.query_specific_bonus_records(db=db, id_record=id)

    # query month and year bonus quotas
    quotas = await serv.query_month_year_quotas(db=db, id_record=id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/bonus/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'record': record,
                'quotas': quotas
            }
        }
    )


# GET -> Bonus Details PDF
@bonus_route.get(Cns.URL_BONUS_DETAILS_PDF.value, response_class=FileResponse)
async def posting_app_bonus_details_pdf_endpoint(
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None]
) -> FileResponse:

    # query records
    records = await serv.query_specific_bonus_records(db=db, id_record=id)
    # test the return dict
    to_dict = await serv.fetching_query_rows_into_dict(record=records, today_=date.today())
    # blueprint file path
    blueprint_file_path = Path(__file__).resolve().parents[3] / "tooling/docs/bonus_docs.docx"
    # file name
    pdf_file_name = f'aguinaldo_{records._ident}_{records._emp_name}_{records._emp_lastname}.pdf'

    # convert to PDF
    pdf_path = await serv.converting_docx_to_pdf_file_libreoffice(
        temp_path=blueprint_file_path, context=to_dict, out_stem=pdf_file_name)

    return FileResponse(
        path=str(pdf_path), media_type="application/pdf", filename=pdf_file_name)


# GET -> Bonus Adjustments
@bonus_route.get(Cns.URL_BONUS_ADJUST.value, response_class=HTMLResponse)
async def getting_app_bonus_adjust_endpoint(
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
        'service/payroll/bonus/adjust.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'calendar': Cns.CALENDAR.value,
                'user_session': user_session
            }
        }
    )


# POST -> Bonus Adjustments
@bonus_route.post(Cns.URL_BONUS_ADJUST_POST.value, response_class=HTMLResponse)
async def posting_app_bonus_adjust_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Bonus_Record, Depends(Update_Bonus_Record.formatting)],
) -> HTMLResponse:

    try:
        # update record
        await serv.updating_bonus_record(db=db, schema=model.model_dump())

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        # redirect to endpoint
        return await getting_app_bonus_adjust_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_bonus_adjust_endpoint(
            request=request, db=db, user_login=user_login, id=model.id, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "aguinaldos", "redirect": "ce", "fg": "_update"
            }
        }
    )
