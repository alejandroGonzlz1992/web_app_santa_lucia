# import
import string, random
from re import compile
from fastapi import HTTPException, status
from logging import getLogger
from typing import Union, Dict
from sqlalchemy.orm import aliased
from sqlalchemy import and_

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

    # fetch active role types
    async def fetching_active_role_type(self, db: object, id_session: Union[int, str]) -> set[str]:
        rows = db.query(
            self.models.Role.type.label('_type')
        ).join(
            self.models.User_Role, self.models.User_Role.id_role == self.models.Role.id_record
        ).filter(
            self.models.User_Role.id_user == id_session,
            self.models.User_Role.status.is_(True)
        ).all()

        # return
        return { (t or "").strip() for (t, ) in rows }

    # query permission object
    async def querying_extra_hours_details(self, db: object, id_login: Union[int, str]) -> object:
        # alias
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        record = db.query(
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            # subject info
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            # approver info
            approver.name.label('_appr_name'),
            approver.lastname.label('_appr_lastname'),
            approver.lastname2.label('_appr_lastname2'),
            # request status
            self.models.Request_Extra_Hour.status.label('_status')
        ).select_from(
            self.models.Request_Extra_Hour
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Request_Extra_Hour.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        )

        role_types = await self.fetching_active_role_type(db=db, id_session=id_login)

        print(role_types)

        if "Administrador" in role_types:
            # see all
            pass

        elif "Jefatura" in role_types:
            record = record.filter(sub_user_role.approver == id_login)

        else:
            record = record.filter(sub_user_role.id_user == id_login)

        # return
        return record.order_by(self.models.Request_Extra_Hour.id_record.desc()).all()

    # register record on db
    async def registering_extra_hour_record(self, db: object, model: Union[dict, object], id_session: int) -> None:
        extra_hours = self.models.Request_Extra_Hour(
            hours=model["hour_quantity_field"],
            date_request=model["hour_date_field"],
            type=model["hour_schedule_type"],
            id_subject=id_session
        )
        # add to model
        db.add(instance=extra_hours)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=extra_hours)

    # collecting subject and approvers email
    async def collecting_subject_approver_emails(self, db: object, id_login: Union[int, str]) -> object:
        # alias
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        # row
        row = db.query(
            subject.email.label("_subj_email"), approver.email.label("_appr_email")
        ).select_from(
            self.models.User_Role
        ).join(
            subject, subject.id_record == self.models.User_Role.id_user
        ).outerjoin(
            approver, approver.id_record == self.models.User_Role.approver
        ).filter(
            self.models.User_Role.id_record == id_login
        ).limit(1).first()

        # return
        return {"user_email": getattr(row, "_subj_email", None), "approver_email": getattr(row, "_appr_email", None)}
