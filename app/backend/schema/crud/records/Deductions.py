# import
from pydantic import BaseModel
from fastapi import Form
from datetime import date


# create deduction
class Create_Deduction(BaseModel):
    deduction_name: str
    deduction_percentage: float
    deduction_create_date: date

    @classmethod
    def formatting(cls, deduction_name: str = Form(...), deduction_percentage: float = Form(...),
                   deduction_create_date: date = Form(...)):
        # return
        return cls(deduction_name=deduction_name, deduction_percentage=deduction_percentage,
                   deduction_create_date=deduction_create_date)


# update deduction
class Update_Deduction(BaseModel):
    id: int
    deduction_name: str
    deduction_percentage: float
    deduction_create_date: date
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), deduction_name: str = Form(...), deduction_percentage: float = Form(...),
                   deduction_create_date: date = Form(...), method: str = Form(...)):
        # return
        return cls(id=id, deduction_name=deduction_name, deduction_percentage=deduction_percentage,
                   deduction_create_date=deduction_create_date, method=method)
