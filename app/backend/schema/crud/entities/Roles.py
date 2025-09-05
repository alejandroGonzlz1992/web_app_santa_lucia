# import
from pydantic import BaseModel
from fastapi import Form
from datetime import date
from typing import Union


# create role
class Create_Role(BaseModel):
    role_name: str
    role_type: str
    role_department: Union[int, str]
    role_schedule: Union[int, str]
    role_create_date: date

    @classmethod
    def formatting(cls, role_name: str = Form(...), role_type: str = Form(...),
                   role_department: Union[int, str] = Form(...), role_schedule: Union[int, str] = Form(...),
                   role_create_date: date = Form(...)):
        # return
        return cls(role_name=role_name, role_type=role_type, role_department=role_department,
                   role_schedule=role_schedule, role_create_date=role_create_date)


# update role
class Update_Role(BaseModel):
    id: int
    role_name: str
    role_type: str
    role_department: Union[int, str]
    role_schedule: Union[int, str]
    role_create_date: date
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), role_name: str = Form(...), role_type: str = Form(...),
                   role_department: Union[int, str] = Form(...), role_schedule: Union[int, str] = Form(...),
                   role_create_date: date = Form(...), method: str = Form(...)):
        # return
        return cls(id=id, role_name=role_name, role_type=role_type, role_department=role_department,
                   role_schedule=role_schedule, role_create_date=role_create_date, method=method)
