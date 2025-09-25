# import
from pydantic import BaseModel
from fastapi import Form
from datetime import date


# role user schema
class Create_Report(BaseModel):
    report_name_field: str
    start_date_field: date
    end_date_field: date
    report_deliver: str

    @classmethod
    def formatting(
            cls, report_name_field: str = Form(...), start_date_field: date = Form(...),
            end_date_field: date = Form(...), report_deliver: str = Form(...)):
        return cls(
            report_name_field=report_name_field, start_date_field=start_date_field, end_date_field=end_date_field,
            report_deliver=report_deliver)
