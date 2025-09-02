# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
reports_route = APIRouter(prefix=Cns.TRANS_REPORT.value, tags=[Cns.TRANS.value])


# GET -> Reports Base
@reports_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_reports_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/report/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
