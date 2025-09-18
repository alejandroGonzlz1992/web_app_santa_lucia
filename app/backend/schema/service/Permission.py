# import
from pydantic import BaseModel, Field
from fastapi import Form, Depends
from typing import Union
from datetime import date


# create extra hours
class Create_Extra_Hours(BaseModel):
    hour_date_field: date
    hour_schedule_type: str
    hour_quantity_field: Union[int, str]

    @classmethod
    def formatting(cls, hour_date_field: date = Form(...), hour_schedule_type: str = Form(...),
                   hour_quantity_field: Union[int, str] = Form(...)):
        # return
        return cls(hour_date_field=hour_date_field,hour_schedule_type=hour_schedule_type,
                   hour_quantity_field=hour_quantity_field)


# create vacations
class Create_Vacations(BaseModel):
    request_vacation: str
    start_date_field: date
    end_date_field: date
    day_field_total: Union[int, str]

    @classmethod
    def formatting(cls, request_vacation: str = Form(...), start_date_field: date = Form(...),
                   end_date_field: date = Form(...), day_field_total: Union[int, str] = Form(...)):
        # return
        return cls(request_vacation=request_vacation, start_date_field=start_date_field,
                   end_date_field=end_date_field, day_field_total=day_field_total)


# update records
class Update_Request(BaseModel):
    id: Union[int, str]
    permission_status_field: str
    method: str

    @classmethod
    def formatting(cls, id: Union[int, str] = Form(...), permission_status_field: str = Form(...),
                   method: str = Form(...)):
        # return
        return cls(id=id, permission_status_field=permission_status_field, method=method)
