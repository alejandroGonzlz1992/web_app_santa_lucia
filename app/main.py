# import
from fastapi import Request
from fastapi.responses import HTMLResponse

# local import
from app import fastapi_app_config
from app.backend.tooling.setting.constants import Constants as Cns

# instance app
app = fastapi_app_config()


# root endpoint
@app.get(Cns.ROOT.value, response_class=HTMLResponse)
async def getting_app_home_page_endpoint(
        request: Request,
) -> HTMLResponse:

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/index.html', context={
            'request': request, 'params': {
                'time_zone': Cns.CR_TIME_ZONE.value
            }
        }
    )
