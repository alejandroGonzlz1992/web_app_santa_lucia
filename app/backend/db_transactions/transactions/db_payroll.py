# import
from numpy.core.records import record
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Union
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, and_, func
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from docxtpl import DocxTemplate
import subprocess
import shutil

# local import
from app.backend.database import models
from app.backend.database.models import Payroll_User
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
                Payroll_User.total_gross_amount.label('_total_gross_amount'),
                Payroll_User.ccss_ivm.label('_ccss_ivm'),
                Payroll_User.ccss_eme.label('_ccss_eme'),
                Payroll_User.ccss_rop.label('_rop'),
                Payroll_User.renta_tax.label('_renta_tax'),
                Payroll_User.child_support.label('_child_support'),
                Payroll_User.debts.label('_debts'),
                Payroll_User.vacations_amount.label('_vacations'),
                Payroll_User.extra_hour_amount.label('_extra_hours'),
                Payroll_User.holiday_amount.label('_holidays'),
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
        to_copy["identification"] = record._ident
        to_copy["payroll_id"] = record._id
        to_copy["payment_date"] = await Payroll_Trans_Manager.formatting_date_to_crc_time(value=record._date_payment)
        to_copy["payment_date2"] = await Payroll_Trans_Manager.formatting_date_to_crc_time(value=record._date_payment2)
        to_copy["frecuency"] = record._frecuency
        to_copy["jf_name"] = record._apr_name
        to_copy["jf_lastname"] = record._apr_lastname
        to_copy["jf_lastname2"] = record._apr_lastname2
        to_copy["gross_amount"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._total_gross_amount)
        to_copy["net_amount"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._net_amount)
        to_copy["rent_tax"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._renta_tax)
        to_copy["ccss_ivm"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._ccss_ivm)
        to_copy["ccss_eme"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._ccss_eme)
        to_copy["rop"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._rop)
        to_copy["vacations"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._vacations)
        to_copy["extra_hours"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._extra_hours)
        to_copy["holidays"] = await Payroll_Trans_Manager.formatting_crc_money_style(value=record._holidays)
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

    # query users for payroll
    async def querying_users_payroll_records(
            self, db: Union[Session, object]) -> list[object]:
        # aliases
        users = aliased(self.models.User)
        roles = aliased(self.models.Role)
        user_role = aliased(self.models.User_Role)

        # rows
        rows = (db.query(
            users.id_record.label('_id'), users.name.label('_name'), users.lastname.label('_lastname'),
            users.lastname2.label('_lastname2'), roles.id_record.label('_id_role'), roles.name.label('_role_name'),
            roles.type.label('_role_type'), user_role.id_record.label('_user_role_id'),
            user_role.gross_income.label('_gross_income')
        ).join(
            user_role, users.id_record == user_role.id_user
        ).join(
            roles, roles.id_record == user_role.id_role
        ).filter(
            user_role.status == True
        ).filter(
            roles.type != 'Administrador'
        ).order_by(
            users.lastname.asc(), users.name.asc()
        ).all())

        # return
        return rows

    # generating payroll calculation
    async def generating_payroll_calculations(
            self, db: Union[Session, object], users: list[object], schema: Union[dict, object]) -> dict:
        # variables
        employees = {
            "id_user_role": None, "payroll_amount": 0.0, "inability_amount": 0.0, "extra_hour_amount": 0.0,
            "holiday_amount": 0.0, "vacations_amount": 0.0, "gross_total_amount": 0.0, "payment_date": 221,
            "net_total_amount": 0.0, "payroll_id": None
        }

        # dates
        dates = schema["payroll_period"]

        for user in users:
            # calculate payroll amount
            payroll_amount = await self.calculating_payroll_amount(db=db, user=user, dates=dates)
            # skip
            if payroll_amount == 0.0: continue
            # update
            employees["id_user_role"] = user._user_role_id
            employees["payroll_amount"] = payroll_amount

            # calculate inability days
            inability_amount = await self.calculating_inability_amount(db=db, user=user, dates=dates)
            employees["inability_amount"] = inability_amount

            # calculate extra hours
            extra_hour_amount = await self.calculating_extra_hours_amount(db=db, user=user, dates=dates)
            employees["extra_hour_amount"] = extra_hour_amount

            # calculate holidays
            holiday_amount = await self.calculating_holiday_records(db=db, user=user, dates=dates)
            employees["holiday_amount"] = holiday_amount

            # calculate vacations
            vacations_amount = await self.calculating_vacations_records(db=db, user=user, dates=dates)
            employees["vacations_amount"] = vacations_amount

            # gross total amount
            await self.adding_up_gross_total(calculated_amounts=employees)

            # applying deductions
            taxes = await self.applying_deductions_to_payroll(db=db, prices=employees)

            # applying taxes
            await self.getting_tax_cut(gross=user._gross_income, tax=taxes)

            # registering information at db
            record = await self.registering_payroll_information(db=db, payroll=employees, tax=taxes)

        # return
        return employees

    # calculating payroll amount
    async def calculating_payroll_amount(
            self, db: Union[Session, object], user: object, dates: list[date]) -> float:
        # variables
        amount = 0.0
        # records
        records = await self.returning_checking_tracker_records(db=db, user=user, dates=dates)

        # skip records
        if not records:
            return amount

        for item in records:
            daily_salary = ((user._gross_income/2) / 15)
            salary_hour = (daily_salary / 8)
            salary_obtain = (salary_hour * item._hours)
            amount += float(salary_obtain)

        # return
        return round(amount, 2)

    async def returning_checking_tracker_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> list[object]:
        # extract start and end date
        start, end = dates[0], dates[1]

        rows = db.query(
            self.models.Checkin_Tracker.id_record.label('_id'),
            self.models.Checkin_Tracker.id_subject.label('_id_user'),
            self.models.Checkin_Tracker.hours.label('_hours'),
            self.models.Checkin_Tracker.log_date.label('_log_date'),
        ).filter(
            and_(
                self.models.Checkin_Tracker.id_subject == user._user_role_id,
                func.date(self.models.Checkin_Tracker.log_date).between(start, end)
            )
        ).order_by(
            self.models.Checkin_Tracker.log_date.asc()
        ).all()

        # return
        return rows or []

    # calculating inability amount
    async def calculating_inability_amount(
            self, db: Union[Session, object], user: object, dates: list[date]) -> float:
        # variables
        amount = 0.0
        # records
        records = await self.returning_inability_records(db=db, user=user, dates=dates)

        # skip records
        if not records:
            return amount

        for item in records:
            # counting days
            days = (item._end_date - item._start_date).days + 1

            if days > 3:
                return amount

            daily_salary = ((user._gross_income / 2) / 15)
            daily_salary_inability = (float(daily_salary) * 0.6)
            amount += float(daily_salary_inability)

        # return
        return round(amount, 2)

    async def returning_inability_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> list[object]:
        # extract start and end date
        start, end = dates[0], dates[1]

        rows = db.query(
            self.models.Inability.id_record.label('_id'),
            self.models.Inability.date_start.label('_start_date'),
            self.models.Inability.date_return.label('_end_date'),
            self.models.Inability.id_subject.label('id_subject'),
            self.models.Inability.status.label('_status'),
            self.models.Inability.log_date.label('_log_date'),
        ).filter(
            and_(
                self.models.Inability.id_subject == user._user_role_id,
                self.models.Inability.status == "Aprobado",
                # date range
                self.models.Inability.date_start >= start,
                self.models.Inability.date_start <= end,
            )
        ).order_by(
            self.models.Inability.date_start.asc()
        ).all()

        # return
        return rows or []

    # calculating extra hour amount
    async def calculating_extra_hours_amount(
            self, db: Union[Session, object], user: object, dates: list[date]) -> float:
        # variables
        amount = 0.0
        # records
        records = await self.returning_extra_hours_records(db=db, user=user, dates=dates)

        # skip records
        if not records:
            return amount

        for item in records:
            daily_salary = ((user._gross_income / 2) / 15)
            salary_hour = (daily_salary / 8)
            salary_obtain = float((salary_hour * item._hours)) * 1.5
            amount += float(salary_obtain)

        return round(amount, 2)

    async def returning_extra_hours_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> list[object]:
        # extract start and end date
        start, end = dates[0], dates[1]

        rows = db.query(
            self.models.Extra_Hour.id_record.label('_id'),
            self.models.Extra_Hour.id_subject.label('_id_user'),
            self.models.Extra_Hour.hours.label('_hours'),
            self.models.Extra_Hour.log_date.label('_log_date'),
        ).filter(
            and_(
                self.models.Extra_Hour.id_subject == user._user_role_id,
                func.date(self.models.Extra_Hour.log_date).between(start, end)
            )
        ).order_by(
            self.models.Extra_Hour.log_date.asc()
        ).all()

        # return
        return rows or []

    # calculating holiday amount
    async def calculating_holiday_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> float:
        # variables
        amount = 0.0
        # records
        records = await self.returning_holiday_records(db=db, user=user, dates=dates)

        # skip records
        if not records:
            return amount

        for item in records:
            daily_salary = ((user._gross_income / 2) / 15)
            salary_hour = (daily_salary / 8)
            salary_obtain = float((salary_hour * item._hours)) * 2
            amount += float(salary_obtain)

        return round(amount, 2)

    async def returning_holiday_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> list[object]:
        # extract start and end date
        start, end = dates[0], dates[1]
        # holiday calendar
        calendar = [(h.month, h.day) for h in self.cns.HOLIDAY_CALENDAR.value.values()]

        # dynamic filtering
        holiday_filter = [
            and_(
                func.extract('month', self.models.Checkin_Tracker.log_date) == month,
                func.extract('day', self.models.Checkin_Tracker.log_date) == day,
            )
            for month, day in calendar
        ]

        # query
        rows = db.query(
            self.models.Checkin_Tracker.id_record.label('_id'),
            self.models.Checkin_Tracker.id_subject.label('_id_user'),
            self.models.Checkin_Tracker.hours.label('_hours'),
            self.models.Checkin_Tracker.log_date.label('_log_date'),
        ).filter(
            and_(
                self.models.Checkin_Tracker.id_subject == user._user_role_id,
                func.date(self.models.Checkin_Tracker.log_date).between(start, end),
                or_(*holiday_filter),
            )
        ).order_by(
            self.models.Checkin_Tracker.log_date.asc()
        ).all()

        # return
        return rows or []

    # calculating vacations amount
    async def calculating_vacations_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> float:
        # variables
        amount = 0.0
        # records
        records = await self.returning_vacations_records(db=db, user=user, dates=dates)

        # skip records
        if not records:
            return amount

        for item in records:
            daily_salary = ((user._gross_income / 2) / 15)
            salary_hour = (daily_salary / 8)
            salary_obtain = float((salary_hour * 8))
            amount += float(salary_obtain)

        return round(amount, 2)

    async def returning_vacations_records(
            self, db: Union[Session, object], user: object, dates: list[date]) -> list[object]:
        # extract start and end date
        start, end = dates[0], dates[1]

        rows = db.query(
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.id_subject.label('_id_user'),
            self.models.Request_Vacation.status.label('_status'),
            self.models.Request_Vacation.log_date.label('_log_date'),
        ).filter(
            and_(
                self.models.Request_Vacation.id_subject == user._user_role_id,
                self.models.Request_Vacation.status == "Aprobado",
                func.date(self.models.Request_Vacation.log_date).between(start, end),
            )
        ).order_by(
            self.models.Request_Vacation.log_date.asc()
        ).all()

        # return
        return rows or []

    # adding up gross total amount
    async def adding_up_gross_total(self, calculated_amounts: dict) -> dict:
        # sum up values
        calculated_amounts["gross_total_amount"] = round((
                (calculated_amounts["payroll_amount"] + calculated_amounts["inability_amount"]) +
                calculated_amounts["extra_hour_amount"] + calculated_amounts["holiday_amount"] +
                calculated_amounts["vacations_amount"]), 2)

        # return
        return calculated_amounts

    # calculating tax cut
    async def getting_tax_cut(self, gross: Union[Decimal, float], tax: dict) -> None:
        # tax scale thresholds
        TAX_SCALE = {
            "Limit_1": 922000.0,
            "Limit_2": 1352000.0,
            "Limit_3": 2373000.0,
            "Limit_4": 4745000.0,
        }

        to_float = float(gross)
        rent_tax = 0.0

        # --- TAX BRACKETS LOGIC ---
        if to_float <= TAX_SCALE["Limit_1"]:
            rent_tax = 0.0
        elif to_float <= TAX_SCALE["Limit_2"]:
            rent_tax = (to_float - TAX_SCALE["Limit_1"]) * 0.10
        elif to_float <= TAX_SCALE["Limit_3"]:
            rent_tax = (TAX_SCALE["Limit_2"] - TAX_SCALE["Limit_1"]) * 0.10 + (to_float - TAX_SCALE["Limit_2"]) * 0.15
        elif to_float <= TAX_SCALE["Limit_4"]:
            rent_tax = (
                    (TAX_SCALE["Limit_2"] - TAX_SCALE["Limit_1"]) * 0.10
                    + (TAX_SCALE["Limit_3"] - TAX_SCALE["Limit_2"]) * 0.15
                    + (to_float - TAX_SCALE["Limit_3"]) * 0.20
            )
        else:
            rent_tax = (
                    (TAX_SCALE["Limit_2"] - TAX_SCALE["Limit_1"]) * 0.10
                    + (TAX_SCALE["Limit_3"] - TAX_SCALE["Limit_2"]) * 0.15
                    + (TAX_SCALE["Limit_4"] - TAX_SCALE["Limit_3"]) * 0.20
                    + (to_float - TAX_SCALE["Limit_4"]) * 0.25
            )

        # assign result
        tax["rent_tax"] = round(rent_tax, 2)

    # applying deductions
    async def applying_deductions_to_payroll(self, db: Union[Session, object], prices: dict) -> None:
        # tax records
        taxes = {"ccss_ivm": 0.0, "ccss_eme": 0.0, "rop": 0.0, "rent_tax": 0.0}
        # records
        records = await self.querying_deductions_book(db=db)

        for item in records:
            if item._id == 200:
                taxes["ccss_ivm"] = round((prices["gross_total_amount"] * item._percentage),2)

            elif item._id == 201:
                taxes["ccss_eme"] = round((prices["gross_total_amount"] * item._percentage),2)

            elif item._id == 202:
                taxes["rop"] = round((prices["gross_total_amount"] * item._percentage),2)

        # updating net amount
        prices["net_total_amount"] = prices["gross_total_amount"] - (
                taxes["ccss_ivm"] + taxes["ccss_eme"] + taxes["rop"] + taxes["rent_tax"])

        # return
        return taxes

    # query deductions records
    async def querying_deductions_book(self, db:Union[Session, object]) -> list[object]:
        # db query
        records = db.query(
            self.models.Deduction.id_record.label('_id'), self.models.Deduction.name.label('_name'),
            self.models.Deduction.percentage.label('_percentage')
        ).all()

        # return
        return records

    # register payroll information
    async def registering_payroll_information(self, db:Union[Session, object], payroll: dict, tax: dict) -> object:
        record = self.models.Payroll_User(
            net_amount=payroll["net_total_amount"],
            ccss_ivm=tax["ccss_ivm"],
            ccss_eme=tax["ccss_eme"],
            ccss_rop=tax["rop"],
            renta_tax=tax["rent_tax"],
            payroll_amount=payroll["payroll_amount"],
            extra_hour_amount=payroll["extra_hour_amount"],
            vacations_amount=payroll["vacations_amount"],
            holiday_amount=payroll["holiday_amount"],
            total_gross_amount=payroll["gross_total_amount"],
            id_user=payroll["id_user_role"],
            id_payment_date=payroll["payment_date"]
        )

        # db add
        db.add(instance=record)
        # db commit
        db.commit()
        # db refresh
        db.refresh(instance=record)

        # add to dict
        payroll["payroll_id"] = record.id_record

        # return
        return record

    # collecting recipient emails
    async def collecting_recipient_emails(
            self, db: Union[Session, object], id_payroll: Union[int, str]) -> list[str]:
        # aliases
        payroll = aliased(self.models.Payroll_User)
        user_role = aliased(self.models.User_Role)
        employee = aliased(self.models.User)

        # query
        rows = db.query(
            employee.email
        ).select_from(
            payroll
        ).join(
            user_role, user_role.id_record == payroll.id_user
        ).join(
            employee, employee.id_record == user_role.id_user
        ).filter(
            user_role.status.is_(True),
        ).distinct().all()

        # collect emails
        emails = [r[0] for r in rows]

        # return
        return emails or []

    # validating payroll periods
    async def validating_payroll_periods(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> None:
        # variables
        today = date.today()
        selected_period = schema["payroll_period"]
        start, end = selected_period[0], selected_period[1]

        # validate if selected period has not started
        if today < start:
            raise self.http_exec(
                self.status.HTTP_400_BAD_REQUEST,
                detail=f"El período seleccionado ({start} → {end}) aún no ha comenzado."
            )

        # query records
        records = db.query(
            self.models.Checkin_Tracker
        ).filter(
            func.date(self.models.Checkin_Tracker.log_date).between(start, end)
        ).count()

        if records == 0:
            raise self.http_exec(
                self.status.HTTP_404_NOT_FOUND,
                detail=f'No existen registros de asistencia para el período ({start} → {end}).')
