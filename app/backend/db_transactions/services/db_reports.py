# import
import pandas, io
from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# class
class Reports_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.cns = Cns
        self.pd = pandas
        self.io = io
        self.response = StreamingResponse

    # querying checking tracker records report
    async def querying_checking_tracker_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # tracker
            self.models.Checkin_Tracker.id_record.label('_id'),
            self.models.Checkin_Tracker.start_hour.label('_start_hour'),
            self.models.Checkin_Tracker.end_hour.label('_end_hour'),
            self.models.Checkin_Tracker.hours.label('_hours'),
            self.models.Checkin_Tracker.status.label('_status'),
            self.models.Checkin_Tracker.status.label('_log_date'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Checkin_Tracker
        ).join(sub_user_role, self.models.Checkin_Tracker.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Checkin_Tracker.log_date >= schema["start_date_field"],
            self.models.Checkin_Tracker.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Checkin_Tracker.log_date.desc(),
            self.models.Checkin_Tracker.id_record.desc(),
        ).all()

        # records
        return records

    # querying inability records report
    async def querying_inability_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # inability
            self.models.Inability.id_record.label('_id'),
            self.models.Inability.date_start.label('_date_start'),
            self.models.Inability.date_return.label('_date_return'),
            self.models.Inability.details.label('_details'),
            self.models.Inability.doc_number.label('_doc_number'),
            self.models.Inability.status.label('_status'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Inability
        ).join(sub_user_role, self.models.Inability.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Inability.log_date >= schema["start_date_field"],
            self.models.Inability.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Inability.log_date.desc(),
            self.models.Inability.id_record.desc(),
        ).all()

        # records
        return records

    # querying settlement records report
    async def querying_settlement_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # inability
            self.models.Settlement.id_record.label('_id'),
            self.models.Settlement.total_amount.label('_total_amount'),
            self.models.Settlement.status.label('_status'),
            self.models.Settlement.type.label('_type'),
            self.models.Settlement.details.label('_details'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Settlement
        ).join(sub_user_role, self.models.Settlement.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Settlement.log_date >= schema["start_date_field"],
            self.models.Settlement.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Settlement.log_date.desc(),
            self.models.Settlement.id_record.desc(),
        ).all()

        # records
        return records

    # querying extra hours records report
    async def querying_extra_hours_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # inability
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.type.label('_type'),
            self.models.Request_Extra_Hour.status.label('_status'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Request_Extra_Hour
        ).join(sub_user_role, self.models.Request_Extra_Hour.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Request_Extra_Hour.log_date >= schema["start_date_field"],
            self.models.Request_Extra_Hour.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Request_Extra_Hour.log_date.desc(),
            self.models.Request_Extra_Hour.id_record.desc(),
        ).all()

        # records
        return records

    # querying bonus records report
    async def querying_bonus_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # inability
            self.models.Bonus.id_record.label('_id'),
            self.models.Bonus.total_amount.label('_total_amount'),
            self.models.Bonus.month_amount.label('_month_amount'),
            self.models.Bonus.month.label('_month'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Bonus
        ).join(sub_user_role, self.models.Bonus.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Bonus.log_date >= schema["start_date_field"],
            self.models.Bonus.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Bonus.log_date.desc(),
            self.models.Bonus.id_record.desc(),
        ).all()

        # records
        return records

    # querying vacations records report
    async def querying_vacations_report(
            self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # alias -> user_role
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        subj_role = aliased(self.models.Role)
        subj_depart = aliased(self.models.Department)

        apr_user_role = aliased(self.models.User_Role)
        approver = aliased(self.models.User)
        apr_role = aliased(self.models.Role)
        apr_depart = aliased(self.models.Department)

        records = db.query(
            # inability
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.days.label('_days'),
            self.models.Request_Vacation.date_start.label('_date_start'),
            self.models.Request_Vacation.date_return.label('_date_return'),
            self.models.Request_Vacation.type.label('_type'),
            self.models.Request_Vacation.status.label('_status'),
            # subject
            subject.identification.label('_subj_ident'),
            subject.name.label('_subj_name'),
            subject.lastname.label('_subj_lastname'),
            subject.lastname2.label('_subj_lastname2'),
            subject.email.label('_subj_email'),
            # subject role/department
            subj_depart.name.label('_subj_dept_name'),
            subj_role.name.label('_subj_role_name'),
            subj_role.type.label('_subj_role_type'),
            # approver
            approver.identification.label('_apr_ident'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
            approver.email.label('_apr_email'),
            # apr_depart role/department
            apr_depart.name.label('_apr_dept_name'),
            apr_role.name.label('_apr_role_name'),
            apr_role.type.label('_apr_role_type'),
        ).select_from(
            self.models.Request_Vacation
        ).join(sub_user_role, self.models.Request_Vacation.id_subject == sub_user_role.id_record
        ).join(subject, sub_user_role.id_user == subject.id_record
        ).join(subj_role, sub_user_role.id_role == subj_role.id_record
        ).join(subj_depart, subj_role.id_department == subj_depart.id_record
        ).outerjoin(approver, sub_user_role.approver == approver.id_record
        ).outerjoin(apr_user_role, apr_user_role.id_user == approver.id_record
        ).outerjoin(apr_role, apr_user_role.id_role == apr_role.id_record
        ).outerjoin(apr_depart, apr_role.id_department == apr_depart.id_record
        ).filter(
            self.models.Request_Vacation.log_date >= schema["start_date_field"],
            self.models.Request_Vacation.log_date <= schema["end_date_field"],
        ).order_by(
            self.models.Request_Vacation.log_date.desc(),
            self.models.Request_Vacation.id_record.desc(),
        ).all()

        # records
        return records

    # generating pandas dataframe
    async def generate_dataframe(self, report: object) -> object:
        # rename headers

        # return
        return self.pd.DataFrame([dict(r._mapping) for r in report])

    # query reports manager
    async def reports_query_manager(self, db: Union[Session, object], schema: Union[BaseModel, object]) -> list[object]:
        # report
        record, to_return = "", ""

        if schema["report_name_field"] == "registro_marcas":
            record = await self.querying_checking_tracker_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)


        elif schema["report_name_field"] == "incapacidades":
            record = await self.querying_inability_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)

        elif schema["report_name_field"] == "liquidaciones":
            record = await self.querying_settlement_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)

        elif schema["report_name_field"] == "registro_horas_extra":
            record = await self.querying_extra_hours_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)

        elif schema["report_name_field"] == "aguinaldos":
            record = await self.querying_bonus_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)

        elif schema["report_name_field"] == "registro_vacaciones":
            record = await self.querying_vacations_report(db=db, schema=schema)
            to_return = await self.generate_dataframe(report=record)

        # return
        return to_return

    # downloadable file for browser
    async def downloadable_file_browser(
            self, df: Union[pandas.DataFrame, object], name: str) -> StreamingResponse:
        # to csv
        to_csv = df.to_csv(index=False).encode("utf-8-sig")
        return self.response(
            self.io.BytesIO(to_csv), media_type="text/csv", headers={
                "Content-Disposition": f'attachment; filename="Reporte_{name}.csv"'
            }
        )
