# import
from pydantic import BaseModel
from fastapi import Form
from datetime import date


# create department
class Create_Department(BaseModel):
    department_name: str
    department_create_date: date

    @classmethod
    def formatting(cls, department_name: str = Form(...), department_create_date: date = Form(...)):
        # return
        return cls(department_name=department_name, department_create_date=department_create_date)


# update department
class Update_Department(BaseModel):
    id: int
    department_name: str
    department_create_date: date
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), department_name: str = Form(...), department_create_date: date = Form(...),
                   method: str = Form(...)):
        # return
        return cls(id=id, department_name=department_name, department_create_date=department_create_date,
                   method=method)
