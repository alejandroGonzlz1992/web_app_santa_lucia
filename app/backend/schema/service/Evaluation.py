# import
from pydantic import BaseModel, Field
from fastapi import Form, Depends
from typing import Union

# local import
from app.backend.db_transactions.services.db_services import Service_Trans_Manager


# instance
trans = Service_Trans_Manager()


# create evaluation
class Create_Evaluation(BaseModel):
    evaluation_user_name_field: str
    evaluation_type: str
    ratings: dict[int, int] = Field(..., description='Mapped question_id -> selected score')
    evaluation_detail: str

    @classmethod
    def formatting(cls, evaluation_user_name_field: str = Form(...), evaluation_type: str = Form(...),
                   ratings: dict[int, int] = Depends(trans.parsing_evaluation_details),
                   evaluation_detail: str = Form(...)):
        # return
        return cls(evaluation_user_name_field=evaluation_user_name_field, evaluation_type=evaluation_type,
                   ratings=ratings, evaluation_detail=evaluation_detail)


# enable evaluation
class Enable_Evaluation(BaseModel):
    evaluation_type: Union[int, str]
    confirm_switch_field: Union[bool, str]

    @classmethod
    def formatting(cls, evaluation_type: Union[int, str] = Form(...),
                   confirm_switch_field: Union[bool, str] = Form(...)):
        # return
        return cls(evaluation_type=evaluation_type, confirm_switch_field=confirm_switch_field)
