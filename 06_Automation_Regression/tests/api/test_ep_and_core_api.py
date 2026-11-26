from pathlib import Path
import pytest
import app as app_module

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture
def isolated_client(tmp_path, monkeypatch):
    """Isolated Flask test client with a fresh temporary SQLite database."""
    test_db = tmp_path / "test_w6_api.db"
    monkeypatch.setattr(app_module, "DATABASE", str(test_db))
    monkeypatch.setitem(app_module.app.config, "TESTING", True)
    monkeypatch.setitem(app_module.app.config, "PROPAGATE_EXCEPTIONS", False)
    app_module.init_db()
    with app_module.app.test_client() as test_client:
        yield test_client


def register_and_login(client, username="aida_w6", password="Password123"):
    """Helper to register and authenticate a user session via API."""
    client.post("/api/register", json={"username": username, "password": password})
    res = client.post("/api/login", json={"username": username, "password": password})
    assert res.status_code == 200


# ---------------------------------------------------------------------------
# 1. EP & White-Box Core Route Tests
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_tc_bb_004_create_valid_task_api(isolated_client):
    """TC-BB-004 / API-TSK-POST-01: Valid task creation returns 201 and persists task."""
    register_and_login(isolated_client)
    res = isolated_client.post(
        "/api/tasks",
        json={"title": "Finish EP Test Design", "description": "Week 6"},
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "Finish EP Test Design"
    assert body["done"] is False


@pytest.mark.regression
def test_tc_bb_005_web_whitespace_title_rejected(isolated_client):
    """TC-BB-005 / TC-SEC-09 (Defect D-011): Web form must reject whitespace-only title."""
    register_and_login(isolated_client)
    isolated_client.post(
        "/tasks/new",
        data={"title": "     ", "description": "", "category_id": "", "due_date": ""},
    )
    tasks = isolated_client.get("/api/tasks").get_json()
    assert len(tasks) == 0


@pytest.mark.regression
def test_tc_wb_f11_10_combined_web_filters(isolated_client):
    """TC-WB-F11-10: Web task list filters by category, status, and search text together."""
    register_and_login(isolated_client)
    cats = {c["name"]: c["id"] for c in isolated_client.get("/api/categories").get_json()}

    isolated_client.post(
        "/api/tasks",
        json={"title": "Submit Quarterly Report", "category_id": cats["Work"]},
    )
    isolated_client.post(
        "/api/tasks",
        json={"title": "Final Exam Revision", "category_id": cats["Study"]},
    )

    res = isolated_client.get("/?category=Work&status=open&q=Quarterly")
    html = res.data.decode("utf-8")
    assert res.status_code == 200
    assert "Submit Quarterly Report" in html
    assert "Final Exam Revision" not in html


# ---------------------------------------------------------------------------
# 2. High-Risk API & Security Regression Tests
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_tc_wb_f14_10_bad_due_date_api_rejected(isolated_client):
    """TC-WB-F14-10 / API-TSK-POST-04 (Defect D-006): Malformed due_date must return 400, not 500."""
    register_and_login(isolated_client)
    res = isolated_client.post(
        "/api/tasks",
        json={"title": "Bad Date Task", "due_date": "04-11-2026"},
    )
    assert res.status_code == 400


@pytest.mark.regression
def test_api_tsk_put_03_empty_title_on_edit_rejected(isolated_client):
    """API-TSK-PUT-03 / TC-API-UI-18 (Defect D-022): PUT /api/tasks/<id> must reject empty title."""
    register_and_login(isolated_client)
    created = isolated_client.post("/api/tasks", json={"title": "Original Title"}).get_json()
    res = isolated_client.put(f"/api/tasks/{created['id']}", json={"title": ""})
    assert res.status_code == 400


@pytest.mark.regression
def test_tc_sec_07_sql_injection_in_search_handled(isolated_client):
    """TC-SEC-07 / API-TSK-GETALL-04 (Defect D-020): Single quote in search query must not cause SQL 500."""
    register_and_login(isolated_client)
    res = isolated_client.get("/api/tasks?q=test'")
    assert res.status_code == 200


@pytest.mark.regression
def test_tc_sec_21_cross_user_delete_blocked(isolated_client):
    """TC-SEC-21 / API-TSK-DEL-05 (Defect D-025): User B must not be able to delete User A's task."""
    register_and_login(isolated_client, username="owner_user")
    created = isolated_client.post("/api/tasks", json={"title": "Owner Private Task"}).get_json()

    register_and_login(isolated_client, username="attacker_user")
    res = isolated_client.delete(f"/api/tasks/{created['id']}")
    assert res.status_code in (403, 404)


@pytest.mark.regression
def test_tc_sec_05_stored_xss_escaped_in_task_list(isolated_client):
    """TC-SEC-05 (Defect D-010): Task title HTML/script tags must be escaped in web task list."""
    register_and_login(isolated_client)
    payload = "<script>alert('xss')</script>"
    isolated_client.post("/api/tasks", json={"title": payload})

    html = isolated_client.get("/").data.decode("utf-8")
    assert payload not in html


@pytest.mark.regression
def test_tc_sec_22_web_delete_enforces_owner_check(isolated_client):
    """TC-SEC-22: Web POST /tasks/<id>/delete blocks cross-user deletion."""
    register_and_login(isolated_client, username="web_owner")
    created = isolated_client.post("/api/tasks", json={"title": "Protected Web Task"}).get_json()

    register_and_login(isolated_client, username="web_other")
    isolated_client.post(f"/tasks/{created['id']}/delete")

    isolated_client.post("/api/login", json={"username": "web_owner", "password": "Password123"})
    check = isolated_client.get(f"/api/tasks/{created['id']}")
    assert check.status_code == 200


# ---------------------------------------------------------------------------
# 3. Week 3 Static HTML / CSS Regression Checks (Test Design Coordinator)
# ---------------------------------------------------------------------------

def test_gui_01_style_css_universal_box_sizing():
    """GUI-01 (Defect D-007): style.css line 1 must use universal '*' selector, not '-'."""
    first_line = (ROOT_DIR / "static" / "style.css").read_text(encoding="utf-8").splitlines()[0].strip()
    assert first_line.startswith("*")


def test_acc_01_form_labels_have_for_attribute(isolated_client):
    """GUI-02 / ACC-01 (Defect D-009): Form labels must associate with inputs via 'for' attribute."""
    html = isolated_client.get("/login").data.decode("utf-8")
    assert 'for="' in html


def test_acc_02_toggle_button_has_aria_label(isolated_client):
    """ACC-02 (Defect D-016): Task completion toggle button must provide an accessible aria-label."""
    register_and_login(isolated_client)
    isolated_client.post("/api/tasks", json={"title": "Accessibility Check Task"})
    html = isolated_client.get("/").data.decode("utf-8")
    assert "aria-label=" in html


def test_acc_09_viewport_meta_tag_present(isolated_client):
    """ACC-09 (Defect D-017): Pages must include <meta name='viewport'> for mobile reflow."""
    html = isolated_client.get("/login").data.decode("utf-8")
    assert 'name="viewport"' in html