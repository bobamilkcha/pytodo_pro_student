import uuid
import pytest


def unique_user(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


# ---------------------------------------------------------------------------
# 1. POST /api/register (API-REG-01 to API-REG-09)
# ---------------------------------------------------------------------------

def test_api_reg_01_valid_registration(client):
    """API-REG-01 / TC-BB-001: Valid user registration returns 201."""
    username = unique_user("reg")
    res = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert res.status_code == 201
    data = res.get_json()
    assert isinstance(data["id"], int)
    assert data["username"] == username


def test_api_reg_02_trimmed_username(client):
    """API-REG-02: Leading and trailing whitespace in username is stripped."""
    username = unique_user("trim")
    res = client.post("/api/register", json={"username": f"  {username}  ", "password": "Password123"})
    assert res.status_code == 201
    assert res.get_json()["username"] == username


def test_api_reg_03_invalid_username(client):
    """API-REG-03: Username shorter than 3 characters returns 400."""
    res = client.post("/api/register", json={"username": "ab", "password": "Password123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_04_invalid_password(client):
    """API-REG-04: Password below minimum length returns 400."""
    res = client.post("/api/register", json={"username": unique_user("pw"), "password": "123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid password"}


def test_api_reg_05_missing_username(client):
    """API-REG-05: Missing username field returns 400."""
    res = client.post("/api/register", json={"password": "Password123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_06_missing_password(client):
    """API-REG-06: Missing password field returns 400."""
    res = client.post("/api/register", json={"username": unique_user("nopw")})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid password"}


def test_api_reg_07_empty_json(client):
    """API-REG-07: Empty JSON payload returns 400."""
    res = client.post("/api/register", json={})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_08_wrong_type_username(client):
    """API-REG-08 (Defect D-019): Non-string username returns 400 instead of 500."""
    res = client.post("/api/register", json={"username": 12345, "password": "Password123"})
    assert res.status_code == 400


@pytest.mark.regression
def test_api_reg_09_duplicate_username(client):
    """API-REG-09 / TC-BB-002 (Defect D-013): Duplicate username must be rejected."""
    username = unique_user("dup")
    first = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert first.status_code == 201

    second = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert second.status_code in (400, 409)


# ---------------------------------------------------------------------------
# 2. POST /api/login (API-LOG-01 to API-LOG-07)
# ---------------------------------------------------------------------------

def test_api_log_01_valid_login(client):
    """API-LOG-01: Valid credentials return 200 and establish an authenticated session."""
    username = unique_user("login")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/login", json={"username": username, "password": "Password123"})
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data["id"], int)
    assert data["username"] == username

    tasks_res = client.get("/api/tasks")
    assert tasks_res.status_code == 200


def test_api_log_02_wrong_password(client):
    """API-LOG-02 / TC-BB-003: Wrong password returns 401."""
    username = unique_user("wrongpw")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/login", json={"username": username, "password": "WrongPassword"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_03_nonexistent_user(client):
    """API-LOG-03: Unknown username returns 401."""
    res = client.post("/api/login", json={"username": "ghost_user_99999", "password": "Password123"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_04_missing_password(client):
    """API-LOG-04: Missing password field returns 401."""
    res = client.post("/api/login", json={"username": "some_user"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_05_empty_json(client):
    """API-LOG-05: Empty JSON payload returns 401."""
    res = client.post("/api/login", json={})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_06_wrong_type_username(client):
    """API-LOG-06 (Defect D-019): Non-string username returns 400 or 401 instead of 500."""
    res = client.post("/api/login", json={"username": 12345, "password": "Password123"})
    assert res.status_code in (400, 401)


def test_api_log_07_non_json_body(client):
    """API-LOG-07: Non-JSON request body returns 401."""
    res = client.post("/api/login", data="not json", content_type="text/plain")
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


# ---------------------------------------------------------------------------
# 3. Week 1 BVA Task Title Boundary (TC-BB-BVA-F08-01 & F08-02)
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_tc_bb_bva_f08_01_empty_task_title(client):
    """TC-BB-BVA-F08-01: Empty task title (0 chars) must be rejected with 400."""
    username = unique_user("bva_task")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/tasks", json={"title": ""})
    assert res.status_code == 400


def test_tc_bb_bva_f08_02_single_char_task_title(client):
    """TC-BB-BVA-F08-02: Single-character task title (1 char minimum) must be accepted."""
    username = unique_user("bva_task")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/tasks", json={"title": "A"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "A"