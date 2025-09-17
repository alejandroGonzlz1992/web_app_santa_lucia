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
