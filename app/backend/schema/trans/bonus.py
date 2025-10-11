# import
from pydantic import BaseModel
from fastapi import Form
from decimal import Decimal
from typing import Union
from datetime import date


# update bonus record
class Update_Bonus_Record(BaseModel):
    id: Union[int, str]
    bonus_month: str
    bonus_year: Union[str, int]
    bonus_amount: Union[Decimal, float]
    bonus_update_date: date

    @classmethod
    def formatting(cls, id: Union[int, str] = Form(...), bonus_month: str = Form(...),
                   bonus_year: Union[str, int] = Form(...), bonus_amount: Union[Decimal, float] = Form(...),
                   bonus_update_date: date = Form(...)):
        # return
        return cls(id=id, bonus_month=bonus_month, bonus_year=bonus_year, bonus_amount=bonus_amount,
                   bonus_update_date=bonus_update_date)
