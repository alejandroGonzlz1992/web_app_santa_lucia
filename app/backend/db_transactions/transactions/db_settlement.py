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
class Settlement_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns

    # fetch active role types
    async def fetching_active_role_type(
            self, db: Union[Session, object], id_session: Union[int, str]) -> set[str]:
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

    # query settlement records
    async def query_settlement_records(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # entity aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        rows = db.query(
            self.models.Settlement.id_record.label('_id'),
            self.models.Settlement.log_date.label('_log_date'),
            self.models.Settlement.type.label('_type'),
            self.models.Settlement.total_amount.label('_total_amount'),
            self.models.Settlement.status.label('_status'),
            # subject info
            subject.id_record.label('_emp_id'),
            subject.identification.label('_ident'),
            subject.name.label('_emp_name'),
            subject.lastname.label('_emp_lastname'),
            subject.lastname2.label('_emp_lastname2'),
            # approver info
            approver.id_record.label('_apr_id'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Settlement.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).filter(
            sub_user_role.status.is_(False),
        )

        # fetching active role types
        roles = await self.fetching_active_role_type(db=db, id_session=id_session)

        if 'Administrador' in roles:
            # see all
            pass
        elif 'Jefatura' in roles:
            rows = rows.filter(or_(sub_user_role.approver == id_session, sub_user_role.id_user == id_session))
        else:
            rows = rows.filter(sub_user_role.id_user == id_session)

        # return
        return rows.order_by(self.models.Settlement.id_record.desc()).all()

    # query specific settlement record
    async def query_specific_settlement_records(
            self, db: Union[Session, object], id_record: Union[int, str]) -> object:
        # entity aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        row = db.query(
            self.models.Settlement.id_record.label('_id'),
            self.models.Settlement.log_date.label('_log_date'),
            self.models.Settlement.type.label('_type'),
            self.models.Settlement.total_amount.label('_total_amount'),
            self.models.Settlement.cesantia.label('_cesantia_amount'),
            self.models.Settlement.vacations.label('_vacations_amount'),
            self.models.Settlement.bonus.label('_bonus_amount'),
            self.models.Settlement.payroll.label('_payroll_amount'),
            self.models.Settlement.status.label('_status'),
            self.models.Settlement.details.label('_details'),
            # subject info
            subject.id_record.label('_emp_id'),
            subject.identification.label('_ident'),
            subject.name.label('_emp_name'),
            subject.lastname.label('_emp_lastname'),
            subject.lastname2.label('_emp_lastname2'),
            # approver info
            approver.id_record.label('_apr_id'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            # termination date
            sub_user_role.termination_date.label('_termination_date')
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Settlement.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).filter(
            self.models.Settlement.id_record == id_record
        ).first()

        # return
        return row
