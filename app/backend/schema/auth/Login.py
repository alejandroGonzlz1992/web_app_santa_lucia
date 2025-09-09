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
