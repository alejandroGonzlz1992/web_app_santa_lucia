# import
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated, Union
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import Session_Controller
from app.backend.db_transactions.crud.db_records import Crud_Records_Manager
from app.backend.schema.crud.records.Deductions import Create_Deduction, Update_Deduction


# router
deduction_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])
# records query
records = Crud_Records_Manager()


# GET -> Deduction Base
@deduction_route.get(Cns.CRUD_DEDUCTION_BASE.value, response_class=HTMLResponse)
async def getting_app_deduction_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # rows
    rows = await records.getting_deduction_crud_rows(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'rows': rows
            }
        }
    )


# GET -> Deduction Register
@deduction_route.get(Cns.CRUD_DEDUCTION_CREATE.value, response_class=HTMLResponse)
async def getting_app_deduction_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # current user logged in

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Deduction Register
@deduction_route.post(Cns.CRUD_DEDUCTION_CREATE.value, response_class=HTMLResponse)
async def posting_app_deduction_register_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[Create_Deduction, Depends(dependency=Create_Deduction.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await records.register_crud_deduction(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await records.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_deduction_register_endpoint(request=request, db=db, fg='_orm_error') # return

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await records.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_deduction_register_endpoint(request=request, db=db, fg='_ops_error')  # return

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'deducciones', 'fg': '_create'
            }
        }
    )


# GET -> Deduction Update
@deduction_route.get(Cns.CRUD_DEDUCTION_UPDATE.value, response_class=HTMLResponse)
async def getting_app_deduction_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
) -> HTMLResponse:

    # current user logged in

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# POST -> Deduction Update
@deduction_route.post(Cns.CRUD_DEDUCTION_POST.value, response_class=HTMLResponse)
async def posting_app_deduction_update_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        model: Annotated[Update_Deduction, Depends(dependency=Update_Deduction.formatting)],
) -> HTMLResponse:

    try:
        # commit to db
        await records.updating_crud_deduction(db=db, model=model.model_dump())

    except SQLAlchemyError as op:
        db.rollback() # db rollback ops
        await records.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_deduction_update_endpoint(
            request=request, id=model.id, db=db, fg='_orm_error') # return

    except OperationalError as op:
        db.rollback()  # db rollback ops
        await records.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_deduction_update_endpoint(
            request=request, id=model.id, db=db, fg='_ops_error')  # return

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'mantenimientos', 'redirect': 'deducciones', 'fg': '_update'
            }
        }
    )
