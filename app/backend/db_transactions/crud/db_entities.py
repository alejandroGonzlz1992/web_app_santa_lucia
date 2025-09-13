# import
import string, random
from fastapi import HTTPException, status
from logging import getLogger
from typing import Union

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_password_to_hash


# logger
logger = getLogger(__name__)


# class
class Crud_Entities_Manager:

    # init
    def __init__(self):
        self.models = models
        self.logger = logger
        self.to_hash = getting_password_to_hash
        self.string = string
        self.random = random
        self.exc = None
        self.cns = Cns

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

    # catching integrity error field
    async def identify_error_integrity(self, catcher: object) -> str:
        to_string = str(catcher)
        if "user_identification_key" in to_string:
            self.exc = "_identification"
        elif "user_email_key" in to_string:
            self.exc = "_email"
        elif "user_phone_key" in to_string:
            self.exc = "_phone"
        return self.exc

    # generate random password / hash password
    async def generating_random_password(self, length: int = 12) -> str:
        # chars pool
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

    # departments crud
    async def getting_departments_crud_rows(self, db: object) -> object:
        departments = db.query(self.models.Department.id_record.label('_id'),
                               self.models.Department.name.label('_name')).all()
        return departments

    # schedules crud
    async def getting_schedule_crud_rows(self, db: object) -> object:
        schedules = db.query(self.models.Schedule.id_record.label('_id'),
                             self.models.Schedule.name.label('_name')).all()
        return schedules

    # roles crud for users
    async def getting_roles_crud_for_users(self, db: object) -> object:
        roles = db.query(self.models.Role.id_record.label('_id'), self.models.Role.name.label('_name'),
                         self.models.Role.type.label('_type')).all()

        return roles

    # roles crud
    async def getting_roles_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Role.id_record.label('_id'),
                        self.models.Role.name.label('_name'),
                        self.models.Role.type.label('_type'),
                        self.models.Role.date_create.label('_create'),
                        self.models.Role.date_update.label('_update'),
                        self.models.Schedule.name.label('_schedule'),
                        self.models.Department.name.label('_dept'))
                .select_from(self.models.Role).join(self.models.Role.department)
                .join(self.models.Role.schedule).all())
        # return
        return rows

    # register role
    async def registering_crud_role(self, db: object, model: Union[dict, object]) -> None:
        # temp model
        roles = self.models.Role(
            name=model["role_name"].title(),
            type=model["role_type"].title(),
            date_create=model["role_create_date"],
            date_update=model["role_create_date"],
            id_schedule=model["role_schedule"],
            id_department=model["role_department"]
        )
        # add to db
        db.add(instance=roles)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=roles)

    # update role
    async def updating_crud_role(self, db: object, model: Union[dict, object]) -> None:
        role = db.query(self.models.Role).filter(
            self.models.Role.id_record == model['id']).first()

        if role:
            role.name = model["role_name"].title()
            role.type = model["role_type"].title()
            role.date_update = model["role_create_date"]
            role.id_schedule = model["role_schedule"]
            role.id_department = model["role_department"]

        # commit changes
        db.commit()

    # users crud
    async def getting_users_crud_rows(self, db: object) -> object:
        # rows
        user = (db.query(self.models.User_Role.id_record.label('_id'), self.models.User.identification.label('_ident'),
                self.models.User.name.label('_name'), self.models.User.lastname.label('_lastname'),
                self.models.User.lastname2.label('_lastname2'), self.models.User.email.label('_email'),
                self.models.Role.name.label('_role'), self.models.User_Role.status.label('_status'),
                self.models.User_Role.hire_date.label('_hire'), self.models.User.id_record.label('_user_id'))
            .select_from(self.models.User_Role)
            .join(self.models.User_Role.user)
            .join(self.models.User_Role.role)
            .all())

        return user

    # register user
    async def registering_crud_users(self, db: object, model: Union[dict, object]) -> dict:
        # generate hash password
        password = await self.generating_random_password()

        # hash password
        to_hash = self.to_hash(password)

        # temp model
        user = self.models.User(
            identification=model['user_identification'],
            name=model['user_name'].title(),
            lastname=model['user_lastname'].title(),
            lastname2=model['user_lastname2'].title(),
            birthday=model['user_birthday'],
            email=model['user_email'].lower(),
            phone=model['user_phone'],
            gender=model['user_gender'],
            marital_status=model['user_marital_status'],
            children=model['user_children'],
            password=to_hash,
            temp_password=to_hash,
            is_temp=True
        )
        # add to db
        db.add(instance=user)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=user)

        # return
        return {"user": user, "temp": password}

    # register User_Role entity
    async def registering_crud_user_role_entity(
            self, db: object, user_id: Union[int, str], model: Union[dict, object]) -> None:
        entity = self.models.User_Role(
            gross_income=model['user_gross_income'],
            hire_date=model['user_create_date'],
            id_user=user_id,
            id_role=model['user_role'],
            approver=model['user_approver']
        )
        # add to db
        db.add(instance=entity)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=entity)

    # update user
    async def updating_crud_users(self, db: object, model: Union[dict, object]) -> None:
        entity = db.query(self.models.User).filter(
            self.models.User.identification == model['user_identification']).first()

        if entity:
            entity.identification = model['user_identification']
            entity.name = model['user_name'].title()
            entity.lastname = model['user_lastname'].title()
            entity.lastname2 = model['user_lastname2'].title()
            entity.birthday = model['user_birthday']
            entity.email = model['user_email'].lower()
            entity.phone = model['user_phone']
            entity.gender = model['user_gender']
            entity.marital_status = model['user_marital_status']
            entity.children = model['user_children']

        # db commit
        db.commit()

    # update User_Role entity
    async def updating_crud_user_role_entity(
            self, db: object, model: Union[dict, object]) -> None:
        entity_role = db.query(self.models.User_Role).filter(
            self.models.User_Role.id_record == model['id']).first()

        if entity_role:
            entity_role.gross_income = model['user_gross_income']
            entity_role.hire_date = model['user_create_date']
            entity_role.id_role = model['user_role']
            entity_role.approver = model['user_approver']

        # db commit
        db.commit()

    # query current user status
    async def querying_user_status_entity(self, db: object, model: Union[dict, object]) -> object:
        entity = (db.query(
            self.models.User_Role.id_record.label('_id'),
            self.models.User_Role.status.label('_status'),
            self.models.User_Role.hire_date.label('_hire'),
            self.models.User_Role.id_user.label('_id_user'),
            self.models.User_Role.id_role.label('_id_role'),
            self.models.User.email.label('_email')
        ).join(
            self.models.User_Role, self.models.User.id_record == self.models.User_Role.id_user).filter(
            self.models.User_Role.id_record == model['id']).first())

        # return
        return entity

    # update current user status
    async def updating_user_status(self, db: object, record: Union[object, None], model: Union[dict, object]) -> dict:
        # flag to email
        deliver_mail = True

        # generate random password
        temp_password = await self.generating_random_password()

        # query entity
        user_role = db.query(self.models.User_Role).filter(self.models.User_Role.id_record == model['id']).first()

        # status
        if bool(model["user_status"]):
            user_role.status = True
            user_role.termination_date = None

            # query current user
            user = db.query(self.models.User).filter(self.models.User.id_record == record._id_user).first()

            if user:
                to_hash = self.to_hash(password=temp_password)

                user.password = to_hash
                user.temp_password = to_hash
                user.is_temp = True

            # db commit
            db.commit()

        else:
            user_role.status = False
            user_role.termination_date = model["termination_date"]

            # update flag
            deliver_mail = False

            # db commit
            db.commit()

        # return
        return {"flag": deliver_mail, "temp": temp_password}

    # fetching vacations date after user create
    async def fetching_vacation_days(self, db: object, user_id: Union[int, str], approver: Union[int, str]) -> None:
        # query user role
        id_user_role_current = db.query(self.models.User_Role.id_record.label('_id')).filter(
            self.models.User_Role.id_user == user_id).first()

        # temp model
        vacations = self.models.Vacation(
            available=self.cns.VACATIONS_QUEUE.value,
            id_subject=id_user_role_current._id,
            id_approver=approver
        )
        # add to model
        db.add(instance=vacations)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=vacations)
