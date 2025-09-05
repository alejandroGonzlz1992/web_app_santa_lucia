# import
from pydantic import BaseModel
from fastapi import Form
from datetime import time, date
from typing import Union


# create schedule
class Create_Schedule(BaseModel):
    schedule_type: str
    schedule_start_time: time
    schedule_end_time: time
    schedule_total_hours: Union[int, str]
    schedule_create_date: date

    @classmethod
    def formatting(cls, schedule_type: str = Form(...), schedule_total_hours: Union[int, str] = Form(...),
                   schedule_start_time: time = Form(...), schedule_end_time: time = Form(...),
                   schedule_create_date: date = Form(...)):
        # return
        return cls(schedule_type=schedule_type, schedule_total_hours=schedule_total_hours,
                   schedule_start_time=schedule_start_time, schedule_end_time=schedule_end_time,
                   schedule_create_date=schedule_create_date)


# update schedule
class Update_Schedule(BaseModel):
    id: int
    schedule_type: str
    schedule_start_time: time
    schedule_end_time: time
    schedule_total_hours: Union[int, str]
    schedule_create_date: date
    method: str

    @classmethod
    def formatting(cls, id:int = Form(...), schedule_type: str = Form(...),
                   schedule_total_hours: Union[int, str] = Form(...), schedule_start_time: time = Form(...),
                   schedule_end_time: time = Form(...),schedule_create_date: date = Form(...),
                   method: str = Form(...)):
        # return
        return cls(id=id, schedule_type=schedule_type, schedule_total_hours=schedule_total_hours,
                   schedule_start_time=schedule_start_time, schedule_end_time=schedule_end_time,
                   schedule_create_date=schedule_create_date, method=method)
