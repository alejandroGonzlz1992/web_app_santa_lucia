# import
import string, random
from re import compile
from fastapi import HTTPException, status
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session

from numpy.core.records import record
from sqlalchemy.orm import aliased
from sqlalchemy import or_

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# class
class Inability_Trans_Manager:

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

    # query inability records
    async def query_inability_records(self, db: object, id_session: Union[int, str]) -> object:
        # entity aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        rows = db.query(
            self.models.Inability.id_record.label('_id'),
            self.models.Inability.date_start.label('_start'),
            self.models.Inability.date_return.label('_return'),
            self.models.Inability.doc_number.label('_doc_number'),
            self.models.Inability.status.label('_status'),
            # subject info
            subject.id_record.label('_emp_id'),
            subject.name.label('_emp_name'),
            subject.lastname.label('_emp_lastname'),
            subject.lastname2.label('_emp_lastname2'),
            # approver info
            approver.id_record.label('_apr_id'),
            approver.name.label('_apr_name'),
            approver.lastname.label('_apr_lastname'),
            approver.lastname2.label('_apr_lastname2'),
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Inability.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
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
        return rows.order_by(self.models.Inability.id_record.desc()).all()

    # register new inability record
    async def register_new_inability_record(
            self, db: Union[Session, object], schema: Union[BaseModel, dict],
            file: Union[bytes, object], id_session: Union[int, str]) -> None:

        # temp model record
        to_add = self.models.Inability(
            date_start=schema["start_date"],
            date_return=schema["return_date"],
            details=schema["inability_detail"].capitalize(),
            document=file,
            doc_number=schema["inability_number"],
            id_subject=id_session
        )
        # add to db models
        db.add(instance=to_add)
        # commit
        db.commit()
        # refresh db models
        db.refresh(instance=to_add)

    # collect the subject and approver email
    async def collecting_subject_and_approver_email(
            self, db: Union[Session, object], id_session: Union[int, str],) -> object:
        # aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        rows = db.query(
            # subject
            subject.email.label('_sub_email'),
            approver.email.label('_apr_email')
        ).select_from(
            sub_user_role
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).filter(
            sub_user_role.id_user == id_session
        ).filter(
            sub_user_role.status.is_(True)
        ).first()

        # return
        return {"sub": rows._sub_email, "apr": rows._apr_email}

    # collecting inability
    async def current_inability_record(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        role_ = aliased(self.models.Role)
        depat = aliased(self.models.Department)

        rows = (db.query(
            # inability
            self.models.Inability.id_record.label('_id'),
            self.models.Inability.date_start.label('_start'),
            self.models.Inability.date_return.label('_return'),
            self.models.Inability.doc_number.label('_doc_number'),
            self.models.Inability.status.label('_status'),
            # subject
            subject.name.label('_emp_name'),
            subject.lastname.label("_emp_lastname"),
            subject.lastname2.label("_emp_lastname2")
        ).select_from(
            self.models.Inability
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Inability.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).filter(
            sub_user_role.id_record == id_session
        ).first())

        # return
        return rows

    # update inability status
    async def updating_inability_status(
            self, db: Union[Session, object], schema: Union[BaseModel, dict]) -> None:
        # record
        row = db.query(
            self.models.Inability
        ).filter(
            self.models.Inability.id_record == int(schema["id"])
        ).first()

        if row:
            row.status = schema["inability_status_field"]

            # db commit
            db.commit()

    # query inability record details
    async def querying_inability_record_details(
            self, db: Union[Session, object], id: Union[int, str]) -> object:
        # aliases
        ur_ = aliased(self.models.User_Role)
        subj_ = aliased(self.models.User)
        role_ = aliased(self.models.Role)
        dept_ = aliased(self.models.Department)

        rows = db.query(
            # inability
            self.models.Inability.id_record.label('_id'),
            self.models.Inability.date_start.label('_start'),
            self.models.Inability.date_return.label('_return'),
            self.models.Inability.doc_number.label('_doc_number'),
            self.models.Inability.status.label('_status'),
            self.models.Inability.details.label('_details'),
            # subject
            subj_.name.label('_emp_name'),
            subj_.lastname.label('_emp_lastname'),
            subj_.lastname2.label('_emp_lastname2'),
            # role and depart
            role_.name.label('_role_name'),
            role_.type.label('_role_type'),
            dept_.name.label('_depart_name')
        ).select_from(
            self.models.Inability
        ).join(
            ur_, ur_.id_record == self.models.Inability.id_subject
        ).join(
            subj_, subj_.id_record == ur_.id_user
        ).join(
            role_, role_.id_record == ur_.id_role
        ).join(
            dept_, dept_.id_record == role_.id_department
        ).filter(
            self.models.Inability.id_record == int(id)
        ).first()

        # return
        return rows

    # query inability record for file
    async def querying_inability_file_record(
            self, db: Union[Session, object], id: Union[int, str]) -> dict:
        # file
        record_file = db.query(
            self.models.Inability.document.label('_document'),
            self.models.Inability.doc_number.label('_doc_number'),
        ).filter(
            self.models.Inability.id_record == int(id)
        ).first()

        # file name
        f_name = f'Incapacidad_boleta_{record_file._doc_number}.pdf'

        # return
        return {"file": record_file._document, "name": f_name}

