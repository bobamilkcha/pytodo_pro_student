# PyTodo Pro: Selected Units for White-Box Testing (Week 2)

Prepared by: QA/Test Lead

This file lists the functions we looked at for white-box testing and the 4 we picked. We are not testing every function. The brief says to choose, and some functions are too simple to learn anything from (for example, ones that only render a template). We picked functions with real decision logic, or that had problems in Week 1.

We read `app.py` and `helpers.py`. There are no other source files. We did not change any app code. The decision counts below are our own manual count, so a tool like coverage.py or radon may count a bit differently.

---

## 1. Candidate list

How we counted decisions: each `if`, `elif`, loop (including generator and list comprehension loops), ternary (`x if c else y`) and `and` / `or` in a condition counts as one. A plain `else` is not counted. The `or {}` and `or ""` defaults on request data count as one each, because they act like a small if.

Week 1 risk is the draft risk (H/M/L) from `01_Black_Box/test_scope_matrix.md`. "n/a" means the function has no feature of its own in the inventory.

| Function | File | What it does | Decisions | Feature ID | Week 1 risk |
|---|---|---|---|---|---|
| compute_urgency | helpers.py | Turns a due date into a label (No due date, Overdue, Due Soon, Upcoming) | 4 | F-14 | H |
| is_valid_password | helpers.py | Checks the password is a string and longer than 8 characters | 1 | F-01, F-02 | H, M |
| is_valid_username | helpers.py | Checks type, length 3-20 and only letters, numbers, underscore | 5 | F-01, F-02 | H, M |
| completed_in_last_n_days | helpers.py | Says if a completion time is within the last N days | 3 | F-15, F-16 | H, L |
| row_to_task | app.py | Turns a database row into a task dict, adds urgency or "Done" | 1 | F-14, F-09 | H, M |
| get_category_name | app.py | Looks up a category name by id | 2 | F-09 | M |
| get_category_id_by_name | app.py | Looks up a category id by name | 1 | F-11 | M |
| login_required_web | app.py | Decorator, redirects to login if no session | 1 | F-06 | M |
| login_required_api | app.py | Decorator, returns 401 if no session | 1 | F-07 | M |
| register_page | app.py | Web register form, validates then creates the user | 3 | F-01 | H |
| login_page | app.py | Web login form, checks username and password | 2 | F-03 | M |
| logout | app.py | Clears the session and redirects | 0 | F-05 | L |
| index | app.py | Task list with category, status and search filters | 6 | F-09, F-11 | M, M |
| new_task | app.py | Web create task | 3 | F-08 | H |
| edit_task | app.py | Web edit task, only for the owner | 4 | F-10 | M |
| toggle_task | app.py | Web mark done / reopen, sets or clears `completed_at` | 3 | F-12 | M (High priority) |
| delete_task_web | app.py | Web delete, scoped to the owner | 0 | F-13 | M |
| dashboard | app.py | Web dashboard counters | 9 | F-15 | H |
| api_register | app.py | API register | 5 | F-02 | M |
| api_login | app.py | API login | 5 | F-04 | L |
| api_categories | app.py | API list of categories | 1 | F-17 | L |
| api_list_tasks | app.py | API task list with filters and paging | 6 | F-18 | M |
| api_get_task | app.py | API get one task | 1 | F-20 | L |
| api_create_task | app.py | API create task | 3 | F-19 | H |
| api_update_task | app.py | API partial update, handles done and `completed_at` | 5 | F-21 | M |
| api_delete_task | app.py | API delete by id (no owner check) | 0 | F-22 | H |
| api_dashboard | app.py | API dashboard counters | 9 | F-16 | L |
| get_db | app.py | Opens the SQLite connection once per request | 1 | n/a | n/a |
| close_connection | app.py | Closes the connection at the end of a request | 1 | n/a | n/a |
| init_db | app.py | Creates tables and default categories | 1 | n/a | n/a |

Notes on the counts:
- `dashboard` and `api_dashboard` have high counts only because of 4 similar generator loops with conditions. They are repetitive, not really hard.
- `register_page` has 3 decisions (POST check, username check, password check). The missing duplicate username check is a case where a decision is *absent*, which a coverage tool will not show.

---

## 2. Selected units

We picked 4. Two are pure functions in `helpers.py` (no Flask needed). Two are Flask routes that need the test client. We wanted a mix, and we wanted each one to have either many decisions or a known problem from Week 1.

Week 1 has no test results yet (the Actual Result columns are still empty), so "Week 1 findings" below means what we noted from reading the code in `feature_inventory.md` and the test cases we wrote.

### Unit 1: `index`

| Item | Detail |
|---|---|
| File and lines | `app.py`, lines 189-222 (decorators at 189-190, function body 191-222) |
| Decisions | 6 (ternary on line 200, ifs on 201, 205, 210, elif on 207, comprehension loop on 216) |
| Assigned to | Test Design Coordinator |

Justification: This is the most complex function we found. It builds an SQL query step by step from three optional filters (category, status, search text), so there are many combinations of paths through it. It is also the main page of the app, so almost every user hits it. The decisions are independent, so we expect the control flow graph to be simple to draw but the path count to be high.

Week 1 link: F-11 (Filter and search) was planned as a decision table. The inventory notes that unknown filter values are ignored and that `%` and `_` act as wildcards because the search text is not escaped. White-box tests can show if every filter branch runs. We should not expect the wildcard behaviour to show up as a coverage gap, since it is not a branch.

How to test: Needs the Flask test client. The function reads `request.args`, uses `session["user_id"]` and queries SQLite, so we cannot call it directly. We will need a test database (a temp file, or monkeypatching `DATABASE`) and a logged-in session.

### Unit 2: `compute_urgency`

| Item | Detail |
|---|---|
| File and lines | `helpers.py`, lines 12-39 |
| Decisions | 4 (if on line 26, if on 28, if on 33, if on 37) |
| Assigned to | Defect & Metrics Coordinator |

Justification: This is the date rule behind the urgency badge and the dashboard Overdue and Due Soon counts, so a mistake here shows up in several places. It has real decision logic with boundaries. It also has a known problem, and it can crash on a badly formatted date because `strptime` is not wrapped in a try.

Week 1 link: Risk observation #5 in the inventory. The docstring says "Due Today" for today's date, but line 33 uses `due <= today`, so today returns "Overdue" and "Due Today" can never be returned. This is a code vs spec difference (F-14, risk H). Observation #7 is also related (a bad date format may cause a 500 error). For white-box, this means no test can ever reach a "Due Today" branch because it does not exist. We will point that out in the coverage report.

How to test: Directly with PyTest. It is a pure function and takes `today` as a parameter, so we can pass a fixed date and need no mocking.

### Unit 3: `completed_in_last_n_days`

| Item | Detail |
|---|---|
| File and lines | `helpers.py`, lines 61-75 |
| Decisions | 3 (if on line 69, if on 71, `and` on line 75, which is two conditions) |
| Assigned to | Automation/Tool Coordinator |

Justification: It feeds the "Completed this week" counter on both dashboards. It has an unusual compound condition (`age.total_seconds() > 0 and age.days < n`), which is good for condition coverage and MC/DC style thinking. It has only 3 decisions, but the boundary is easy to get wrong.

Week 1 link: Risk observation #10 and F-15 (risk H). The docstring says "inclusive of exactly N days ago", but `age.days < n` leaves out anything that is 7 days or older. Also, `total_seconds() > 0` rejects a completion time that is in the future or exactly equal to now. In Week 1 we were not sure how to create a 7-day-old task from the UI. With white-box tests we can pass a `now` value, so this problem goes away.

How to test: Directly with PyTest. It takes `now` as a parameter, so we do not need to mock the clock. A badly formatted string would raise `ValueError`, which we can also check with `pytest.raises`.

### Unit 4: `toggle_task`

| Item | Detail |
|---|---|
| File and lines | `app.py`, lines 269-281 (decorators at 269-270, function body 271-281) |
| Decisions | 3 (if on line 276, ternary on 277, ternary on 278) |
| Assigned to | QA/Test Lead |

Justification: This is the status change logic of the app. It flips `done` and sets or clears `completed_at`, and the dashboard counts depend on it. It also has a permission check, because the query includes `user_id`, so a user cannot toggle someone else's task. Few decisions, but each one matters, and a mistake here quietly corrupts data.

Week 1 link: This is F-12, and the state transition test cases we wrote (TC-BB-070, 071, 073, 077) cover it from the outside. In the state transition notes, toggling another user's task could not be done by hand in the browser because it is a POST. White-box tests with the test client can cover that gap. Doing this also lets us check the `else` branch where the task is not found (T9) in a controlled way.

How to test: Needs the Flask test client. It is a POST route that depends on the session and the database. We will need to set the session (or log in through `/login`) and read the database afterwards to check `done` and `completed_at`.

### Summary of assignments

| Member | Function | File | Lines | Test approach |
|---|---|---|---|---|
| Test Design Coordinator | `index` | app.py | 189-222 | Flask test client |
| Defect & Metrics Coordinator | `compute_urgency` | helpers.py | 12-39 | Direct PyTest |
| Automation/Tool Coordinator | `completed_in_last_n_days` | helpers.py | 61-75 | Direct PyTest |
| QA/Test Lead | `toggle_task` | app.py | 269-281 | Flask test client |

We matched people to the features they had in Week 1 where we could (Automation had F-15, Defect & Metrics had the F-14 decision table, the Test Lead had F-12). The Test Design Coordinator has the most complex function, as agreed, since they lead the control-flow analysis.
