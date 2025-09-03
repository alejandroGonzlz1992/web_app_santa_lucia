# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
payroll_route = APIRouter(prefix=Cns.URL_PAYROLL.value, tags=[Cns.TRANS.value])


# GET -> Payroll Base
@payroll_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_payroll_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/payroll/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Payroll Details
@payroll_route.get(Cns.URL_BONUS_DETAILS.value, response_class=HTMLResponse)
async def getting_app_payroll_details_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/payroll/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Payroll Adjustments
@payroll_route.get(Cns.URL_BONUS_ADJUST.value, response_class=HTMLResponse)
async def getting_app_payroll_adjust_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/payroll/adjust.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
