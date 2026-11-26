"""
Week 6 - Automated state transition tests (from Week 1).

Owner: QA/Test Lead
Source: 01_Black_Box/tc_state_transition.md

Automated here: TC-BB-060, 061, 062, 064, 065, 068 to 075, 077, 078, 079
(16 cases, the ones assigned to the QA/Test Lead in automation_candidates.md).

Not automated here:
    TC-BB-063  we have not decided what the app should do (login while logged in)
    TC-BB-066  low value (logout page while logged out)
    TC-BB-067  Back button, needs a real browser (defect D-036)
    TC-BB-076  confirm popup, needs a real browser (checked in the Selenium script)

How these tests work:
    - They use the Flask test client and a temporary database, so they do not
      touch pytodo_pro.db.
    - They go through the web pages (/login, /tasks/new, ...), like the manual cases.
    - Every test registers its own new user, so the tests do not depend on each
      other or on the run order.

Run from the project root:
    pytest 06_Automation_Regression/tests/api/test_state_transition.py -v
"""

import re
import uuid
from datetime import date, timedelta

import pytest

import app as app_module

PASSWORD = "testpass123"


@pytest.fixture
def isolated_client(tmp_path, monkeypatch):
    """Flask test client with a fresh temporary SQLite database."""
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "test_st.db"))
    monkeypatch.setitem(app_module.app.config, "TESTING", True)
    monkeypatch.setitem(app_module.app.config, "PROPAGATE_EXCEPTIONS", False)
    app_module.init_db()
    with app_module.app.test_client() as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def new_name():
    return "st_" + uuid.uuid4().hex[:8]


def register(client, username=None):
    """Register a new user on the web form. We are logged in afterwards."""
    username = username or new_name()
    client.post("/register", data={"username": username, "password": PASSWORD})
    return username


def log_in(client, username, password=PASSWORD):
    return client.post("/login", data={"username": username, "password": password})


def page(client, path="/"):
    return client.get(path).get_data(as_text=True)


def category_id(client, name):
    return next(c["id"] for c in client.get("/api/categories").get_json() if c["name"] == name)


def create_task(client, title, category=None, due=None):
    """Create a task on the web form and return its id."""
    data = {"title": title, "description": ""}
    if category:
        data["category_id"] = category_id(client, category)
    if due:
        data["due_date"] = due
    client.post("/tasks/new", data=data)
    return task_id(client, title)


def task_id(client, title):
    """Find a task id by title (None if the task is not in our list)."""
    for t in client.get("/api/tasks").get_json():
        if t["title"] == title:
            return t["id"]
    return None


def toggle(client, tid):
    return client.post(f"/tasks/{tid}/toggle")


def row_of(html, title):
    """The <tr> of the task list that contains this title, or None."""
    for row in re.findall(r"<tr class=.*?</tr>", html, re.S):
        if title in row:
            return row
    return None


def is_done_row(row):
    return "✓" in row and ">Done<" in row


def is_open_row(row):
    return "○" in row and ">Done<" not in row


def dashboard(client):
    """Read the five counters from the dashboard page."""
    values = re.findall(r'stat-value">(\d+)<', page(client, "/dashboard"))
    keys = ["total", "open", "overdue", "due_soon", "completed"]
    return dict(zip(keys, map(int, values)))


def days_from_today(n):
    return (date.today() + timedelta(days=n)).isoformat()


# ---------------------------------------------------------------------------
# Scenario A: getting into and out of a session (F-05)
# ---------------------------------------------------------------------------

def test_TC_BB_060_valid_login_reaches_logged_in(isolated_client):
    """TC-BB-060 (S1): a valid login lands on the task list and shows the top bar."""
    c = isolated_client
    name = register(c)
    c.get("/logout")

    res = log_in(c, name)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/")
    html = page(c)
    assert name in html
    assert "Dashboard" in html
    assert "Log out" in html


def test_TC_BB_061_register_goes_straight_to_logged_in(isolated_client):
    """TC-BB-061 (S2): registering logs us in and lands on the task list."""
    c = isolated_client
    name = new_name()

    res = c.post("/register", data={"username": name, "password": PASSWORD})

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/")
    html = page(c)
    assert name in html
    assert "Log out" in html


def test_TC_BB_062_logout_returns_to_anonymous(isolated_client):
    """TC-BB-062 (S6): logout lands on the login page and the top bar loses its links."""
    c = isolated_client
    register(c)

    res = c.get("/logout")

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/login")
    html = page(c, "/login")
    assert "Log out" not in html
    assert "Dashboard" not in html


# ---------------------------------------------------------------------------
# Scenario B: things that should not work (F-05)
# ---------------------------------------------------------------------------

def test_TC_BB_064_wrong_password_keeps_us_anonymous(isolated_client):
    """TC-BB-064 (S3): a wrong password shows an error and the task list stays blocked."""
    c = isolated_client
    name = register(c)
    c.get("/logout")

    res = log_in(c, name, "wrongpass999")

    assert res.status_code == 200
    assert "Invalid username or password." in res.get_data(as_text=True)
    after = c.get("/")
    assert after.status_code == 302
    assert after.headers["Location"].endswith("/login")


@pytest.mark.regression
@pytest.mark.parametrize("path", ["/dashboard", "/tasks/new", "/"])
def test_TC_BB_065_protected_pages_blocked_after_logout(isolated_client, path):
    """TC-BB-065 (S4): after logout, each protected page redirects to the login page."""
    c = isolated_client
    register(c)
    c.get("/logout")

    res = c.get(path)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/login")


def test_TC_BB_068_stale_page_action_after_logout(isolated_client):
    """TC-BB-068 (S9): a toggle from an old page after logout is refused and changes nothing."""
    c = isolated_client
    name = register(c)
    tid = create_task(c, "stale tab task")
    c.get("/logout")  # logout done in "another tab"

    res = toggle(c, tid)  # click on the old page

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/login")
    log_in(c, name)
    row = row_of(page(c), "stale tab task")
    assert row is not None and is_open_row(row)


# ---------------------------------------------------------------------------
# Scenario C: normal task life cycle (F-12, F-10, F-13)
# ---------------------------------------------------------------------------

def test_TC_BB_069_create_task_starts_as_open(isolated_client):
    """TC-BB-069 (T1): a new task is Open, shows Upcoming, and raises Total and Open by 1."""
    c = isolated_client
    register(c)
    before = dashboard(c)

    create_task(c, "ST open task", category="Study", due=days_from_today(5))

    row = row_of(page(c), "ST open task")
    assert row is not None
    assert is_open_row(row)
    assert ">Upcoming<" in row
    assert "Study" in row
    after = dashboard(c)
    assert after["total"] == before["total"] + 1
    assert after["open"] == before["open"] + 1
    assert after["completed"] == before["completed"]


@pytest.mark.regression
def test_TC_BB_070_open_to_done(isolated_client):
    """TC-BB-070 (T2): toggling an Open task makes it Done and updates the dashboard."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST open task", due=days_from_today(5))
    before = dashboard(c)

    toggle(c, tid)

    row = row_of(page(c), "ST open task")
    assert is_done_row(row)
    assert row_of(page(c, "/?status=done"), "ST open task") is not None
    after = dashboard(c)
    assert after["open"] == before["open"] - 1
    assert after["completed"] == before["completed"] + 1
    assert after["total"] == before["total"]


@pytest.mark.regression
def test_TC_BB_071_done_back_to_open(isolated_client):
    """TC-BB-071 (T3): toggling a Done task reopens it and takes it out of Completed."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST open task", due=days_from_today(5))
    toggle(c, tid)
    before = dashboard(c)

    toggle(c, tid)

    row = row_of(page(c), "ST open task")
    assert is_open_row(row)
    assert ">Upcoming<" in row
    after = dashboard(c)
    assert after["open"] == before["open"] + 1
    assert after["completed"] == before["completed"] - 1


def test_TC_BB_072_edit_keeps_open_task_open(isolated_client):
    """TC-BB-072 (T4): editing an Open task changes the text but not its state."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST open task", category="Study", due=days_from_today(5))
    before = dashboard(c)

    c.post(f"/tasks/{tid}/edit", data={
        "title": "ST open task edited", "description": "",
        "category_id": category_id(c, "Work"), "due_date": days_from_today(5),
    })

    row = row_of(page(c), "ST open task edited")
    assert row is not None
    assert is_open_row(row)
    assert "Work" in row
    assert dashboard(c) == before


def test_TC_BB_073_edit_keeps_done_task_done(isolated_client):
    """TC-BB-073 (T5): editing a Done task changes the title but it stays Done."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST done task")
    toggle(c, tid)
    before = dashboard(c)

    c.post(f"/tasks/{tid}/edit", data={"title": "ST done task edited", "description": ""})

    row = row_of(page(c), "ST done task edited")
    assert row is not None
    assert is_done_row(row)
    assert dashboard(c)["completed"] == before["completed"]


@pytest.mark.regression
def test_TC_BB_074_delete_open_task(isolated_client):
    """TC-BB-074 (T6): deleting an Open task removes it and lowers Total and Open by 1."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST delete open")
    other = create_task(c, "ST keep me")
    before = dashboard(c)

    c.post(f"/tasks/{tid}/delete")

    html = page(c)
    assert row_of(html, "ST delete open") is None
    assert row_of(html, "ST keep me") is not None  # only the right task is deleted
    after = dashboard(c)
    assert after["total"] == before["total"] - 1
    assert after["open"] == before["open"] - 1
    assert other is not None


def test_TC_BB_075_delete_done_task(isolated_client):
    """TC-BB-075 (T7): deleting a Done task lowers Total and Completed by 1, Open is unchanged."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST delete done")
    toggle(c, tid)
    before = dashboard(c)

    c.post(f"/tasks/{tid}/delete")

    assert row_of(page(c), "ST delete done") is None
    after = dashboard(c)
    assert after["total"] == before["total"] - 1
    assert after["completed"] == before["completed"] - 1
    assert after["open"] == before["open"]


# ---------------------------------------------------------------------------
# Scenario D: things that should not change a task (F-12, F-10)
# ---------------------------------------------------------------------------

def test_TC_BB_077_toggle_on_deleted_task(isolated_client):
    """TC-BB-077 (T9): toggling a task that is already deleted does not crash or add a task."""
    c = isolated_client
    register(c)
    tid = create_task(c, "ST stale")
    c.post(f"/tasks/{tid}/delete")
    total_before = dashboard(c)["total"]

    res = toggle(c, tid)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/")
    assert row_of(page(c), "ST stale") is None
    assert dashboard(c)["total"] == total_before


def test_TC_BB_078_edit_page_of_deleted_task(isolated_client):
    """TC-BB-078 (T10): the edit page of a deleted task does not crash and shows no form.

    The app sends us back to the list with no message. Whether a message is
    needed is a usability question, so we only check the app does not crash.
    """
    c = isolated_client
    register(c)
    tid = create_task(c, "ST gone")
    c.post(f"/tasks/{tid}/delete")

    res = c.get(f"/tasks/{tid}/edit")

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/")
    assert "Save Changes" not in res.get_data(as_text=True)


def test_TC_BB_079_edit_page_of_another_users_task(isolated_client):
    """TC-BB-079 (T11): another user cannot open or change our task through the edit URL."""
    c = isolated_client
    owner = register(c)
    tid = create_task(c, "ST private task")
    c.get("/logout")
    register(c)  # a second, new user

    res = c.get(f"/tasks/{tid}/edit")
    c.post(f"/tasks/{tid}/edit", data={"title": "hacked", "description": ""})

    assert res.status_code == 302
    assert "ST private task" not in res.get_data(as_text=True)
    c.get("/logout")
    log_in(c, owner)
    html = page(c)
    assert row_of(html, "ST private task") is not None
    assert "hacked" not in html
