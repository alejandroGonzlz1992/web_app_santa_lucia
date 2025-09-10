# import
from typing import Union

from pydantic import BaseModel
from fastapi import Form


# user login
class User_Login(BaseModel):
    email_login_field: str
    password_login_field: str

    @classmethod
    def formatting(
            cls, email_login_field: str = Form(...),
            password_login_field: str = Form(...)):
        # return
        return cls(
            email_login_field=email_login_field,
            password_login_field=password_login_field)


# token data
class Token_Data(BaseModel):
    user_role_id: Union[int, str]
    user_id: Union[int, str]
    role_id: Union[int, str]
    role_type: str

    # ignore "exp" from token encode portion
    class Config:
        extra = "ignore"


# restore password
class Restore_Password(BaseModel):
    user_identification: Union[str, int]
    temp_password_field: str
    new_password_field: str
    confirm_password_field: str

    @classmethod
    def formatting(
            cls, user_identification: Union[int, str] = Form(...), temp_password_field: str = Form(...),
            new_password_field: str = Form(...), confirm_password_field: str = Form(...)):

        # return
        return cls(user_identification=user_identification, temp_password_field=temp_password_field,
                   new_password_field=new_password_field, confirm_password_field=confirm_password_field)
