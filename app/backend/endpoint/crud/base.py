# import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# router
crud_route = APIRouter(prefix=Cns.CRUD_BASE.value, tags=[Cns.CRUD.value])


# GET -> Crud Base
@crud_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_crud_base_endpoint(
        request: Request
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'crud/index.html', context={
            'request': request, 'params': {
                'default': 'default'
            }
        }
    )
