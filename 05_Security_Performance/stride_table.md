# PyTodo Pro: STRIDE Threat Table (Week 5)

**Prepared by:** QA/Test Lead
**Based on:** reading `app.py`, `helpers.py`, `templates/`, `static/style.css`, `01_Black_Box/feature_inventory.md`, `01_Black_Box/test_scope_matrix.md`, `01_Black_Box/defect_log.md` and `03_Special_Testing/usability_observations.md`. We did not change any app code and we did not run any attack or tool to write this table. The ratings are our own guesses from reading the code.

## 1. Introduction

STRIDE is a checklist for thinking about what could go wrong with a system. The letters stand for Spoofing (pretending to be someone else), Tampering (changing data), Repudiation (denying an action and no way to prove it), Information disclosure (leaking data), Denial of service (making the app unusable) and Elevation of privilege (doing something you are not allowed to do). We use it because it gives us a simple way to go through the app in order, and it helps us pick safe tests for the rest of Week 5.

## 2. Assets

| Asset ID | Asset | Where it lives | Why it matters |
|---|---|---|---|
| A-01 | User accounts | `users` table (id, username). `/register`, `/login`, `/api/register`, `/api/login` | The account decides who owns which tasks. A fake or duplicate account can confuse people or let someone act as another user. |
| A-02 | Passwords | `users.password_hash`. Hashed with `generate_password_hash` in `app.py` | People reuse passwords, so a leak can hurt them on other sites too. |
| A-03 | Tasks | `tasks` table. `/`, `/tasks/new`, `/tasks/<id>/...`, `/api/tasks` | Titles, descriptions and dates are private. Losing or leaking them hurts the user. |
| A-04 | Session cookie | The `session` cookie Flask sets after login | Whoever holds the cookie is logged in as that user. |
| A-05 | Secret key | `app.config["SECRET_KEY"]` in `app.py` | Flask uses it to sign the cookie. Anyone who knows it can make a cookie that looks real. |
| A-06 | Database file | `pytodo_pro.db` in the project folder. It is not tracked by git (it is in `.gitignore`) | All users, hashes and tasks are in this one file. |
| A-07 | The app and server | `app.py`, `app.run(debug=True)`, the Werkzeug debug console, the Flask dev server | If it is down or taken over, nothing works. Debug mode gives extra access. |

## 3. Safe testing rules

- Everything runs on our local copy at `127.0.0.1:5000`. Nothing outside our own machine.
- We use our own test accounts (`syasya_test1`, `syasya_test2`) and throwaway accounts only.
- Normal browser actions, DevTools, or a short script of our own. No external scanners, no password cracking, no flooding.
- Where a test sends many requests, we keep the number small (for example 20).
- Reset by deleting `pytodo_pro.db` after the tests, as in the Week 1 notes.

How to read the ratings. **Likelihood** is how easy it would be to happen if someone tried. **Impact** is how bad it is if it happens. Both are H (high), M (medium) or L (low).

## 4. STRIDE threat table

| Threat ID | STRIDE category | Asset ID | Function/Route | Threat | Evidence from code or earlier testing | Likelihood | Impact | Safe test idea | Test now or Week 4? |
|---|---|---|---|---|---|---|---|---|---|
| TH-01 | Spoofing | A-02, A-01 | `/login`, `/api/login` | Someone guesses a user's password by trying again and again. Nothing slows them down, and the password rule is weak (any 9 or more characters). | `app.py::login_page` has no attempt counter or delay. `helpers.py::is_valid_password` only checks length. Suspected, to confirm by testing. | M | H | Enter 10 wrong passwords in a row for `syasya_test1` by hand and check we are never blocked or slowed. | Test now |
| TH-02 | Spoofing | A-01 | `/register`, `/api/register`, `/login` | A new user registers a name that is already taken, so two accounts look the same. Login picks one of them, so one user may be locked out, and other people may mix them up. | `app.py::register_page` has the comment "no uniqueness check". The `users` table has no UNIQUE rule. US-04, D-013. | H | M | Register the same username twice with different passwords, then log in with each password and see which account loads. | Test now |
| TH-03 | Spoofing | A-04, A-05 | All logged-in routes | If someone knows the secret key, they can sign their own cookie and pretend to be any user id. The key is written in the source code. | `app.py`: `SECRET_KEY = "pytodo-pro-dev-secret"`. Flask signs the cookie with it. Suspected, to confirm by testing. | M | H | In DevTools, read our own cookie and check it only holds the user id and username. Then sign a cookie for `syasya_test2` with the key from the source, on our local copy. | Test now for reading the cookie, Week 4 for the forging script |
| TH-04 | Spoofing | A-04 | `/logout` | A copied cookie may still work after the user logs out, because the login is kept in the cookie and not on the server. | `app.py::logout` only calls `session.clear()`, which clears the browser's copy. The app keeps no list of valid sessions. Suspected, to confirm by testing. | L | M | In DevTools, copy our own cookie value, log out, paste the old value back, reload `/` and see if we are still logged in. | Test now |
| TH-05 | Tampering | A-03 | `/`, `/tasks/new`, `/tasks/<id>/edit` | HTML or script in a task title runs in the browser. If another site can add a task to someone else's account (see TH-06), the script runs in that person's browser. | `templates/index.html` prints the title with the `safe` filter. D-010, GUI-10 (bold tags worked). | M | H | Create a task titled `<b>x</b>` (done in GUI-10), then one with `<script>alert(1)</script>`, on our own test account only. | Test now |
| TH-06 | Tampering | A-03, A-04 | POST `/tasks/new`, `/tasks/<id>/edit`, `/tasks/<id>/toggle`, `/tasks/<id>/delete` | Another website could make a logged-in user's browser send these requests without the user knowing. The forms have no CSRF token. | No token in `app.py` or in any form in `templates/`. Chrome may block some of this by default, other browsers may not. Suspected, to confirm by testing. | M | M | Write a small HTML page on our own machine with a form that posts to `http://127.0.0.1:5000/tasks/new`. Open it while logged in and see if a task appears. Try Chrome and Firefox. | Test now |
| TH-07 | Tampering | A-03, A-06 | GET `/api/tasks?q=` | The search text goes straight into the SQL. A user can change the query. A single quote may break it, and an always-true condition may switch off the filter by user id. | `app.py::api_list_tasks`: `query += f" AND title LIKE '%{q}%'"`, with the comment "intentionally simple". Feature inventory risk 1. | H | H | With two test accounts, send `q=a'` and look for a 500 error. Then send a simple always-true condition and check if the other account's tasks come back. | Week 4 |
| TH-08 | Tampering | A-03 | `/` search box | `%` and `_` in the search act as wildcards, so results do not match what the user typed. Only the user's own tasks can match, so the harm is small. | `app.py::index`: `LIKE ?` with `%{q}%`, no escaping. US-24, D-014. | H | L | Already done: searching `due_today` matched "due today" (US-24). Repeat with `%`. | Test now (done for `_`) |
| TH-09 | Tampering | A-03 | `/tasks/new`, `/tasks/<id>/edit`, `/api/tasks` | The server accepts a title of only spaces, a title of any length, and any category or date text. Bad data gets saved. | `app.py::new_task` and `edit_task` strip the title but never check it is empty. US-11, D-011, D-012. | H | L | Create a task with a title of only spaces and one with a very long title (done in US-11). | Test now (done) |
| TH-10 | Repudiation | A-01, A-03 | All routes | A user could say "I did not delete that task" and we could not prove it. Nothing records who did what and when. Failed logins are not recorded either. | No logging code in `app.py` or `helpers.py`. Tasks only store `created_at` and `completed_at`. Flask only prints requests to the console. | M | L | Create, edit and delete a task, then look in the console output and in `pytodo_pro.db` for any record of the delete. | Test now |
| TH-11 | Information disclosure | A-07 | Any error page, `/console` | Debug mode shows error pages with source code and variables. It also turns on the Werkzeug console, which can run Python code if someone gets past its PIN. It is only reachable from other machines if the host is changed. | `app.py` last line: `app.run(debug=True)`. Feature inventory risk 8. | M | H | On `127.0.0.1` open `/console` and see if it loads. Note what the error page shows when we get a 500 error. | Test now |
| TH-12 | Information disclosure | A-03, A-04 | `/dashboard`, `/` after `/logout` | After logout, the Back button shows old pages with the user's tasks and counts. On a shared computer the next person can read them. | No `Cache-Control` header is set in `app.py`. US-29 (seen on the dashboard). | M | M | Log out, press Back and see which pages still show. Repeat on the task list. | Test now |
| TH-13 | Information disclosure | A-02, A-06 | `pytodo_pro.db` | The database file sits in the project folder. Anyone who can open the project folder on the machine can read usernames and password hashes. The file is not committed to git, so a copy of the repo does not contain it. | `.gitignore` lists `pytodo_pro.db` and `git ls-files` shows no `.db` file (checked 26 Nov). Passwords are hashed with `generate_password_hash` in `app.py::register_page` (we think scrypt with a salt, to confirm). `/static/` only serves the static folder, so the app does not serve the file. | M | H | Open the database file on our own machine with a viewer and check the `password_hash` of our test accounts starts with a hash type like `scrypt:` and not the plain password. | Test now |
| TH-14 | Information disclosure | A-01, A-02, A-03 | GET `/api/tasks?q=` | Same SQL problem as TH-07, but used for reading. Someone could read other users' tasks, and maybe the `users` table with its password hashes. | Same code as TH-07 (`app.py::api_list_tasks`). The `users` table has a `password_hash` column. | H | H | With two test accounts, check that account 2 can see account 1's tasks through `q`. We only try this on our own accounts. | Week 4 |
| TH-15 | Information disclosure | A-04 | The `session` cookie | The cookie holds the user id and username in a readable form (it is signed, not encrypted). We think it has no Secure flag, and the app sets no SameSite option. On plain http it can be copied on a shared network. | `app.py` sets no `SESSION_COOKIE_*` options. We think Flask's defaults are HttpOnly on and Secure off. Suspected, to confirm by testing. | L | M | In DevTools (Application, Cookies) check the HttpOnly, Secure and SameSite columns for our cookie. | Test now |
| TH-16 | Information disclosure | A-07 | GET `/api/categories` | It works without logging in. Category names are not secret, so harm is small. | F-17 in the feature inventory. `app.py::api_categories` has no login check. | H | L | Open `http://127.0.0.1:5000/api/categories` in a private window. | Test now |
| TH-17 | Denial of service | A-03, A-07 | `/`, `/dashboard`, `/api/tasks` | One badly formatted due date makes the task list and dashboard return a 500 error for that user every time. They cannot reach their tasks any more. The web date picker blocks bad dates, but the server does not check them. | `helpers.py::compute_urgency` calls `strptime` with no error handling. D-006 (confirmed through the API in Week 2). Through the web form, suspected, to confirm by testing. | M | H | On a throwaway account, use the API to save a task with date `04-11-2026`, then open `/` as that account and see if it breaks. | Week 4 |
| TH-18 | Denial of service | A-07 | `/`, `/api/tasks`, `/tasks/new` | There are no size limits. The web list loads every task with no paging. The API `per_page` has no maximum. Titles have no length limit. A big list or a long title makes the page slow or hard to read. | `app.py::index` has no LIMIT. `api_list_tasks` takes `per_page` from the URL. D-012, US-11 (long title squashed the table). | M | M | Add a few dozen tasks and one very long title on a test account and see how the pages react. In Week 4, try a large `per_page`. | Test now for the web pages, Week 4 for the API |
| TH-19 | Denial of service | A-07, A-01 | `/register`, `/login`, `/api/register`, `/api/login` | There is no limit on how often someone can register or log in. Many sign-ups fill the database. Password hashing uses CPU, so many logins can also slow the server. | No rate limit in `app.py`. Hashing uses `generate_password_hash` and `check_password_hash`. Suspected, to confirm by testing. | M | M | Send about 20 login requests one after another to our own server with a short script and time each one. | Week 4 |
| TH-20 | Denial of service | A-04 | GET `/logout` | A link or image on another page can log the user out, because logout is a plain GET link. It is annoying but does not leak data. | `app.py::logout` has no `methods` limit, so it accepts GET. US-29. | M | L | Type `127.0.0.1:5000/logout` in the address bar while logged in. Also put it in an `<img>` tag on our test page from TH-06. | Test now |
| TH-21 | Elevation of privilege | A-03 | DELETE `/api/tasks/<id>` | Any logged-in user can delete any other user's task by changing the id. | `app.py::api_delete_task` has the comment "deletes by id only" and no `user_id` in the query. Feature inventory risk 2, F-22. | H | H | Log in as `syasya_test2`, delete the id of one of `syasya_test1`'s tasks, then log in as `syasya_test1` and check it is gone. | Week 4 |
| TH-22 | Elevation of privilege | A-03 | `/tasks/<id>/edit`, `/toggle`, `/delete`, GET and PUT `/api/tasks/<id>` | A user opens, edits, toggles or deletes another user's task by changing the id. The code looks safe, because each of these queries also checks `user_id`. | `edit_task`, `toggle_task`, `delete_task_web`, `api_get_task` and `api_update_task` all use `AND user_id = ?`. Looks safe, to confirm by testing. | L | H | As `syasya_test2` open `/tasks/<id of a test1 task>/edit`. For toggle and delete, change the id in the form action using DevTools. Check nothing changes. | Test now |

### 4.1 Outcome after the Week 5 tests (added 26 Nov)

This table was written before the tests. We added the results later so it matches `security_test_cases.md` and `07_Test_Management/defect_log.md`. A Fail means the weakness is confirmed.

| Threat | Test | Result | Defect |
|---|---|---|---|
| TH-01 | TC-SEC-01 | Fail | D-026 |
| TH-02 | TC-SEC-02 | Fail | D-013 |
| TH-03 | TC-SEC-03 | Fail | D-027 |
| TH-04 | TC-SEC-04 | Fail | D-028 |
| TH-05 | TC-SEC-05 | Fail | D-010 |
| TH-06 | TC-SEC-06 | Fail | D-029 |
| TH-07 | TC-SEC-07 | Fail | D-020 |
| TH-08 | TC-SEC-08 | Fail | D-014 |
| TH-09 | TC-SEC-09 | Fail | D-011 |
| TH-10 | TC-SEC-10 | Fail | D-030 |
| TH-11 | TC-SEC-11 | Fail | D-031 |
| TH-12 | TC-SEC-12 | Fail | D-032 |
| TH-13 | TC-SEC-13 | Pass | none |
| TH-14 | TC-SEC-14 | Fail | D-020 |
| TH-15 | TC-SEC-15 | Fail | D-033 |
| TH-16 | TC-SEC-16 | Pass | none |
| TH-17 | TC-SEC-17 | Fail | D-006 |
| TH-18 | TC-SEC-18 | Fail | D-034 (the title length part is D-012) |
| TH-19 | TC-SEC-19 | Fail | D-026 |
| TH-20 | TC-SEC-20 | Fail | D-035 |
| TH-21 | TC-SEC-21 | Fail | D-025 |
| TH-22 | TC-SEC-22 | Pass | none |

TH-13 changed after testing: the database is not in git, so the threat is only about someone who can open the project folder. The Likelihood and Impact ratings in the table above were not changed. They were set when we thought the file was in git, so the group should look at them again.

Note on Elevation of privilege: the app has no admin role. There are only two kinds of visitor, anonymous and logged in. So here it means acting as another user or touching their data. TH-03, TH-07 and TH-14 also belong to this idea.

Note on Spoofing: the login page gives the same message for a wrong username and a wrong password, so it does not show which usernames exist. We count that as good.

## 5. Summary: highest-risk threats

We score Likelihood and Impact as H = 3, M = 2, L = 1 and multiply them. The top five:

| Rank | Threat | Score | Why it is high |
|---|---|---|---|
| 1 | TH-21 API delete does not check the owner | 9 | Any logged-in user can delete anyone's task with one request. The code even says it does not check. |
| 2 | TH-07 and TH-14 SQL injection in the API search | 9 | The query is built from user text. It can break the query and may let a user read other people's tasks. |
| 3 | TH-03 Hard-coded secret key | 6 | The key is in the source code. If someone has it, they can act as any user. We still have to confirm this by testing. |
| 4 | TH-05 Task title shown as HTML, with TH-06 no CSRF protection | 6 | Script in a title runs by itself. Together with no CSRF token, another site may be able to put it in someone else's account. We rate TH-05 as M for likelihood only because of that extra step. |
| 5 | TH-11 Debug mode on | 6 | Error pages show code, and the console can run Python code. It is only open to our own machine for now, but it must not be switched on in a real deployment. |

TH-01 (password guessing) and TH-17 (one bad date breaks an account) also score 6 and come next. TH-22 (other users' tasks through the web pages) scores low because the code looks safe, but we still test it, because the impact would be high if we are wrong.

By timing: 15 of the 22 threats can be tested now through the web pages. 5 need the API test setup, so they go to Week 4 (TH-07, TH-14, TH-17, TH-19 and TH-21). TH-03 and TH-18 are split: we test the web part now and the script or API part in Week 4.

## 6. Limitations

- We only read the code and tested a local copy. This is not a real deployment, so some things (HTTPS, the host setting, real network risks) are not covered.
- The ratings come from our own judgement. Another group could rate them differently.
- Many rows say "suspected, to confirm by testing". We do not know yet if they are real until the tests are done.
- We only looked at the code in this repo. We did not check Flask or Werkzeug themselves, or the packages they use.
- We tested nothing outside our own machine, so we cannot say how the app would hold up against real attackers.
- Four people and one week, so we kept the tests small and chose only the ones that look most useful.
