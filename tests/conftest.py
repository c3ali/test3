"""
Configuration pytest et fixtures pour les tests.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database import Base, get_db
from app.main import app

# Créer une base de données SQLite en mémoire pour les tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture pour la session de base de données de test."""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """Fixture pour le client de test FastAPI."""
    from fastapi.testclient import TestClient

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
