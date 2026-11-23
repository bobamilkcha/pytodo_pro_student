# Week 4: API Test Cases — Auth & Categories

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Endpoints Covered:** `POST /api/register`, `POST /api/login`, `GET /api/categories`  
**Test File:** `04_Web_API/tests/test_api_auth.py`  
**Summary:** 16 Passed, 3 Failed (3 defects identified)

---

## 1. `POST /api/register`

| Test ID | Test Type | Scenario | Request Body (JSON) | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-REG-01** | Valid | Register a new user with valid username and password | `{"username": "new_user1", "password": "Password123"}` | `201 Created`<br>JSON contains `"id"` (int) and `"username"` | `201 Created`; returned `id` and `username` as expected | **Pass** |
| **API-REG-02** | Valid (Edge) | Register with leading/trailing spaces in username | `{"username": "  trimmed_user  ", "password": "Password123"}` | `201 Created`<br>JSON returns trimmed `"username"` | `201 Created`; whitespace stripped properly | **Pass** |
| **API-REG-03** | Invalid Input | Username too short / invalid | `{"username": "ab", "password": "Password123"}` | `400 Bad Request`<br>`{"error": "invalid username"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-REG-04** | Invalid Input | Password too short / invalid | `{"username": "valid_user2", "password": "123"}` | `400 Bad Request`<br>`{"error": "invalid password"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-REG-05** | Missing Field | Missing `username` field | `{"password": "Password123"}` | `400 Bad Request`<br>`{"error": "invalid username"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-REG-06** | Missing Field | Missing `password` field | `{"username": "valid_user3"}` | `400 Bad Request`<br>`{"error": "invalid password"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-REG-07** | Missing Field | Empty JSON body `{}` | `{}` | `400 Bad Request`<br>`{"error": "invalid username"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-REG-08** | Wrong Data Type | Non-string `username` (integer) | `{"username": 12345, "password": "Password123"}` | `400 Bad Request` | Unhandled `AttributeError: 'int' object has no attribute 'strip'` at `app.py:318` | **Fail** |
| **API-REG-09** | Edge Condition | Duplicate username (already registered) | `{"username": "<existing>", "password": "Password123"}` | `400` or `409 Conflict` | Returned `201 Created` and inserted duplicate user | **Fail** |

---

## 2. `POST /api/login`

| Test ID | Test Type | Scenario | Request Body (JSON) | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-LOG-01** | Valid | Log in with valid existing credentials | `{"username": "<valid>", "password": "Password123"}` | `200 OK`; session allows access to `GET /api/tasks` | `200 OK`; session cookie granted `200` on `GET /api/tasks` | **Pass** |
| **API-LOG-02** | Invalid Input | Existing username with wrong password | `{"username": "<valid>", "password": "WrongPassword"}` | `401 Unauthorized`<br>`{"error": "invalid credentials"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-LOG-03** | Invalid Input | Non-existent username | `{"username": "ghost_user_99999", "password": "Password123"}` | `401 Unauthorized`<br>`{"error": "invalid credentials"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-LOG-04** | Missing Field | Missing `password` field | `{"username": "some_user"}` | `401 Unauthorized`<br>`{"error": "invalid credentials"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-LOG-05** | Missing Field | Empty JSON body `{}` | `{}` | `401 Unauthorized`<br>`{"error": "invalid credentials"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-LOG-06** | Wrong Data Type | Non-string `username` (integer) | `{"username": 12345, "password": "Password123"}` | `400` or `401 Unauthorized` | Unhandled `AttributeError: 'int' object has no attribute 'strip'` at `app.py:336` | **Fail** |
| **API-LOG-07** | Edge Condition | Non-JSON request body (plain text) | Raw string `"not json"` | `401 Unauthorized`<br>`{"error": "invalid credentials"}` | `401 Unauthorized`; exact error returned | **Pass** |

---

## 3. `GET /api/categories`

| Test ID | Test Type | Scenario | Request / Auth | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-CAT-01** | Valid | Retrieve categories without logging in | Unauthenticated `GET /api/categories` | `200 OK`; JSON list of `{"id", "name"}` objects | `200 OK`; valid JSON list returned | **Pass** |
| **API-CAT-02** | Valid | Verify categories are sorted alphabetically by `name` | Unauthenticated `GET /api/categories` | `200 OK`; names sorted ascending | `200 OK`; list sorted alphabetically | **Pass** |
| **API-CAT-03** | Edge Condition | Unsupported HTTP method (`POST /api/categories`) | Unauthenticated `POST /api/categories` | `405 Method Not Allowed` | `405 Method Not Allowed` | **Pass** |