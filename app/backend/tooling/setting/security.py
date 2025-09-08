# import
from passlib.context import CryptContext

# local import
# from app.backend.tooling.setting.env import env


# bcrypt object
pwd_context: object = CryptContext(schemes=['bcrypt'], deprecated='auto')


# hash incoming password
def getting_password_to_hash(password: str) -> str:
    return pwd_context.hash(password)


# verify hash password
def verifying_hash_password(plain: str, hash_password: str) -> bool:
    return pwd_context.verify(plain, hash_password)
