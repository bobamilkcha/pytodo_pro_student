"""
Week 6 - Automated Decision Table tests (from Week 1) and known-defect checks.

Owner: Nafiesa (Defect & Metrics Coordinator)
Source: 01_Black_Box/tc_defect_coordinator.md (Week 1, Decision Table technique)

Part A - Week 1 decision tables, now automated:
    TC-BB-F03-01..04  F-03 Login (web), 4 rules
    TC-BB-F11-01..04  F-11 Filter and search (web), 4 rules
    TC-BB-F14-01..04  F-14 Urgency badge, 4 rules (checked through the API,
                      which uses the same compute_urgency() as the web page)

Part B - Known-defect regression checks asked for in Week 6 task 6:
    REG-D004-01..03   8-character password (D-004): helper and web register route
    REG-D001-01..02   Task due today (D-001): helper and dashboard counter

These tests use the Flask test client (no browser) and a temporary database,
so they run on a fresh clone and do not touch pytodo_pro.db.

Tests that guard a known open defect are EXPECTED TO FAIL until the
developers fix that defect. A failure here means "the defect is still there".

Run from the repository root:
    pytest 06_Automation_Regression/tests/unit/test_reg_decision_table.py -v
"""

import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import app as app_module
from helpers import compute_urgency, is_valid_password

USERNAME = "ryulemontea"
PASSWORD = "Kimryulhensem"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "test_dt.db"))
    app_module.app.config["TESTING"] = True
    # Behave like the real server: an unhandled error becomes HTTP 500.
    app_module.app.config["PROPAGATE_EXCEPTIONS"] = False
    app_module.init_db()
    return app_module.app.test_client()


@pytest.fixture
def registered(client):
    """A client with the account ryulemontea registered, then logged out."""
    client.post("/api/register", json={"username": USERNAME, "password": PASSWORD})
    client.get("/logout")
    return client


@pytest.fixture
def logged_in(registered):
    registered.post("/login", data={"username": USERNAME, "password": PASSWORD})
    return registered


def category_id(client, name):
    return next(c["id"] for c in client.get("/api/categories").get_json() if c["name"] == name)


def add_task(client, title, category=None, due=None, done=False):
    body = {"title": title}
    if category:
        body["category_id"] = category_id(client, category)
    if due is not None:
        body["due_date"] = due
    task_id = client.post("/api/tasks", json=body).get_json()["id"]
    if done:
        client.put(f"/api/tasks/{task_id}", json={"done": True})
    return task_id


def days(n):
    return (date.today() + timedelta(days=n)).isoformat()


# ===========================================================================
# Part A1 - F-03 Login (web). Conditions: C1 user exists, C2 password correct
# ===========================================================================

@pytest.mark.regression
def test_tc_bb_f03_01_rule1_user_exists_correct_password(registered):
    """TC-BB-F03-01 (Rule 1: Y/Y): login succeeds and the user can open the task list."""
    res = registered.post("/login", data={"username": USERNAME, "password": PASSWORD})
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/")
    assert registered.get("/").status_code == 200


@pytest.mark.regression
def test_tc_bb_f03_02_rule2_user_exists_wrong_password(registered):
    """TC-BB-F03-02 (Rule 2: Y/N): login refused with an error message."""
    res = registered.post("/login", data={"username": USERNAME, "password": "Kimryulhensom"})
    assert res.status_code == 200
    assert b"Invalid username or password" in res.data


def test_tc_bb_f03_03_rule3_unknown_user_correct_password(registered):
    """TC-BB-F03-03 (Rule 3: N/Y): login refused with an error message."""
    res = registered.post("/login", data={"username": "ryulemonteaa", "password": PASSWORD})
    assert res.status_code == 200
    assert b"Invalid username or password" in res.data


def test_tc_bb_f03_04_rule4_unknown_user_wrong_password(registered):
    """TC-BB-F03-04 (Rule 4: N/N): login refused with an error message."""
    res = registered.post("/login", data={"username": "mingyuKim", "password": "Abcdefgh"})
    assert res.status_code == 200
    assert b"Invalid username or password" in res.data


# ===========================================================================
# Part A2 - F-11 Filter and search (web). Conditions: category, status, keyword
# ===========================================================================

@pytest.fixture
def filter_data(logged_in):
    add_task(logged_in, "Weekly Report", category="Work")
    add_task(logged_in, "Report draft done", category="Work", done=True)
    add_task(logged_in, "Buy groceries", category="Personal")
    add_task(logged_in, "Read chapter 3", category="Study", done=True)
    return logged_in


def test_tc_bb_f11_01_no_filters_shows_all(filter_data):
    """TC-BB-F11-01: Category All, Status All, no keyword -> all 4 tasks shown."""
    page = filter_data.get("/").data
    for title in (b"Weekly Report", b"Report draft done", b"Buy groceries", b"Read chapter 3"):
        assert title in page


@pytest.mark.regression
def test_tc_bb_f11_02_all_three_filters_combined(filter_data):
    """TC-BB-F11-02: Work + Open + "Report" -> only "Weekly Report"."""
    page = filter_data.get("/?category=Work&status=open&q=Report").data
    assert b"Weekly Report" in page
    assert b"Report draft done" not in page
    assert b"Buy groceries" not in page


def test_tc_bb_f11_03_status_done_only(filter_data):
    """TC-BB-F11-03: Status Done -> only the 2 done tasks."""
    page = filter_data.get("/?status=done").data
    assert b"Report draft done" in page
    assert b"Read chapter 3" in page
    assert b"Weekly Report" not in page
    assert b"Buy groceries" not in page


def test_tc_bb_f11_04_no_match_shows_empty_message(filter_data):
    """TC-BB-F11-04: Work + Open + "image scanner" -> no rows, empty-list message shown."""
    page = filter_data.get("/?category=Work&status=open&q=image+scanner").data
    assert b"No tasks match your filters." in page
    assert b"Weekly Report" not in page


# ===========================================================================
# Part A3 - F-14 Urgency badge. Conditions: done?, due date (none/past/today/future)
# ===========================================================================

def urgency(client, task_id):
    return client.get(f"/api/tasks/{task_id}").get_json()["urgency"]


def test_tc_bb_f14_01_open_task_no_due_date(logged_in):
    """TC-BB-F14-01: Open task with no due date -> "No due date"."""
    assert urgency(logged_in, add_task(logged_in, "Submit report")) == "No due date"


@pytest.mark.regression
def test_tc_bb_f14_02_open_task_due_today(logged_in):
    """TC-BB-F14-02: Open task due today -> "Due Today". EXPECTED TO FAIL: D-001."""
    assert urgency(logged_in, add_task(logged_in, "Mock Interview", due=days(0))) == "Due Today"


@pytest.mark.regression
def test_tc_bb_f14_03_open_task_due_tomorrow(logged_in):
    """TC-BB-F14-03: Open task due tomorrow -> "Due Soon"."""
    assert urgency(logged_in, add_task(logged_in, "Dental appointment", due=days(1))) == "Due Soon"


@pytest.mark.regression
def test_tc_bb_f14_04_done_task_due_yesterday(logged_in):
    """TC-BB-F14-04: Done task due yesterday -> "Done" (not "Overdue")."""
    task_id = add_task(logged_in, "Proposal decommissioning", due=days(-1), done=True)
    assert urgency(logged_in, task_id) == "Done"


# ===========================================================================
# Part B - Known-defect regression checks (Week 6 task 6)
# ===========================================================================

@pytest.mark.regression
@pytest.mark.parametrize(
    "password, expected",
    [
        ("1234567", False),     # 7 characters: below the limit
        ("12345678", True),     # 8 characters: exactly the limit. EXPECTED TO FAIL: D-004
        ("123456789", True),    # 9 characters: above the limit
    ],
)
def test_reg_d004_01_password_length_boundary(password, expected):
    """REG-D004-01: Spec says "at least 8 characters". Checks 7, 8 and 9 characters."""
    assert is_valid_password(password) is expected


@pytest.mark.regression
def test_reg_d004_02_web_register_accepts_8_char_password(client):
    """REG-D004-02: Web register with an 8-character password creates the account. EXPECTED TO FAIL: D-004."""
    res = client.post("/register", data={"username": "eight_chars", "password": "abcd1234"})
    assert res.status_code == 302, "8-character password was rejected by /register"


@pytest.mark.regression
def test_reg_d004_03_api_register_accepts_8_char_password(client):
    """REG-D004-03: API register with an 8-character password returns 201. EXPECTED TO FAIL: D-004."""
    res = client.post("/api/register", json={"username": "eight_api", "password": "abcd1234"})
    assert res.status_code == 201


@pytest.mark.regression
def test_reg_d001_01_helper_due_today():
    """REG-D001-01: compute_urgency() for today's date returns "Due Today". EXPECTED TO FAIL: D-001."""
    today = date(2026, 11, 25)
    assert compute_urgency("2026-11-25", today=today) == "Due Today"


@pytest.mark.regression
def test_reg_d001_02_dashboard_does_not_count_today_as_overdue(logged_in):
    """REG-D001-02: A task due today is not counted in the dashboard Overdue number. EXPECTED TO FAIL: D-001."""
    add_task(logged_in, "Due today", due=days(0))
    data = logged_in.get("/api/dashboard").get_json()
    assert data["overdue"] == 0
