# import
from fastapi import APIRouter, Request, Depends, BackgroundTasks, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_evaluation import Service_Trans_Manager
from app.backend.schema.service.Evaluation import Create_Evaluation, Enable_Evaluation
from app.backend.database.config import Session_Controller
from app.backend.tooling.bg_tasks import bg_tasks


# router
evaluation_route = APIRouter(prefix=Cns.URL_EVALUATION.value, tags=[Cns.TRANS.value])
# trans
trans = Auth_Manager()
# service trans
serv = Service_Trans_Manager()


# GET -> Evaluation Base
@evaluation_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_evaluation_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# GET -> Evaluation Employee
@evaluation_route.get(Cns.URL_EVALUATION_EMPLOYEE.value, response_class=HTMLResponse)
async def getting_app_evaluation_employee_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # evaluation type
    eval_type = await serv.query_evaluation_type_and_status_employee(db=db)

    # evaluation questions
    questions = await serv.query_evaluation_questions(db=db)

    # users
    users = await serv.query_evaluation_user_specific_record(db=db)

    # evaluation status
    if eval_type._status is False:
        fg = "_fail"

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/employee.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'eval_type': eval_type,
                'questions': questions, 'users': users
            }
        }
    )


# GET -> Evaluation Supervisor
@evaluation_route.get(Cns.URL_EVALUATION_SUPERVISOR.value, response_class=HTMLResponse)
async def getting_app_evaluation_supervisor_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # evaluation type
    eval_type = await serv.query_evaluation_type_and_status_supervisor(db=db)

    # evaluation questions
    questions = await serv.query_evaluation_questions(db=db)

    # users
    users = await serv.query_evaluation_user_specific_record(db=db)

    # evaluation status
    if eval_type._status is False:
        fg = "_fail"

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/supervisor.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'eval_type': eval_type,
                'questions': questions, 'users': users
            }
        }
    )


# POST -> Evaluation Results
@evaluation_route.post(Cns.URL_EVALUATION_POST_RESULT.value, response_class=HTMLResponse)
async def posting_app_evaluation_results(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Evaluation, Depends(Create_Evaluation.formatting)],
        background_tasks: BackgroundTasks
) -> HTMLResponse:

    try:
        await serv.registering_evaluation_results(db=db, model=model.model_dump(), sup_id=user_login.user_role_id)

        # disable evaluation form
        await serv.disabling_evaluation_module(db=db, model=model.model_dump())

        # complex: querying evaluation data
        records = await serv.collecting_evaluation_records(db=db, model=model.model_dump())

        # flag for returning and bg tasks
        to_return = '_employee' if model.evaluation_type == 'Rendimiento Empleado' else '_supervisor'

        # bg tasks
        if to_return == '_employee':
            background_tasks.add_task(
                bg_tasks.bg_task_send_evaluation_results, [records._subj_email, records._sup_email], records, "_employee")

        elif to_return == '_supervisor':
            background_tasks.add_task(
                bg_tasks.bg_task_send_evaluation_results, [records._subj_email, records._sup_email], records, "_supervisor")

    except SQLAlchemyError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_error(exception=op)  # log errors
        if model.evaluation_type == "Rendimiento Empleado":
            return await getting_app_evaluation_employee_endpoint(
                request=request, db=db, user_login=user_login, fg='_ops_error')
        else:
            return await getting_app_evaluation_supervisor_endpoint(
                request=request, db=db, user_login=user_login, fg='_ops_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        if model.evaluation_type == "Rendimiento Empleado":
            return await getting_app_evaluation_employee_endpoint(
                request=request, db=db, user_login=user_login, fg='_ops_error')
        else:
            return await getting_app_evaluation_supervisor_endpoint(
                request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/redirect.html', context={
            'request': request, 'params': {
                'domain': 'evaluaciones', 'redirect': 'ce', 'fg': to_return
            }
        },
        background=background_tasks
    )


# GET -> Evaluation Enable
@evaluation_route.get(Cns.URL_EVALUATION_ENABLE.value, response_class=HTMLResponse)
async def getting_app_evaluation_enable_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # types
    eval_types = await serv.query_evaluation_types(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'service/evaluation/enable.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'eval_types': eval_types
            }
        }
    )


# POST -> Evaluation Enable
@evaluation_route.post(Cns.URL_EVALUATION_ENABLE.value, response_class=RedirectResponse)
async def posting_app_evaluation_enable_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Enable_Evaluation, Depends(Enable_Evaluation.formatting)],
        background_tasks: BackgroundTasks,
) -> RedirectResponse:

    try:
        # enable evaluation status
        await serv.enable_evaluation_status(db=db, model=model.model_dump())

        # define flag for background task
        eval_type = await serv.evaluation_specific_type(db=db, model=model.model_dump())

        flag = "supervisor" if eval_type._type == "Rendimiento Empleado" else "employee"

        # query list of recipients (employees/supervisors)
        recipients = await serv.evaluation_recipient_lists(db=db)

        # background tasks
        if flag == "supervisor":
            background_tasks.add_task(
                bg_tasks.bg_task_send_evaluation_status_recipients, recipients, "supervisor")

        else:
            background_tasks.add_task(
                bg_tasks.bg_task_send_evaluation_status_recipients, recipients, "employee")

    except SQLAlchemyError as op:
        db.rollback() # db rollback
        await serv.logger_sql_alchemy_error(exception=op) # log errors
        return await getting_app_evaluation_enable_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    except OperationalError as op:
        db.rollback()  # db rollback
        await serv.logger_sql_alchemy_ops_error(exception=op)  # log errors
        return await getting_app_evaluation_enable_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    # response object
    resp = RedirectResponse(url=f'{Cns.URL_REDIRECT_TO_EVALUATION_MAIN.value}?fg=_enable',
                            status_code=status.HTTP_303_SEE_OTHER)
    # return
    return resp
