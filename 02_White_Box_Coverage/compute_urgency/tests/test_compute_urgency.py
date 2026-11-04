"""
White-box unit tests for compute_urgency (helpers.py, lines 12-39).

Owner: Defect & Metrics Coordinator
Feature: F-14 Task urgency
Technique: statement + branch coverage (V(G) = 5)

Decisions in the code:
  B1  line 26  if today is None
  B2  line 28  if not due_date_str
  B3  line 33  if due <= today
  B4  line 37  if delta_days <= 2

One test function = one test case ID, so results trace back to the
test case table in 02_White_Box_Coverage/compute_urgency.md.

Run from the project root (the folder that holds helpers.py):
  pytest 02_White_Box_Coverage/compute_urgency/tests/test_compute_urgency.py \
         --cov=helpers --cov-branch --cov-report=term-missing --cov-report=html
"""

import os
import sys
from datetime import date, timedelta

import pytest

# Make helpers.py / app.py importable when pytest runs from any folder.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers import compute_urgency  # noqa: E402

# Fixed "today" so results never depend on the day the tests are run.
TODAY = date(2026, 11, 10)


def iso(d):
    """Turn a date into the "YYYY-MM-DD" string the function expects."""
    return d.strftime("%Y-%m-%d")


# --- B2 True: no due date -------------------------------------------------

def test_wb_f14_01_none_due_date():
    """TC-WB-F14-01: None as due date -> "No due date" (B2 True)."""
    assert compute_urgency(None, today=TODAY) == "No due date"


def test_wb_f14_02_empty_string_due_date():
    """TC-WB-F14-02: empty string as due date -> "No due date" (B2 True)."""
    assert compute_urgency("", today=TODAY) == "No due date"


# --- B3 True: due date on or before today ---------------------------------

def test_wb_f14_03_past_date_is_overdue():
    """TC-WB-F14-03: due yesterday -> "Overdue" (B3 True, due < today)."""
    assert compute_urgency(iso(TODAY - timedelta(days=1)), today=TODAY) == "Overdue"


def test_wb_f14_04_due_today_label():
    """TC-WB-F14-04: due today -> "Due Today" per docstring/README.

    Expected to FAIL. Line 33 uses `due <= today`, so a task due today
    takes the Overdue path. There is no "Due Today" branch in the code.
    Linked defect: D-001.
    """
    assert compute_urgency(iso(TODAY), today=TODAY) == "Due Today"


# --- B3 False, B4 True: Due Soon -----------------------------------------

def test_wb_f14_05_one_day_away_is_due_soon():
    """TC-WB-F14-05: due tomorrow -> "Due Soon" (B3 False, B4 True)."""
    assert compute_urgency(iso(TODAY + timedelta(days=1)), today=TODAY) == "Due Soon"


def test_wb_f14_06_two_days_away_is_due_soon():
    """TC-WB-F14-06: due in 2 days -> "Due Soon" (B4 True, upper boundary)."""
    assert compute_urgency(iso(TODAY + timedelta(days=2)), today=TODAY) == "Due Soon"


# --- B4 False: Upcoming ---------------------------------------------------

def test_wb_f14_07_three_days_away_is_upcoming():
    """TC-WB-F14-07: due in 3 days -> "Upcoming" (B4 False, first value past boundary)."""
    assert compute_urgency(iso(TODAY + timedelta(days=3)), today=TODAY) == "Upcoming"


# --- B1 True: default today ----------------------------------------------

def test_wb_f14_08_default_today_used_when_not_given():
    """TC-WB-F14-08: no `today` argument -> function uses date.today() (B1 True)."""
    far_future = iso(date.today() + timedelta(days=30))
    assert compute_urgency(far_future) == "Upcoming"


# --- Line 31: bad input (exception path) ----------------------------------

@pytest.mark.parametrize("bad_value", ["04-11-2026", "abc", "2026-02-30", " "])
def test_wb_f14_09_bad_format_raises_value_error(bad_value):
    """TC-WB-F14-09: badly formatted or impossible date -> ValueError at line 31.

    The spec gives no rule for bad input. This test records what the code
    really does: strptime is not wrapped in try/except, so it raises.
    See TC-WB-F14-10 for the impact on the running app.
    """
    with pytest.raises(ValueError):
        compute_urgency(bad_value, today=TODAY)


# --- Impact check: does the unhandled ValueError reach the user? -----------

def test_wb_f14_10_bad_due_date_via_api_breaks_task_list(tmp_path, monkeypatch):
    """TC-WB-F14-10: a bad due_date saved through the API should not break the app.

    Expected: the API rejects the bad date (400), or the task list still loads (200).
    Expected to FAIL: POST /api/tasks stores any string, then GET /api/tasks
    calls compute_urgency on it (via row_to_task) and returns HTTP 500.
    The JSON API is used because it needs no HTML templates.
    """
    import app as app_module

    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "test.db"))
    app_module.app.config["TESTING"] = False  # let Flask return 500 instead of re-raising
    app_module.app.config["PROPAGATE_EXCEPTIONS"] = False
    app_module.init_db()

    client = app_module.app.test_client()
    reg = client.post("/api/register", json={"username": "wb_tester", "password": "password123"})
    assert reg.status_code == 201

    # Control: the task list works before the bad task exists.
    assert client.get("/api/tasks").status_code == 200

    create = client.post("/api/tasks", json={"title": "Bad date task", "due_date": "04-11-2026"})
    listing = client.get("/api/tasks")

    assert create.status_code == 400 or listing.status_code == 200, (
        f"API create returned HTTP {create.status_code}; "
        f"task list then returned HTTP {listing.status_code}"
    )
