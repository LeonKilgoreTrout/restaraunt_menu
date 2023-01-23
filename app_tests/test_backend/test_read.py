import pytest
from httpx import AsyncClient
from pydantic import parse_obj_as
from typing import List

from app.backend.schemas import *
from app.backend.main import app
from app_tests.test_backend.reqs import *


@pytest.mark.anyio
async def test_get_menu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        await ac.post("/api/v1/menus", json=updated_menu)
        menu_id = MenuOut.parse_obj(response.json()).id
        # FIXME: rebase get_all func in main
        # get_all_response = await ac.get('/api/v1/menus/')
        get_by_id_response = await ac.get(f'/api/v1/menus/{menu_id}')

    assert MenuOut.parse_obj(get_by_id_response.json())


@pytest.mark.anyio
async def test_get_submenu(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        await ac.post("/api/v1/menus", json=updated_menu)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        # FIXME: rebase get_all func in main
        get_by_id_response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')

    assert SubmenuOut.parse_obj(get_by_id_response.json())


@pytest.mark.anyio
async def test_get_dish(test_db):

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/menus", json=menu_req)
        await ac.post("/api/v1/menus", json=updated_menu)
        menu_id = MenuOut.parse_obj(response.json()).id
        response2 = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_req)
        submenu_id = SubmenuOut.parse_obj(response2.json()).id
        response3 = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_req)
        dish_id = DishOut.parse_obj(response3.json()).id
        # FIXME: rebase get_all func in main
        get_by_id_response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')

    assert DishOut.parse_obj(get_by_id_response.json())
