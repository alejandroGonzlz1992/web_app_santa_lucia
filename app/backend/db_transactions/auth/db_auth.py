# import
import random, string
from fastapi import HTTPException, status
from logging import getLogger
from typing import Union
from sqlalchemy.orm import joinedload

# local import
from app.backend.database import models
from app.backend.tooling.setting.security import getting_password_to_hash

# logger
logger = getLogger(__name__)


# class
class Auth_Manager:

    # init
    def __init__(self):
        self.string = string
        self.random = random
        self.models = models
        self.logger = logger
        self.to_hash = getting_password_to_hash

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

    # generating random password
    async def generating_random_password(self, length: int = 12) -> str:
        lower, upper = self.string.ascii_lowercase, self.string.ascii_uppercase
        digits, symbols = self.string.digits, self.string.punctuation
        # guarantee at least one char from each pool
        chars = [
            self.random.choice(lower), self.random.choice(upper),
            self.random.choice(digits), self.random.choice(symbols)]

        # fill password length
        all_chars = lower + upper + digits + symbols
        chars += self.random.choices(all_chars, k=length - len(chars))

        # shuffle password
        self.random.shuffle(chars)

        # return string
        return "".join(chars)

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

    # getting user restore entity
    async def user_restore_entity(self, db: object, model: Union[dict, object]) -> object:
        # query
        entity = db.query(
            self.models.User.id_record.label('_id'),
            self.models.User.identification.label('_ident'),
            self.models.User.email.label('_email'),
            self.models.User.temp_password.label('_temp'),
            self.models.User.is_temp.label('_is_temp'),
            self.models.Role.type.label('_role'),
        ).join(self.models.User_Role, self.models.User.id_record == self.models.User_Role.id_user).join(
            self.models.Role, self.models.User_Role.id_role == self.models.Role.id_record).filter(
            self.models.User.identification == model['user_identification']).first()

        # verify record exists
        if entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found")

        # return
        return entity

    # updating user new password
    async def user_updating_new_password(self, db: object, id: Union[str, int], model: Union[dict, object]) -> None:
        entity = db.query(self.models.User).filter(self.models.User.id_record == id).first()

        if entity:
            # hash new password
            to_hash = self.to_hash(password=model["new_password_field"])

            # update field
            entity.password = to_hash
            entity.temp_password = None
            entity.is_temp = False

            # db commit
            db.commit()

    # query current user password recover
    async def user_current_password_recover(self, db: object, input_email: str) -> dict:
        # format input email address
        to_email = input_email.strip().lower()
        # query entity record with email address
        entity = db.query(
            self.models.User.id_record.label('_id'),
            self.models.User.email.label('_email')
        ).filter(self.models.User.email == to_email).first()

        if entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Found With Email")

        # generate random password
        temp_password = await self.generating_random_password()

        # return
        return {"id": entity._id, "email": entity._email, "temp_password": temp_password}

    # update temp_password and status field
    async def updating_temp_password_field(self, db: object, entity: dict) -> None:
        # id to int
        to_int = int(entity['id'])
        # query
        user_update = db.query(self.models.User).filter(self.models.User.id_record == to_int).first()

        if user_update:
            # to hash
            to_hash = self.to_hash(password=entity['temp_password'])

            user_update.password = to_hash
            user_update.temp_password = to_hash
            user_update.is_temp = True

            # db commit
            db.commit()

