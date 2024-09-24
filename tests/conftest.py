from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from passlib.context import CryptContext
import pytest
import alembic

import config
from database import get_db
from main import app
from users.models import UserDB
from payments.models import Payment, Product
from database import Base


TEST_SQLALCHEMY_DB_URL = "postgresql+psycopg2://test_postgres:test_postgres@test_db:5432/test_postgres"
test_engine = create_engine(TEST_SQLALCHEMY_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


Base.metadata.create_all(bind=test_engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope='function', autouse=True)
def test_session():
    db_session = TestSessionLocal()
    connection = db_session.connection()
    transaction = connection.begin_nested()
    yield db_session
    transaction.rollback()
    db_session.close()


@pytest.fixture(scope='function')
def client(test_session):
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


def get_password_hash(password: str):
    return pwd_context.hash(password)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def create_test_user(test_session):
    test_user = UserDB(
        email="testuser@example.com",
        hashed_password=get_password_hash("fakehashedpassword"),
    )
    test_session.add(test_user)
    test_session.commit()
    yield test_user
