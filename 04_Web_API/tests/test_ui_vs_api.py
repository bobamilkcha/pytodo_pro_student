"""
UI vs API comparison tests (Week 4).

One test for each case TC-API-UI-01 to TC-API-UI-30 in
04_Web_API/ui_vs_api_comparison.md.

Each test checks the EXPECTED rule (the rule the web form is meant to follow),
not what the app does today. A failing test means the API does not follow the
shared rule. That can be a defect, so check the result before logging it.

We use the Flask test client, so there are no real network calls.
Each test gets its own temporary database, so the real pytodo_pro.db is not touched.

Run:  pytest 04_Web_API/tests/test_ui_vs_api.py -v
"""

import sys
import uuid
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import app as app_module  # noqa: E402

flask_app = app_module.app

PASSWORD = "Password123"


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def client(tmp_path, monkeypatch):
    """A test client that uses a fresh temporary database."""
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "ui_vs_api.db"))
    app_module.init_db()
    flask_app.config["TESTING"] = True
    # Turn a crash into a 500 response so the test fails on the status code.
    flask_app.config["PROPAGATE_EXCEPTIONS"] = False
    # No "with" block here. A "with" client keeps its request context open,
    # and a second client then shares it and hits a closed database.
    yield flask_app.test_client()
    flask_app.config["PROPAGATE_EXCEPTIONS"] = None


def new_client():
    """A second client with its own cookies (a different browser)."""
    return flask_app.test_client()


def unique_name(prefix="u"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def register(c, username=None, password=PASSWORD):
    """Register through the API. This also logs the client in."""
    username = username or unique_name()
    res = c.post("/api/register", json={"username": username, "password": password})
    return username, res


def logged_in_client():
    """A client that is already registered and logged in."""
    c = new_client()
    username, res = register(c)
    assert res.status_code == 201
    return c, username


def make_task(c, **fields):
    body = {"title": "seed task"}
    body.update(fields)
    res = c.post("/api/tasks", json=body)
    assert res.status_code == 201, res.get_data(as_text=True)
    return res.get_json()


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

def test_tc_api_ui_01_password_7_chars_rejected(client):
    _, res = register(client, password="1234567")
    assert res.status_code == 400


def test_tc_api_ui_02_password_8_chars_accepted(client):
    # Spec says min 8. We expect this to fail because the code needs more than 8 (D-004).
    _, res = register(client, password="12345678")
    assert res.status_code == 201


def test_tc_api_ui_03_password_9_chars_accepted(client):
    _, res = register(client, password="123456789")
    assert res.status_code == 201


def test_tc_api_ui_04_duplicate_username_rejected(client):
    name, first = register(client)
    assert first.status_code == 201
    _, second = register(new_client(), username=name)
    assert second.status_code in (400, 409)


def test_tc_api_ui_05_username_2_chars_rejected(client):
    _, res = register(client, username="ab")
    assert res.status_code == 400


def test_tc_api_ui_06_username_as_number_rejected(client):
    res = client.post("/api/register", json={"username": 12345, "password": PASSWORD})
    assert res.status_code == 400


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def test_tc_api_ui_07_login_empty_password_rejected(client):
    name, res = register(client)
    assert res.status_code == 201
    fresh = new_client()
    res = fresh.post("/api/login", json={"username": name, "password": ""})
    assert res.status_code in (400, 401)
    # and we are not logged in
    assert fresh.get("/api/tasks").status_code == 401


def test_tc_api_ui_08_login_wrong_password_rejected(client):
    name, res = register(client)
    assert res.status_code == 201
    fresh = new_client()
    res = fresh.post("/api/login", json={"username": name, "password": "WrongPassword1"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


# ---------------------------------------------------------------------------
# Create task
# ---------------------------------------------------------------------------

def test_tc_api_ui_09_create_title_empty_rejected(client):
    register(client)
    res = client.post("/api/tasks", json={"title": ""})
    assert res.status_code == 400


def test_tc_api_ui_10_create_title_only_spaces_rejected(client):
    register(client)
    res = client.post("/api/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_tc_api_ui_11_create_title_1_char_accepted(client):
    register(client)
    res = client.post("/api/tasks", json={"title": "A"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "A"


def test_tc_api_ui_12_create_title_500_chars_rejected(client):
    # The spec has no length rule. We assume a limit should exist (D-012),
    # so we expect 400. Change this test if the group decides there is no limit.
    register(client)
    res = client.post("/api/tasks", json={"title": "x" * 500})
    assert res.status_code == 400


def test_tc_api_ui_13_create_due_date_in_past_is_overdue(client):
    register(client)
    past = (date.today() - timedelta(days=30)).isoformat()
    res = client.post("/api/tasks", json={"title": "past", "due_date": past})
    assert res.status_code == 201
    assert res.get_json()["urgency"] == "Overdue"


def test_tc_api_ui_14_create_due_date_today_is_due_today(client):
    # Spec says "Due Today". We expect this to fail (D-001).
    register(client)
    today = date.today().isoformat()
    res = client.post("/api/tasks", json={"title": "today", "due_date": today})
    assert res.status_code == 201
    assert res.get_json()["urgency"] == "Due Today"


def test_tc_api_ui_15_create_due_date_wrong_format_rejected(client):
    register(client)
    res = client.post("/api/tasks", json={"title": "bad date", "due_date": "04-11-2026"})
    assert res.status_code == 400


def test_tc_api_ui_16_create_category_not_found_rejected(client):
    register(client)
    res = client.post("/api/tasks", json={"title": "bad category", "category_id": 999})
    assert res.status_code == 400


# ---------------------------------------------------------------------------
# Edit task
# ---------------------------------------------------------------------------

def test_tc_api_ui_17_edit_missing_task_gives_404(client):
    register(client)
    res = client.put("/api/tasks/999999", json={"title": "new title"})
    assert res.status_code == 404


def test_tc_api_ui_18_edit_title_empty_rejected(client):
    register(client)
    task = make_task(client)
    res = client.put(f"/api/tasks/{task['id']}", json={"title": ""})
    assert res.status_code == 400


def test_tc_api_ui_19_edit_other_users_task_gives_404(client):
    register(client)
    task = make_task(client, title="owner's task")
    other, _ = logged_in_client()
    res = other.put(f"/api/tasks/{task['id']}", json={"title": "changed by someone else"})
    assert res.status_code == 404
    # the title did not change
    assert client.get(f"/api/tasks/{task['id']}").get_json()["title"] == "owner's task"


# ---------------------------------------------------------------------------
# Toggle done (the API has no toggle endpoint, so we use PUT with "done")
# ---------------------------------------------------------------------------

def test_tc_api_ui_20_toggle_done_then_reopen(client):
    register(client)
    task = make_task(client)

    res = client.put(f"/api/tasks/{task['id']}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True
    assert res.get_json()["completed_at"] is not None

    res = client.put(f"/api/tasks/{task['id']}", json={"done": False})
    assert res.status_code == 200
    assert res.get_json()["done"] is False
    assert res.get_json()["completed_at"] is None


def test_tc_api_ui_21_toggle_missing_task_gives_404(client):
    register(client)
    res = client.put("/api/tasks/999999", json={"done": True})
    assert res.status_code == 404


def test_tc_api_ui_22_done_as_text_false_does_not_complete_task(client):
    register(client)
    task = make_task(client)
    res = client.put(f"/api/tasks/{task['id']}", json={"done": "false"})
    assert res.status_code == 400 or res.get_json()["done"] is False


# ---------------------------------------------------------------------------
# Delete task
# ---------------------------------------------------------------------------

def test_tc_api_ui_23_delete_missing_task_gives_404(client):
    # We expect this to fail: the API always returns 200.
    register(client)
    res = client.delete("/api/tasks/999999")
    assert res.status_code == 404


def test_tc_api_ui_24_delete_other_users_task_is_refused(client):
    # We expect this to fail: the API delete does not check the owner (TH-21).
    register(client)
    task = make_task(client, title="owner's task")
    other, _ = logged_in_client()
    res = other.delete(f"/api/tasks/{task['id']}")
    assert res.status_code in (403, 404)
    # the task is still there for its owner
    assert client.get(f"/api/tasks/{task['id']}").status_code == 200


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def test_tc_api_ui_25_search_underscore_is_plain_text(client):
    register(client)
    make_task(client, title="due_today")
    make_task(client, title="due today")
    res = client.get("/api/tasks", query_string={"q": "due_today"})
    assert res.status_code == 200
    assert [t["title"] for t in res.get_json()] == ["due_today"]


def test_tc_api_ui_26_search_percent_is_plain_text(client):
    register(client)
    make_task(client, title="100% done")
    make_task(client, title="100 done")
    res = client.get("/api/tasks", query_string={"q": "100%"})
    assert res.status_code == 200
    assert [t["title"] for t in res.get_json()] == ["100% done"]


def test_tc_api_ui_27_search_single_quote_is_plain_text(client):
    # We expect this to fail: the text is pasted into the SQL (TH-07).
    register(client)
    make_task(client, title="it's a task")
    res = client.get("/api/tasks", query_string={"q": "a'"})
    assert res.status_code == 200


# ---------------------------------------------------------------------------
# No login at all
# ---------------------------------------------------------------------------

def test_tc_api_ui_28_create_task_without_login_refused(client):
    res = client.post("/api/tasks", json={"title": "no login"})
    assert res.status_code == 401


def test_tc_api_ui_29_edit_task_without_login_refused(client):
    res = client.put("/api/tasks/1", json={"title": "no login"})
    assert res.status_code == 401


def test_tc_api_ui_30_delete_task_without_login_refused(client):
    res = client.delete("/api/tasks/1")
    assert res.status_code == 401
