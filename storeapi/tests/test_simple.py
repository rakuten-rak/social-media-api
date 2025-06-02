async def test_add_two():
    x = 1
    y = 3
    res = x + y
    assert res == 4


async def test_dict_contain():
    x = {"x":3,"y":7}
    exp = {"x":3}
    assert exp.items() <= x.items()