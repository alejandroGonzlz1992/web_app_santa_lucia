# import
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Union
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from docxtpl import DocxTemplate
import subprocess
import shutil

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# class
class Payroll_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns
        self.temp_dir = TemporaryDirectory()
        self.sub_process = subprocess
        self.shutil = shutil
        self.docx = DocxTemplate

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

    # query payroll records
    async def query_payroll_records(
            self, db: Union[Session, object], id_login: Union[int, str]) -> object:
        # alias
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        record = db.query(
            self.models.Payroll_User.id_record.label('_id'),
            # subject info
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            # approver info
            approver.name.label('_appr_name'),
            approver.lastname.label('_appr_lastname'),
            approver.lastname2.label('_appr_lastname2'),
            # request status
            self.models.Payment_Date.frecuency.label('_frecuency'),
            self.models.Payment_Date.date_payment.label('_payment_date'),
            self.models.Payment_Date.date_payment2.label('_payment_date2')
        ).select_from(
            self.models.Payroll_User
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Payroll_User.id_user
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).join(
            self.models.Payment_Date, self.models.Payment_Date.id_record == self.models.Payroll_User.id_payment_date
        )

        # validate rol type
        role_types = await self.fetching_active_role_type(db=db, id_session=id_login)

        if "Administrador" in role_types:
            # see all
            pass

        elif "Jefatura" in role_types:
            record = record.filter(or_(
                sub_user_role.approver == id_login, sub_user_role.id_user == id_login))

        else:
            record = record.filter(sub_user_role.id_user == id_login)

        # return
        return record.order_by(self.models.Payroll_User.id_record.desc()).all()

    # query specific payroll record
    async def query_specific_payroll_record(
            self, db: Union[Session, object], id_record: Union[int, str]) -> object:
        # entity aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        Payroll_User = self.models.Payroll_User
        Payment_Date = self.models.Payment_Date

        row = (
            db.query(
                Payroll_User.id_record.label('_id'),
                Payroll_User.net_amount.label('_net_amount'),
                Payroll_User.ccss_ivm.label('_ccss_ivm'),
                Payroll_User.ccss_eme.label('_ccss_eme'),
                Payroll_User.ccss_rop.label('_rop'),
                Payroll_User.renta_tax.label('_renta_tax'),
                Payroll_User.child_support.label('_child_support'),
                Payroll_User.debts.label('_debts'),
                Payroll_User.association.label('_association'),
                Payroll_User.others.label('_others'),
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
                # payroll/payment info
                sub_user_role.gross_income.label('_gross_income'),
                Payment_Date.frecuency.label('_frecuency'),
                Payment_Date.date_payment.label('_date_payment'),
                Payment_Date.date_payment2.label('_date_payment2'),
            )
            .select_from(Payroll_User)
            .join(sub_user_role, sub_user_role.id_record == Payroll_User.id_user)  # ← fix ON
            .join(subject, subject.id_record == sub_user_role.id_user)
            .join(approver, approver.id_record == sub_user_role.approver)
            .join(Payment_Date, Payment_Date.id_record == Payroll_User.id_payment_date)
            .filter(Payroll_User.id_record == id_record)
            .first()
        )

        return row
