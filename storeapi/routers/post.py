# SO IN HERE CONTAIN ALL THE ASYNC FUNC WE CREATED TO HANDLE THE POST AND GET 
import logging
# API ROUTER IS A FASTAPI ROUTER INSTEAD OF RUNNING ON IT OWN IT CAN BE INCLUDED IN AN EXISTED APPLICATION
from typing import List
from fastapi import FastAPI,APIRouter,HTTPException
from pydantic import BaseModel
from storeapi.database import comment_table,post_table,database

# THIS IS OUR FIRST POST WE CREATE BUT MOVE TO DIFF FOLDER, WAY WE IMPORT IT BACK
from storeapi.models.post import UserPost,UserPostIn,CommentIn,Comment,UserPostWithComment

app = FastAPI()
router = APIRouter()

logger = logging.getLogger(__name__)


# # FIRST TAKING THE USER POST IN THE API WITH BASEMODEL
# class UserPostIn(BaseModel):
#     body:str

# # RETURNING THE DATA BACK TO THE USER WE INCLUDE THE ID TO IDENTIFY THE USER
# class UserPost(UserPostIn):
#     id: int

# NOW WE CREATE OUR DATA DB TO STORE ALL THE POST
# post_table = {}
# comment_table = {}

async def find_post(post_id:int):
    logger.info(f"finding all post by {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    # return post_table.get(post_id)
    logger.debug(query)
    return await database.fetch_one(query)


# NOW WE CREATE THE ENDPOINT FOR THE POSTIN AND POSTOUT
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    # CONVERT THE POST INTO A DICT()
    data = post.model_dump() # or you can use dict()
    query = post_table.insert().values(data)
    last_record_id  = await database.execute(query)
    return {**data, "id":last_record_id}
    # CHECK FOR THE POST AND ID LENGTH IN OUR DB
    # last_record_id = len(post_table)
    # NOW TO CREAE A NEW POST AN ID WILL BE ATTACHED
    # new_post = {**data, "id":last_record_id}
    # NOW TO RETRIVE A POST OR IDENTIFY A POST IN OUR API
    # post_table[last_record_id] = new_post
    # return new_post

#NOW HOW TO GET POST THE USER POST
@router.get("/post", response_model=List[UserPost])
async def get_all_posts():
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)
    # return list(post_table.values())

# NOW WE CREATE THE ENDPOINT FOR THE COMMENTIN AND COMMENTOUT
@router.post("/comment", response_model=Comment,status_code=201)
async def create_comment(comment: CommentIn):
    #CHECK TO SEE IF THE COMMENT WE ARE CREATING THE POST EXIST
    logger.info("creatinga comments")
    post = await find_post(comment.post_id)
    if  not post:
        logger.error(f"post with id {comment.post_id} not found")
        raise HTTPException(status_code=404,detail="Post Not Found")
    # CONVERT THE POST INTO A DICT()
    data = comment.model_dump()
    query  = comment_table.insert().values(data)
    # CHECK FOR THE POST AND ID LENGTH IN OUR DB
    # last_record_id = len(comment_table)
    last_record_id = await database.execute(query)
    return {**data, "id":last_record_id}
    # NOW TO CREAE A NEW POST AN ID WILL BE ATTACHED
    # new_comment = {**data, "id":last_record_id}
    # NOW TO RETRIVE A POST OR IDENTIFY A POST IN OUR API
    # comment_table[last_record_id] = new_comment
    # return new_comment

# NOW WE CREATE ENDPOITN TO GET A COMMENT ON A POST
@router.get("/post/{post_id}/comment", response_model=list[Comment])
#NOW WE PASS THE POST_ID TO GET_COMMENTS_ON_POST FOR A POST
async def get_comments_on_post(post_id:int):
    logger.info("getting comment on post")
    query = comment_table.select().where(comment_table.c.post_id ==  post_id)
    
    logger.debug(query,extra={'email': 'bob@example.com'})
    return await database.fetch_all(query)
    # return [
    #     comment for comment in comment_table.values() if comment["post_id"] == post_id
    # ]

# GET POST WITH A COMMENT
@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    # CONVERT THE POST INTO A DICT()
    logger.info("getting post with its comments")
    post = await find_post(post_id)
    if not post:
        logger.error(f"post with post id {post_id} not found")
        raise HTTPException(status_code=404,detail="Post Not Found")
    return {"post":post, "comments":await get_comments_on_post(post_id)}



# BASIC AND FIRST API INITIATED
# @app.get("/")
# async def root():
#     return {"message":"Hello,World"}

