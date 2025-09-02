# import
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from logging import getLogger, CRITICAL

# local import


# suppress bcrypt version warning
getLogger('passlib.handlers.bcrypt').setLevel(CRITICAL)


# fastapi app config
def fastapi_app_config() -> FastAPI:
    """

    :return:
    """

    # launch db model metadata create

    # app instance
    app = FastAPI()

    # mount static folder for url_for
    # app.mount()

    # include api routes
    # for route in routing_list:
    #     app.include_router(router=route)

    # return
    return app
