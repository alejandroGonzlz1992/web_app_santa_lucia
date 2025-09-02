# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
deduction_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])


# GET -> Deduction Base
@deduction_route.get(Cns.CRUD_DEDUCTION_BASE.value, response_class=HTMLResponse)
async def getting_app_deduction_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Deduction Register
@deduction_route.get(Cns.CRUD_DEDUCTION_CREATE.value, response_class=HTMLResponse)
async def getting_app_deduction_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Deduction Update
@deduction_route.get(Cns.CRUD_DEDUCTION_UPDATE.value, response_class=HTMLResponse)
async def getting_app_deduction_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/deduction/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
