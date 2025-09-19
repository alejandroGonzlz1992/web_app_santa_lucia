# import
from pydantic import BaseModel
from fastapi import Form
from datetime import date
from typing import Union


# create inability
class Create_Inability(BaseModel):
    start_date: date
    return_date: date
    inability_number: Union[str, int]
    inability_detail: str

    @classmethod
    def formatting(cls, start_date: date = Form(...), return_date: date = Form(...),
                   inability_number: Union[str, int] = Form(...), inability_detail: str = Form(...)):
        # return
        return cls(start_date=start_date, return_date=return_date, inability_number=inability_number,
                   inability_detail=inability_detail)


# update inability
class Update_Inability(BaseModel):
    id: Union[int, str]
    inability_status_field: str

    @classmethod
    def formatting(cls, id: Union[str, int] = Form(...), inability_status_field: str = Form(...)):
        # return
        return cls(id=id, inability_status_field=inability_status_field)
