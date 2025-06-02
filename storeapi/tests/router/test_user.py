import pytest
from httpx import AsyncClient

async def register_users(async_client:AsyncClient,email:str,password:str):
    return await async_client.post(
        '/register',
        json={"email":email, "password":password}
    )

@pytest.mark.anyio
async def test_register_user(async_client:AsyncClient):
    response = await register_users(async_client,'test@example.com','1234')
    assert response.status_code == 201
    assert "user created" in response.json()["detail"]

@pytest.mark.anyio
async def test_register_user_already_exist(async_client:AsyncClient,register_user:dict):
    response = await register_users(async_client, register_user["email"], register_user["password"])
    assert response.status_code == 400
    assert "already exist" in response.json()["detail"] 