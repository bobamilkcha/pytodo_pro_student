import uuid
import pytest


def unique_user(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


# ---------------------------------------------------------------------------
# 1. POST /api/register
# ---------------------------------------------------------------------------

def test_api_reg_01_valid_registration(client):
    username = unique_user("reg")
    res = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert res.status_code == 201
    data = res.get_json()
    assert isinstance(data["id"], int)
    assert data["username"] == username


def test_api_reg_02_trimmed_username(client):
    username = unique_user("trim")
    res = client.post("/api/register", json={"username": f"  {username}  ", "password": "Password123"})
    assert res.status_code == 201
    assert res.get_json()["username"] == username


def test_api_reg_03_invalid_username(client):
    res = client.post("/api/register", json={"username": "ab", "password": "Password123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_04_invalid_password(client):
    res = client.post("/api/register", json={"username": unique_user("pw"), "password": "123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid password"}


def test_api_reg_05_missing_username(client):
    res = client.post("/api/register", json={"password": "Password123"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_06_missing_password(client):
    res = client.post("/api/register", json={"username": unique_user("nopw")})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid password"}


def test_api_reg_07_empty_json(client):
    res = client.post("/api/register", json={})
    assert res.status_code == 400
    assert res.get_json() == {"error": "invalid username"}


def test_api_reg_08_wrong_type_username(client):
    res = client.post("/api/register", json={"username": 12345, "password": "Password123"})
    assert res.status_code == 400


def test_api_reg_09_duplicate_username(client):
    username = unique_user("dup")
    first = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert first.status_code == 201

    second = client.post("/api/register", json={"username": username, "password": "Password123"})
    assert second.status_code in (400, 409)


# ---------------------------------------------------------------------------
# 2. POST /api/login
# ---------------------------------------------------------------------------

def test_api_log_01_valid_login(client):
    username = unique_user("login")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/login", json={"username": username, "password": "Password123"})
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data["id"], int)
    assert data["username"] == username

    # Verify session cookie grants access to protected endpoint
    tasks_res = client.get("/api/tasks")
    assert tasks_res.status_code == 200


def test_api_log_02_wrong_password(client):
    username = unique_user("wrongpw")
    client.post("/api/register", json={"username": username, "password": "Password123"})

    res = client.post("/api/login", json={"username": username, "password": "WrongPassword"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_03_nonexistent_user(client):
    res = client.post("/api/login", json={"username": "ghost_user_99999", "password": "Password123"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_04_missing_password(client):
    res = client.post("/api/login", json={"username": "some_user"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_05_empty_json(client):
    res = client.post("/api/login", json={})
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


def test_api_log_06_wrong_type_username(client):
    res = client.post("/api/login", json={"username": 12345, "password": "Password123"})
    assert res.status_code in (400, 401)


def test_api_log_07_non_json_body(client):
    res = client.post("/api/login", data="not json", content_type="text/plain")
    assert res.status_code == 401
    assert res.get_json() == {"error": "invalid credentials"}


# ---------------------------------------------------------------------------
# 3. GET /api/categories
# ---------------------------------------------------------------------------

def test_api_cat_01_public_categories_list(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)


def test_api_cat_02_categories_sorted_alphabetically(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    names = [c["name"] for c in res.get_json()]
    assert names == sorted(names)


def test_api_cat_03_unsupported_method(client):
    res = client.post("/api/categories")
    assert res.status_code == 405