# import
import pandas, io
from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from datetime import datetime
from zoneinfo import ZoneInfo

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
        self.cr_time_now = datetime.now(ZoneInfo('America/Costa_Rica'))

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

    # loading new headers name
    async def new_headers_name_load(self, df: Union[pandas.DataFrame, object], name: str) -> pandas.DataFrame:
        mapping = self.cns.HEADERS.value
        df_2 = df.rename(columns=mapping.get(name, {}))
        # return
        return df_2

    # styling xlsx report headers
    async def styling_xlsx_report_headers(
            self, df: Union[pandas.DataFrame, object], name_report: str = "Reporte") -> bytes:
        # buffer in-memory var
        in_buffer = self.io.BytesIO()

        # style pd frame with context manager
        with self.pd.ExcelWriter(in_buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name=name_report)
            wb = writer.book
            ws = writer.sheets[name_report]

            # header formatting
            headers_format = wb.add_format({
                    "bold": True,
                    "align": "left",
                    "valign": "vcenter",
                    "bg_color": "#EEEEEE",
                    "bottom": 1
                })
            # cell formatting
            cell_format = wb.add_format({"align": "left", "valign": "top"})
            # date formatting
            date_format = wb.add_format({"align": "left", "valign": "vcenter", "num_format": "dd-mm-yyyy"})

            # rewrite headers with style
            for col_index, name in enumerate(df.columns):
                ws.write(0, col_index, name, headers_format)

            # auto-fit-ish widths + cell formats
            for col_index in range(df.shape[1]):
                col_name = df.columns[col_index]
                col_series = df.iloc[:, col_index]

                # max content length
                if not col_series.empty:
                    max_cell_length = int(col_series.dropna().astype(str).map(len).max() or 0)
                else:
                    max_cell_length = 0

                # width
                width = min(max(len(str(col_name)), max_cell_length) +2, 50)

                # format for dates
                if self.pd.api.types.is_datetime64_any_dtype(col_series):
                    ws.set_column(col_index, col_index, width, date_format)
                else:
                    ws.set_column(col_index, col_index, width, cell_format)

            ws.freeze_panes(1, 0)

        # return
        return in_buffer.getvalue()

    # downloadable file for browser
    async def downloadable_file_browser(
            self, df: Union[pandas.DataFrame, object], name: str) -> StreamingResponse:
        # add rename headers
        df = await self.new_headers_name_load(df=df, name=name)
        # xlsx file var
        xlsx_file = await self.styling_xlsx_report_headers(df=df)
        # file name
        file_name = f'reporte_{name}_{self.cr_time_now.strftime("%d_%m_%Y")}.xlsx'
        # return
        return self.response(
            self.io.BytesIO(xlsx_file),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"'},
        )

    # attachment for email delivery
    async def attachment_for_email_delivery(
            self, df: Union[pandas.DataFrame, object], name: str) -> dict:
        # add rename headers
        df = await self.new_headers_name_load(df=df, name=name)
        # xlsx file var
        xlsx_file = await self.styling_xlsx_report_headers(df=df)
        # file name
        file_name = f'reporte_{name}_{self.cr_time_now.strftime("%d_%m_%Y")}.xlsx'

        # return
        return {"report": xlsx_file, "name": file_name}

    # getting current recipient
    async def getting_current_recipient(self, db: Union[Session, object], id_session: Union[int, str]) -> str:
        # current record
        record = db.query(
            self.models.User.email.label('_email')
        ).select_from(
            self.models.User_Role
        ).join(
            self.models.User, self.models.User_Role.id_user == self.models.User.id_record
        ).filter(
            self.models.User_Role.id_record == id_session
        ).first()

        # return
        return record
