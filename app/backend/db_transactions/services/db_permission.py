# import
import string, random
from re import compile
from pydantic import BaseModel
from fastapi import HTTPException, status
from logging import getLogger
from typing import Union
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from datetime import date, timedelta

# local import
from app.backend.database import models
from app.backend.database.models import User_Role
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
        # subject and approver User-Role relationship
        subj_user_role = aliased(self.models.User_Role)
        appr_user_role = aliased(self.models.User_Role)
        # subject
        subject = aliased(self.models.User)
        subject_role = aliased(self.models.Role)
        # approver
        approver = aliased(self.models.User)
        approver_role = aliased(self.models.Role)

        # base query
        records = (db.query(
            # request info
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            self.models.Request_Extra_Hour.status.label('_status'),
            # subject info
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject_role.type.label('_subject_role'),
            # approver info
            approver.name.label('_appr_name'),
            approver.lastname.label('_appr_lastname'),
            approver.lastname2.label('_appr_lastname2'),
            approver_role.type.label('_approver_role'),
        ).select_from(
            self.models.Request_Extra_Hour
        )
        .join(
            # subject user-role relationship
            subj_user_role, subj_user_role.id_record == self.models.Request_Extra_Hour.id_subject
        ).join(
            subject, subject.id_record == subj_user_role.id_user
        ).join(
            subject_role, subject_role.id_record == subj_user_role.id_role
        ).join(
            # approver user entity
            approver, approver.id_record == subj_user_role.approver
        ).outerjoin(
            # approver own role
            appr_user_role, appr_user_role.id_user == approver.id_record
        ).outerjoin(
            approver_role, approver_role.id_record == appr_user_role.id_role
        ))

        # get the user currently logged in
        current_logged_in = db.query(
            self.models.Role.type
        ).join(
            self.models.User_Role, self.models.User_Role.id_role == self.models.Role.id_record
        ).filter(
            self.models.User_Role.id_user == id_login
        ).scalar()

        # role-base filtering
        if current_logged_in == "Empleado":
            records = records.filter(subj_user_role.id_user == id_login)

        elif current_logged_in == "Jefatura":
            records = records.filter(or_(
                    subj_user_role.id_user == id_login,
                    approver_role.type == "Jefatura"
                )
            )

        elif current_logged_in == "Gerencia":
            records = records.filter(
                or_(
                    subj_user_role.id_user == id_login,
                    subject_role.type == "Jefatura"
                )
            )

        elif current_logged_in == "Administrador":
            pass

        # return
        return {
            "records": records.order_by(self.models.Request_Extra_Hour.id_record.desc()).all(),
            "logged_in": current_logged_in
        }

    # register record on db
    async def registering_extra_hour_record(self, db: object, model: Union[dict, object], id_session: int) -> object:
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

        # return
        return extra_hours

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

    # current request record
    async def current_extra_hour_request_record(self, db: object, id_request: Union[int, str]) -> object:
        # alias
        subject_role = aliased(self.models.User_Role)
        subject_user = aliased(self.models.User)

        record = (db.query(
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            self.models.Request_Extra_Hour.status.label('_status'),
            self.models.Request_Extra_Hour.id_subject.label('_id_user_role'),
            # subject's user fields
            subject_user.name.label('_subj_name'),
            subject_user.lastname.label('_subj_lastname'),
            subject_user.lastname2.label('_subj_lastname2'),
        ).select_from(
            self.models.Request_Extra_Hour
        ).join(
            subject_role, subject_role.id_record == self.models.Request_Extra_Hour.id_subject
        ).join(
            subject_user, subject_user.id_record == subject_role.id_user
        ).filter(
            self.models.Request_Extra_Hour.id_record == id_request
        ).first())

        # return
        return record

    # update record on db
    async def updating_extra_hour_record(self, db: object, model: Union[dict, object]) -> object:
        # record
        record = db.query(
            self.models.Request_Extra_Hour
        ).filter(
            self.models.Request_Extra_Hour.id_record == model["id"]
        ).first()

        if record:
            record.status = model["permission_status_field"]

            # db commit
            db.commit()
            # db refresh
            db.refresh(instance=record)

        # return
        return record

    # register extra hours
    async def registering_user_extra_hours(
            self, db: object, model: Union[dict, object]) -> None:
        # query record from request
        request_record = db.query(
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.id_subject.label('_id_subject')
        ).filter(
            self.models.Request_Extra_Hour.id_record == model["id"]
        ).first()

        # calendar
        holidays = self.cns.HOLIDAY_CALENDAR.value
        # build a set
        holiday_set = set(holidays.values())
        # is_holiday
        is_holiday_in = request_record._date_request in holiday_set

        new_hours = self.models.Extra_Hour(
            hours = request_record._hours,
            date_request = request_record._date_request,
            is_holiday = is_holiday_in,
            id_subject = request_record._id_subject,
        )
        # add to model
        db.add(instance=new_hours)
        # db commit
        db.commit()
        # db refresh
        db.refresh(instance=new_hours)

    # query vacations object
    async def querying_vacations_details(self, db: object, id_login: Union[int, str]) -> object:
        # subject and approver User-Role relationship
        subj_user_role = aliased(self.models.User_Role)
        appr_user_role = aliased(self.models.User_Role)
        # subject
        subject = aliased(self.models.User)
        subject_role = aliased(self.models.Role)
        # approver
        approver = aliased(self.models.User)
        approver_role = aliased(self.models.Role)

        records = db.query(
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.date_start.label('_start'),
            self.models.Request_Vacation.date_return.label('_return'),
            self.models.Request_Vacation.days.label('_days'),
            self.models.Request_Vacation.status.label('_status'),
            # subject info
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject_role.type.label('_subject_role'),
                # approver info
            approver.name.label('_appr_name'),
            approver.lastname.label('_appr_lastname'),
            approver.lastname2.label('_appr_lastname2'),
            approver_role.type.label('_approver_role'),
        ).select_from(
            self.models.Request_Vacation
        ).join(
            # subject user-role relationship
            subj_user_role, subj_user_role.id_record == self.models.Request_Vacation.id_subject
        ).join(
            subject, subject.id_record == subj_user_role.id_user
        ).join(
            subject_role, subject_role.id_record == subj_user_role.id_role
        ).join(
            # approver user entity
            approver, approver.id_record == subj_user_role.approver
        ).outerjoin(
            # approver own role
            appr_user_role, appr_user_role.id_user == approver.id_record
        ).outerjoin(
            approver_role, approver_role.id_record == appr_user_role.id_role
        )

        # get the user currently logged in
        current_logged_in = db.query(
            self.models.Role.type
        ).join(
            self.models.User_Role, self.models.User_Role.id_role == self.models.Role.id_record
        ).filter(
            self.models.User_Role.id_user == id_login
        ).scalar()

        # role-base filtering
        if current_logged_in == "Empleado":
            records = records.filter(subj_user_role.id_user == id_login)

        elif current_logged_in == "Jefatura":
            records = records.filter(or_(
                    subj_user_role.id_user == id_login,
                    approver_role.type == "Jefatura"
                )
            )

        elif current_logged_in == "Gerencia":
            records = records.filter(
                or_(
                    subj_user_role.id_user == id_login,
                    subject_role.type == "Jefatura"
                )
            )

        elif current_logged_in == "Administrador":
            pass

        # return
        return {
            "records": records.order_by(self.models.Request_Vacation.id_record.desc()).all(),
            "logged_in": current_logged_in
        }

    # traversing holidays
    async def traversing_holidays(self, schema: Union[BaseModel, dict]) -> int:
        current_date = schema["start_date_field"]
        end_date = schema["end_date_field"]
        days = int(schema["day_field_total"])

        while current_date <= end_date:
            for holiday in self.cns.HOLIDAY_CALENDAR.value.values():
                # compare month and day
                if current_date.month == holiday.month and current_date.day == holiday.day:
                    days -= 1
                    break
            # update date count
            current_date += timedelta(days=1)

        # ensure days do not reach 0
        if days < 0:
            days = 0

        # return
        return days

    # register record on db
    async def registering_vacations_record(self, db: object, model: Union[dict, object], id_session: int) -> object:

        # validating if holidays
        days_ = await self.traversing_holidays(schema=model)

        vacations = self.models.Request_Vacation(
            days=days_,
            date_start=model["start_date_field"],
            date_return=model["end_date_field"],
            type=model["request_vacation"],
            id_subject=id_session
        )
        # add to model
        db.add(instance=vacations)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=vacations)

        # return
        return vacations

    # query current vacation record
    async def current_vacation_available_record(
            self, db: object, id_session: Union[int, str], schema: Union[BaseModel, dict]) -> object:
        # row
        row = db.query(
            self.models.Vacation.available.label('_available')
        ).filter(
            self.models.Vacation.id_subject == id_session
        ).first()

        if row is None:
            pass

        if row._available < int(schema["day_field_total"]):
            raise self.http_exec(status_code=self.status.HTTP_400_BAD_REQUEST,
                                 detail='Vacation available is less than 1')

    # current vacation record
    async def current_vacation_request_record(self, db: object, id_request: Union[int, str]) -> object:
        # alias
        subject_role = aliased(self.models.User_Role)
        subject_user = aliased(self.models.User)

        record = (db.query(
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.days.label('_days'),
            self.models.Request_Vacation.date_start.label('_start'),
            self.models.Request_Vacation.date_return.label('_return'),
            self.models.Request_Vacation.type.label('_type'),
            self.models.Request_Vacation.status.label('_status'),
            self.models.Request_Vacation.id_subject.label('_id_user_role'),
            # subject's user fields
            subject_user.name.label('_subj_name'),
            subject_user.lastname.label('_subj_lastname'),
            subject_user.lastname2.label('_subj_lastname2'),
        ).select_from(
            self.models.Request_Vacation
        ).join(
            subject_role, subject_role.id_record == self.models.Request_Vacation.id_subject
        ).join(
            subject_user, subject_user.id_record == subject_role.id_user
        ).filter(
            self.models.Request_Vacation.id_record == id_request
        ).first())

        # return
        return record

    # update record on db
    async def updating_vacations_record(self, db: object, model: Union[dict, object]) -> object:
        # record
        record = db.query(
            self.models.Request_Vacation
        ).filter(
            self.models.Request_Vacation.id_record == model["id"]
        ).first()

        if record:
            record.status = model["permission_status_field"]

            # db commit
            db.commit()
            # db refresh
            db.refresh(instance=record)

        # return
        return record

    # register vacations
    async def registering_user_vacations(
            self, db: object, model: Union[dict, object]) -> object:
        # query record from request
        request_record = db.query(
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.days.label('_days'),
            self.models.Request_Vacation.date_start.label('_start'),
            self.models.Request_Vacation.date_return.label('_return'),
            self.models.Request_Vacation.type.label('_type'),
            self.models.Request_Vacation.status.label('_status'),
            self.models.Request_Vacation.id_subject.label('_id_subject')
        ).filter(
            self.models.Request_Vacation.id_record == model["id"]
        ).first()

        # add temp db model
        new_vacations = self.models.Vacation(
            used_days=request_record._days,
            id_subject=request_record._id_subject,
        )
        # add to model
        db.add(instance=new_vacations)
        # db commit
        db.commit()
        # db refresh
        db.refresh(instance=new_vacations)

        # return
        return new_vacations

    # update used days vacations
    async def updating_used_days_vacations(self, db: object, record: object) -> None:
        # query record
        current_row = db.query(
            self.models.Vacation
        ).filter(
            self.models.Vacation.id_subject == record._id_user_role,
        ).first()

        # update records
        current_days = int(current_row.available - record._days)

        if current_row:
            current_row.available = current_days
            current_row.used_days = record._days

            # db commit
            db.commit()