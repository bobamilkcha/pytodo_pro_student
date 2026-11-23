import sys
from pathlib import Path
import pytest

# Allow importing app.py from the repository root
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Isolated temporary SQLite database for safe local security testing."""
    test_db = tmp_path / "test_security.db"
    monkeypatch.setattr(app_module, "DATABASE", str(test_db))
    app_module.app.config["TESTING"] = True
    app_module.init_db()
    with app_module.app.test_client() as c:
        yield c


def register_web(client, username="syasya_test1", password="Password123"):
    return client.post(
        "/register",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


# ===========================================================================
# SPOOFING (TH-01 to TH-04)
# ===========================================================================

def test_sec_01_th01_login_brute_force_rate_limit(client):
    """TH-01: Repeated failed logins should trigger rate limiting or lockout."""
    register_web(client, "syasya_test1", "Password123")
    client.get("/logout")

    statuses = []
    for _ in range(10):
        res = client.post(
            "/login",
            data={"username": "syasya_test1", "password": "WrongPassword99"},
        )
        statuses.append(res.status_code)

    assert any(s in (403, 429) for s in statuses), "No rate limit or lockout after 10 failed logins"


def test_sec_02_th02_duplicate_username_registration(client):
    """TH-02: Registering an existing username should be rejected."""
    register_web(client, "syasya_test1", "Password123")
    client.get("/logout")
    register_web(client, "syasya_test1", "DifferentPass123")

    with app_module.app.app_context():
        db = app_module.get_db()
        count = db.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", ("syasya_test1",)
        ).fetchone()[0]

    assert count == 1, f"Duplicate username allowed: {count} accounts created"


def test_sec_03_th03_hardcoded_secret_key_cookie_forgery(client):
    """TH-03: Hardcoded SECRET_KEY allows forging a valid session cookie for another user."""
    register_web(client, "syasya_test1", "Password123")
    client.get("/logout")
    register_web(client, "syasya_test2", "Password123")
    client.get("/logout")

    serializer = app_module.app.session_interface.get_signing_serializer(app_module.app)
    forged_cookie = serializer.dumps({"user_id": 2, "username": "syasya_test2"})
    client.set_cookie("session", forged_cookie)

    res = client.get("/")
    assert res.status_code == 302, "Forged cookie signed with hardcoded SECRET_KEY granted access"


def test_sec_04_th04_session_cookie_replay_after_logout(client):
    """TH-04: Captured session cookie should not remain valid after /logout."""
    register_web(client, "syasya_test1", "Password123")
    client.get("/logout")

    login_res = client.post(
        "/login", data={"username": "syasya_test1", "password": "Password123"}
    )
    set_cookie = login_res.headers.get("Set-Cookie", "")
    old_session = set_cookie.split(";")[0].split("=", 1)[1]

    client.get("/logout")
    client.set_cookie("session", old_session)
    res = client.get("/")
    assert res.status_code == 302, "Old session cookie still authenticated user after logout"


# ===========================================================================
# TAMPERING (TH-05 to TH-09)
# ===========================================================================

def test_sec_05_th05_stored_xss_in_task_title(client):
    """TH-05: HTML/script tags in task title should be escaped, not rendered raw."""
    register_web(client, "syasya_test1", "Password123")
    payload = "<script>alert(1)</script>"
    client.post("/tasks/new", data={"title": payload})

    res = client.get("/")
    assert payload.encode() not in res.data, "Unescaped <script> tag rendered via |safe filter"


def test_sec_06_th06_missing_csrf_token_on_task_form(client):
    """TH-06: State-changing POST forms should include CSRF protection."""
    register_web(client, "syasya_test1", "Password123")
    form_page = client.get("/tasks/new")
    assert b"csrf" in form_page.data.lower(), "No CSRF token found in /tasks/new form"


def test_sec_07_th07_api_search_sql_injection_syntax_error(client):
    """TH-07: Single quote in /api/tasks?q= should be safely parameterized."""
    register_web(client, "syasya_test1", "Password123")
    res = client.get("/api/tasks?q=a'")
    assert res.status_code == 200


def test_sec_08_th08_web_search_sql_wildcard_escaping(client):
    """TH-08: Literal % in web search should not match unrelated tasks."""
    register_web(client, "syasya_test1", "Password123")
    client.post("/tasks/new", data={"title": "100% Completed"})
    client.post("/tasks/new", data={"title": "Unrelated Task"})

    res = client.get("/?q=%")
    assert b"Unrelated Task" not in res.data, "Unescaped % wildcard matched all tasks"


def test_sec_09_th09_whitespace_title_server_validation(client):
    """TH-09: Server should reject whitespace-only task titles."""
    register_web(client, "syasya_test1", "Password123")
    res = client.post("/tasks/new", data={"title": "     "})
    assert res.status_code == 400, "Whitespace-only title was accepted and saved"


# ===========================================================================
# REPUDIATION (TH-10)
# ===========================================================================

def test_sec_10_th10_audit_trail_for_task_deletion(client):
    """TH-10: Destructive actions (task deletion) should leave an audit log record."""
    register_web(client, "syasya_test1", "Password123")
    client.post("/tasks/new", data={"title": "Audit Test Task"})
    client.post("/tasks/1/delete")

    with app_module.app.app_context():
        db = app_module.get_db()
        tables = [
            r[0]
            for r in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        ]

    assert any("audit" in t or "log" in t for t in tables), "No audit log table exists in database"


# ===========================================================================
# INFORMATION DISCLOSURE (TH-11 to TH-16)
# ===========================================================================

def test_sec_11_th11_debug_mode_disabled_in_source():
    """TH-11: Flask debug=True should not be hardcoded in app.py."""
    app_source = (ROOT_DIR / "app.py").read_text(encoding="utf-8")
    assert "debug=True" not in app_source, "app.run(debug=True) exposes Werkzeug debugger"


def test_sec_12_th12_no_store_cache_control_header(client):
    """TH-12: Authenticated pages should send Cache-Control: no-store to prevent Back-button leak."""
    register_web(client, "syasya_test1", "Password123")
    res = client.get("/dashboard")
    cache_control = res.headers.get("Cache-Control", "")
    assert "no-store" in cache_control.lower(), "Missing Cache-Control: no-store header on /dashboard"


def test_sec_13_th13_password_stored_as_salted_hash(client):
    """TH-13: User passwords in pytodo_pro.db must be hashed, never plaintext."""
    register_web(client, "syasya_test1", "Password123")
    with app_module.app.app_context():
        db = app_module.get_db()
        pw_hash = db.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("syasya_test1",)
        ).fetchone()[0]

    assert pw_hash != "Password123"
    assert pw_hash.startswith(("scrypt:", "pbkdf2:"))


def test_sec_14_th14_api_search_sqli_cross_user_data_leak(client):
    """TH-14: SQL injection in /api/tasks?q= must not leak another user's private tasks."""
    register_web(client, "syasya_test1", "Password123")
    client.post("/api/tasks", json={"title": "Test1 Private Secret"})
    client.get("/logout")

    register_web(client, "syasya_test2", "Password123")
    res = client.get("/api/tasks?q=' OR 1=1 --")
    tasks = res.get_json()
    assert all(t["title"] != "Test1 Private Secret" for t in tasks), "SQLi leaked another user's task"


def test_sec_15_th15_session_cookie_security_flags(client):
    """TH-15: Session cookie should include HttpOnly, SameSite, and Secure flags."""
    res = register_web(client, "syasya_test1", "Password123")
    cookie_header = res.headers.get("Set-Cookie", "")
    assert "HttpOnly" in cookie_header
    assert "SameSite" in cookie_header and "Secure" in cookie_header, "Missing SameSite/Secure flags"


def test_sec_16_th16_unauthenticated_categories_exposes_no_user_data(client):
    """TH-16: Unauthenticated /api/categories returns only non-sensitive category names."""
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert all(set(item.keys()) == {"id", "name"} for item in data)


# ===========================================================================
# DENIAL OF SERVICE (TH-17 to TH-20)
# ===========================================================================

def test_sec_17_th17_malformed_due_date_availability(client):
    """TH-17: Malformed due_date should be rejected rather than crashing / with 500."""
    register_web(client, "syasya_test1", "Password123")
    client.post("/tasks/new", data={"title": "Bad Date Task", "due_date": "04-11-2026"})
    res = client.get("/")
    assert res.status_code == 200


def test_sec_18_th18_unbounded_per_page_limit(client):
    """TH-18: API pagination per_page parameter should enforce a safe maximum cap."""
    register_web(client, "syasya_test1", "Password123")
    for i in range(25):
        client.post("/api/tasks", json={"title": f"Task {i}"})

    res = client.get("/api/tasks?per_page=1000")
    assert len(res.get_json()) <= 20, "Unbounded per_page returned all 25 tasks without cap"


def test_sec_19_th19_api_login_burst_throttling(client):
    """TH-19: Rapid sequential login requests should trigger throttling."""
    register_web(client, "syasya_test1", "Password123")
    client.get("/logout")

    statuses = [
        client.post("/api/login", json={"username": "syasya_test1", "password": "bad"}).status_code
        for _ in range(20)
    ]
    assert 429 in statuses, "All 20 rapid login attempts processed with no throttling"


def test_sec_20_th20_logout_requires_post_not_get(client):
    """TH-20: GET /logout should not terminate session (prevents cross-site image logout)."""
    register_web(client, "syasya_test1", "Password123")
    res = client.get("/logout")
    assert res.status_code == 405, "GET /logout terminated session without POST/CSRF protection"


# ===========================================================================
# ELEVATION OF PRIVILEGE (TH-21 to TH-22)
# ===========================================================================

def test_sec_21_th21_api_delete_cross_user_idor(client):
    """TH-21: User B must not be able to delete User A's task via DELETE /api/tasks/<id>."""
    register_web(client, "syasya_test1", "Password123")
    task_id = client.post("/api/tasks", json={"title": "Test1 Protected Task"}).get_json()["id"]
    client.get("/logout")

    register_web(client, "syasya_test2", "Password123")
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code in (403, 404), "IDOR: User B deleted User A's task via API"


def test_sec_22_th22_web_routes_enforce_task_ownership(client):
    """TH-22: User B must be blocked from editing, toggling, or deleting User A's task via web routes."""
    register_web(client, "syasya_test1", "Password123")
    client.post("/tasks/new", data={"title": "Test1 Web Task"})
    client.get("/logout")

    register_web(client, "syasya_test2", "Password123")
    client.get("/tasks/1/edit")
    client.post("/tasks/1/toggle")
    client.post("/tasks/1/delete")

    with app_module.app.app_context():
        db = app_module.get_db()
        row = db.execute("SELECT title, done FROM tasks WHERE id = 1").fetchone()

    assert row is not None and row["title"] == "Test1 Web Task" and row["done"] == 0