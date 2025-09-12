# import
import string, random
from re import compile
from fastapi import HTTPException, status, Request
from logging import getLogger
from typing import Union, Dict

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# logger
logger = getLogger(__name__)


# class
class Permission_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.logger = logger
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns

    # query permission object
