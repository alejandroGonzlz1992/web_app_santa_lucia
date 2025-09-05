# import
import re
from logging import getLogger
from typing import Union

from dns.e164 import query

# local import
from app.backend.database import models


# logger
logger = getLogger(__name__)


# class
class Db_Crud_Request:

    # init
    def __init__(self):
        self.models = models
        self.logger = logger
        self.re = re
        self.patter_triples = self.re.compile(r'([a-záéíóúüñ])\1{2,}', self.re.IGNORECASE)

    # formatting text questions
    async def formatting_question(self, text: str) -> str:
        text = text.strip() # remove leading spaces
        if not text.startswith('¿'):
            text = '¿' + text

        text = text.rstrip() # trim trailing spaces
        text = text.rstrip('?') + '?' # normalize single ? at the end, instead of ??

        text = text[0] + text[1:].lower() # lower case all after first char (?)

        text = self.patter_triples.sub(r'\1\1', text)

        # capitalize the first alpha char after ?
        for item, char in enumerate(text[1:], start=1):
            if char.isalnum():
                text = text[:item] + char.upper() + text[item+1:]
                break

        text = self.re.sub(r'\s+', ' ', text) # normalize internal spaces

        return text

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

    # questions crud
    async def getting_questions_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Evaluation_Question.id_record.label('_id'),
                        self.models.Evaluation_Question.question.label('_question'),
                        self.models.Evaluation_Type.type.label('_type'),
                        self.models.Evaluation_Question.log_date.label('_log_date'))
                .join(self.models.Evaluation_Type, self.models.Evaluation_Question.type).all())
        # return
        return rows

    # evaluation type
    async def getting_evaluation_types_rows(self, db: object) -> object:
        # rows
        rows = db.query(self.models.Evaluation_Type.id_record.label('_id'),
                        self.models.Evaluation_Type.type.label('_type')).all()
        # return
        return rows

    # register crud question
    async def register_crud_eval_question(self, db: object, model: Union[dict, object]) -> None:
        text = await self.formatting_question(text=model['evaluation_question']) # string format question

        question = self.models.Evaluation_Question(
            question=text,
            id_evaluation_type=model["evaluation_type"]
        )

        db.add(instance=question) # add temp model
        db.commit() # commit to db
        db.refresh(instance=question) # refresh model

    # updating crud question
    async def updating_crud_eval_question(self, db: object, model: Union[dict, object]) -> None:
        text = await self.formatting_question(text=model['evaluation_question']) # string format question

        question = db.query(self.models.Evaluation_Question).filter(
            self.models.Evaluation_Question.id_record == model["id"]).first()

        if question:
            question.question = text
            question.id_evaluation_type = model["evaluation_type"]

        # commit
        db.commit()

    # payment dates crud
    async def getting_payment_dates_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Payment_Date.id_record.label('_id'),
                        self.models.Payment_Date.date_payment.label('_date'),
                        self.models.Payment_Date.date_payment2.label('_date2'),
                        self.models.Payment_Date.frecuency.label('_frecuency'),
                        self.models.Payment_Date.log_date.label('_log_date')).all())
        # return
        return rows

    # register payment date
    async def register_crud_payment_dates(self, db: object, model: Union[dict, object]) -> None:
        payment_date = self.models.Payment_Date(
            date_payment=model["payment_date"],
            date_payment2=model["payment2_date"],
            frecuency=model["payment_frecuency"]
        )

        db.add(instance=payment_date) # add temp model
        db.commit() # commit to db
        db.refresh(instance=payment_date) # refresh model

    # updating payment date
    async def updating_crud_payment_dates(self, db: object, model: Union[dict, object]) -> None:
        payment_date = db.query(self.models.Payment_Date).filter(
            self.models.Payment_Date.id_record == model["id"]).first()

        if payment_date:
            payment_date.date_payment = model["payment_date"],
            payment_date.date_payment2 = model["payment2_date"],
            payment_date.frecuency = model["payment_frecuency"]

        # commit
        db.commit()

    # deduction crud
    async def getting_deduction_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Deduction.id_record.label('_id'),
                         self.models.Deduction.name.label('_name'),
                         self.models.Deduction.percentage.label('_percentage'),
                         self.models.Deduction.log_date.label('_log_date')).all())
        # return
        return rows

    # register deduction
    async def register_crud_deduction(self, db: object, model: Union[dict, object]) -> None:
        deduction = self.models.Deduction(
            name=model["deduction_name"].upper(),
            percentage=model["deduction_percentage"]
        )

        db.add(instance=deduction)  # add temp model
        db.commit()  # commit to db
        db.refresh(instance=deduction)  # refresh model

    # updating deduction date
    async def updating_crud_deduction(self, db: object, model: Union[dict, object]) -> None:
        deduction = db.query(self.models.Deduction).filter(
            self.models.Deduction.id_record == model["id"]).first()

        if deduction:
            deduction.name = model["deduction_name"].upper(),
            deduction.percentage = model["deduction_percentage"]

        # commit
        db.commit()

    # schedule crud
    async def getting_schedule_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Schedule.id_record.label('_id'),
                         self.models.Schedule.name.label('_name'),
                         self.models.Schedule.start_time.label('_start'),
                         self.models.Schedule.end_time.label('_end'),
                         self.models.Schedule.hours.label('_hours'),
                         self.models.Schedule.date_create.label('_create'),
                         self.models.Schedule.date_update.label('_update')).all())
        # return
        return rows

    # register deduction
    async def register_crud_schedule(self, db: object, model: Union[dict, object]) -> None:
        schedule = self.models.Schedule(
            name=model["schedule_type"],
            start_time=model["schedule_start_time"],
            end_time=model["schedule_end_time"],
            hours=model["schedule_total_hours"],
            date_create=model["schedule_create_date"],
            date_update=model["schedule_create_date"]
        )

        db.add(instance=schedule)  # add temp model
        db.commit()  # commit to db
        db.refresh(instance=schedule)  # refresh model

    # updating schedule crud
    async def updating_crud_schedule(self, db: object, model: Union[dict, object]) -> None:
        schedule = db.query(self.models.Schedule).filter(
            self.models.Schedule.id_record == model["id"]).first()

        if schedule:
            schedule.name = model["schedule_type"]
            schedule.start_time = model["schedule_start_time"]
            schedule.end_time = model["schedule_end_time"]
            schedule.hours = model["schedule_total_hours"]
            schedule.date_update = model["schedule_create_date"]

        # commit
        db.commit()

    # department crud
    async def getting_department_crud_rows(self, db: object) -> object:
        # rows
        rows = (db.query(self.models.Department.id_record.label('_id'),
                         self.models.Department.name.label('_name'),
                         self.models.Department.date_create.label('_create'),
                         self.models.Department.date_update.label('_update')).all())
        # return
        return rows

    # register department
    async def register_crud_department(self, db: object, model: Union[dict, object]) -> None:
        department = self.models.Department(
            name=model["department_name"].title(),
            date_create=model["department_create_date"],
            date_update=model["department_create_date"]
        )

        db.add(instance=department)  # add temp model
        db.commit()  # commit to db
        db.refresh(instance=department)  # refresh model

    # updating department
    async def updating_crud_department(self, db: object, model: Union[dict, object]) -> None:
        department = db.query(self.models.Department).filter(
            self.models.Department.id_record == model["id"]).first()

        if department:
            department.name = model["department_name"].title()
            department.date_update = model["department_create_date"]

        # commit
        db.commit()

