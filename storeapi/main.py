import logging
from asgi_correlation_id import CorrelationIdMiddleware

from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    HTTPException
)
from fastapi.exception_handlers import http_exception_handler

from storeapi.logging_conf import configure_logging
from pydantic import BaseModel
from storeapi.routers.post import router as post_router
from storeapi.database import database
from storeapi.routers.users import router as user_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    configure_logging()
    logger.info("fastapi")
    await database.connect()
    yield
    await database.disconnect()

# # THIS IS OUR FIRST POST WE CREATE BUT MOVE TO DIFF FOLDER, WAY WE IMPORT IT BACK
# from storeapi.models.post import UserPost,UserPostIn

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(post_router) # YOU CAN INCLUDE A PREFIX WHICH LILE AN ENDPOINT TO BE BUILD ON
app.include_router(user_router)

# # # FIRST TAKING THE USER POST IN THE API WITH BASEMODEL
# # class UserPostIn(BaseModel):
# #     body:str

# # # RETURNING THE DATA BACK TO THE USER WE INCLUDE THE ID TO IDENTIFY THE USER
# # class UserPost(UserPostIn):
# #     id: int

# # NOW WE CREATE OUR DATA DB TO STORE ALL THE POST
# post_table = {}


# # NOW WE CREATE THE ENDPOINT FOR THE POSTIN AND POSTOUT
# @app.post("/", response_model=UserPost)
# async def create_post(post: UserPostIn):
#     # CONVERT THE POST INTO A DICT()
#     data = post.model_dump()
#     # CHECK FOR THE POST AND ID LENGTH IN OUR DB
#     last_record_id = len(post_table)
#     # NOW TO CREAE A NEW POST AN ID WILL BE ATTACHED
#     new_post = {**data, "id":last_record_id}
#     # NOW TO RETRIVE A POST OR IDENTIFY A POST IN OUR API
#     post_table[last_record_id] = new_post
#     return new_post

# #NOW HOW TO GET POST THE USER POST
# @app.get("/post", response_model=list[UserPost])
# async def get_all_posts():
#     return list(post_table.values())




# # BASIC AND FIRST API INITIATED
# # @app.get("/")
# # async def root():
# #     return {"message":"Hello,World"}

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request,excs):
    logger.error(f"httpException erro {excs.status_code} {excs.detail}")
    return http_exception_handler(request,excs)