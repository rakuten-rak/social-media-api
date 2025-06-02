import pytest
from storeapi import security


@pytest.mark.anyio
async def test_get_user(register_user:dict):
    user = await security.get_user(register_user["email"])
    assert (user == register_user["email"]) 

@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user('test@exmpl.com')
    assert user is None

@pytest.mark.anyio
async def test_verify_password():
    password = 'password'
    assert security.verify_password(password,user.password)
