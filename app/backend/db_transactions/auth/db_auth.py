# import
from fastapi import HTTPException, status
from logging import getLogger
from typing import Union
from sqlalchemy.orm import joinedload

# local import
from app.backend.database import models


# logger
logger = getLogger(__name__)


# class
class Auth_Manager:

    # init
    def __init__(self):
        self.models = models
        self.logger = logger

    # logger messages
    async def logger_sql_alchemy_error(self, exception: Union[object, str]) -> None:
        self.logger.error(f'SQLAlchemyError: {str(exception)}')
        if hasattr(exception, 'orig'):
            self.logger.error(f'Original error: {exception.orig}')

    async def logger_sql_alchemy_ops_error(self, exception: Union[object, str]) -> None:
        self.logger.error(f'Operational Error: {str(exception)}')
        self.logger.error(f'Statement: {getattr(exception, "statement", None)}')
        self.logger.error(f'Params: {getattr(exception, "params", None)}')
        if hasattr(exception, 'orig'):
            self.logger.error(f'Original error: {exception.orig}')
            if hasattr(exception.orig, 'pgcode'):
                self.logger.error(f'PostgreSQL error code: {exception.orig.pgcode}')
            if hasattr(exception.orig, 'pgerror'):
                self.logger.error(f'PostgreSQL error message: {exception.orig.pgerror}')

    # getting credentials
    async def getting_credentials_login(self, db: object, model: Union[dict, object]) -> object:
        entity = db.query(self.models.User).options(joinedload(self.models.User.user_roles)
                                                    .joinedload(self.models.User_Role.role)).filter(
            self.models.User.email == model['email_login_field']).one_or_none()

        if entity is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Record Not Found")

        return entity

    # confirm if user is temp password
    async def validating_is_temp_password(self, db: object, payload: Union[dict, object]) -> bool:
        is_temp_password = db.query(self.models.User.is_temp.label('_is_temp')).filter(
            self.models.User.id_record == payload['user_id']).one_or_none()

        if is_temp_password[0]:
            return True
        else:
            return False

    # fetching current user
    async def fetching_current_user(self, db: object, user: object) -> object:
        # user_id -> int
        to_int = int(user.user_id)
        # query the current logged-in user
        row = db.query(
            self.models.User.id_record.label('_id'),
            self.models.User.name.label('_name'),
            self.models.User.lastname.label('_lastname'),
            self.models.User.lastname2.label('_lastname2'),
            self.models.User.gender.label('_gender'),
        ).filter(self.models.User.id_record == to_int).first()

        # return
        return row
