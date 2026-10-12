# PyTodo Pro: Feature Inventory (Black-Box Testing)

**Prepared by:** QA Test Lead
**Based on:** reading `app.py`, `helpers.py`, the `templates/` folder, `static/style.css` and `README.md`. We did not change any app code.

**How to read this document**
- **To verify in UI** means we couldn't tell from the code alone, so someone has to run the app and check.
- **(code vs spec)** means the code does something different from what its own comments, README or form hints say. These are good candidates for test cases.
- Technique short forms: **EP** = equivalence partitioning, **BVA** = boundary value analysis, **DT** = decision table, **ST** = state transition.

---

## 1. Application Overview

PyTodo Pro is a small task manager website. A user signs up, logs in, and then can add tasks with an optional category and due date, tick them off when done, search and filter them, and look at a dashboard that counts how many tasks are overdue, due soon, and so on. Everything is also available as a JSON API under `/api`, which uses the same login session.

It is built with Flask 3.0.3 (Python), SQLite for storage and Jinja2 HTML templates. There is no JavaScript apart from a delete confirm popup and an auto-submit on the filter dropdowns.

**To run it:**
1. `python -m venv venv` and activate it
2. `pip install -r requirements.txt`
3. `python app.py`
4. Open `http://127.0.0.1:5000/` and register an account (there is no default login)

The first run creates `pytodo_pro.db` and four categories: Work, Personal, Study, Urgent.

**Who uses it:**
- **Anonymous visitor:** can only see register/login (plus `/api/categories`).
- **Logged-in user:** can manage their own tasks.

---

## 2. Feature Inventory

Each feature lists the file and function where it is implemented.

### 2.1 Authentication

| ID | Feature | Description | Actor | Inputs | Expected Behaviour | Page/Route | Notes |
|---|---|---|---|---|---|---|---|
| F-01 | Register (web) | Make a new account and get logged in straight away. `app.py::register_page` | Anonymous | **username**: 3-20 chars, letters/numbers/underscore, trimmed. **password**: form says min 8, code needs more than 8. Both required. | Valid: account created, logged in, goes to `/`. Bad username or password: error message on the form. Duplicate username: not checked in code, so **to verify in UI**. | `/register` (GET, POST) | **BVA**: length limits are clear boundaries (username 2/3/20/21, password 7/8/9). |
| F-02 | Register (API) | Same as F-01 but with JSON. `app.py::api_register` | Anonymous | JSON `username`, `password` (same rules). | 201 with `{id, username}`. Invalid input: 400 with an error message. Also logs the caller in. | `/api/register` (POST) | **BVA + EP**: same limits as F-01, plus wrong data types. |
| F-03 | Login (web) | Log in with username and password. `app.py::login_page` | Anonymous | **username** (trimmed), **password**. Both required. | Correct: session set, goes to `/`. Wrong: "Invalid username or password." (same message for both cases). | `/login` (GET, POST) | **DT**: two conditions (user exists, password correct) give different outcomes. |
| F-04 | Login (API) | Same as F-03 with JSON. `app.py::api_login` | Anonymous | JSON `username`, `password`. | 200 with `{id, username}` or 401 `invalid credentials`. | `/api/login` (POST) | **DT**: same as F-03. |
| F-05 | Logout | Ends the session. `app.py::logout` | Logged in | None | Session cleared, goes to `/login`. Uses a plain GET link. | `/logout` (GET) | **ST**: logged in to logged out. |
| F-06 | Page protection (web) | Protected pages redirect to login. `app.py::login_required_web` | Anonymous | Typing the URL directly | Redirect to `/login` for `/`, `/dashboard`, `/tasks/...`. | All pages in section 3 | **EP**: two groups, logged in or not. |
| F-07 | Endpoint protection (API) | Protected API calls return 401. `app.py::login_required_api` | Anonymous | Direct API call | 401 `authentication required`. `/api/categories` is NOT protected. | All `/api/tasks*` and `/api/dashboard` | **EP**: two groups, logged in or not. |

### 2.2 Task management (web pages)

| ID | Feature | Description | Actor | Inputs | Expected Behaviour | Page/Route | Notes |
|---|---|---|---|---|---|---|---|
| F-08 | Create task | Add a new task. `app.py::new_task` | Logged in | **title**: trimmed, browser "required", no server check, no max length. **description**: optional. **category**: None or one of 4. **due date**: date picker, optional, not checked by server. | Task saved as open, appears at top of list, redirect to `/`. Whitespace-only title: **to verify in UI**. | `/tasks/new` (GET, POST) | **BVA + EP**: title length edges, and category/date groups. |
| F-09 | View task list | Show my tasks, newest first. `app.py::index` | Logged in | None | Table with title, category, due date, urgency badge. Empty message if nothing matches. | `/` (GET) | **EP**: no tasks vs some tasks. |
| F-10 | Edit task | Change title, description, category or due date. `app.py::edit_task` | Task owner | Same fields as F-08, pre-filled. | Saved, redirect to `/`. Done status is unchanged. Wrong or missing id: silently goes back to `/`. | `/tasks/<id>/edit` (GET, POST) | **EP**: own, someone else's, or missing task id. |
| F-11 | Filter and search | Narrow the list by category, status and title text. `app.py::index` | Logged in | **category**: dropdown. **status**: all / open / done. **q**: text, matches part of title. | Filters are combined (AND). Unknown values are ignored. `%` and `_` act as wildcards. | `/?category=&status=&q=` | **DT**: three filters combine into many cases. |
| F-12 | Mark done / reopen | Toggle a task's done state. `app.py::toggle_task` | Task owner | Task id (POST) | Open to done: records completion time. Done to open: clears it. Someone else's or missing id: nothing happens. | `/tasks/<id>/toggle` (POST) | **ST**: task moves between open and done. |
| F-13 | Delete task (web) | Remove a task after a confirm popup. `app.py::delete_task_web` | Task owner | Task id (POST) | Deleted only if it is yours. Redirect to `/`. | `/tasks/<id>/delete` (POST) | **EP**: own, other, or missing task id. |
| F-14 | Urgency badge | Label each task by its due date. `helpers.py::compute_urgency`, `app.py::row_to_task` | Logged in | Due date `YYYY-MM-DD` or blank | By spec: none = "No due date", past = "Overdue", today = "Due Today", 1-2 days = "Due Soon", 3+ days = "Upcoming". Done tasks = "Done". **Code returns "Overdue" for today and never "Due Today"** *(code vs spec)*. Bad date format: **to verify in UI**. | Shown on `/` and in `/api/tasks*` | **BVA**: labels change at clear day boundaries (-1, 0, +1, +2, +3). |

### 2.3 Dashboard

| ID | Feature | Description | Actor | Inputs | Expected Behaviour | Page/Route | Notes |
|---|---|---|---|---|---|---|---|
| F-15 | Dashboard (web) | Five counters: Total, Open, Overdue, Due Soon, Completed (last 7 days). `app.py::dashboard`, `helpers.py::completed_in_last_n_days` | Logged in | None | Counts only my tasks. Overdue and Due Soon count open tasks only. Spec says "inclusive of exactly 7 days ago" but code excludes it *(code vs spec)*. Tasks due today are counted as Overdue (see F-14). | `/dashboard` (GET) | **BVA**: the 7-day cutoff is a boundary (6d 23h, 7d, 7d 1s). |
| F-16 | Dashboard (API) | Same counters as JSON. `app.py::api_dashboard` | Logged in | None | 200 with `total, open, overdue, due_soon, completed_this_week`. Should match F-15. | `/api/dashboard` (GET) | **EP**: compare against F-15 as the expected result. |

### 2.4 Task API

| ID | Feature | Description | Actor | Inputs | Expected Behaviour | Page/Route | Notes |
|---|---|---|---|---|---|---|---|
| F-17 | List categories | Get all categories (shared by everyone). `app.py::api_categories` | Anyone | None | 200 array sorted by name: Personal, Study, Urgent, Work. | `/api/categories` (GET) | **EP**: logged in vs not (no login needed). |
| F-18 | List tasks (API) | Paged, filtered list of my tasks. `app.py::api_list_tasks` | Logged in | **page**: int, default 0 (starts at 0). **per_page**: int, default 10. **category**, **status**, **q**: as F-11. Non-numbers fall back to defaults. | 200 array, newest first. Zero or negative `per_page`/`page`: **to verify in UI**. | `/api/tasks` (GET) | **BVA**: page and per_page have edges (-1, 0, 1, last, last+1). |
| F-19 | Create task (API) | Make a task from JSON. `app.py::api_create_task` | Logged in | **title**: required, trimmed. **description**, **category_id**, **due_date**: not validated. | 201 with the new task. Missing or blank title: 400. A bad category id is accepted and shows category `null`. Number as title: likely 500. | `/api/tasks` (POST) | **EP**: valid vs invalid groups for title, category_id and due_date. |
| F-20 | Get one task | Fetch one of my tasks. `app.py::api_get_task` | Task owner | Task id in path | 200 with task, or 404 `not found` (also for other users' tasks). | `/api/tasks/<id>` (GET) | **EP**: own, other user's, missing, non-numeric id. |
| F-21 | Update task | Partial update, including done. `app.py::api_update_task` | Task owner | Any of `title`, `description`, `category_id`, `due_date`, `done`. Omitted keys stay the same. Nothing is validated. | 200 with updated task. `done` false to true sets completion time; true to false clears it. Other user's or missing: 404. String `"false"` counts as done: **to verify in UI**. | `/api/tasks/<id>` (PUT) | **ST**: same open/done states as F-12. |
| F-22 | Delete task (API) | Delete by id. `app.py::api_delete_task` | Logged in | Task id | Always 200 `ok`, even for missing ids. **Not limited to your own tasks** (a code comment says so). | `/api/tasks/<id>` (DELETE) | **EP**: own, other user's, or missing task id. |

---

## 3. Routes and Endpoints

| Method | Path | Purpose | Auth required | Type |
|---|---|---|---|---|
| GET | `/register` | Show registration form | No | UI page |
| POST | `/register` | Submit registration | No | UI page |
| GET | `/login` | Show login form | No | UI page |
| POST | `/login` | Submit login | No | UI page |
| GET | `/logout` | Log out | No | UI page (redirect) |
| GET | `/` | Task list with filters | Yes | UI page |
| GET | `/tasks/new` | New task form | Yes | UI page |
| POST | `/tasks/new` | Create task | Yes | UI page |
| GET | `/tasks/<id>/edit` | Edit form | Yes | UI page |
| POST | `/tasks/<id>/edit` | Save edits | Yes | UI page |
| POST | `/tasks/<id>/toggle` | Toggle done | Yes | UI page (redirect) |
| POST | `/tasks/<id>/delete` | Delete task | Yes | UI page (redirect) |
| GET | `/dashboard` | Counters page | Yes | UI page |
| POST | `/api/register` | Register and log in | No | API |
| POST | `/api/login` | Log in | No | API |
| GET | `/api/categories` | List categories | **No** | API |
| GET | `/api/tasks` | List, filter, paginate | Yes | API |
| POST | `/api/tasks` | Create task | Yes | API |
| GET | `/api/tasks/<id>` | Get one task | Yes | API |
| PUT | `/api/tasks/<id>` | Update task | Yes | API |
| DELETE | `/api/tasks/<id>` | Delete task | Yes | API |
| GET | `/api/dashboard` | Counters JSON | Yes | API |
| GET | `/static/style.css` | Stylesheet | No | Static file |

**Things the app does not have:** category management, password change, account deletion, password reset, task detail page, API logout.

---

## 4. States and Transitions

### 4.1 Task done / open

| Current state | What triggers it | New state | What else changes |
|---|---|---|---|
| (none) | Create task (F-08, F-19) | Open | `completed_at` is empty |
| Open | Web toggle (F-12) or API `done` true (F-21) | Done | `completed_at` = now |
| Done | Web toggle (F-12) or API `done` false (F-21) | Open | `completed_at` cleared |
| Done | API `done` true again | Done | `completed_at` stays the same |
| Open or Done | Edit title, category or date | Same | Done status unchanged |
| Open or Done | Delete (F-13, F-22) | Deleted | Row removed |

### 4.2 Urgency (worked out when the page loads, not stored)

Checked in this order:

| Condition | Label |
|---|---|
| Task is done | Done |
| No due date | No due date |
| Due date is today or earlier | Overdue (spec says only *past* dates; "Due Today" is never returned) |
| 1 to 2 days away | Due Soon |
| 3 or more days away | Upcoming |

It changes when someone edits the due date, toggles done, or when midnight passes on the server.

### 4.3 Login session

| Current state | What triggers it | New state |
|---|---|---|
| Anonymous | Successful register or login (web/API) | Logged in |
| Logged in | `GET /logout` | Anonymous |
| Anonymous | Failed login | Anonymous (error / 401) |
| Logged in | Login or register as another user | Logged in as the new user (**to verify in UI**) |

---

## 5. Initial Risk Observations

These are the 10 things we think matter most. We only described them and did not fix anything. Severity is our first guess to help decide what to test first.

| # | What we noticed | Where | Severity |
|---|---|---|---|
| 1 | **SQL injection:** the API search text is pasted straight into the SQL query. A single quote in `q` can break it or change results. | `app.py::api_list_tasks` | Critical |
| 2 | **Anyone can delete anyone's task via the API:** the delete query only uses the task id, not the owner. | `app.py::api_delete_task` | Critical |
| 3 | **Stored XSS:** the task title is output with the `safe` filter in the list, so HTML or script typed into a title runs in the browser. | `templates/index.html` | Critical |
| 4 | **Password of exactly 8 characters is rejected**, even though the form says "min 8" (code needs more than 8). | `helpers.py::is_valid_password` | High |
| 5 | **"Due Today" can never appear.** Tasks due today are shown and counted as Overdue. | `helpers.py::compute_urgency` | High |
| 6 | **Duplicate usernames are allowed** (web and API) and the database has no UNIQUE rule. Login picks the first match, so a duplicate may be unusable. | `app.py::register_page`, `api_register`, `init_db` | High |
| 7 | **Dates and categories are never validated.** A badly formatted date saved through the API may crash the list and dashboard pages for that user (500 error). To verify. | `app.py::api_create_task`, `helpers.py::compute_urgency` | High |
| 8 | **Debug mode is on** (`debug=True`), which shows detailed error pages and the Werkzeug debugger. | `app.py` bottom | High |
| 9 | **The secret key is written in the source code**, so session cookies could be forged. | `app.py` | High |
| 10 | **"Completed in last 7 days" leaves out tasks completed exactly 7 days ago**, though the comment says it should include them. | `helpers.py::completed_in_last_n_days` | Medium |

**Smaller things we spotted but left out of the top 10:** web forms don't check the title on the server, API update validates nothing, wrong JSON types likely cause 500 errors, pagination has no limits, no CSRF protection, no rate limiting on login, and `/api/categories` needs no login.

### Notes for running the tests

- The database file `pytodo_pro.db` keeps everything between runs, so delete it for a fresh start.
- Urgency and "last 7 days" tests depend on today's date, so create tasks with dates relative to today.
