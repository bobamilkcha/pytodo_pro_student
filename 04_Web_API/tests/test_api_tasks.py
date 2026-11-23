import sys
from datetime import datetime
from pathlib import Path
import pytest

# Allow importing app.py from the repository root
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create an isolated temporary SQLite database for every test run."""
    test_db = tmp_path / "test_api_tasks.db"
    monkeypatch.setattr(app_module, "DATABASE", str(test_db))
    app_module.app.config["TESTING"] = True
    app_module.init_db()
    with app_module.app.test_client() as c:
        yield c


def register_and_login(client, username="user_a_qa", password="Password123"):
    res = client.post("/api/register", json={"username": username, "password": password})
    assert res.status_code == 201
    return res.get_json()


# ===========================================================================
# Section 4: GET /api/tasks (7 tests)
# ===========================================================================

def test_api_tsk_getall_01_valid_default(client):
    register_and_login(client)
    client.post("/api/tasks", json={"title": "First task"})
    client.post("/api/tasks", json={"title": "Second task"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Second task"  # Ordered by id DESC


def test_api_tsk_getall_02_valid_filters(client):
    register_and_login(client)
    cats = {c["name"]: c["id"] for c in client.get("/api/categories").get_json()}
    client.post("/api/tasks", json={"title": "Annual Report Draft", "category_id": cats["Work"]})
    client.post("/api/tasks", json={"title": "Study Notes", "category_id": cats["Study"]})
    res = client.get("/api/tasks?category=Work&status=open&q=Report&page=0&per_page=5")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Annual Report Draft"


def test_api_tsk_getall_03_sql_injection_q(client):
    # User A creates a private task
    register_and_login(client, username="victim_user")
    client.post("/api/tasks", json={"title": "User A Secret Task"})

    # User B logs in and attempts SQL injection via ?q=
    client.post("/api/register", json={"username": "attacker_user", "password": "Password123"})
    res = client.get("/api/tasks?q=' OR '1'='1")
    assert res.status_code == 200
    data = res.get_json()
    assert all(t["title"] != "User A Secret Task" for t in data)


def test_api_tsk_getall_04_unclosed_quote_q(client):
    register_and_login(client)
    res = client.get("/api/tasks?q=test'")
    assert res.status_code == 200
    assert res.get_json() == []


def test_api_tsk_getall_05_missing_auth(client):
    res = client.get("/api/tasks")
    assert res.status_code == 401
    assert res.get_json() == {"error": "authentication required"}


def test_api_tsk_getall_06_wrong_type_pagination(client):
    register_and_login(client)
    res = client.get("/api/tasks?page=abc&per_page=xyz")
    assert res.status_code in (200, 400)


def test_api_tsk_getall_07_edge_high_page(client):
    register_and_login(client)
    client.post("/api/tasks", json={"title": "Only one"})
    res = client.get("/api/tasks?page=99&per_page=10")
    assert res.status_code == 200
    assert res.get_json() == []


# ===========================================================================
# Section 5: GET /api/tasks/<int:task_id> (5 tests)
# ===========================================================================

def test_api_tsk_getone_01_valid_own_task(client):
    register_and_login(client)
    created = client.post("/api/tasks", json={"title": "Single Task"}).get_json()
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    body = res.get_json()
    for key in ("id", "title", "description", "category_id", "category", "due_date", "done", "urgency", "completed_at", "created_at"):
        assert key in body


def test_api_tsk_getone_02_not_found(client):
    register_and_login(client)
    res = client.get("/api/tasks/99999")
    assert res.status_code == 404
    assert res.get_json() == {"error": "not found"}


def test_api_tsk_getone_03_missing_auth(client):
    res = client.get("/api/tasks/1")
    assert res.status_code == 401


def test_api_tsk_getone_04_wrong_type_id(client):
    register_and_login(client)
    res = client.get("/api/tasks/abc")
    assert res.status_code == 404


def test_api_tsk_getone_05_cross_user_idor(client):
    register_and_login(client, username="owner_user")
    task_id = client.post("/api/tasks", json={"title": "Private"}).get_json()["id"]

    client.post("/api/register", json={"username": "other_user", "password": "Password123"})
    res = client.get(f"/api/tasks/{task_id}")
    assert res.status_code == 404


# ===========================================================================
# Section 6: POST /api/tasks (8 tests)
# ===========================================================================

def test_api_tsk_post_01_valid_full(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={
        "title": "Submit STQA Week 4",
        "description": "API suite",
        "category_id": 3,
        "due_date": "2026-11-30",
    })
    assert res.status_code == 201
    assert res.get_json()["done"] is False


def test_api_tsk_post_02_valid_minimal(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"title": "Quick reminder"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["description"] == ""
    assert data["category_id"] is None
    assert data["due_date"] is None


def test_api_tsk_post_03_invalid_whitespace_title(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"title": "     "})
    assert res.status_code == 400
    assert res.get_json() == {"error": "title is required"}


def test_api_tsk_post_04_invalid_due_date_format(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"title": "Bad date test", "due_date": "not-a-date"})
    assert res.status_code == 400


def test_api_tsk_post_05_missing_title(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"description": "Missing title"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "title is required"}


def test_api_tsk_post_06_missing_auth(client):
    res = client.post("/api/tasks", json={"title": "Test"})
    assert res.status_code == 401


def test_api_tsk_post_07_wrong_type_title(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"title": 12345})
    assert res.status_code == 400


def test_api_tsk_post_08_edge_invalid_category_id(client):
    register_and_login(client)
    res = client.post("/api/tasks", json={"title": "Invalid category", "category_id": 9999})
    assert res.status_code == 400


# ===========================================================================
# Section 7: PUT /api/tasks/<int:task_id> (7 tests)
# ===========================================================================

def test_api_tsk_put_01_valid_update(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Old Title"}).get_json()["id"]
    res = client.put(f"/api/tasks/{task_id}", json={"title": "Updated Title", "due_date": "2026-12-05"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "Updated Title"


def test_api_tsk_put_02_valid_toggle_done(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Toggle Task"}).get_json()["id"]

    res_done = client.put(f"/api/tasks/{task_id}", json={"done": True})
    assert res_done.status_code == 200
    assert res_done.get_json()["urgency"] == "Done"
    assert res_done.get_json()["completed_at"] is not None

    res_open = client.put(f"/api/tasks/{task_id}", json={"done": False})
    assert res_open.status_code == 200
    assert res_open.get_json()["completed_at"] is None


def test_api_tsk_put_03_invalid_empty_title(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Keep Title"}).get_json()["id"]
    res = client.put(f"/api/tasks/{task_id}", json={"title": ""})
    assert res.status_code == 400


def test_api_tsk_put_04_not_found(client):
    register_and_login(client)
    res = client.put("/api/tasks/99999", json={"title": "Ghost"})
    assert res.status_code == 404


def test_api_tsk_put_05_missing_fields_noop(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Unchanged"}).get_json()["id"]
    res = client.put(f"/api/tasks/{task_id}", json={})
    assert res.status_code == 200
    assert res.get_json()["title"] == "Unchanged"


def test_api_tsk_put_06_wrong_type_done_string(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Bool Type Test"}).get_json()["id"]
    res = client.put(f"/api/tasks/{task_id}", json={"done": "false"})
    assert res.status_code == 400 or res.get_json()["done"] is False


def test_api_tsk_put_07_cross_user_idor(client):
    register_and_login(client, username="owner_put")
    task_id = client.post("/api/tasks", json={"title": "Owner Task"}).get_json()["id"]

    client.post("/api/register", json={"username": "attacker_put", "password": "Password123"})
    res = client.put(f"/api/tasks/{task_id}", json={"title": "Hacked"})
    assert res.status_code == 404


# ===========================================================================
# Section 8: DELETE /api/tasks/<int:task_id> (5 tests)
# ===========================================================================

def test_api_tsk_del_01_valid_delete(client):
    register_and_login(client)
    task_id = client.post("/api/tasks", json={"title": "Delete Me"}).get_json()["id"]
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    assert res.get_json() == {"result": "ok"}
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_api_tsk_del_02_invalid_not_found(client):
    register_and_login(client)
    res = client.delete("/api/tasks/99999")
    assert res.status_code == 404


def test_api_tsk_del_03_missing_auth(client):
    res = client.delete("/api/tasks/1")
    assert res.status_code == 401


def test_api_tsk_del_04_wrong_type_id(client):
    register_and_login(client)
    res = client.delete("/api/tasks/abc")
    assert res.status_code == 404


def test_api_tsk_del_05_cross_user_idor(client):
    register_and_login(client, username="owner_del")
    task_id = client.post("/api/tasks", json={"title": "Do Not Delete"}).get_json()["id"]

    client.post("/api/register", json={"username": "attacker_del", "password": "Password123"})
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code in (403, 404)


# ===========================================================================
# Section 9: GET /api/dashboard (4 tests)
# ===========================================================================

def test_api_dash_01_valid_mixed_metrics(client):
    register_and_login(client)
    today = datetime.now().strftime("%Y-%m-%d")
    client.post("/api/tasks", json={"title": "Overdue Task", "due_date": "2020-01-01"})
    client.post("/api/tasks", json={"title": "Due Soon Task", "due_date": today})
    done_id = client.post("/api/tasks", json={"title": "Done Task"}).get_json()["id"]
    client.put(f"/api/tasks/{done_id}", json={"done": True})

    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 3
    assert data["open"] == 2
    assert data["overdue"] == 1
    assert data["due_soon"] == 1
    assert data["completed_this_week"] == 1


def test_api_dash_02_valid_empty_metrics(client):
    register_and_login(client)
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    assert res.get_json() == {
        "total": 0,
        "open": 0,
        "overdue": 0,
        "due_soon": 0,
        "completed_this_week": 0,
    }


def test_api_dash_03_missing_auth(client):
    res = client.get("/api/dashboard")
    assert res.status_code == 401


def test_api_dash_04_edge_method_not_allowed(client):
    register_and_login(client)
    res = client.post("/api/dashboard")
    assert res.status_code == 405
    