import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.backend.schemas import *
from app.backend.main import app
from app_tests.test_backend.reqs import *


@pytest.mark.anyio
async def test_delete_menu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        delete_response = await ac.delete(f'/api/v1/menus/{menu_id}')
        delete_response2 = await ac.delete(f'/api/v1/menus/{uuid4()}')
    assert delete_response.status_code == 200
    assert delete_response.json() is None
    assert delete_response2.status_code == 404


@pytest.mark.anyio
async def test_delete_submenu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        delete_response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        delete_response2 = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{uuid4()}')
    assert delete_response.status_code == 200
    assert delete_response.json() is None
    assert delete_response2.status_code == 404


@pytest.mark.anyio
async def test_delete_dish(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        response3 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_req)
        dish_id = DishOut.parse_obj(response3.json()).id
        delete_response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        delete_response2 = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{uuid4()}/dishes/{uuid4()}')
    assert delete_response.status_code == 200
    assert delete_response.json() is None
    assert delete_response2.status_code == 404
