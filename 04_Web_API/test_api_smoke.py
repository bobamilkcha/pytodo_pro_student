import sys
from pathlib import Path
import pytest

# Allow importing app.py from the repository root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_categories_returns_200(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_tasks_requires_auth(client):
    res = client.get("/api/tasks")
    assert res.status_code == 401