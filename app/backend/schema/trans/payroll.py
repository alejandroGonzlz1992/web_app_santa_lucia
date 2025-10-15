# import
from pydantic import BaseModel
from fastapi import Form
from decimal import Decimal
from typing import Union


# update payroll record
class Update_Payroll_Record(BaseModel):
    id: Union[int, str]
    ccss_ivm: Union[Decimal, float]
    ccss_eme: Union[Decimal, float]
    rop_popular: Union[Decimal, float]
    rent_tax: Union[Decimal, float]
    loan_request: Union[Decimal, float]
    child_support: Union[Decimal, float]
    association: Union[Decimal, float]
    other_deductions: Union[Decimal, float]
    payroll_details: str

    @classmethod
    def formatting(cls, id: Union[int, str] = Form(...), ccss_ivm: Union[Decimal, float] = Form(...),
                   ccss_eme: Union[Decimal, float] = Form(...), rop_popular: Union[Decimal, float] = Form(...),
                   rent_tax: Union[Decimal, float] = Form(...), loan_request: Union[Decimal, float] = Form(...),
                   child_support: Union[Decimal, float] = Form(...), association: Union[Decimal, float] = Form(...),
                   other_deductions: Union[Decimal, float] = Form(...), payroll_details: str = Form(...)
                   ):
        # return
        return cls(id=id, ccss_ivm=ccss_ivm, ccss_eme=ccss_eme, rop_popular=rop_popular, rent_tax=rent_tax,
                   loan_request=loan_request, child_support=child_support, association=association,
                   other_deductions=other_deductions, payroll_details=payroll_details)
