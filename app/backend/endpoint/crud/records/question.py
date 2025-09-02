# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, Union

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
question_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])


# GET -> Question Base
@question_route.get(Cns.CRUD_QUESTION_BASE.value, response_class=HTMLResponse)
async def getting_app_question_base_endpoint(
        request: Request,
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/eval_question/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Question Register
@question_route.get(Cns.CRUD_QUESTION_CREATE.value, response_class=HTMLResponse)
async def getting_app_question_register_endpoint(
        request: Request,
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/eval_question/create.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )


# GET -> Question Update
@question_route.get(Cns.CRUD_QUESTION_UPDATE.value, response_class=HTMLResponse)
async def getting_app_question_update_endpoint(
        request: Request,
        id: Annotated[Union[int, str], None],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/records/eval_question/update.html', context={
            'request': request, 'params': {
                'id': id, 'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value
            }
        }
    )
