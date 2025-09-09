# import
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

# local import
from app.backend.tooling.setting.constants import Constants as Cns
from app.backend.tooling.setting.env import env
from app.backend.schema.auth.Login import Token_Data


# bcrypt object
pwd_context: object = CryptContext(schemes=['bcrypt'], deprecated='auto')
# oauth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Cns.OAUTH2_SCHEMA_URL.value, auto_error=False)


# hash incoming password
def getting_password_to_hash(password: str) -> str:
    return pwd_context.hash(password)


# verify hash password
def verifying_hash_password(plain: str, hash_password: str) -> bool:
    return pwd_context.verify(plain, hash_password)


# load token payload data
def loading_payload_data(record: object) -> dict:
    return {
        'user_role_id': record.user_roles[0].id_record,
        'user_id': record.id_record,
        'role_id': record.user_roles[0].role.id_record,
        'role_type': record.user_roles[0].role.type
    }


# generate access token
def generating_access_token(data: dict, expires_delta: int) -> str:
    # copy dict
    to_copy = data.copy()

    # set expire delta
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # update dict
    to_copy.update({"exp": expire})
    # define token
    token_create = jwt_encode(to_copy, env.tkn_key, algorithm=env.tkn_algo)
    # return
    return token_create


# verifying access token
async def verifying_access_token(token: str, exc: dict) -> Token_Data:
    if not token:
        raise exc['_http_redirect_url']

    try:
        # extract user_role_id from payload
        payload = jwt_decode(token, env.tkn_key, algorithms=[env.tkn_algo], options={"require": ["exp"]}, leeway=5)

        # extract data
        token_data = Token_Data(**payload)

        # validate id
        if token_data.user_id is None:
            raise exc

    except ExpiredSignatureError:
        raise exc['_http_session_expired']

    except InvalidTokenError:
        raise exc['_http_invalid_token']

    # return
    return token_data


# getting current user logged in
async def getting_current_user(request: Request, token: str | None = Depends(oauth2_scheme)):
    # exceptions
    exc_book = {
        "_http_redirect_url": HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Redirect to Login Page",
            headers={"Location": Cns.OAUTH2_SCHEMA_URL.value},
        ),
        "_http_session_expired": HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Session Expired",
            headers={"Location": f'{Cns.OAUTH2_SCHEMA_URL.value}?fg=_expire'},
        ),
        "_http_invalid_token": HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Invalid Token",
            headers={"Location": f'{Cns.OAUTH2_SCHEMA_URL.value}?fg=_expire'},
        ),
    }

    # bearer token fetch on browser cookies
    bearer = token or request.cookies.get("access_token")

    # return
    return await verifying_access_token(token=bearer, exc=exc_book)


# custom raise exceptions: Login as Admin User Login Page
class Privilege_Access_As_Admin_Exception(Exception):
    pass


# custom raise exceptions: Login as User Admin Login Page
class Privilege_Access_As_User_Exception(Exception):
    pass


# temp password invalid custom exception
class Temporary_Invalid_Password_Exception(Exception):
    pass


# user as inactive status
class User_Inactive_Status_Exception(Exception):
    pass
