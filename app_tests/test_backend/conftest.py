import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.models import Base
from app.backend.services import get_db
from app.backend.main import app


DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
TestingSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
