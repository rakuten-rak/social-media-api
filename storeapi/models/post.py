from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

# SO HERE IS FROM THE MAIN SOTREAPI POST AND GET USERPOST WE CREATED BUT WE ARE SPLITTING IT 
#INTO DIFF FOLDERS/


# FIRST TAKING THE USER POST IN THE API WITH BASEMODEL
class UserPostIn(BaseModel):
    body:str

# RETURNING THE DATA BACK TO THE USER WE INCLUDE THE ID TO IDENTIFY THE USER
class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CommentIn(BaseModel):
    body:str
    post_id:int

class Comment(CommentIn):
    model_config = ConfigDict(from_attributes=True)

    id:int

class UserPostWithComment(BaseModel):
    post:UserPost
    comment:list[Comment]