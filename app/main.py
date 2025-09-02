# import
from fastapi import Request
from fastapi.responses import HTMLResponse

# local import
from app import fastapi_app_config


# instance app
app = fastapi_app_config()


# root endpoint
@app.get('/santalucia/api/v/')
async def getting_app_home_page_endpoint(
        request: Request,
) -> dict:

    # return
    return {"app init": "successful launch"}
