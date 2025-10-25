# import
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Union
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# class
class Checkin_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns

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
        return {(t or "").strip() for (t,) in rows}

    # fetching current checkin tracker records
    async def querying_current_checkin_records(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # entity aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        sub_role = aliased(self.models.Role)

        rows = db.query(
            # checkin
            self.models.Checkin_Tracker.id_record.label('_id'),
            self.models.Checkin_Tracker.start_hour.label('_start'),
            self.models.Checkin_Tracker.end_hour.label('_end'),
            self.models.Checkin_Tracker.hours.label('_hours'),
            self.models.Checkin_Tracker.status.label('_status'),
            self.models.Checkin_Tracker.log_date.label('_log_date'),
            # subject info
            subject.id_record.label('_emp_id'),
            subject.identification.label('_emp_ident'),
            subject.name.label('_emp_name'),
            subject.lastname.label('_emp_lastname'),
            subject.lastname2.label('_emp_lastname2'),
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Checkin_Tracker.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            sub_role, sub_role.id_record == sub_user_role.id_role
        )

        # get role type
        user_role_type = (
            db.query(sub_role.type)
            .join(sub_user_role, sub_user_role.id_role == sub_role.id_record)
            .filter(sub_user_role.id_user == id_session)
            .scalar()
        )

        # return
        if user_role_type != "Administrador":
            rows = rows.filter(sub_user_role.id_user == id_session)
            return rows

        # return
        return rows.order_by(self.models.Checkin_Tracker.id_record.desc()).all()

    # registering new checkin tracker
    async def registering_new_checkin_mark(
            self, db: Union[Session, object], schema: Union[BaseModel, object], id_session: Union[int, str]) -> object:
        # checkin
        checkin = self.models.Checkin_Tracker(
            start_hour = schema["checkin_value"],
            end_hour = schema["checkout_value"],
            hours = schema["hours_value"],
            id_subject = id_session,
        )
        # add model
        db.add(instance=checkin)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=checkin)
