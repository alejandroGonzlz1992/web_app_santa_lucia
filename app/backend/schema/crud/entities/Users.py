# import
from pydantic import BaseModel
from decimal import Decimal
from fastapi import Form
from datetime import date
from typing import Union


# create user
class Create_User(BaseModel):
    user_identification: str
    user_name: str
    user_lastname: str
    user_lastname2: str
    user_gender: str
    user_birthday: date
    user_marital_status: str
    user_children: Union[int, str]
    user_email: str
    user_phone: str
    user_role: Union[int, str]
    user_gross_income: Union[Decimal, float]
    user_create_date: date
    user_approver: Union[int, str]

    @classmethod
    def formatting(cls, user_identification: str = Form(...), user_name: str = Form(...), user_lastname: str = Form(...),
                   user_lastname2: str = Form(...), user_gender: str = Form(...), user_birthday: date = Form(...),
                   user_marital_status: str = Form(...), user_children: Union[int, str] = Form(...),
                   user_email: str = Form(...), user_role: Union[int, str] = Form(...),
                   user_phone: str = Form(...), user_gross_income: Union[Decimal, float] = Form(...),
                   user_create_date: date = Form(...), user_approver: Union[int, str] = Form(...)):
        # return
        return cls(user_identification=user_identification, user_name=user_name, user_lastname=user_lastname,
                   user_lastname2=user_lastname2, user_gender=user_gender, user_birthday=user_birthday,
                   user_marital_status=user_marital_status, user_children=user_children, user_email=user_email,
                   user_phone=user_phone, user_role=user_role, user_gross_income=user_gross_income,
                   user_create_date=user_create_date, user_approver=user_approver)


# update user
class Update_User(BaseModel):
    id: int
    user_identification: str
    user_name: str
    user_lastname: str
    user_lastname2: str
    user_gender: str
    user_birthday: date
    user_marital_status: str
    user_children: Union[int, str]
    user_email: str
    user_phone: str
    user_role: Union[int, str]
    user_gross_income: Union[Decimal, float]
    user_create_date: date
    user_approver: Union[int, str]
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), user_identification: str = Form(...), user_name: str = Form(...),
                   user_lastname: str = Form(...), user_lastname2: str = Form(...), user_gender: str = Form(...),
                   user_birthday: date = Form(...), user_marital_status: str = Form(...),
                   user_children: Union[int, str] = Form(...), user_email: str = Form(...),
                   user_phone: str = Form(...), user_role: Union[int, str] = Form(...),
                   user_gross_income: Union[Decimal, float] = Form(...), user_create_date: date = Form(...),
                   method: str = Form(...), user_approver: Union[int, str] = Form(...)):
        # return
        return cls(id=id, user_identification=user_identification, user_name=user_name, user_lastname=user_lastname,
                   user_lastname2=user_lastname2, user_gender=user_gender, user_birthday=user_birthday,
                   user_marital_status=user_marital_status, user_children=user_children, user_email=user_email,
                   user_phone=user_phone, user_role=user_role, user_gross_income=user_gross_income,
                   user_create_date=user_create_date, method=method, user_approver=user_approver)


# update user status
class User_Status(BaseModel):
    id: Union[int, str]
    user_status: bool
    termination_date: date

    @classmethod
    def formatting(cls, id: Union[int, str] = Form(...), user_status: bool = Form(...),
                   termination_date: date = Form(...)):
        # return
        return cls(id=id, user_status=user_status, termination_date=termination_date)
