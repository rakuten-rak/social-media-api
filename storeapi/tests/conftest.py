from typing import AsyncGenerator,Generator
import os
# ALL IMPORT HERE ARE USED FOR PYTESTING ON OUR FASTAPI OR REQUEST
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from storeapi.database import comment_table,post_table,database,user_table
os.environ["ENV_STATE"] = "test"

# from storeapi.routers.post import comment_table,post_table

from storeapi.main import app #noqa: E402 
#IF WE HAVE AN ASYNC FUNC USING ASYNCGENERATOR IN OUR TEST WE NEED A ASYNIO TO RUN ON 
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"



#WE MAKE A TEST CLIENT CONNECTION
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

# AFTER WE MAKE A DATABAE CONNECTION
@pytest.fixture(autouse=True) # THE AUTOUSE MAKE IT POSSIBLE TO RUN ON EVREY WHERE
async def db() -> AsyncGenerator:
    await database.connect()
    # comment_table.clear()
    # post_table.clear()
    yield
    await database.disconnect()

# HERE USES THE HTTPX TO MAKE REQUEST WITH ASYNCCLIENT
# THE FUNC ASYNC_CLIENT ALSO WORK WITH THE CLIENT FUNC

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client.base_url) as ac:
        yield ac

@pytest.fixture()
async def register_user(async_client:AsyncClient) -> dict:
    user_detail = {"email":"test@example.com","pasword":"1234"}
    await async_client.post('/register',json=user_detail)
    query = user_table.select().where(user_table.c.email == user_detail["email"])
    user = await database.find_one(query)
    user_detail["id"] = user.id
    return user_detail







