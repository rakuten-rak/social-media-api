import logging
from storeapi.database import database,user_table
from jose import jwt
from fastapi import HTTPException,status

from passlib.context import CryptContext

logger = logging.getLogger(__name__)


SECRET_KEY = 'a very long str'
ALGORITHM = 'HS256' 
pwd_context = CryptContext(schemes=["bcrypt"])
credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential")


def create_acces_token(email:str):
    logger.debug("creating an access token", extra={"email":email})
    expire = datetime.datetime.now(datetime.utc) + datetime.timedelta(minutes=30)
    jwt_data = {"sub":email,"exp":expire}
    encoded_jwt = jwt.encode(jwt_data,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password,hash_password) -> bool:
    return pwd_context.verify(plain_password,hash_password)

async def get_user(email:str):
    logging.debug("Fetching user from the database", extra={'email':email})
    query= user_table.select().where(user_table.c.email == email)
    result = await database.find_all(query)
    if result:
        return result
    return

async def authenticat_user(email:str, password:str):
    logging.debug("Authenticatin user ", extra={'email':email})
    user = await get_user(email)
    if not user:
        raise credential_exception
    if not verify_password(password,user.password):
        raise credential_exception
    return user

