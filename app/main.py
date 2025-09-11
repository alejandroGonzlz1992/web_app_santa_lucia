# import
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated

# local import
from app import fastapi_app_config
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.security import getting_current_user
from app.backend.db_transactions.auth.db_auth import Auth_Manager
from app.backend.database.config import Session_Controller

# instance app
app = fastapi_app_config()
# trans
trans = Auth_Manager()


# root endpoint
@app.get(Cns.ROOT.value, response_class=HTMLResponse)
async def getting_app_home_page_endpoint(
        request: Request,
        db: Annotated[Session, Depends(dependency=Session_Controller)],
        user_login: Annotated[object, Depends(dependency=getting_current_user)],
) -> HTMLResponse:

    # fetching current User logged-in
    user_session = await trans.fetching_current_user(db=db, user=user_login)

    # watcher: functions

    # add one vacation day per month work, use hire date vs current date. If current day/month = hire date day/month
    # vacation += 1 day

    # payroll
    # if current date if same as paymentdate1 or paymentdate2 (for quincenal) execute deduction calculations, register
    # at database, calculate net payment, add one quota to aguinaldo and generate payment report to be downloaded.


    # return
    return Cns.HTML_.value.TemplateResponse(
        'base/index.html', context={
            'request': request, 'params': {
                'time_zone': Cns.CR_TIME_ZONE.value, 'user_session': user_session
            }
        }
    )


# close session
@app.get(Cns.URL_SIGN_OUT.value, response_class=RedirectResponse)
async def getting_sign_out_session(
        request: Request,
) -> RedirectResponse:

    # response object
    resp = RedirectResponse(url=request.url_for('getting_app_user_login_endpoint'),
                            status_code=status.HTTP_302_FOUND)
    # remove cookie from web browser
    resp.delete_cookie('access_token')
    # refresh
    resp.delete_cookie('refresh_token')

    # return
    return resp
