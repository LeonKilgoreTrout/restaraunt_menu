from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy
import uuid

from app.backend.database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    submenus = relationship('Submenu', passive_deletes=True)


class Submenu(Base):
    __tablename__ = 'submenus'
    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    dishes = relationship('Dish', passive_deletes=True)
    menu_id = sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey('menus.id', ondelete='CASCADE'))


class Dish(Base):
    __tablename__ = 'dishes'
    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    price = sqlalchemy.Column(sqlalchemy.String, index=True)
    submenu_id = sqlalchemy.Column(UUID(as_uuid=True), sqlalchemy.ForeignKey('submenus.id', ondelete='CASCADE'))
