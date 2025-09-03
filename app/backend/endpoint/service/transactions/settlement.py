# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
settlement_route = APIRouter(prefix=Cns.URL_SETTLEMENT.value, tags=[Cns.TRANS.value])


# GET -> Settlement Base
@settlement_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_settlement_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Settlement Details
@settlement_route.get(Cns.URL_SETTLEMENT_DETAILS.value, response_class=HTMLResponse)
async def getting_app_settlement_details_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Settlement Adjustments
@settlement_route.get(Cns.URL_SETTLEMENT_ADJUST.value, response_class=HTMLResponse)
async def getting_app_settlement_adjust_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/settlement/adjust.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
