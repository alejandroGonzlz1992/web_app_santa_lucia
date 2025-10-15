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
                Payroll_User.details.label('_details'),
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

    # format to money CRC style
    @staticmethod
    async def formatting_crc_money_style(value: Union[str, int, float, Decimal]) -> str:
        # validate default value
        if value is None: value = 0
        # str formatted
        format_str = f'{float(value):,.2f}'
        # return
        return format_str.replace(',', 'X').replace('.', ',').replace('X', '.')

    # format date to CRC format
    @staticmethod
    async def formatting_date_to_crc_time(value: Union[date, str]) -> str:
        # if not date return empty
        if value is None:
            return ""
        # if instance of date
        if isinstance(value, (date, datetime)):
            return value.strftime("%d-%m-%Y")
        # try common ISO strings
        try:
            return datetime.fromisoformat(str(value)).strftime("%d-%m-%Y")
        except Exception:
            return str(value)

    @staticmethod
    async def manage_libreoffice_suffixes(
            to_pdf: Union[object, str], temp: Union[object, str], context: Union[object, str], name: str) -> object:
        # validate
        if not to_pdf.exists():
            candidates = list(temp.glob(f'{name}*.pdf'))
            if not candidates:
                context.cleanup()
                raise RuntimeError('PDF conversion succeeded but PDF not found.')
            # rename
            candidates[0].rename(to_pdf)

    # converting docx file to pdf file (libreoffice)
    async def converting_docx_to_pdf_file_libreoffice(
            self, temp_path: Path, context: Union[dict, object], out_stem: str) -> Path:
        # temp vars
        temp_dir = Path(self.temp_dir.name)

        # render .docx file and add context
        filled_docx = temp_dir / f'{out_stem}.docx'
        tpl = self.docx(str(temp_path))
        tpl.render(context)
        tpl.save(str(filled_docx))

        # perform convertion to PDF
        self.sub_process.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(temp_dir), str(filled_docx)],
            check=True)

        # manage suffixes
        fill_pdf = temp_dir / f'{out_stem}.pdf'
        await Payroll_Trans_Manager.manage_libreoffice_suffixes(
            to_pdf=fill_pdf, temp=temp_dir, context=self.temp_dir, name=out_stem)

        # return
        return fill_pdf

    # fetching information from query
    async def fetching_query_rows_into_dict(self, record: list, today_: date, default: float = 0.0) -> dict:
        # map record names into dict keys
        to_copy = self.cns.PAYROLL_QUERY_CONTEXT.value.copy()
        # fetch info
        to_copy["name"] = record._emp_name
        to_copy["lastname"] = record._emp_lastname
        to_copy["lastname2"] = record._emp_lastname2
        to_copy["current_date"] = await Payroll_Trans_Manager.formatting_date_to_crc_time(value=today_)
        to_copy["identification"] = record._emp_id
        to_copy["payroll_id"] = record._id
        to_copy["payment_date"] = await Payroll_Trans_Manager.formatting_date_to_crc_time(value=record._date_payment)
        to_copy["payment_date2"] = await Payroll_Trans_Manager.formatting_date_to_crc_time(value=record._date_payment2)
        to_copy["frecuency"] = record._frecuency
        to_copy["jf_name"] = record._apr_name
        to_copy["jf_lastname"] = record._apr_lastname
        to_copy["jf_lastname2"] = record._apr_lastname2
        to_copy["gross_amount"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._gross_income)
        to_copy["net_amount"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._net_amount)
        to_copy["rent_tax"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._renta_tax)
        to_copy["ccss_ivm"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._ccss_ivm)
        to_copy["ccss_eme"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._ccss_eme)
        to_copy["rop"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._rop)
        to_copy["association"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._association)
        to_copy["debt"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._debts)
        to_copy["support"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._child_support)
        to_copy["others"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._others)
        to_copy["payment_details"] = record._details

        # return
        return to_copy

    # update payroll record
    async def updating_payroll_record(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> None:

        # query record
        record = db.query(
            self.models.Payroll_User
        ).filter(
            self.models.Payroll_User.id_record == schema["id"]
        ).first()

        # update
        if record:
            record.ccss_ivm = schema["ccss_ivm"]
            record.ccss_eme = schema["ccss_eme"]
            record.ccss_rop = schema["rop_popular"]
            record.renta_tax = schema["rent_tax"]
            record.child_support = schema["child_support"]
            record.debts = schema["loan_request"]
            record.association = schema["association"]
            record.others = schema["other_deductions"]
            record.details = schema["payroll_details"].title()

            # commit
            db.commit()
