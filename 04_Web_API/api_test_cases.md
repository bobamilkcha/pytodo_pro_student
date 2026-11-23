# Week 4: API Test Cases (All 9 Endpoints)

**Prepared & Executed by:** Automation/Tool Coordinator (Nisrina — Sections 1–3) & Test Design Coordinator (Aida — Sections 4–9)  
**Test Scripts & Evidence:** `tests/test_api_auth.py` (`evidence_api_auth.txt`), `tests/test_api_tasks.py` (`evidence_api_tasks.txt`)  
**Summary:** 55 Total Test Cases — **43 Passed, 12 Failed** (Nisrina: 16 Passed, 3 Failed | Aida: 27 Passed, 9 Failed)

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
---

## 4. `GET /api/tasks` (Prepared & Executed by Test Design Coordinator — Aida)

| Test ID | Test Type | Scenario | Request / Query Params | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-TSK-GETALL-01** | Valid | Retrieve all tasks for authenticated user with default pagination | Authenticated `GET /api/tasks` | `200 OK`; JSON array of current user's tasks ordered by `id DESC` (max 10) | `200 OK`; returned user's tasks in descending ID order | **Pass** |
| **API-TSK-GETALL-02** | Valid | Filter tasks by `category`, `status`, `q`, and pagination | Authenticated `GET /api/tasks?category=Work&status=open&q=Report&page=0&per_page=5` | `200 OK`; returns only matching open `Work` tasks containing `"Report"` | `200 OK`; filtered task list returned accurately | **Pass** |
| **API-TSK-GETALL-03** | Invalid Input | SQL injection payload in search parameter `q` | Authenticated `GET /api/tasks?q=' OR '1'='1` | `200 OK`; safely treated as literal text returning `[]` (no cross-user leak) | `200 OK`; returned `[]` (trailing `%` in `LIKE '%{q}%'` prevented `'1'='1%'` match, though query remains unparameterized) | **Pass** |
| **API-TSK-GETALL-04** | Invalid Input | Unclosed single quote in search parameter `q` | Authenticated `GET /api/tasks?q=test'` | `200 OK`; safely escaped search returning `[]` | Unhandled `sqlite3.OperationalError: unrecognized token` at `app.py:384` (`500` error) | **Fail** |
| **API-TSK-GETALL-05** | Missing Auth | Access task list without active session cookie | Unauthenticated `GET /api/tasks` | `401 Unauthorized`<br>`{"error": "authentication required"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-TSK-GETALL-06** | Wrong Data Type | Non-integer values for `page` and `per_page` | Authenticated `GET /api/tasks?page=abc&per_page=xyz` | `200 OK` (defaults to `page=0`, `per_page=10`) or `400 Bad Request` | `200 OK`; Flask `type=int` safely defaulted to `0` and `10` | **Pass** |
| **API-TSK-GETALL-07** | Edge Condition | Request page index beyond available tasks | Authenticated `GET /api/tasks?page=99&per_page=10` | `200 OK`; empty JSON array `[]` | `200 OK`; returned `[]` | **Pass** |

---

## 5. `GET /api/tasks/<int:task_id>`

| Test ID | Test Type | Scenario | Request / Auth | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-TSK-GETONE-01** | Valid | Retrieve single task owned by logged-in user | Authenticated `GET /api/tasks/<own_id>` | `200 OK`; JSON object containing `id`, `title`, `description`, `category_id`, `category`, `due_date`, `done`, `urgency`, `completed_at`, `created_at` | `200 OK`; full task JSON returned | **Pass** |
| **API-TSK-GETONE-02** | Invalid Input | Request non-existent `task_id` | Authenticated `GET /api/tasks/99999` | `404 Not Found`<br>`{"error": "not found"}` | `404 Not Found`; exact error returned | **Pass** |
| **API-TSK-GETONE-03** | Missing Auth | Retrieve task without authentication | Unauthenticated `GET /api/tasks/1` | `401 Unauthorized`<br>`{"error": "authentication required"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-TSK-GETONE-04** | Wrong Data Type | Non-integer `task_id` in URL path | Authenticated `GET /api/tasks/abc` | `404 Not Found` | `404 Not Found`; Flask `<int:task_id>` rejected string path | **Pass** |
| **API-TSK-GETONE-05** | Edge Condition | Cross-user access attempt (IDOR check on another user's task) | User B authenticated `GET /api/tasks/<user_a_task_id>` | `404 Not Found`<br>`{"error": "not found"}` | `404 Not Found`; `WHERE id = ? AND user_id = ?` blocked access | **Pass** |

---

## 6. `POST /api/tasks`

| Test ID | Test Type | Scenario | Request Body (JSON) | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-TSK-POST-01** | Valid | Create task with all valid fields | `{"title": "Submit STQA Week 4", "description": "API suite", "category_id": 3, "due_date": "2026-11-30"}` | `201 Created`; returns created task JSON with `done: false` | `201 Created`; task saved and returned | **Pass** |
| **API-TSK-POST-02** | Valid (Minimal) | Create task with only required `title` | `{"title": "Quick reminder"}` | `201 Created`; defaults `description: ""`, `category_id: null`, `due_date: null` | `201 Created`; defaults applied properly | **Pass** |
| **API-TSK-POST-03** | Invalid Input | Whitespace-only `title` | `{"title": "     "}` | `400 Bad Request`<br>`{"error": "title is required"}` | `400 Bad Request`; `.strip()` caught blank title | **Pass** |
| **API-TSK-POST-04** | Invalid Input | Malformed `due_date` string | `{"title": "Bad date test", "due_date": "not-a-date"}` | `400 Bad Request` (invalid date format) | Unhandled `ValueError: time data 'not-a-date' does not match format '%Y-%m-%d'` in `helpers.py:31` via `app.py:420` (`500` error) | **Fail** |
| **API-TSK-POST-05** | Missing Field | Omit required `title` field | `{"description": "Missing title"}` | `400 Bad Request`<br>`{"error": "title is required"}` | `400 Bad Request`; exact error returned | **Pass** |
| **API-TSK-POST-06** | Missing Auth | Create task while logged out | Unauthenticated `POST /api/tasks` with `{"title": "Test"}` | `401 Unauthorized`<br>`{"error": "authentication required"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-TSK-POST-07** | Wrong Data Type | Non-string `title` (integer) | `{"title": 12345}` | `400 Bad Request` | Unhandled `AttributeError: 'int' object has no attribute 'strip'` at `app.py:405` (`500` error) | **Fail** |
| **API-TSK-POST-08** | Edge Condition | Non-existent `category_id` foreign key | `{"title": "Invalid category", "category_id": 9999}` | `400 Bad Request` (invalid category) | Returned `201 Created` and saved `category_id: 9999` with `category: null` | **Fail** |

---

## 7. `PUT /api/tasks/<int:task_id>`

| Test ID | Test Type | Scenario | Request Body (JSON) | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-TSK-PUT-01** | Valid | Update `title` and `due_date` of own task | `{"title": "Updated Title", "due_date": "2026-12-05"}` | `200 OK`; returns updated task JSON | `200 OK`; fields updated accurately | **Pass** |
| **API-TSK-PUT-02** | Valid (State) | Mark open task as completed (`done: true`) and reopen (`done: false`) | `{"done": true}` then `{"done": false}` | `200 OK`; `done: true` sets `urgency: "Done"` and `completed_at`; `done: false` clears `completed_at` to `null` | `200 OK`; `completed_at` timestamp toggled properly | **Pass** |
| **API-TSK-PUT-03** | Invalid Input | Update task with empty string `title` | `{"title": ""}` | `400 Bad Request`<br>`{"error": "title is required"}` | Returned `200 OK` and overwrote `title` with blank `""` (no empty check on `PUT`) | **Fail** |
| **API-TSK-PUT-04** | Invalid Input | Update non-existent `task_id` | `PUT /api/tasks/99999` with `{"title": "Ghost"}` | `404 Not Found`<br>`{"error": "not found"}` | `404 Not Found`; exact error returned | **Pass** |
| **API-TSK-PUT-05** | Missing Field | Send empty JSON body `{}` | `{}` | `200 OK`; retains all existing task fields unchanged | `200 OK`; existing values preserved | **Pass** |
| **API-TSK-PUT-06** | Wrong Data Type | String `"false"` passed for boolean `done` | `{"done": "false"}` | `400 Bad Request` (or evaluates as `false`) | Python `bool("false")` evaluated to `True`, erroneously marking task as `done: true` | **Fail** |
| **API-TSK-PUT-07** | Edge Condition | Cross-user update attempt (IDOR check) | User B authenticated `PUT /api/tasks/<user_a_task_id>` with `{"title": "Hacked"}` | `404 Not Found`<br>`{"error": "not found"}` | `404 Not Found`; ownership check blocked update | **Pass** |

---

## 8. `DELETE /api/tasks/<int:task_id>`

| Test ID | Test Type | Scenario | Request / Auth | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-TSK-DEL-01** | Valid | Delete existing task owned by logged-in user | Authenticated `DELETE /api/tasks/<own_id>` | `200 OK`<br>`{"result": "ok"}` (subsequent `GET` returns `404`) | `200 OK`; task permanently deleted | **Pass** |
| **API-TSK-DEL-02** | Invalid Input | Delete non-existent `task_id` | Authenticated `DELETE /api/tasks/99999` | `404 Not Found`<br>`{"error": "not found"}` | Returned `200 OK` `{"result": "ok"}` even though no record existed | **Fail** |
| **API-TSK-DEL-03** | Missing Auth | Delete task without active session | Unauthenticated `DELETE /api/tasks/1` | `401 Unauthorized`<br>`{"error": "authentication required"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-TSK-DEL-04** | Wrong Data Type | Non-integer `task_id` in URL | Authenticated `DELETE /api/tasks/abc` | `404 Not Found` | `404 Not Found`; rejected by `<int:task_id>` | **Pass** |
| **API-TSK-DEL-05** | Edge Condition | Cross-user deletion attempt (IDOR security check) | User B authenticated `DELETE /api/tasks/<user_a_task_id>` | `403 Forbidden` or `404 Not Found` (User A's task remains intact) | Returned `200 OK` `{"result": "ok"}` and deleted User A's task (`DELETE FROM tasks WHERE id = ?` omits `user_id`) | **Fail** |

---

## 9. `GET /api/dashboard`

| Test ID | Test Type | Scenario | Request / Auth | Expected Status & Response | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **API-DASH-01** | Valid | Retrieve dashboard metrics for user with mixed task states | Authenticated `GET /api/dashboard` | `200 OK`; accurate counts for `total: 3`, `open: 2`, `overdue: 1`, `due_soon: 1`, `completed_this_week: 1` | Returned `overdue: 2, due_soon: 0` because `compute_urgency(today)` classifies `due_date == today` as `"Overdue"` (`due <= today`) rather than `"Due Soon"` | **Fail** |
| **API-DASH-02** | Valid (Empty) | Retrieve dashboard metrics for new user with 0 tasks | Authenticated `GET /api/dashboard` | `200 OK`<br>`{"total": 0, "open": 0, "overdue": 0, "due_soon": 0, "completed_this_week": 0}` | `200 OK`; all 5 counters returned `0` | **Pass** |
| **API-DASH-03** | Missing Auth | Retrieve dashboard summary while unauthenticated | Unauthenticated `GET /api/dashboard` | `401 Unauthorized`<br>`{"error": "authentication required"}` | `401 Unauthorized`; exact error returned | **Pass** |
| **API-DASH-04** | Edge Condition | Unsupported HTTP method (`POST /api/dashboard`) | Authenticated `POST /api/dashboard` | `405 Method Not Allowed` | `405 Method Not Allowed` | **Pass** |