# import
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from logging import getLogger, CRITICAL

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.database.config import BASE, engine
from app.backend.database import models


# suppress bcrypt version warning
getLogger('passlib.handlers.bcrypt').setLevel(CRITICAL)


# fastapi app config
def fastapi_app_config() -> FastAPI:
    """

    :return:
    """

    # launch db model metadata create
    models.BASE.metadata.create_all(bind=engine)

    # app instance
    app = FastAPI()

    # mount static folder for url_for
    app.mount(Cns.STATIC_DIR.value, StaticFiles(directory=Cns.STATIC_PATH.value), name=Cns.STATIC_NAME.value)

    # include api routes
    # for route in routing_list:
    #     app.include_router(router=route)

    # return
    return app
