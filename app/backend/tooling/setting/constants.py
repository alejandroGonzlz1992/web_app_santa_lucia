# import
from fastapi.templating import Jinja2Templates
from enum import Enum
from zoneinfo import ZoneInfo
from datetime import datetime
from pathlib import Path

# local import
from app.backend.tooling.setting.env import env

# constants class
class Constants(Enum):

    # connection string
    CONNECTION_STRING = f"postgresql://{env.db_username}:{env.db_password}@{env.db_host}:{env.db_port}/{env.db_name}"

    # static dir
    STATIC_DIR, STATIC_PATH, STATIC_NAME = '/frontend', 'app/frontend', 'static'

    # jinja2 template
    TEMPLATES = Path(__file__).resolve().parent.parent.parent.parent
    TEMPLATES_DIR = f'{TEMPLATES}/frontend/templates'
    HTML_ = Jinja2Templates(directory=TEMPLATES_DIR)

    # general
    CR_TIME_ZONE = datetime.now(ZoneInfo('America/Costa_Rica')).strftime("%d-%m-%Y | %-I:%M %p")

    # endpoint
    ROOT = '/santalucia/api/v/'