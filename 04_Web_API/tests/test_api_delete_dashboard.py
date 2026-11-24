"""
Week 4 - Extra API tests for DELETE /api/tasks/<id> and GET /api/dashboard.

Owner: Nafiesa (Defect & Metrics Coordinator)
Test case IDs: API-DD-01 to API-DD-10

These tests add to Aida's API-TSK-DEL-01..05 and API-DASH-01..04 in
test_api_tasks.py. They check the things those tests do not:
  - whether data is really lost after a cross-user delete (IDOR),
  - whether the dashboard only counts the logged-in user's tasks,
  - the date boundaries behind each dashboard counter (Due Soon, 7-day window).

Each test uses its own temporary database, so the tests do not depend on
pytodo_pro.db and can run on a fresh clone.

Run from the repository root:
    pytest 04_Web_API/tests/test_api_delete_dashboard.py -v
"""

import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import app as app_module

PASSWORD = "Password123"


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "test_delete_dashboard.db"
    monkeypatch.setattr(app_module, "DATABASE", str(path))
    app_module.app.config["TESTING"] = True
    # Behave like the real server: an unhandled error becomes HTTP 500.
    app_module.app.config["PROPAGATE_EXCEPTIONS"] = False
    app_module.init_db()
    return path


@pytest.fixture
def user_a(db_path):
    c = app_module.app.test_client()
    c.post("/api/register", json={"username": "user_a", "password": PASSWORD})
    return c


@pytest.fixture
def user_b(db_path):
    c = app_module.app.test_client()
    c.post("/api/register", json={"username": "user_b", "password": PASSWORD})
    return c


def create(client, title, due=None):
    body = {"title": title}
    if due is not None:
        body["due_date"] = due
    return client.post("/api/tasks", json=body).get_json()["id"]


def days(n):
    return (date.today() + timedelta(days=n)).isoformat()


def set_completed(task_id, days_ago):
    """Mark a task done with completed_at set N days in the past (direct DB seed)."""
    stamp = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
    with app_module.app.app_context():
        db = app_module.get_db()
        db.execute("UPDATE tasks SET done = 1, completed_at = ? WHERE id = ?", (stamp, task_id))
        db.commit()


# ---------------------------------------------------------------------------
# DELETE /api/tasks/<id>
# ---------------------------------------------------------------------------

def test_api_dd_01_cross_user_delete_loses_data(user_a, user_b):
    """API-DD-01: After User B sends DELETE for User A's task, User A can still GET the task (200)."""
    task_id = create(user_a, "A's private task")
    res_b = user_b.delete(f"/api/tasks/{task_id}")
    res_a = user_a.get(f"/api/tasks/{task_id}")
    print(f"B delete -> {res_b.status_code} {res_b.get_json()}; A get -> {res_a.status_code}")
    assert res_a.status_code == 200


def test_api_dd_02_delete_same_task_twice(user_a):
    """API-DD-02: Deleting the same task a second time -> 404 (it no longer exists)."""
    task_id = create(user_a, "Delete me twice")
    first = user_a.delete(f"/api/tasks/{task_id}")
    second = user_a.delete(f"/api/tasks/{task_id}")
    print(f"first -> {first.status_code}; second -> {second.status_code} {second.get_json()}")
    assert first.status_code == 200
    assert second.status_code == 404


def test_api_dd_03_delete_updates_dashboard(user_a):
    """API-DD-03: After deleting one of two tasks, dashboard total drops from 2 to 1."""
    keep = create(user_a, "Keep")
    gone = create(user_a, "Remove")
    before = user_a.get("/api/dashboard").get_json()["total"]
    user_a.delete(f"/api/tasks/{gone}")
    after = user_a.get("/api/dashboard").get_json()["total"]
    assert (before, after) == (2, 1)
    assert user_a.get(f"/api/tasks/{keep}").status_code == 200


# ---------------------------------------------------------------------------
# GET /api/dashboard
# ---------------------------------------------------------------------------

def test_api_dd_04_dashboard_counts_only_own_tasks(user_a, user_b):
    """API-DD-04: User B's 3 tasks are not counted in User A's dashboard (A total = 1)."""
    create(user_a, "A task")
    for i in range(3):
        create(user_b, f"B task {i}", days(-1))
    data = user_a.get("/api/dashboard").get_json()
    assert data["total"] == 1
    assert data["overdue"] == 0


def test_api_dd_05_done_task_not_overdue(user_a):
    """API-DD-05: A done task with a past due date is not counted as overdue or open."""
    tid = create(user_a, "Finished late", days(-5))
    user_a.put(f"/api/tasks/{tid}", json={"done": True})
    data = user_a.get("/api/dashboard").get_json()
    assert data["overdue"] == 0
    assert data["open"] == 0
    assert data["completed_this_week"] == 1


def test_api_dd_06_due_soon_upper_boundary(user_a):
    """API-DD-06: Due in 2 days counts as Due Soon; due in 3 days does not (BVA on the 2-day limit)."""
    create(user_a, "In 2 days", days(2))
    create(user_a, "In 3 days", days(3))
    data = user_a.get("/api/dashboard").get_json()
    assert data["due_soon"] == 1
    assert data["overdue"] == 0


def test_api_dd_07_overdue_lower_boundary(user_a):
    """API-DD-07: Due yesterday counts as Overdue; due tomorrow counts as Due Soon."""
    create(user_a, "Yesterday", days(-1))
    create(user_a, "Tomorrow", days(1))
    data = user_a.get("/api/dashboard").get_json()
    assert data["overdue"] == 1
    assert data["due_soon"] == 1


def test_api_dd_08_completed_exactly_7_days_ago(user_a):
    """API-DD-08: A task completed exactly 7 days ago is counted in completed_this_week (spec: last 7 days). Retest of D-005."""
    tid = create(user_a, "Done a week ago")
    set_completed(tid, 7)
    assert user_a.get("/api/dashboard").get_json()["completed_this_week"] == 1


def test_api_dd_09_completed_8_days_ago_not_counted(user_a):
    """API-DD-09: A task completed 8 days ago is NOT counted in completed_this_week."""
    tid = create(user_a, "Done 8 days ago")
    set_completed(tid, 8)
    assert user_a.get("/api/dashboard").get_json()["completed_this_week"] == 0


def test_api_dd_10_dashboard_with_bad_due_date(user_a):
    """API-DD-10: If a task with a bad due_date exists, the dashboard still loads (200). Effect of D-006."""
    user_a.post("/api/tasks", json={"title": "Bad date", "due_date": "31-12-2026"})
    res = user_a.get("/api/dashboard")
    print(f"dashboard -> {res.status_code}")
    assert res.status_code == 200
