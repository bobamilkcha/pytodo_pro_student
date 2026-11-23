# Week 4: Application Programming Interface (API) Request & Test Data (`api_test_data.md`)

**Prepared by:** Test Design Coordinator (Aida)  
**Purpose:** Standardized JavaScript Object Notation (JSON) request bodies, query parameters, path inputs, and seed user datasets mapped to Week 4 Application Programming Interface (API) test cases (`api_test_cases.md`) and automated PyTest suites (`tests/test_api_auth.py`, `tests/test_api_tasks.py`).

---

## 1. Test User Accounts & Seed Reference Data

| Dataset Key | Field / Parameter | Value | Usage & Notes |
| :--- | :--- | :--- | :--- |
| **Primary Test User (User A)** | `username` / `password` | `"user_a_qa"` / `"Password123"` | Authenticated Create, Read, Update, and Delete (CRUD) and dashboard tests (`9+` characters to bypass Defect `D-004`). |
| **Secondary Test User (User B)** | `username` / `password` | `"attacker_del"` / `"Password123"` | Cross-user Insecure Direct Object Reference (IDOR) isolation tests (`API-TSK-GETONE-05`, `API-TSK-PUT-07`, `API-TSK-DEL-05`). |
| **Seeded Categories** | `categories` table | `"Work"`, `"Personal"`, `"Study"`, `"Urgent"` | Default categories inserted by `init_db()` in `app.py` (`DEFAULT_CATEGORIES`). |

---

## 2. Authentication Request Payloads (`POST /api/register`, `POST /api/login`)

| Test Case ID(s) | Input Category | JavaScript Object Notation (JSON) Request Body | Expected Handling |
| :--- | :--- | :--- | :--- |
| `API-REG-01`, `API-LOG-01` | Valid Credentials | `{"username": "new_user1", "password": "Password123"}` | Valid `3–20` character username and valid password (`201 Created` / `200 OK`). |
| `API-REG-02` | Valid (Whitespace Trim) | `{"username": "  trimmed_user  ", "password": "Password123"}` | Leading and trailing spaces stripped before database insert (`201 Created`). |
| `API-REG-03`, `API-REG-04` | Invalid Boundary Values | `{"username": "ab", "password": "Password123"}`<br>`{"username": "valid_user2", "password": "123"}` | Below minimum length rules (`400 Bad Request`). |
| `API-REG-05` to `07`, `API-LOG-04` to `05` | Missing Required Fields | `{"password": "Password123"}`<br>`{"username": "valid_user3"}`<br>`{}` | Missing required keys (`400 Bad Request` on register, `401 Unauthorized` on login). |
| `API-REG-08`, `API-LOG-06` | Wrong Data Type | `{"username": 12345, "password": "Password123"}` | Integer passed instead of string to test `.strip()` type safety. |
| `API-REG-09` | Edge (Duplicate Username) | `{"username": "new_user1", "password": "Password123"}` | Tests uniqueness enforcement on an already-registered username. |
| `API-LOG-02`, `API-LOG-03` | Invalid Credentials | `{"username": "new_user1", "password": "WrongPassword"}`<br>`{"username": "ghost_user_99999", "password": "Password123"}` | Mismatched password or unknown user (`401 Unauthorized`). |
| `API-LOG-07` | Edge (Malformed Body) | Raw plain text `"not json"` (`Content-Type: text/plain`) | Tests `request.get_json(silent=True) or {}` fallback (`401 Unauthorized`). |

---

## 3. Task Query & Path Parameters (`GET /api/tasks`, `GET /api/tasks/<id>`, `DELETE /api/tasks/<id>`)

| Test Case ID(s) | Input Category | Uniform Resource Locator (URL) Query / Path Input | Expected Handling |
| :--- | :--- | :--- | :--- |
| `API-TSK-GETALL-01` | Valid (Default Pagination) | `/api/tasks` | Defaults to `page=0`, `per_page=10`, ordered by `id DESC` (`200 OK`). |
| `API-TSK-GETALL-02` | Valid (Combined Filters) | `/api/tasks?category=Work&status=open&q=Report&page=0&per_page=5` | Filters by category name, `done=0`, substring match, and pagination (`200 OK`). |
| `API-TSK-GETALL-03` | Invalid (Structured Query Language (SQL) Injection) | `/api/tasks?q=' OR '1'='1` | Tests unparameterized `LIKE '%{q}%'` clause for cross-user data leakage. |
| `API-TSK-GETALL-04` | Invalid (Syntax Break) | `/api/tasks?q=test'` | Unclosed single quote testing Structured Query Language (SQL) string escaping. |
| `API-TSK-GETALL-06` | Wrong Data Type | `/api/tasks?page=abc&per_page=xyz` | Non-integer pagination parameters (`type=int` fallback check). |
| `API-TSK-GETALL-07` | Edge (High Page Offset) | `/api/tasks?page=99&per_page=10` | Offset beyond existing task count returns empty array `[]` (`200 OK`). |
| `API-TSK-GETONE-02`, `API-TSK-DEL-02` | Invalid (Non-Existent ID) | `/api/tasks/99999` | Non-existent `task_id` expected to return `404 Not Found`. |
| `API-TSK-GETONE-04`, `API-TSK-DEL-04` | Wrong Data Type (Path ID) | `/api/tasks/abc` | Non-integer path parameter rejected by Flask `<int:task_id>` (`404 Not Found`). |

---

## 4. Task Creation & Update Payloads (`POST /api/tasks`, `PUT /api/tasks/<id>`)

| Test Case ID | Input Category | JavaScript Object Notation (JSON) Request Body | Expected Handling |
| :--- | :--- | :--- | :--- |
| `API-TSK-POST-01` | Valid (Full Payload) | `{"title": "Submit STQA Week 4", "description": "API suite", "category_id": 3, "due_date": "2026-11-30"}` | Creates complete task record with `done: false` (`201 Created`). |
| `API-TSK-POST-02` | Valid (Minimal Payload) | `{"title": "Quick reminder"}` | Creates task using defaults `description: ""`, `category_id: null`, `due_date: null` (`201 Created`). |
| `API-TSK-POST-03` | Invalid (Blank Title) | `{"title": "     "}` | Whitespace-only title rejected after `.strip()` (`400 Bad Request`). |
| `API-TSK-POST-04` | Invalid (Malformed Date) | `{"title": "Bad date test", "due_date": "not-a-date"}` | Invalid date string passed to `compute_urgency()` (`YYYY-MM-DD` format check). |
| `API-TSK-POST-05` | Missing Required Field | `{"description": "Missing title"}` | Omitted `title` key rejected (`400 Bad Request`). |
| `API-TSK-POST-07` | Wrong Data Type | `{"title": 12345}` | Integer `title` tests type validation before `.strip()`. |
| `API-TSK-POST-08` | Edge (Invalid Foreign Key) | `{"title": "Invalid category", "category_id": 9999}` | Non-existent `category_id` foreign-key integrity check. |
| `API-TSK-PUT-01` | Valid (Partial Update) | `{"title": "Updated Title", "due_date": "2026-12-05"}` | Updates specified fields while keeping remaining fields intact (`200 OK`). |
| `API-TSK-PUT-02` | Valid (State Toggle) | `{"done": true}` followed by `{"done": false}` | Verifies `completed_at` timestamp population and clearing (`200 OK`). |
| `API-TSK-PUT-03` | Invalid (Empty Update) | `{"title": ""}` | Empty string update check on `PUT`. |
| `API-TSK-PUT-05` | Missing Fields (No-Op) | `{}` | Empty JavaScript Object Notation (JSON) object leaves existing record unchanged (`200 OK`). |
| `API-TSK-PUT-06` | Wrong Data Type (Boolean) | `{"done": "false"}` | String `"false"` instead of boolean `false` (tests Python `bool()` truthiness). |

---

## 5. Dashboard & Category Test Inputs (`GET /api/categories`, `GET /api/dashboard`)

| Test Case ID(s) | Input Category | Request Method & Seed State | Expected Handling |
| :--- | :--- | :--- | :--- |
| `API-CAT-01`, `API-CAT-02` | Valid (Unauthenticated) | `GET /api/categories` (no session cookie) | Returns alphabetically sorted list of all seeded categories (`200 OK`). |
| `API-CAT-03`, `API-DASH-04` | Edge (Unsupported Method) | `POST /api/categories` and `POST /api/dashboard` | Rejected by Flask routing (`405 Method Not Allowed`). |
| `API-DASH-01` | Valid (Mixed Task States) | `GET /api/dashboard` with 1 past-due task (`2020-01-01`), 1 current-day task, and 1 completed task (`done: true`) | Verifies `total`, `open`, `overdue`, `due_soon`, and `completed_this_week` counters (`200 OK`). |
| `API-DASH-02` | Valid (Empty User State) | `GET /api/dashboard` for newly registered user with 0 tasks | Returns zeroed summary object (`200 OK`). |