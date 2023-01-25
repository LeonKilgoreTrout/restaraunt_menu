from sqlalchemy.orm import relationship
import sqlalchemy
import uuid

from app.backend.database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = sqlalchemy.Column(sqlalchemy.String(length=36), primary_key=True, default=str(uuid.uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    submenus = relationship('Submenu', passive_deletes=True)


class Submenu(Base):
    __tablename__ = 'submenus'
    id = sqlalchemy.Column(sqlalchemy.String(length=36), primary_key=True, default=str(uuid.uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    dishes = relationship('Dish', passive_deletes=True)
    menu_id = sqlalchemy.Column(sqlalchemy.String(length=36), sqlalchemy.ForeignKey('menus.id', ondelete='CASCADE'))


class Dish(Base):
    __tablename__ = 'dishes'
    id = sqlalchemy.Column(sqlalchemy.String(length=36), primary_key=True, default=str(uuid.uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    price = sqlalchemy.Column(sqlalchemy.String, index=True)
    submenu_id = sqlalchemy.Column(sqlalchemy.String(length=36), sqlalchemy.ForeignKey('submenus.id', ondelete='CASCADE'))
