# import
import string, random
from re import compile
from fastapi import HTTPException, status
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
