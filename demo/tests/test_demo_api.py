import pytest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from demo.app.database import Base, get_db
from demo.app.main import app, seed_products


@pytest.fixture(scope="session")
def test_db_path():
    """Create a temporary database file for testing."""
    temp_dir = tempfile.gettempdir()
    db_path = Path(temp_dir) / "test_demo.db"

    # Clean up any existing test database
    if db_path.exists():
        db_path.unlink()

    yield str(db_path)

    # Clean up after tests (don't fail if file is locked)
    try:
        if db_path.exists():
            db_path.unlink()
    except (PermissionError, OSError):
        pass


@pytest.fixture(scope="session")
def test_engine(test_db_path):
    """Create a test database engine."""
    engine = create_engine(f"sqlite:///{test_db_path}")
    Base.metadata.create_all(bind=engine)

    # Seed products once
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    seed_products(db)
    db.close()

    yield engine

    # Clean up engine connections
    engine.dispose()


@pytest.fixture
def client(test_engine):
    """Create a test client with overridden database dependency."""

    def override_get_db():
        SessionLocal = sessionmaker(bind=test_engine)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_health_endpoint(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_products_endpoint_returns_products(client) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_cart_and_checkout_flow(client) -> None:
    cart_response = client.post(
        "/cart",
        json={
            "session_id": "test_session_001",
            "product_id": 1,
            "quantity": 1,
        },
    )

    assert cart_response.status_code == 201

    checkout_response = client.post(
        "/checkout",
        json={
            "session_id": "test_session_001",
        },
    )

    assert checkout_response.status_code == 201
    assert checkout_response.json()["message"] == "Checkout completed successfully"
