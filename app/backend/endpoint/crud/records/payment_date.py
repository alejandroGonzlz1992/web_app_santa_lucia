# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
payment_date_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])


# GET -> Payment Date Base
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_BASE.value, response_class=HTMLResponse)
async def getting_app_payment_date_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Payment Date Register
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_CREATE.value, response_class=HTMLResponse)
async def getting_app_payment_date_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Payment Date Update
@payment_date_route.get(Cns.CRUD_PAYMENT_DATE_UPDATE.value, response_class=HTMLResponse)
async def getting_app_payment_date_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/payment_date/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
