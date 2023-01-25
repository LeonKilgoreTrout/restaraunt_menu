from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.configs.logger import Logger
from app.configs.configs import get_app_settings
from app.backend.schemas import *
from app.backend.services import *


Settings = get_app_settings()

openapi_tags = [
    {
        "name": "menus",
        "description": "Operations with menus.",
    },
    {
        "name": "submenus",
        "description": "Operations with submenus."
    },
    {
        "name": "dishes",
        "description": "Operations with dishes."
    },
]

app = FastAPI(
    title=Settings.title,
    description=Settings.description,
    version=Settings.version,
    debug=Settings.debug,
    openapi_tags=openapi_tags
)


@app.get('/api/v1/menus', tags=["menus"])
async def get_menus(
        db: Session = Depends(get_db)
) -> List[MenuOut]:
    menus = await get_all_menus(db=db)
    Logger.disabled = True
    menus = [await get_menu(api_test_menu_id=menu.id, db=db) for menu in menus]
    Logger.disabled = False
    Logger.debug(f'GET | All menus viewed')
    return menus


@app.get('/api/v1/menus/{api_test_menu_id}', tags=["menus"])
async def get_menu(
        api_test_menu_id: str,
        db: Session = Depends(get_db),
) -> MenuOut:

    model = await get_menu_by_id(id=api_test_menu_id, db=db)
    submenus = model.submenus
    nof_submenus = len(submenus)
    nof_dishes = 0
    for submenu in submenus:
        nof_dishes += len(submenu.dishes)
    model = MenuOut.from_orm(model)
    model.submenus_count = nof_submenus
    model.dishes_count = nof_dishes
    Logger.debug(f'GET | {model.__class__.__name__}: {model}')

    return model


@app.post('/api/v1/menus', status_code=201, tags=["menus"])
async def add_menu(
        menu: MenuIn,
        db: Session = Depends(get_db)
) -> MenuOut:

    model = await add_new_menu(menu=menu, db=db)
    model = MenuOut.from_orm(model)
    Logger.debug(f'POST | {model.__class__.__name__}:{model}')
    return model


@app.patch('/api/v1/menus/{api_test_menu_id}', tags=["menus"])
async def update_menu(
        api_test_menu_id: str,
        menu: MenuIn,
        db: Session = Depends(get_db)
) -> MenuOut:

    model = await update_menu_by_id(id=api_test_menu_id, menu=menu, db=db)
    model = MenuOut.from_orm(model)
    Logger.debug(f'PATCH | {model.__class__.__name__}:{model}')
    return model


@app.delete('/api/v1/menus/{api_test_menu_id}', tags=["menus"])
async def delete_menu(
        api_test_menu_id: str,
        db: Session = Depends(get_db)
) -> None:

    await delete_menu_by_id(id=api_test_menu_id, db=db)
    Logger.debug(f'DELETE | Menu {api_test_menu_id} has successfully deleted')


@app.get('/api/v1/menus/{target_menu_id}/submenus', tags=["submenus"])
async def get_submenus(
        target_menu_id: str,
        db: Session = Depends(get_db)
) -> List[SubmenuOut]:

    model = await get_submenus_by_menu_id(menu_id=target_menu_id, db=db)
    Logger.disabled = True
    models = [await get_submenu(target_menu_id=target_menu_id,
                                target_submenu_id=submenu.id,
                                db=db) for submenu in model]
    Logger.disabled = False
    Logger.debug(f'GET | {models}')

    return models


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', tags=["submenus"])
async def get_submenu(
        target_menu_id: str,
        target_submenu_id: str,
        db: Session = Depends(get_db)
) -> SubmenuOut:
    model = await get_submenu_by_ids(menu_id=target_menu_id, submenu_id=target_submenu_id, db=db)
    nof_dishes = len(model.dishes)
    model = SubmenuOut.from_orm(model)
    model.dishes_count = nof_dishes
    Logger.debug(f'GET | {model.__class__.__name__}:{model}')
    return model


@app.post('/api/v1/menus/{target_menu_id}/submenus', status_code=201, tags=["submenus"])
async def add_submenu(
    submenu: SubmenuIn,
    target_menu_id: str,
    db: Session = Depends(get_db)
) -> SubmenuOut:
    model = await add_new_submenu(submenu=submenu, menu_id=target_menu_id, db=db)
    model = SubmenuOut.from_orm(model)
    Logger.debug(f'POST | {model.__class__.__name__}:{model}')
    return model


@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=SubmenuOut, tags=["submenus"])
async def update_submenu(
        target_menu_id: str,
        target_submenu_id: str,
        submenu: SubmenuIn,
        db: Session = Depends(get_db)
) -> SubmenuOut:
    model = await update_submenu_by_ids(menu_id=target_menu_id, submenu_id=target_submenu_id, submenu=submenu, db=db)
    model = SubmenuOut.from_orm(model)
    Logger.debug(f'PATCH | {model.__class__.__name__}:{model}')
    return model


@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', tags=["submenus"])
async def delete_submenu(
        target_menu_id: str,
        target_submenu_id: str,
        db: Session = Depends(get_db)
) -> None:
    await delete_submenu_by_ids(menu_id=target_menu_id, submenu_id=target_submenu_id, db=db)
    Logger.debug(f'DELETE | Submenu {target_submenu_id} has successfully deleted from Menu {target_menu_id}')


@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=201, tags=["dishes"])
async def add_dish(
        dish: DishIn,
        target_menu_id: str,
        target_submenu_id: str,
        db: Session = Depends(get_db)
) -> DishOut:
    model = await add_new_dish(dish=dish, menu_id=target_menu_id, submenu_id=target_submenu_id, db=db)
    model = DishOut.from_orm(model)
    Logger.debug(f'POST | {model.__class__.__name__}:{model}')
    return model


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=["dishes"])
async def get_dishes(
    target_menu_id: str,
    target_submenu_id: str,
    db: Session = Depends(get_db)
) -> List[DishOut]:
    model = await get_dishes_by_ids(menu_id=target_menu_id, submenu_id=target_submenu_id, db=db)
    Logger.disabled = True
    models = [await get_dish_by_ids(menu_id=target_menu_id,
                                    submenu_id=target_submenu_id,
                                    dish_id=dish.id,
                                    db=db) for dish in model]
    Logger.disabled = False
    Logger.debug(f'GET | {models}')
    return models


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{api_test_dish_id}', tags=["dishes"])
async def get_dish(
    target_menu_id: str,
    target_submenu_id: str,
    api_test_dish_id: str,
    db: Session = Depends(get_db)
) -> DishOut:
    model = await get_dish_by_ids(menu_id=target_menu_id,
                                  submenu_id=target_submenu_id,
                                  dish_id=api_test_dish_id,
                                  db=db)
    model = DishOut.from_orm(model)
    Logger.debug(f'GET | {model.__class__.__name__}:{model}')
    return model


@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{api_test_dish_id}', tags=["dishes"])
async def update_dish(
        target_menu_id: str,
        target_submenu_id: str,
        api_test_dish_id: str,
        dish: DishIn,
        db: Session = Depends(get_db)
) -> DishOut:
    model = await update_dish_by_ids(menu_id=target_menu_id,
                                     submenu_id=target_submenu_id,
                                     dish_id=api_test_dish_id,
                                     dish=dish,
                                     db=db)
    model = DishOut.from_orm(model)
    Logger.debug(f'PATCH | {model.__class__.__name__}:{model}')
    return model


@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{api_test_dish_id}', tags=["dishes"])
async def delete_submenu(
        target_menu_id: str,
        target_submenu_id: str,
        api_test_dish_id: str,
        db: Session = Depends(get_db)
) -> None:
    await delete_dish_by_ids(menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=api_test_dish_id, db=db)
    Logger.debug(f'DELETE | Dish {target_submenu_id} has successfully deleted from Submenu {target_submenu_id}')
