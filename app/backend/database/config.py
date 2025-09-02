# import
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# local import
from app.backend.tooling.setting.constants import Constants as Cns


# define engine object
engine: object = create_engine(url=Cns.CONNECTION_STRING.value, echo=False)

# define session object
session: object = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# define BASE class for models
BASE = declarative_base()


# db session controller
def Session_Controller():
    # instance session
    database = session()
    # yield session when needed
    try:
        yield database
    finally:
        database.close()
