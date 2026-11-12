import os
import sys
import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create an isolated Flask test client with a temporary SQLite database."""
    test_db = tmp_path / "test_pytodo.db"
    monkeypatch.setattr(app_module, "DATABASE", str(test_db))
    app_module.app.config["TESTING"] = True
    app_module.init_db()

    with app_module.app.app_context():
        db = app_module.get_db()
        # Create primary test user (id=1) and secondary user (id=2)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("aida", "hash1"))
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("other_user", "hash2"))
        db.commit()

    with app_module.app.test_client() as test_client:
        yield test_client


def login_as(client, user_id=1, username="aida"):
    """Helper to inject an authenticated user into the Flask session."""
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["username"] = username


def seed_tasks():
    """Insert sample tasks covering multiple categories, statuses, and users."""
    with app_module.app.app_context():
        db = app_module.get_db()
        work_id = app_module.get_category_id_by_name(db, "Work")
        study_id = app_module.get_category_id_by_name(db, "Study")

        tasks = [
            (1, "Submit Quarterly Report", "", work_id, "2026-11-20", 0, None, "2026-11-01T10:00:00"),
            (1, "Archive Old Invoices", "", work_id, "2026-11-05", 1, "2026-11-04 12:00:00", "2026-11-01T10:05:00"),
            (1, "Final Exam Revision", "", study_id, "2026-11-25", 0, None, "2026-11-01T10:10:00"),
            (2, "Secret Other User Task", "", work_id, "2026-11-20", 0, None, "2026-11-01T10:15:00"),
        ]
        db.executemany(
            "INSERT INTO tasks (user_id, title, description, category_id, due_date, done, completed_at, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            tasks,
        )
        db.commit()


# TC-WB-F11-01: Unauthenticated access redirected by @login_required_web
def test_index_unauthenticated_redirects(client):
    resp = client.get("/")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


# TC-WB-F11-02: No filters, empty task list (B1=F, B2=F, B3=F, B4=F, B5=F, B6=0 iterations)
def test_index_no_filters_empty_tasks(client):
    login_as(client, user_id=1)
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"No tasks match your filters." in resp.data


# TC-WB-F11-03: No filters, populated task list + user isolation (B6>=1 iterations)
def test_index_no_filters_returns_only_own_tasks(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Archive Old Invoices" in html
    assert "Final Exam Revision" in html
    assert "Secret Other User Task" not in html


# TC-WB-F11-04: Valid category filter (B1=T, B2=T)
def test_index_valid_category_filter(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?category=Study")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Final Exam Revision" in html
    assert "Submit Quarterly Report" not in html


# TC-WB-F11-05: Unknown/invalid category filter (B1=T, B2=F)
def test_index_unknown_category_filter_ignored(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?category=NonExistentCategory")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Final Exam Revision" in html


# TC-WB-F11-06: Status filter = done (B3=T)
def test_index_status_filter_done(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?status=done")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Archive Old Invoices" in html
    assert "Submit Quarterly Report" not in html


# TC-WB-F11-07: Status filter = open (B3=F, B4=T)
def test_index_status_filter_open(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?status=open")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Archive Old Invoices" not in html


# TC-WB-F11-08: Unrecognized status value (B3=F, B4=F)
def test_index_unknown_status_filter_ignored(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?status=archived")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Archive Old Invoices" in html


# TC-WB-F11-09: Search query q with surrounding whitespace (B5=T)
def test_index_search_query_filter(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?q=  Report  ")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Final Exam Revision" not in html


# TC-WB-F11-10: All filters combined simultaneously (B1=T, B2=T, B3=F, B4=T, B5=T, B6=T)
def test_index_combined_filters(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?category=Work&status=open&q=Quarterly")
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Archive Old Invoices" not in html
    assert "Final Exam Revision" not in html


# TC-WB-F11-11: SQL LIKE wildcard edge case ('%' matches all tasks even when none contain '%')
def test_index_search_sql_wildcard_unescaped(client):
    seed_tasks()
    login_as(client, user_id=1)
    resp = client.get("/?q=%25")  # URL-encoded '%'
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Final Exam Revision" in html