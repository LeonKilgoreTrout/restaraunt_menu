import pytest
from httpx import AsyncClient

from app.backend.schemas import *
from app.backend.main import app
from app_tests.test_backend.reqs import *


@pytest.mark.anyio
async def test_create_menu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
    assert response.status_code == 201
    assert MenuOut.parse_obj(response.json())


@pytest.mark.anyio
async def test_create_submenu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)

    assert response2.status_code == 201
    assert SubmenuOut.parse_obj(response2.json())


@pytest.mark.anyio
async def test_create_dish(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        response3 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_req)

    assert response3.status_code == 201
    assert DishOut.parse_obj(response3.json())
