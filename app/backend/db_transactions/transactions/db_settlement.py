# import
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from fastapi import HTTPException, status
from typing import Union
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, and_, func
from pathlib import Path
from tempfile import TemporaryDirectory
from docxtpl import DocxTemplate
from datetime import date
import subprocess
import shutil

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
        self.temp_dir = TemporaryDirectory()
        self.sub_process = subprocess
        self.shutil = shutil
        self.docx = DocxTemplate

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
            self, db: Union[Session, object], id_login: Union[int, str]) -> object:
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
            self.models.Settlement.id_record.label('_id'),
            self.models.Settlement.log_date.label('_log_date'),
            self.models.Settlement.type.label('_type'),
            self.models.Settlement.total_amount.label('_total_amount'),
            self.models.Settlement.status.label('_status'),
            # subject info
            subject.identification.label('_subj_ident'),
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
            self.models.Settlement
        ).join(
            # subject user-role relationship
            subj_user_role, subj_user_role.id_record == self.models.Settlement.id_subject
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
            "records": records.order_by(self.models.Settlement.id_record.desc()).all(),
            "logged_in": current_logged_in
        }

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
            self.models.Settlement.pre_check.label('_precheck_amount'),
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
        await Settlement_Trans_Manager.manage_libreoffice_suffixes(
            to_pdf=fill_pdf, temp=temp_dir, context=self.temp_dir, name=out_stem)

        # return
        return fill_pdf

    # fetching information from query
    async def fetching_query_rows_into_dict(self, record: list, today_: date) -> dict:
        # map record names into dict keys
        to_copy = self.cns.SETTLE_QUERY_CONTEXT.value.copy()
        # fetch info
        to_copy["name"] = record._emp_name
        to_copy["lastname"] = record._emp_lastname
        to_copy["lastname2"] = record._emp_lastname2
        to_copy["current_date"] = await Settlement_Trans_Manager.formatting_date_to_crc_time(value=today_)
        to_copy["identification"] = record._ident
        to_copy["settlement_id"] = record._id
        to_copy["termination_date"] = await Settlement_Trans_Manager.formatting_date_to_crc_time(
            value=record._termination_date)
        to_copy["jf_name"] = record._apr_name
        to_copy["jf_lastname"] = record._apr_lastname
        to_copy["jf_lastname2"] = record._apr_lastname2
        to_copy["status"] = record._status
        to_copy["settlement_type"] = record._type
        to_copy["total_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._total_amount)
        to_copy["payroll_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._payroll_amount)
        to_copy["cesantia_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._cesantia_amount)
        to_copy["vacations_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._vacations_amount)
        to_copy["bonus_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._bonus_amount)
        to_copy["precheck_amount"] = await Settlement_Trans_Manager.formatting_crc_money_style(
            value=record._precheck_amount)
        to_copy["settlement_details"] = record._details

        # return
        return to_copy

    # query specific users for settlement calculation
    async def querying_specific_users_for_settle_calculation(self, db: Union[Session, object]) -> list[object]:
        # query records
        records = db.query(
            self.models.User_Role.id_record.label('_id_user_role'), self.models.User.name.label('_emp_name'),
            self.models.User.lastname.label('_emp_lastname'), self.models.User.lastname2.label('_emp_lastname2'),
            self.models.Role.type.label('_role_type')
        ).join(
            self.models.User, self.models.User.id_record == self.models.User_Role.id_user
        ).join(
            self.models.Role, self.models.Role.id_record == self.models.User_Role.id_role
        ).filter(
            and_(self.models.User_Role.status.is_(True), self.models.Role.type != "Administrador")
        ).order_by(
            self.models.User_Role.id_record.asc()
        ).all()

        # return
        return records

    # validating settlement periods
    async def validating_settlement_user_payroll(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> None:

        # validate previous month records
        records = db.query(
            self.models.Payroll_User
        ).filter(
            self.models.Payroll_User.id_user == schema["settlement_employee"]
        ).count()

        if records < 4:
            raise self.http_exec(
                self.status.HTTP_404_NOT_FOUND,
                detail=f'El empleado seleccionado no cuenta con el mínimo de 4 registros de planilla '
                       f'requeridos para calcular la liquidación. Registros actuales: {records}.')

    # update settlement record
    async def updating_settlement_record(self, db: Union[Session, object], schema: Union[BaseModel, object]) -> None:
        # query record
        record = db.query(
            self.models.Settlement
        ).filter(
            self.models.Settlement.id_record == schema["id"]
        ).first()

        # update
        if record:
            record.cesantia = schema["cesantia_amount"]
            record.vacations = schema["vacation_amount"]
            record.bonus = schema["bonus_amount"]
            record.payroll = schema["payroll_amount"]
            record.type = schema["settlement_type"]
            record.status = schema["settlement_status"]
            record.details = schema["settlement_details"].title()

            # commit
            db.commit()

    # generate settlement amount
    async def generate_settlement_amount(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # variables
        record = {
            "id_user_role": None, "total_amount": 0.0, "cesantia_amount": 0.0, "vacations_amount": 0.0,
            "bonus_amount": 0.0, "payroll_amount": 0.0, "pre_check_amount": 0.0, "status": None, "type": None,
            "details": None
        }

        # query employee payroll records
        payroll = await self.querying_employee_salary_info(db=db, schema=schema)
        # counting records
        counting = await self.counting_payment_periods(db=db, schema=schema)
        # avg
        avg_payment = await self.avg_monthly_and_daily_payments(payrolls=payroll, periods=counting)

        # vacations
        vacations = await self.calculate_vacation_amount(db=db, schema=schema, spd=avg_payment["avg_daily"])
        record["vacations_amount"] = vacations

        # bonus and last payroll
        bonus_last_payroll = await Settlement_Trans_Manager.calculate_bonus_amount(payroll=payroll, periods=counting)
        record["bonus_amount"] = bonus_last_payroll["bonus"]
        record["payroll_amount"] = bonus_last_payroll["latest_payment"]

        if schema["settlement_type"] == "Responsabilidad Patronal":
            # cesantia
            days_work = await Settlement_Trans_Manager.counting_employee_worked_days(payrolls=payroll)
            # convert to month
            months_work = days_work / 30
            # days to pay
            days_to_pay = await self.get_cesantia_days(month_worked=months_work)
            # amount
            cesantia_amount = round(float(avg_payment["avg_daily"]) * days_to_pay, 2)
            # record
            record["cesantia_amount"] = cesantia_amount
            # settlement total
            record["total_amount"] = round(
                (vacations + bonus_last_payroll["bonus"] + bonus_last_payroll["latest_payment"] + cesantia_amount), 2)
        else:
            # settlement total
            record["total_amount"] = round(
                (vacations + bonus_last_payroll["bonus"] + bonus_last_payroll["latest_payment"]), 2)

        # adding schema to records
        record["id_user_role"] = schema["settlement_employee"]
        record["type"] = schema["settlement_type"]
        record["status"] = "Procesado"
        record["details"] = schema["settlement_detail"]

        # return
        return record

    # query salary information
    async def querying_employee_salary_info(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:

        # query all users payrolls
        payrolls = db.query(
            self.models.Payroll_User.id_user.label('_id_user_role'),
            self.models.Payroll_User.total_gross_amount.label('_gross_amount'),
            self.models.Payroll_User.net_amount.label('_net_amount'),
            self.models.Payroll_User.payment_period.label('_period')
        ).filter(
            self.models.Payroll_User.id_user == schema["settlement_employee"]
        ).order_by(
            self.models.Payroll_User.payment_period.desc()
        ).all()

        # return
        return payrolls

    # counting total payment months (records on payroll * 0.5)
    async def counting_payment_periods(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> int:
        records = db.query(
            self.models.Payroll_User
        ).filter(
            self.models.Payroll_User.id_user == schema["settlement_employee"]
        ).count()

        return records

    # avg payroll monthly avg payroll daily
    async def avg_monthly_and_daily_payments(
            self, payrolls: list[object], periods: int) -> dict:

        # total gross
        total_gross = sum([num._gross_amount for num in payrolls])
        # avg monthly
        avg_monthly = round(float(total_gross) / float((periods * 0.5)), 2)
        # avg daily
        avg_daily = round(float(avg_monthly) / 30, 2)

        # return
        return {"avg_month": avg_monthly, "avg_daily": avg_daily}

    # count total vacation days as available
    async def calculate_vacation_amount(
            self, db: Union[Session, object], schema: Union[BaseModel, object], spd: Union[float, int]) -> float:
        #
        vacations = db.query(
            func.coalesce(
                func.sum(self.models.Vacation.available), 0)
        ).filter(
            self.models.Vacation.id_subject == schema["settlement_employee"]
        ).scalar()

        if vacations:
            # calculate amount
            amount = round(float(vacations) * spd, 2)
        else:
            amount = 0.0

        # return
        return amount

    # sum up all gross_amount (payroll table) and divided by 12
    @staticmethod
    async def calculate_bonus_amount(payroll: list[object], periods: Union[int, float]) -> float:

        payments = [num._gross_amount for num in payroll]
        latest_payment = round(float(payments[0]), 2)
        total_bonus = round(float(sum(payments[1::])), 2)
        # bonus
        bonus = round((latest_payment + total_bonus) / periods, 2)

        # return
        return {"bonus": bonus, "latest_payment": latest_payment}

    # getting worked days
    async def get_cesantia_days(self, month_worked: Union[float, int]) -> float:
        for min_month, max_month, days in self.cns.CESANTIA_DAYS.value:
            if month_worked >= min_month and month_worked < max_month:
                return days

        # default
        return 0.0

    # count total labored days (count days from first quincena until the lastone in Payroll table)
    @staticmethod
    async def counting_employee_worked_days(payrolls: list[object]) -> int:
        # edge case
        if not payrolls: return 0

        # collect periods
        periods = [row._period for row in payrolls]
        # old and new payroll date
        first_date, last_date = min(periods), max(periods)

        # difference in days (inclusive)
        days_worked = (last_date - first_date).days + 1

        # return
        return days_worked

    # sum up all these value to obtain total amount settlement
    @staticmethod
    async def getting_settlement_total(values: Union[dict, object]) -> float:
        pass

    # register information on settlement table.
    async def register_settlement_info(self, db: Union[Session, object], record: dict) -> None:
        # settlement 
        new_settlement = self.models.Settlement(
            total_amount=record["total_amount"],
            cesantia=record["cesantia_amount"],
            vacations=record["vacations_amount"],
            bonus=record["bonus_amount"],
            payroll=record["payroll_amount"],
            status=record["status"],
            type=record["type"],
            details=record["details"],
            id_subject=record["id_user_role"]
        )

        # add
        db.add(instance=new_settlement)
        # commit
        db.commit()
        # refresh
        db.refresh(instance=new_settlement)
