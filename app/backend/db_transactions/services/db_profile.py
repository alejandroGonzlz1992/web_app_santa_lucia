# import
from fastapi import HTTPException, status
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import verifying_hash_password, getting_password_to_hash


# class
class Profile_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns
        self.verify_hash = verifying_hash_password
        self.to_hash = getting_password_to_hash

    # querying province, canton, and districts
    async def querying_province_canton_and_districts(
            self, db: Union[Session, object]) -> dict[object]:

        # provinces
        all_province = db.query(
            self.models.Province.id_record.label('_prov_id'),
            self.models.Province.name.label('_prov_name'),
        ).all()
        province_return = [{"_prov_id": _prov_id, "_prov_name": _prov_name} for _prov_id, _prov_name in all_province]

        # cantons
        all_canton = db.query(
            self.models.Canton.id_record.label('_cant_id'),
            self.models.Canton.name.label('_cant_name'),
            self.models.Canton.id_province.label('_prov_id'),
        ).all()
        canton_return = [{"_cant_id": _cant_id, "_cant_name": _cant_name, "_prov_id": _prov_id}
                         for _cant_id, _cant_name, _prov_id in all_canton]

        # districts
        all_district = db.query(
            self.models.District.id_record.label('_dist_id'),
            self.models.District.name.label('_dist_name'),
            self.models.District.id_canton.label('_cant_id'),
        ).all()
        district_return = [{"_dist_id": _dist_id, "_dist_name": _dist_name, "_cant_id": _cant_id}
                         for _dist_id, _dist_name, _cant_id in all_district]

        # return
        return {"province": province_return, "canton": canton_return, "district": district_return}

    # registering / updating contact profile information
    async def registering_updating_contact_info(
            self, db: Union[Session, object], schema: Union[BaseModel, object], id_session: Union[int, str]
    ) -> None:

        # record
        record_address = db.query(
            self.models.Address
        ).filter(
            self.models.Address.id_user == id_session
        ).first()

        # if not record -> add | do not update email and phone
        if record_address is None:
            to_add = self.models.Address(
                details=schema['address_detail_field'].title(),
                postal_code=schema['postal_code_field'],
                id_district=schema['district_field'],
                id_user=id_session
            )
            # add to model
            db.add(instance=to_add)
            # commit
            db.commit()
            # refresh
            db.refresh(instance=to_add)

        else:
            # query user record
            user_record = db.query(
                self.models.User
            ).filter(
                self.models.User.id_record == id_session
            ).first()

            # if record -> update_
            record_address.details = schema['address_detail_field'].title()
            record_address.postal_code = schema['postal_code_field']
            record_address.id_district = schema['district_field']

            if user_record:
                user_record.email = schema['email_field']
                user_record.phone = schema['phone_field']

            # db commit
            db.commit()

    # updating password profile information
    async def updating_password_info(
            self, db: Union[Session, object], schema: Union[BaseModel, object], id_session: Union[int, str]
    ) -> None:
        # record
        record = db.query(
            self.models.User
        ).filter(
            self.models.User.id_record == id_session
        ).first()

        # verify current password
        if not self.verify_hash(plain=schema['password_current_field'], hash_password=record.password):
            raise self.http_exec(
                status_code=self.status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        # hash password
        to_hash = self.to_hash(password=schema['new_password_field'])
        # update record
        record.password = to_hash

        #db commit
        db.commit()

    # query user profile information: Address
    async def querying_profile_info_address(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # address records
        address = db.query(
            self.models.Province.name.label('_prov_name'),
            self.models.Canton.name.label('_cant_name'),
            self.models.District.name.label('_dist_name'),
            self.models.Address.details.label('_address_detail'),
            self.models.Address.postal_code.label('_postal_code')
        ).select_from(
            self.models.Province
        ).join(
            self.models.Address.district
        ).join(
            self.models.District.canton
        ).join(
            self.models.Canton.province
        ).filter(
            self.models.Address.id_user == id_session
        ).first()

        # return
        return address

    # query user user_role information: User/Role
    async def querying_user_role_profile_info(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # record
        record = (db.query(
            self.models.User.name.label('_name'),
            self.models.User.lastname.label('_lastname'),
            self.models.User.lastname2.label('_lastname2'),
            self.models.User.email.label('_email'),
            self.models.User.phone.label('_phone'),
            self.models.User.identification.label('_ident'),
            self.models.Role.name.label('_rol_name'),
            self.models.Role.type.label('_rol_type'),
            self.models.Department.name.label('_dept_name'),
            self.models.User_Role.hire_date.label('_hire_date')
        ).select_from(
            self.models.User_Role
        ).join(
            self.models.User, self.models.User.id_record == self.models.User_Role.id_user
        ).join(
            self.models.Role, self.models.Role.id_record == self.models.User_Role.id_role
        ).join(
            self.models.Department, self.models.Department.id_record == self.models.Role.id_department
        ).filter(
            self.models.User_Role.id_user == id_session
        ).first())

        # return
        return record

    # query vacations
    async def querying_vacations(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # record
        record = db.query(
            self.models.Vacation.available.label('_available'),
            self.models.Vacation.used_days.label('_used_days'),
            self.models.User_Role.hire_date.label('_hire_date')
        ).join(
            self.models.User_Role, self.models.Vacation.id_subject == self.models.User_Role.id_record
        ).filter(
            self.models.User_Role.id_record == id_session
        ).first()

        # return
        return record

    # query vacations requests
    async def querying_vacations_requests(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        rows = db.query(
            # vacations
            self.models.Request_Vacation.id_record.label('_id'),
            self.models.Request_Vacation.date_start.label('_start'),
            self.models.Request_Vacation.date_return.label('_end'),
            self.models.Request_Vacation.days.label('_days'),
            self.models.Request_Vacation.status.label('_status'),
            self.models.Request_Vacation.log_date.label('_log_date'),
            # subject
            subject.identification.label('_ident'),
            # approver
            approver.name.label('_aprv_name'),
            approver.lastname.label('_aprv_lastname'),
            approver.lastname2.label('_aprv_lastname2'),
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Request_Vacation.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).filter(
            sub_user_role.id_record == id_session
        ).all()

        # return
        return rows

    # query extra hours
    async def querying_extra_hours(
            self, db:Union[Session, object], id_session: Union[int, str]) -> object:
        # record
        extra_hours = aliased(self.models.Extra_Hour)
        extra_hours_request = aliased(self.models.Request_Extra_Hour)

        record = (db.query(
            extra_hours.hours.label('_hours'),
            extra_hours_request.hours.label('_pend_hours'),
            extra_hours_request.status.label('_status'),
            extra_hours_request.log_date.label('_log_date'),
        ).select_from(
            extra_hours
        ).join(
            extra_hours_request, extra_hours_request.id_subject == extra_hours.id_subject
        ).filter(
            extra_hours.id_subject == id_session
        ).first())

        # return
        return record

    # query extra hours requests
    async def querying_extra_hours_requests(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # aliases
        sub_user_role = aliased(self.models.User_Role)
        subject = aliased(self.models.User)
        approver = aliased(self.models.User)

        rows = db.query(
            # vacations
            self.models.Request_Extra_Hour.id_record.label('_id'),
            self.models.Request_Extra_Hour.date_request.label('_date_request'),
            self.models.Request_Extra_Hour.hours.label('_hours'),
            self.models.Request_Extra_Hour.type.label('_type'),
            self.models.Request_Extra_Hour.status.label('_status'),
            # subject
            subject.identification.label('_ident'),
            # approver
            approver.name.label('_aprv_name'),
            approver.lastname.label('_aprv_lastname'),
            approver.lastname2.label('_aprv_lastname2'),
        ).join(
            sub_user_role, sub_user_role.id_record == self.models.Request_Extra_Hour.id_subject
        ).join(
            subject, subject.id_record == sub_user_role.id_user
        ).join(
            approver, approver.id_record == sub_user_role.approver
        ).filter(
            sub_user_role.id_record == id_session
        ).all()

        # return
        return rows

    # counting extra hoursRechazado
    async def counting_extra_hours(
            self, rows: Union[list, list[object]]) -> dict:
        # counters
        approved: int = 0
        in_progress: int = 0
        reject: int = 0

        # traverse rows records
        for record in rows:
            if record._status == "Aprobado":
                approved += 1

            elif record._status == "En Proceso":
                in_progress += 1

            elif record._status == "Rechazado":
                reject += 1

        # return dict
        return {"approve": approved, "in_progress": in_progress, "reject": reject}

    # query user_hire date
    async def querying_user_hire_date(
            self, db: Union[Session, object], id_session: Union[int, str]) -> object:
        # record
        record = db.query(
            self.models.User_Role.hire_date.label('_hire_date'),
        ).filter(
            self.models.User_Role.id_record == id_session
        ).first()

        # return
        return record
