from pydantic import BaseSettings
from yaml import Loader
from pathlib import Path
from functools import lru_cache
import yaml


class AppSettings(BaseSettings):

    title: str
    description: str
    version: str = "0.0.1"
    debug: bool


class PostgresSettings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_PORT: str
    DB_HOST: str
    POSTGRES_DB: str
    PGDATA: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'


settings_path = Path(__file__).parent / 'app_config.yaml'

with settings_path.open('r') as f:
    yaml_settings = yaml.load(f, Loader=Loader)


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings(**yaml_settings)


@lru_cache()
def get_pg_settings() -> PostgresSettings:
    return PostgresSettings()
