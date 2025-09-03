# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
bonus_route = APIRouter(prefix=Cns.URL_BONUS.value, tags=[Cns.TRANS.value])


# GET -> Bonus Base
@bonus_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_bonus_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/bonus/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Bonus Details
@bonus_route.get(Cns.URL_BONUS_DETAILS.value, response_class=HTMLResponse)
async def getting_app_bonus_details_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/bonus/details.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Bonus Adjustments
@bonus_route.get(Cns.URL_BONUS_ADJUST.value, response_class=HTMLResponse)
async def getting_app_bonus_adjust_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/payroll/bonus/adjust.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'ops': Cns.OPS_CRUD.value, 'calendar': Cns.CALENDAR.value
            }
        }
    )
