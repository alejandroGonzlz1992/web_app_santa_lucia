# import
from pydantic import BaseModel, field_validator
from fastapi import Form
from decimal import Decimal
from typing import Union
from datetime import date
from re import findall


# generate bonus
class Generate_Bonus_Record(BaseModel):
    bonus_period: Union[list[date], list[str]]

    @field_validator('bonus_period')
    def parsing_dates(cls, value):
        # if values are datetime already
        if isinstance(value, list) and all(isinstance(v, date) for v in value):
            return value

        # cast from str to date
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            text = value[0]
            matches = findall(r"datetime\.date\((\d+),\s*(\d+),\s*(\d+)\)", text)
            if matches:
                return [date(int(y), int(m), int(d)) for y, m, d in matches]

        return None

    @classmethod
    def formatting(cls, bonus_period: Union[list[date], list[str]] = Form(...)):
        # return
        return cls(bonus_period=bonus_period)


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
