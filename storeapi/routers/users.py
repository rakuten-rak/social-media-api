import logging
from fastapi import APIRouter,HTTPExcepion,status
from storeapi import database
from storeapi.models.users import UserIn
from storeapi.security import get_password_hash, get_user
from storeapi.database import user_table

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/register',status_code=201)
async def register(user:UserIn):
    if await get_user(user.email):
        raise HTTPExcepion(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name already exist"
        )
    
    hash_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email,password=hash_password)
    logger.debug(query)
    await database.execute(query)
    return {'detail':'user created'}

@router.post('/token')
async def login(user:UserIn):

    user = await authenticat_user(user.email,user.password)
    access_token = create_acces_token(user.email)
    return {"access_token":access_token, "access_type":"bearer"}
    