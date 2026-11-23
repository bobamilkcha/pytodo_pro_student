# Week 4: REST API Endpoints Inventory

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Source:** `app.py` (JSON REST API routes)  
**Authentication Mechanism:** Session cookie (`session["user_id"]`) set via `POST /api/login` or `POST /api/register`. Protected routes use `@login_required_api` (returns `401 Unauthorized` when unauthenticated).

---

## 1. Endpoint Summary Table

| # | Method | Path | Auth Required | Request Body / Query Params | Expected Status Codes | Response / Behavior |
| :-: | :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | `POST` | `/api/register` | No | **JSON Body:** `{"username": "str", "password": "str"}` | `201 Created`<br>`400 Bad Request` | Registers a new user and starts a session. Returns `{"id", "username"}` (`201`) or `{"error": "invalid username" / "invalid password"}` (`400`). |
| 2 | `POST` | `/api/login` | No | **JSON Body:** `{"username": "str", "password": "str"}` | `200 OK`<br>`401 Unauthorized` | Authenticates user and sets session cookie. Returns `{"id", "username"}` (`200`) or `{"error": "invalid credentials"}` (`401`). |
| 3 | `GET` | `/api/categories` | No | None | `200 OK` | Returns a JSON list of all categories ordered by name: `[{"id", "name"}, ...]`. |
| 4 | `GET` | `/api/tasks` | Yes | **Query Params (optional):**<br>`page` (int, default `0`)<br>`per_page` (int, default `10`)<br>`category` (str)<br>`status` (`open` \| `done`)<br>`q` (str, title search) | `200 OK`<br>`401 Unauthorized` | Returns a paginated JSON list of tasks belonging to the logged-in user, ordered by `id DESC`. |
| 5 | `GET` | `/api/tasks/<int:task_id>` | Yes | None | `200 OK`<br>`404 Not Found`<br>`401 Unauthorized` | Returns a single task JSON object if it exists and belongs to the logged-in user; otherwise `{"error": "not found"}` (`404`). |
| 6 | `POST` | `/api/tasks` | Yes | **JSON Body:**<br>`title` (str, **required**)<br>`description` (str, optional)<br>`category_id` (int, optional)<br>`due_date` (str `YYYY-MM-DD`, optional) | `201 Created`<br>`400 Bad Request`<br>`401 Unauthorized` | Creates a new task (`done = 0`). Returns the created task object (`201`) or `{"error": "title is required"}` (`400`). |
| 7 | `PUT` | `/api/tasks/<int:task_id>` | Yes | **JSON Body (all optional):**<br>`title` (str)<br>`description` (str)<br>`category_id` (int)<br>`due_date` (str)<br>`done` (bool) | `200 OK`<br>`404 Not Found`<br>`401 Unauthorized` | Updates fields on an existing task owned by the user. Sets `completed_at` when `done` transitions to `true`, clears it when `false`. Returns updated task (`200`). |
| 8 | `DELETE` | `/api/tasks/<int:task_id>` | Yes | None | `200 OK`<br>`401 Unauthorized` | Deletes the task by `task_id` and returns `{"result": "ok"}` (`200`). |
| 9 | `GET` | `/api/dashboard` | Yes | None | `200 OK`<br>`401 Unauthorized` | Returns task summary counts for the logged-in user: `{"total", "open", "overdue", "due_soon", "completed_this_week"}`. |

---

## 2. Implementation Notes & Risk Areas for Testing

While inspecting `app.py`, the following edge cases and potential defects were identified for Week 4 API test design:

* **Broken Access Control (IDOR) on `DELETE /api/tasks/<id>`:** The SQL query (`DELETE FROM tasks WHERE id = ?`) does **not** filter by `session["user_id"]`, allowing an authenticated user to delete another user's task. It also returns `200 OK` even if the `task_id` does not exist.
* **SQL Injection Risk on `GET /api/tasks?q=`:** The `q` search parameter is interpolated directly into the SQL `LIKE` clause (`f" AND title LIKE '%{q}%'"`) instead of using a parameterized query.
* **Duplicate Username on `POST /api/register`:** There is no `try/except` around the `INSERT INTO users` statement; registering an existing username may trigger an unhandled `500 Internal Server Error` instead of `400`/`409`.
* **No Validation on `POST`/`PUT` `due_date` or `category_id`:** Invalid date formats or non-existent `category_id` values are not explicitly validated before database insertion.