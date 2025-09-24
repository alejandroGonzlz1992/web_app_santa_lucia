# import
from pydantic import BaseModel
from fastapi import Form
from typing import Union


# profile contact info
class Create_Contact_Info(BaseModel):
    province_field: Union[int, str]
    canton_field: Union[int, str]
    district_field: Union[int, str]
    postal_code_field: Union[str, int]
    address_detail_field: str
    email_field: str
    phone_field: str

    @classmethod
    def formatting(cls, province_field: Union[int, str] = Form(...), canton_field: Union[int, str] = Form(...),
                   district_field: Union[int, str] = Form(...), postal_code_field: Union[str, int] = Form(...),
                   address_detail_field: str = Form(...), email_field: str = Form(...),
                   phone_field: str = Form(...)):
        # return
        return cls(province_field=province_field, canton_field=canton_field, district_field=district_field,
                   postal_code_field=postal_code_field, address_detail_field=address_detail_field,
                   email_field=email_field, phone_field=phone_field)


# profile password update
class Update_Password_Info(BaseModel):
    password_current_field: str
    new_password_field: str
    confirm_password_field: str

    @classmethod
    def formatting(cls, password_current_field: str = Form(...), new_password_field: str = Form(...),
                   confirm_password_field: str = Form(...)):
        # return
        return cls(password_current_field=password_current_field, new_password_field=new_password_field,
                   confirm_password_field=confirm_password_field)
