# import
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from typing import Annotated

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.tooling.setting.error_log import Logs_Manager
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.db_transactions.services.db_profile import Profile_Trans_Manager
from app.backend.schema.profile.Contact import Create_Contact_Info, Update_Password_Info
from app.backend.database.config import Session_Controller


# router
profile_route = APIRouter(prefix=Cns.PROFILE_BASE.value, tags=[Cns.SERV.value])
# trans
trans = Auth_Manager()
# serv
serv = Profile_Trans_Manager()
# logs
exc_logs = Logs_Manager()


# GET -> Profile Base
@profile_route.get(Cns.BASE.value, response_class=HTMLResponse)
async def getting_app_profile_base_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # query address records
    address = await serv.querying_profile_info_address(db=db, id_session=user_login.user_id)

    # query user_role records
    record = await serv.querying_user_role_profile_info(db=db, id_session=user_login.user_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/index.html', context={
            'request': request, 'params': {
                'fg': fg, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, 'address': address, 'record': record
            }
        }
    )


# GET -> Profile Address
@profile_route.get(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def getting_app_profile_address_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # fetch province, canton, and district records
    address = await serv.querying_province_canton_and_districts(db=db)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/address.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session, "address": address
            }
        }
    )


# POST -> Profile Address
@profile_route.post(Cns.PROFILE_ADDRESS.value, response_class=HTMLResponse)
async def posting_app_profile_address_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Create_Contact_Info, Depends(dependency=Create_Contact_Info.formatting)],
) -> HTMLResponse:

    try:
        # register / update records
        await serv.registering_updating_contact_info(
            db=db, schema=model.model_dump(), id_session=user_login.user_id)

    except IntegrityError as exc:
        db.rollback()  # -> db rollback
        info = await exc_logs.logger_sql_alchemy_integrity_error(exc=exc)  # -> error logs
        # flag
        constraint = (info or {}).get("constraint")
        flag = "_email" if constraint == "user_email_key" else "_phone"
        # redirect to endpoint
        return await getting_app_profile_address_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail', exc=flag)

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        # redirect to endpoint
        return await getting_app_profile_address_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_profile_address_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "perfil", "redirect": "ce", "fg": "_contact_info"
            }
        }
    )


# GET -> Profile Password
@profile_route.get(Cns.PROFILE_PASSWORD.value, response_class=HTMLResponse)
async def getting_app_profile_password_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        fg: Annotated[str, None] = None,
        exc: Annotated[str, None] = None
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/password.html', context={
            'request': request, 'params': {
                'fg': fg, 'exc': exc, 'ops': Cns.OPS_CRUD.value, 'user_session': user_session
            }
        }
    )


# POST -> Profile Password
@profile_route.post(Cns.PROFILE_PASSWORD.value, response_class=HTMLResponse)
async def posting_app_profile_password_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
        model: Annotated[Update_Password_Info, Depends(dependency=Update_Password_Info.formatting)],
) -> HTMLResponse:

    try:
        # update user password
        await serv.updating_password_info(
            db=db, schema=model.model_dump(), id_session=user_login.user_id)

    except HTTPException:
        db.rollback() # -> db rollback
        return await getting_app_profile_password_endpoint(
            request=request, db=db, user_login=user_login, fg='_fail', exc='_password')

    except SQLAlchemyError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_error(exc=SQLAlchemyError)  # -> error logs
        # redirect to endpoint
        return await getting_app_profile_password_endpoint(
            request=request, db=db, user_login=user_login, fg='_orm_error')

    except OperationalError:
        db.rollback()  # -> db rollback
        await exc_logs.logger_sql_alchemy_operational_error(exc=OperationalError)  # -> error logs
        # redirect to endpoint
        return await getting_app_profile_password_endpoint(
            request=request, db=db, user_login=user_login, fg='_ops_error')

    # return
    return Cns.HTML_.value.TemplateResponse(
        "base/redirect.html", context={
            "request": request, "params": {
                "domain": "perfil", "redirect": "ce", "fg": "_password"
            }
        }
    )


# GET -> Profile Vacations
@profile_route.get(Cns.PROFILE_VACATIONS.value, response_class=HTMLResponse)
async def getting_app_profile_vacation_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # hire date
    hire_date = await serv.querying_user_hire_date(db=db, id_session=user_login.user_role_id)

    # vacations
    record = await serv.querying_vacations(db=db, id_session=user_login.user_role_id)

    # vacations requests
    vac_record = await serv.querying_vacations_requests(db=db, id_session=user_login.user_role_id)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/vacations.html', context={
            'request': request, 'params': {
                'record': record, 'vac_record': vac_record, 'user_session': user_session, 'hire_date': hire_date
            }
        }
    )


# GET -> Profile Extra Hours
@profile_route.get(Cns.PROFILE_EXTRA_HOURS.value, response_class=HTMLResponse)
async def getting_app_profile_extra_hours_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # current extra hours records
    record = await serv.querying_extra_hours(db=db, id_session=user_login.user_role_id)

    # extra hours requests
    ehs_record = await serv.querying_extra_hours_requests(db=db, id_session=user_login.user_role_id)

    # counters
    counters = await serv.counting_extra_hours(rows=ehs_record)

    print(counters)

    # return
    return Cns.HTML_.value.TemplateResponse(
        'profile/profile/extra_hours.html', context={
            'request': request, 'params': {
                'record': record, 'ehs_record': ehs_record, 'user_session': user_session, "counters": counters
            }
        }
    )
