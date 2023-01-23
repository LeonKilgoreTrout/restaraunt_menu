import pytest
from httpx import AsyncClient

from app.backend.schemas import *
from app.backend.main import app
from app_tests.test_backend.reqs import *


@pytest.mark.anyio
async def test_update_menu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        updated_response = await ac.patch(f'/api/v1/menus/{menu_id}', json=updated_menu)
    assert MenuOut.parse_obj(updated_response.json())


@pytest.mark.anyio
async def test_update_submenu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        updated_response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=updated_submenu)
    assert SubmenuOut.parse_obj(updated_response.json())


@pytest.mark.anyio
async def test_update_submenu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        response3 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_req)
        dish_id = DishOut.parse_obj(response3.json()).id
        updated_response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                                          json=updated_dish)
    assert SubmenuOut.parse_obj(updated_response.json())
