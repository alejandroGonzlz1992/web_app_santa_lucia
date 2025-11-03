# import
from pydantic import BaseModel
from fastapi import Form
from decimal import Decimal
from typing import Union


# generate settlement
class Generate_Settlement(BaseModel):
    settlement_employee: str
    settlement_type: str
    settlement_detail: str

    @classmethod
    def formatting(cls, settlement_employee: str = Form(...), settlement_type: str = Form(...),
                   settlement_detail: str = Form(...)):
        # return
        return cls(settlement_employee=settlement_employee, settlement_type=settlement_type,
                   settlement_detail=settlement_detail)


# update settlement record
class Update_Settlement_Record(BaseModel):
    id: Union[int, str]
    cesantia_amount: Union[Decimal, float]
    vacation_amount: Union[Decimal, float]
    bonus_amount: Union[Decimal, float]
    payroll_amount: Union[Decimal, float]
    settlement_type: str
    settlement_status: str
    settlement_details: str

    @classmethod
    def formatting(cls, id: Union[int, str] = Form(...), cesantia_amount: Union[Decimal, float] = Form(...),
                   vacation_amount: Union[Decimal, float] = Form(...), bonus_amount: Union[Decimal, float] = Form(...),
                   payroll_amount: Union[Decimal, float] = Form(...), settlement_type: str = Form(...),
                   settlement_status: str = Form(...), settlement_details: str = Form(...)):
        # return
        return cls(id=id, cesantia_amount=cesantia_amount, vacation_amount=vacation_amount, bonus_amount=bonus_amount,
                   payroll_amount=payroll_amount, settlement_type=settlement_type, settlement_status=settlement_status,
                   settlement_details=settlement_details)
