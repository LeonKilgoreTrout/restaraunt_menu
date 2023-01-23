import sqlalchemy
from sqlalchemy.ext import declarative
from sqlalchemy import orm
from app.configs.configs import get_pg_settings

Settings = get_pg_settings()

engine = sqlalchemy.create_engine(Settings.DATABASE_URL)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()
