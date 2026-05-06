import pytest
from fastapi.testclient import TestClient
from main import app, items_db, users_db, next_item_id, next_user_id

@pytest.fixture(scope="function")
def clean_db():
    """Очистка базы данных перед каждым тестом"""
    items_db.clear()
    users_db.clear()
    global next_item_id, next_user_id
    next_item_id = 1
    next_user_id = 1
    yield
    items_db.clear()
    users_db.clear()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)