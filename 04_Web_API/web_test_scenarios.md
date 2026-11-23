# Week 4: Web Test Scenarios & Client–Server Validation (`web_test_scenarios.md`)

**Owner:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro Web UI (`http://127.0.0.1:5000/`)  
**Reference Files:** `app.py`, `templates/register.html`, `templates/login.html`, `templates/index.html`, `templates/task_form.html`, `templates/dashboard.html`, `templates/base.html`

---

## 1. End-to-End Web Workflows (`WTS-01` to `WTS-08`)

These scenarios verify complete multi-step user journeys across the Flask Web UI routes, session management, database persistence, and UI state updates.

| Scenario ID | Workflow Name | Feature ID(s) | Route Sequence | End-to-End Workflow Steps | Expected End-to-End Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WTS-01** | New User Registration & Auto-Login | F-01, F-02, F-06 | `GET /register` -> `POST /register` -> `GET /` | 1. Open `/register`.<br>2. Enter a valid unique username (`3–20` alphanumeric/underscore chars) and valid password (`9+` chars due to `D-004`).<br>3. Submit form. | User record is saved in `users` table with hashed password, `session["user_id"]` and `session["username"]` are initialized, and user is redirected to `/` with navbar showing username and `Log out`. |
| **WTS-02** | Existing User Login & Session Persistence | F-03, F-04 | `GET /login` -> `POST /login` -> `GET /` -> `GET /dashboard` | 1. Open `/login` and submit valid credentials.<br>2. Verify redirect to `/`.<br>3. Navigate between `Tasks` (`/`) and `Dashboard` (`/dashboard`) and refresh browser. | Session cookie persists across pages; user remains authenticated without re-entering credentials, and only tasks matching `session["user_id"]` are loaded. |
| **WTS-03** | End-to-End Task Creation & Urgency Classification | F-08, F-09, F-14 | `GET /` -> `GET /tasks/new` -> `POST /tasks/new` -> `GET /` | 1. Click `+ New Task` on `/`.<br>2. Fill in `title`, `description`, `category_id` (e.g., `Study`), and `due_date` (today or tomorrow).<br>3. Submit form. | Task is inserted into `tasks` table with `done = 0`, redirects to `/`, and appears at the top of the table (`ORDER BY id DESC`) with category badge and `Due Soon` urgency badge. |
| **WTS-04** | Multi-Criteria Task Filtering & Search | F-11 | `GET /` -> `GET /?category=...&status=...&q=...` | 1. Ensure user has multiple tasks across different categories (`Work`, `Study`) and states (`open`, `done`).<br>2. Select a category, choose status `open`, enter a partial title keyword in `q`, and click `Filter`. | URL updates with query parameters; SQL query filters by `user_id`, `category_id`, `done = 0`, and parameterized `title LIKE ?`; form inputs retain selected filter state. |
| **WTS-05** | Task Modification & Persistence | F-10 | `GET /` -> `GET /tasks/<id>/edit` -> `POST /tasks/<id>/edit` -> `GET /` | 1. Click `Edit` on an existing task.<br>2. Verify existing fields pre-populate.<br>3. Modify `title`, change `category_id` to `None`, update `due_date`, and click `Save Changes`. | Database row updates accurately for matching `id` and `user_id`; redirects to `/` displaying updated title, blank/none category, and recalculated urgency status. |
| **WTS-06** | Task Completion Toggle & Dashboard Metric Sync | F-12, F-15 | `GET /` -> `POST /tasks/<id>/toggle` -> `GET /` -> `GET /dashboard` | 1. Click the toggle button (`○`) on an open overdue task.<br>2. Observe task row state on `/`.<br>3. Navigate to `/dashboard`. | `done` updates to `1` and `completed_at` records current timestamp; row renders `✓` with strikethrough and `Done` urgency; `/dashboard` decrements `Open` and `Overdue` counts by 1 and increments `Completed (last 7 days)` by 1. |
| **WTS-07** | Task Deletion & Cross-User Isolation | F-13 | `GET /` -> `POST /tasks/<id>/delete` -> `GET /` | 1. Click `Delete` on a task and accept the browser confirmation dialog.<br>2. Attempt a direct `POST /tasks/<other_user_task_id>/delete` using another user's task ID. | User's own task is permanently removed from `tasks` and disappears from `/`; attempting to delete another user's task via web route fails silently (`WHERE id = ? AND user_id = ?`) without deleting the victim's record. |
| **WTS-08** | Logout & Unauthenticated Route Guard | F-05, F-06 | `GET /logout` -> `GET /login` -> `GET /` -> `GET /dashboard` | 1. Click `Log out` in the top navbar.<br>2. Attempt to directly visit `/`, `/tasks/new`, and `/dashboard` via browser address bar. | `session.clear()` terminates session and redirects to `/login`; all `@login_required_web` routes block access and redirect unauthenticated requests back to `/login`. |

---

## 2. Client-Side vs. Server-Side Validation Matrix (`WTS-VAL-01` to `WTS-VAL-06`)

This section compares the HTML5/JavaScript rules enforced in the browser templates against the Python/Flask validation logic in `app.py` when client-side constraints are bypassed (e.g., via browser DevTools, whitespace padding, or direct `POST` requests).

| Validation ID | Feature / Route | Client-Side Enforcement (HTML5 / JS) | Server-Side Enforcement (`app.py`) | Bypass / Edge Test Method | Expected Result | Actual Result & Validation Gap |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WTS-VAL-01** | Registration Username & Password (`POST /register`) | `register.html` applies HTML5 `required` only; **no** `minlength`, `maxlength`, or `pattern` attributes exist on `<input>` tags. | Calls `is_valid_username()` (`3–20` chars) and `is_valid_password()` (`helpers.py`) and renders `.error` banner on failure. | Submit username `"ab"` (2 chars) or password `"1234567"` (7 chars) directly in browser form. | Form rejects invalid inputs and displays clear error messages. | **Consistent (with `D-004` caveat):** Client allows submission because HTML5 lacks `minlength`/`pattern`, so server-side validation catches it—though `is_valid_password()` has an off-by-one defect (`D-004`) rejecting 8-character passwords. |
| **WTS-VAL-02** | Duplicate Username Registration (`POST /register`) | None (cannot be checked purely client-side). | `app.py` `register_page()` includes `# NOTE: no uniqueness check against existing usernames here.` | Register two accounts with the exact same `username` (`"aida_test"`). | Server rejects duplicate username with a user-friendly validation error. | **Server-Side Gap:** `users.username` has no `UNIQUE` constraint and `register_page()` performs no lookup, allowing duplicate usernames in the database. |
| **WTS-VAL-03** | Create / Edit Task Empty or Whitespace Title (`POST /tasks/new`, `POST /tasks/<id>/edit`) | `task_form.html` applies `<input type="text" name="title" required>`. | `new_task()` and `edit_task()` run `title = request.form.get("title", "").strip()` and **immediately execute `INSERT`/`UPDATE`** without checking `if not title:`. | 1. Enter spaces `"     "` into `Title` (passes HTML5 `required`).<br>2. Or remove `required` via DevTools and submit empty `Title`. | Server rejects empty/whitespace-only title and re-renders form with an error message (matching `POST /api/tasks` which returns `400`). | **Defect (`D-009`):** Client-side `required` is easily bypassed; server strips whitespace into `""` and inserts a blank-title task into SQLite. |
| **WTS-VAL-04** | Task Due Date Format & Range (`POST /tasks/new`, `POST /tasks/<id>/edit`) | `task_form.html` uses `<input type="date" name="due_date">`, restricting browser UI to `YYYY-MM-DD`. | `due_date = request.form.get("due_date") or None` is stored directly as `TEXT` without date format validation. | Change `<input type="date">` to `type="text"` in DevTools and submit `"invalid-date"` or `"2026-99-99"`. | Server validates `YYYY-MM-DD` format and rejects malformed dates before saving. | **Server-Side Gap:** Server accepts malformed strings into `due_date`, which can later cause `compute_urgency()` on `/` or `/dashboard` to fail or misclassify urgency. |
| **WTS-VAL-05** | Task Category ID Integrity (`POST /tasks/new`, `POST /tasks/<id>/edit`) | `task_form.html` renders a `<select name="category_id">` populated from `categories` table. | `category_id = request.form.get("category_id") or None` is inserted without verifying that `category_id` exists in `categories`. | Edit `<option value="1">` in DevTools to `value="9999"` and submit the form. | Server validates that `category_id` exists in `categories` (or defaults to `None`). | **Server-Side Gap:** SQLite saves `category_id = 9999` (no foreign-key enforcement), causing `get_category_name()` to return `None` silently. |
| **WTS-VAL-06** | Destructive Task Deletion (`POST /tasks/<id>/delete`) | `index.html` uses JS `onsubmit="return confirm('Delete this task?')"` to prevent accidental clicks. | `delete_task_web()` verifies `session["user_id"]` and executes `DELETE FROM tasks WHERE id = ? AND user_id = ?` (no CSRF token). | Send direct `POST /tasks/<id>/delete` bypassing the JS `confirm()` dialog. | Authorized user can delete own task; unauthorized user cannot delete another user's task. | **Owner Check Secure, No CSRF:** Server enforces `user_id` ownership (unlike `DELETE /api/tasks/<id>`), though no CSRF protection exists on state-changing `POST` forms. |

---

## 3. Summary of Key Web vs. API Validation Discrepancies

Comparing the Web UI routes against the REST API routes in `app.py` highlights three architectural inconsistencies that directly inform our API test cases (Task 3b) and UI-vs-API comparison (Task 6):

1. **Missing Title Validation in Web UI vs. API (`D-009`):** `POST /api/tasks` explicitly validates `if not title: return jsonify({"error": "title is required"}), 400`, whereas `POST /tasks/new` and `POST /tasks/<id>/edit` rely solely on HTML5 `required` and allow blank/whitespace task titles into the database.
2. **Owner Scoping on Delete in Web UI vs. API:** `POST /tasks/<id>/delete` safely scopes deletion to `WHERE id = ? AND user_id = ?`, whereas `DELETE /api/tasks/<id>` omits `user_id`, exposing an Insecure Direct Object Reference (IDOR) vulnerability.
3. **Parameterized Search in Web UI vs. API:** `GET /` safely parameterizes search queries (`AND title LIKE ?`), whereas `GET /api/tasks?q=` uses raw string interpolation (`f" AND title LIKE '%{q}%'"`), creating a SQL injection risk.

---

## 4. Draft Defect Report (For Handoff to Defect & Metrics Coordinator)

### Defect ID: D-009
- **Title:** Web UI task creation (`POST /tasks/new`) and editing (`POST /tasks/<id>/edit`) lack server-side empty-title validation, allowing blank/whitespace titles
- **Affected Feature:** F-08 Create Task, F-10 Edit Task (`app.py` lines 206–215, 228–236)
- **Environment:** Windows 11, Microsoft Edge, Localhost (`http://127.0.0.1:5000/`)
- **Preconditions:** User is logged into PyTodo Pro and opens `/tasks/new` (or `/tasks/<id>/edit`).
- **Steps to Reproduce:**
  1. Navigate to `http://127.0.0.1:5000/tasks/new`.
  2. Enter only spaces (`"     "`) in the **Title** field (or remove the HTML5 `required` attribute via browser DevTools and leave **Title** empty).
  3. Click **Create Task**.
* **Expected Result:** Server rejects the empty/whitespace title and displays a validation error message without creating a task (consistent with `POST /api/tasks` returning `400 Bad Request`).
* **Actual Result:** `.strip()` converts the spaces into `""`, and the server inserts and displays a task with a completely blank title on `/`.
* **Severity:** Moderate
* **Priority:** Medium
* **Evidence:** `04_Web_API/evidence/WTS-VAL-03.png`
* **Status:** Open