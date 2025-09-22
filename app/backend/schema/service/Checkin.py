# import
from pydantic import BaseModel
from fastapi import Form
from datetime import time
from typing import Union


# create checkin tracker
class Create_Checkin_Tracker(BaseModel):
    checkin_value: time
    checkout_value: time
    hours_value: Union[int, str]

    @classmethod
    def formatting(cls, checkin_value: time = Form(...), checkout_value: time = Form(...),
                   hours_value: Union[int, str] = Form(...)):
        # return
        return cls(checkin_value=checkin_value, checkout_value=checkout_value, hours_value=hours_value)
