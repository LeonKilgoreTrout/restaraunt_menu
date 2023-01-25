from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.backend.database import Base, SessionLocal, engine
from app.backend.models import Menu, Submenu, Dish
from app.backend.schemas import *


__all__ = ['get_db', 'get_menu_by_id', 'add_new_menu', 'update_menu_by_id', 'delete_menu_by_id', 'get_all_menus',
           'add_new_submenu', 'get_submenus_by_menu_id', 'get_submenu_by_ids', 'update_submenu_by_ids',
           'delete_submenu_by_ids', 'add_new_dish', 'get_dishes_by_ids', 'get_dish_by_ids', 'update_dish_by_ids',
           'delete_dish_by_ids']


def create_tables():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def add_new_menu(
        menu: MenuIn,
        db: Session
):
    menu = Menu(**menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


async def get_menu_by_id(
        id: str,
        db: Session
):
    response = db.query(Menu).filter(Menu.id == id).first()
    if response is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return response


async def update_menu_by_id(
        id: str,
        menu: MenuIn,
        db: Session
):
    old_menu = await get_menu_by_id(id=id, db=db)
    for attr in menu.__fields__.keys():
        exec(f'old_menu.{attr} = menu.{attr}')
    db.commit()
    db.refresh(old_menu)

    return old_menu


async def delete_menu_by_id(
        id: str,
        db: Session
) -> None:
    # checks that such menu exist
    await get_menu_by_id(id=id, db=db)
    db.query(Menu).filter(Menu.id == id).delete()
    db.commit()


async def get_all_menus(
        db: Session
):
    return db.query(Menu).all()


async def add_new_submenu(
        submenu: SubmenuIn,
        menu_id: str,
        db: Session
):
    submenu = Submenu(**submenu.dict())
    submenu.menu_id = menu_id
    db.add(submenu)
    # checks that such menu exist
    await get_menu_by_id(id=menu_id, db=db)
    db.commit()
    db.refresh(submenu)
    return submenu


async def get_submenus_by_menu_id(
        menu_id: str,
        db: Session
):
    # checks that such menu exist
    await get_menu_by_id(id=menu_id, db=db)
    response = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    return response


async def get_submenu_by_ids(
        menu_id: str,
        submenu_id: str,
        db: Session
):
    # checks that such menu exist
    await get_menu_by_id(id=menu_id, db=db)
    response = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if response is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return response


async def update_submenu_by_ids(
        menu_id: str,
        submenu_id: str,
        submenu: SubmenuIn,
        db: Session
):
    old_submenu = await get_submenu_by_ids(menu_id=menu_id, submenu_id=submenu_id, db=db)
    for attr in submenu.__fields__.keys():
        exec(f'old_submenu.{attr} = submenu.{attr}')
    db.commit()
    db.refresh(old_submenu)

    return old_submenu


async def delete_submenu_by_ids(
        menu_id: str,
        submenu_id: str,
        db: Session
):
    # checks that such submenu exist
    await get_submenu_by_ids(menu_id=menu_id, submenu_id=submenu_id, db=db)
    db.query(Submenu).filter(Submenu.id == submenu_id).delete(synchronize_session='fetch')
    db.commit()


async def add_new_dish(
        dish: DishIn,
        menu_id: str,
        submenu_id: str,
        db: Session
):
    dish = Dish(**dish.dict())
    dish.submenu_id = submenu_id
    db.add(dish)

    # checks that such submenu exists
    await get_submenu_by_ids(menu_id=menu_id, submenu_id=submenu_id, db=db)
    # checks that such menu exists
    await get_menu_by_id(id=menu_id, db=db)

    db.commit()
    db.refresh(dish)
    return dish


async def get_dishes_by_ids(
        menu_id: str,
        submenu_id: str,
        db: Session
):
    # checks that such menu exists
    await get_menu_by_id(id=menu_id, db=db)
    # FIXME: one postman test failes while running with line below
    # await get_submenu_by_ids(menu_id=menu_id, submenu_id=submenu_id, db=db) # checks that such submenu exists
    response = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    return response


async def get_dish_by_ids(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session
):
    # checks that such menu exist
    await get_menu_by_id(id=menu_id, db=db)
    # checks that such submenu exist
    await get_submenu_by_ids(menu_id=menu_id, submenu_id=submenu_id, db=db)
    response = db.query(Dish).filter(Dish.id == dish_id).first()
    if response is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return response


async def update_dish_by_ids(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish: DishIn,
        db: Session
):
    old_dish = await get_dish_by_ids(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
    for attr in dish.__fields__.keys():
        exec(f'old_dish.{attr} = dish.{attr}')
    db.commit()
    db.refresh(old_dish)

    return old_dish


async def delete_dish_by_ids(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session
):
    # checks that dish with such dish_id, submenu_id and menu_id exists
    await get_dish_by_ids(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
    db.query(Dish).filter(Dish.id == dish_id).delete(synchronize_session='fetch')
    db.commit()
