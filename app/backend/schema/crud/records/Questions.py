# import
from pydantic import BaseModel
from fastapi import Form
from typing import Union


# create evaluation question
class Create_Eval_Question(BaseModel):
    evaluation_type: Union[int, str]
    evaluation_question: str

    @classmethod
    def formatting(cls, evaluation_type: Union[int, str] = Form(...), evaluation_question: str = Form(...)):
        # return
        return cls(evaluation_type=evaluation_type, evaluation_question=evaluation_question)


# update evaluation question
class Update_Eval_Question(BaseModel):
    id: int
    evaluation_type: Union[int, str]
    evaluation_question: str
    method: str

    @classmethod
    def formatting(cls, id: int = Form(...), evaluation_type: Union[int, str] = Form(...), evaluation_question: str = Form(...),
                   method: str = Form(...)):
        # return
        return cls(id=id, evaluation_type=evaluation_type, evaluation_question=evaluation_question, method=method)


