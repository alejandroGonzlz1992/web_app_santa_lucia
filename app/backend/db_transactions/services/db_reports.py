# import
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

    # querying checking tracker report
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
