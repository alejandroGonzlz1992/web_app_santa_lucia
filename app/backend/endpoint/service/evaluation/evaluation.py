# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
evaluation_route = APIRouter(prefix=Cns.URL_EVALUATION.value, tags=[Cns.TRANS.value])


# GET -> Evaluation Base
@evaluation_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_evaluation_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Evaluation Employee
@evaluation_route.get(Cns.URL_EVALUATION_EMPLOYEE.value, response_class=HTMLResponse)
async def getting_app_evaluation_employee_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/employee.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Evaluation Supervisor
@evaluation_route.get(Cns.URL_EVALUATION_SUPERVISOR.value, response_class=HTMLResponse)
async def getting_app_evaluation_supervisor_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/supervisor.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Evaluation Enable
@evaluation_route.get(Cns.URL_EVALUATION_ENABLE.value, response_class=HTMLResponse)
async def getting_app_evaluation_enable_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/enable.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
