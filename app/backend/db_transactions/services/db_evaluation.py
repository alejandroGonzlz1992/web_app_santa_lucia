# import
from re import compile
from fastapi import HTTPException, status, Request
from logging import getLogger
from typing import Union, Dict
from sqlalchemy import func, true, and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import lateral
from sqlalchemy.dialects.postgresql import aggregate_order_by

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

    # parsing average value
    async def parsing_average_value(self, values: list) -> float:
        average = round(float(sum(values)/len(values)), 2)
        return average

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

    # query evaluation approver
    async def query_evaluation_approver(self, db: object, id_session: Union[int, str]) -> object:
        approver = db.query(
            self.models.User_Role.approver.label('_id_approver'),
        ).filter(
            self.models.User_Role.id_record == id_session
        ).first()

        # return
        return approver

    # query user-specific records
    async def query_evaluation_user_specific_record(self, db: object) -> object:
        users = db.query(
            self.models.User.id_record.label('_id'),
            self.models.User.name.label('_name'),
            self.models.User.lastname.label('_lastname'),
            self.models.User.lastname2.label('_lastname2'),
            self.models.Role.type.label('_role'),
            self.models.User_Role.id_record.label('_id_user_role'),
            self.models.User_Role.approver.label('_approver')
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

    # registering evaluation results
    async def registering_evaluation_results(self, db: object, model: Union[dict, object], sup_id: Union[int, str]) -> None:
        # temp model
        evaluation = self.models.Evaluation(
            score=list(model["ratings"].values()),
            average=await self.parsing_average_value(values=list(model["ratings"].values())),
            details=model["evaluation_detail"].capitalize(),
            questions=list(model["ratings"].keys()),
            id_subject=model["evaluation_user_name_field"]
        )
        # add model to db
        db.add(instance=evaluation)
        # db commit
        db.commit()
        # db refresh
        db.refresh(instance=evaluation)

    # disable evaluation form
    async def disabling_evaluation_module(self, db: object, model: Union[dict, object]) -> None:
        eval_status = db.query(
            self.models.Evaluation_Type
        ).filter(
            self.models.Evaluation_Type.type == model["evaluation_type"]
        ).first()

        if eval_status:
            eval_status.status = False

        # db commit
        db.commit()

    # query aliases
    async def query_aliases_for_evaluation(self) -> dict:
        return {
            'subj_role': aliased(self.models.User_Role), 'subj_user': aliased(self.models.User),
            'subj_job': aliased(self.models.Role), 'sup_role': aliased(self.models.User_Role),
            'sup_user': aliased(self.models.User), 'sup_job': aliased(self.models.Role),
            'questions': aliased(self.models.Evaluation_Question)
        }

    # query evaluation results
    async def collecting_evaluation_records(
            self, db: object, model: Union[dict, object]) -> object:
        # input ids
        subject_user_role_id = int(model["evaluation_user_name_field"])
        # supervisor_user_id = int(model["evaluation_approver_field"])

        # aliases for subject and approver
        entities = await self.query_aliases_for_evaluation()

        pos = lateral(
            func.generate_subscripts(self.models.Evaluation.questions, 1).table_valued('pos')
        ).alias('pos')

        # query records
        records = (db.query(
            self.models.Evaluation.id_record.label('_eval_id'),
            # subject
            entities["subj_user"].name.label('_subj_name'),
            entities["subj_user"].lastname.label('_subj_lastname'), entities["subj_user"].lastname2.label('_subj_lastname2'),
            entities["subj_user"].email.label('_subj_email'), entities["subj_job"].name.label('_subj_role_name'),
            # supervisor
            entities["sup_user"].name.label('_sup_name'), entities["sup_user"].lastname.label('_sup_lastname'),
            entities["sup_user"].lastname2.label('_sup_lastname2'), entities["sup_user"].email.label('_sup_email'),
            entities["sup_job"].name.label('_sup_role_name'),
            # evaluation fields
            self.models.Evaluation.average.label('_avg'),
            self.models.Evaluation.questions.label('_ques_ids'), self.models.Evaluation.score.label('_scores'),
            self.models.Evaluation.details.label('_feedback'),
            # order question texts
            func.array_agg(aggregate_order_by(entities["questions"].question, pos.c.pos)).label('_ques_texts')
        ).select_from(
            self.models.Evaluation
        ).join(
            entities["subj_role"], entities["subj_role"].id_record == self.models.Evaluation.id_subject
        ).join(
            entities["subj_user"], entities["subj_user"].id_record == entities["subj_role"].id_user
        ).join(
            entities["subj_job"], entities["subj_job"].id_record == entities["subj_role"].id_role

        ).join(
            entities["sup_user"], entities["sup_user"].id_record == entities["subj_role"].approver
        ).join(
            entities["sup_role"], and_(
                entities["sup_role"].id_user == entities["sup_user"].id_record,
                entities["sup_role"].status.is_(True),
            )
        ).join(
            entities["sup_job"], entities["sup_job"].id_record == entities["sup_role"].id_role
        ).join(
            pos, true()
        ).join(
            entities["questions"], entities["questions"].id_record == self.models.Evaluation.questions[pos.c.pos]
        ).filter(
            entities["subj_role"].id_record == subject_user_role_id
        ).group_by(
            self.models.Evaluation.id_record,
            entities["subj_user"].id_record, entities["sup_user"].id_record,
            entities["subj_job"].id_record, entities["sup_job"].id_record,
            self.models.Evaluation.average, self.models.Evaluation.questions,
            self.models.Evaluation.score, self.models.Evaluation.details
        ))

        # return
        return records.first()

