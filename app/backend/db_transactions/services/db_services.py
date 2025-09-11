# import
import string, random
from re import compile
from fastapi import HTTPException, status, Request
from logging import getLogger
from typing import Union, Dict

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# logger
logger = getLogger(__name__)


# class
class Service_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.logger = logger
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns
        self.regex_ratings = compile(r"^ratings\[(\d+)\]$")

    # logger messages
    async def logger_sql_alchemy_error(self, exception: Union[object, str]) -> None:
        self.logger.error(f'SQLAlchemyError: {str(exception)}')
        if hasattr(exception, 'orig'):
            self.logger.error(f'Original error: {exception.orig}')

    async def logger_sql_alchemy_ops_error(self, exception: Union[object, str]) -> None:
        self.logger.error(f'Operational Error: {str(exception)}')
        self.logger.error(f'Statement: {getattr(exception, "statement", None)}')
        self.logger.error(f'Params: {getattr(exception, "params", None)}')
        if hasattr(exception, 'orig'):
            self.logger.error(f'Original error: {exception.orig}')
            if hasattr(exception.orig, 'pgcode'):
                self.logger.error(f'PostgreSQL error code: {exception.orig.pgcode}')
            if hasattr(exception.orig, 'pgerror'):
                self.logger.error(f'PostgreSQL error message: {exception.orig.pgerror}')

    # query evaluation status and type of evaluation employee
    async def query_evaluation_type_and_status_employee(self, db: object) -> object:
        eval_status = db.query(
            self.models.Evaluation_Type.id_record.label('_id'),
            self.models.Evaluation_Type.type.label('_type'),
            self.models.Evaluation_Type.status.label('_status'),
        ).filter(
            self.models.Evaluation_Type.type == self.cns.EMPLOYEE_EVALUATION.value
        ).first()

        # return
        return eval_status

    # query evaluation status and type of evaluation supervisor
    async def query_evaluation_type_and_status_supervisor(self, db: object) -> object:
        eval_status = db.query(
            self.models.Evaluation_Type.id_record.label('_id'),
            self.models.Evaluation_Type.type.label('_type'),
            self.models.Evaluation_Type.status.label('_status'),
        ).filter(
            self.models.Evaluation_Type.type == self.cns.SUPERVISOR_EVALUATION.value
        ).first()

        # return
        return eval_status

    # query all evaluation types
    async def query_evaluation_types(self, db: object) -> object:
        types = db.query(
            self.models.Evaluation_Type.id_record.label('_id'),
            self.models.Evaluation_Type.type.label('_type'),
            self.models.Evaluation_Type.status.label('_status')
        ).all()

        # return
        return types

    # parse evaluation ratings
    async def parsing_evaluation_details(self, request: Request) -> Dict[int, int]:
        # define form object and ratings dict
        form = await request.form()
        ratings: Dict[int, int] = {}

        # traverse over the form items
        for key, value in form.items():
            matching = self.regex_ratings.match(key)
            if not matching:
                continue

            try:
                question_id = int(matching.group(1))
                score = int(value)

            except ValueError as ve:
                raise self.http_exec(status_code=self.status.HTTP_422_UNPROCESSABLE_ENTITY,
                                     detail=f'Invalid rating value for {key}. Details: {ve}')

            # from 1 to 6 only selections are available
            if not (1 <= score <= 6):
                raise self.http_exec(status_code=self.status.HTTP_422_UNPROCESSABLE_ENTITY,
                                     detail=f'Score for question {question_id} must be between 1 and 6.')

            # append value
            ratings[question_id] = score

        # return
        return ratings

    # query evaluation questions
    async def query_evaluation_questions(self, db: object) -> object:
        questions = db.query(
            self.models.Evaluation_Question.id_record.label('_id'),
            self.models.Evaluation_Question.question.label('_question'),
            self.models.Evaluation_Type.type.label('_type'),
        ).select_from(
            self.models.Evaluation_Question
        ).join(
            self.models.Evaluation_Question.type
        ).all()

        # return
        return questions

    # query user-specific records
    async def query_evaluation_user_specific_record(self, db: object) -> object:
        users = db.query(
            self.models.User.id_record.label('_id'),
            self.models.User.name.label('_name'),
            self.models.User.lastname.label('_lastname'),
            self.models.User.lastname2.label('_lastname2'),
            self.models.Role.type.label('_role'),
            self.models.User_Role.id_record.label('_id_user_role')
        ).select_from(
            self.models.User_Role
        ).join(
            self.models.User_Role.user
        ).join(
            self.models.User_Role.role
        ).all()

        # return
        return users

    # enable evaluation status
    async def enable_evaluation_status(self, db: object, model: Union[dict, object]) -> None:
        eval_status = db.query(
            self.models.Evaluation_Type
        ).filter(
            self.models.Evaluation_Type.id_record == model["evaluation_type"]
        ).first()

        if eval_status:
            eval_status.status = True

        # db commit
        db.commit()

    # evaluation specific type
    async def evaluation_specific_type(self, db: object, model: Union[dict, object]) -> object:
        eval_type = db.query(
            self.models.Evaluation_Type.id_record.label('_id'),
            self.models.Evaluation_Type.type.label('_type')
        ).filter(
            self.models.Evaluation_Type.id_record == model["evaluation_type"]
        ).first()

        # return
        return eval_type

    # evaluation recipient lists
    async def evaluation_recipient_lists(self, db: object) -> dict:
        # employees
        employee_rows = db.query(
            self.models.User.email.label('_email')
        ).join(
            self.models.User.user_roles
        ).join(
            self.models.User_Role.role
        ).filter(
            self.models.Role.type == "Empleado"
        ).all()

        # supervisors
        supervisor_rows = db.query(
            self.models.User.email.label('_email')
        ).join(
            self.models.User.user_roles
        ).join(
            self.models.User_Role.role
        ).filter(
            self.models.Role.type == "Jefatura"
        ).all()

        # lists
        emp_list = [item._email for item in employee_rows]
        sup_list = [item._email for item in supervisor_rows]

        # return
        return {"employees": emp_list, "supervisors": sup_list}
