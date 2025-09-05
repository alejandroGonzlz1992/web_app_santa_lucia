# import
from pydantic import BaseModel, model_validator
from fastapi import Form
from datetime import date
from typing import Optional


# create payment date
class Create_Payment_Date(BaseModel):
    payment_frecuency: str
    payment_date: date
    payment2_date: Optional[date] = None

    @classmethod
    def formatting(cls, payment_frecuency: str = Form(...), payment_date: date = Form(...),
                   payment2_date: Optional[date] = Form(None)):
        # return
        return cls(payment_frecuency=payment_frecuency, payment_date=payment_date, payment2_date=payment2_date)

    @model_validator(mode="after")
    def _enforce_mensual_rule(self):
        freq = (self.payment_frecuency or "").strip().lower()
        if freq == "mensual":
            self.payment2_date = self.payment_date
        return self


# update payment date
class Update_Payment_Date(BaseModel):
    id: int
    payment_frecuency: str
    payment_date: date
    payment2_date: Optional[date] = None
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), payment_frecuency: str = Form(...), payment_date: date = Form(...),
                   payment2_date: Optional[date] = Form(None), method: str = Form(...)):
        # return
        return cls(id=id, payment_frecuency=payment_frecuency, payment_date=payment_date,
                   payment2_date=payment2_date, method=method)

    @model_validator(mode="after")
    def _enforce_mensual_rule(self):
        freq = (self.payment_frecuency or "").strip().lower()
        if freq == "mensual":
            self.payment2_date = self.payment_date
        return self
