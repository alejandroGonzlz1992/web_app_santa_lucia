# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_records import Db_Crud_Request
from app.backend.schema.crud.records.Payments import Create_Payment_Date, Update_Payment_Date


# router
payment_date_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])
# records query
records = Db_Crud_Request()


# GET -> Payment Date Base
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_BASE.value, response_class=HTMLResponse)
async def getting_app_payment_date_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # rows
    rows = await records.getting_payment_dates_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'rows': rows
            }
        }
    )


# GET -> Payment Date Register
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_CREATE.value, response_class=HTMLResponse)
async def getting_app_payment_date_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # current user logged in

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Payment Date Register
@payment_date_route.post(Cns.CRUD_PAYMENT_DATE_CREATE.value, response_class=HTMLResponse)
async def posting_app_payment_date_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[Create_Payment_Date, Depends(dependency=Create_Payment_Date.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await records.register_crud_payment_dates(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await records.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_payment_date_register_endpoint(request=request, db=db, fg='_orm_error') # return

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await records.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_payment_date_register_endpoint(request=request, db=db, fg='_ops_error')  # return

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'fechas_pago', 'fg': '_create'
            }
        }
    )


# GET -> Payment Date Update
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_UPDATE.value, response_class=HTMLResponse)
async def getting_app_payment_date_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Payment Date Update
@payment_date_route.post(Cns.CRUD_PAYMENT_DATE_POST.value, response_class=HTMLResponse)
async def posting_app_payment_date_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[Update_Payment_Date, Depends(dependency=Update_Payment_Date.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await records.updating_crud_payment_dates(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await records.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_payment_date_update_endpoint(
            request=request, id=model.id, db=db, fg='_orm_error') # return

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await records.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_payment_date_update_endpoint(
            request=request, id=model.id, db=db, fg='_ops_error')  # return

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'fechas_pago', 'fg': '_update'
            }
        }
    )

