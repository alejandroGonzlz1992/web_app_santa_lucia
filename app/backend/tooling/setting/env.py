# import
from pydantic_settings import BaseSettings
from pathlib import Path
from datetime import timedelta


# local env class
class Local_Env_Vars(BaseSettings):

    # define key vars for .env attrs
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    pg_admin_user: str
    pg_admin_password: str
    tkn_key: str
    tkn_algo: str
    tkn_expire: int
    app_key: str

    # load .env file
    class Config:
        env_file = Path(__file__).resolve().parents[4] / ".env"


env = Local_Env_Vars()
