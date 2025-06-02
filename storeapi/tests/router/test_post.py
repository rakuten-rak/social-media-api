from httpx import AsyncClient
import pytest
# from twisted.internet import defer, error

#  A FUNC THAT CALLS OUR API AND CREATE A POST
async def create_post(body:str, async_client:AsyncClient) -> dict:
    response  = await async_client.post("/post", json={"body":body})
    return response.json()

#WE ALSO CREATED A CREATE_COMMENT
async def create_comment(body:str, post_id:int, async_client:AsyncClient) -> dict:
    response  = await async_client.post("/comment", json={"body":body,"post_id":post_id})
    return response.json()

#  NOW WE CALL THE FIXTURE THAT IS GOING TO USE THE POST
@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("test Post", async_client)


#  NOW WE CALL THE FIXTURE THAT IS GOING TO USE THE POST
@pytest.fixture()
async def created_comment(async_client: AsyncClient,created_post:dict):
    return await create_comment("test Comment",created_post["id"], async_client)

# LET CREATE A POST
# FOR US TO RUN THE ANYIO ON OUR POST WE NEED TO USE THE MARK.ANYIO CUS FASTAPI USE ANYIIO
@pytest.mark.anyio
async def test_create_post(async_client:AsyncClient):
    body = "Test Post"
    response = await async_client.post("/post", json={"body":body})
    assert response.status_code == 201
    # assert {"id":1,"body":body}.items() <= response.json().items()

# CREATING A POST WITHOUT A BODY
@pytest.mark.anyio
async def test_create_post_without_body(async_client:AsyncClient):
    # body = ""
    response = await async_client.post("/post", json={})
    assert response.status_code == 422
    # assert {"id":0,"body":body}.items() <= response.json().items()

@pytest.mark.anyio
async def test_get_all_post(async_client:AsyncClient,created_post:dict):
    # body = "Test Post"
    response = await async_client.get("/post")
    assert response.status_code == 200
    # assert {"id":0,"body":body}.items() <= response.items()
    # assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client:AsyncClient,created_post:dict):
    body = "Test Comment"
    response = await async_client.post("/comment", json={"body":body,"post_id":created_post["id"]})
    assert response.status_code == 201
    # assert {
    #     "id":1,
    #     "body":body,
    #     "post_id":created_post["id"]
    # }.items() <= response.json().items()

@pytest.mark.anyio
async def test_get_post_comment(async_client:AsyncClient,created_post:dict,created_comment:dict):
    # body = "Test Comment"
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    # assert {
    #     "id":0,
    #     "body":body,
    #     "post_id":created_post["id"]
    # }.items() <= response.json().items()
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_post_with_comment_empty(async_client:AsyncClient,created_post:dict):
    # body = "Test Comment"
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    # assert {
    #     "id":0,
    #     "body":body,
    #     "post_id":created_post["id"]
    # }.items() <= response.json().items()
    assert response.json() == []



# ALSO WHEN A POST A COMMENT DOES NOT EXIT PROGRAM TO HANDLE THAT
# THE AS PASSING THE CREATED_POST AND CREATED COMMENT BUT IF THERE IS NOT DATA == 440/200 RAISE AN ERROR