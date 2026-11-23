# UI vs API Comparison (Week 4)

**Prepared by:** QA/Test Lead
**Based on:** `app.py`, `helpers.py`, `templates/`, `04_Web_API/api_endpoints.md`, `04_Web_API/api_test_cases.md`, `01_Black_Box/feature_inventory.md`, `01_Black_Box/tc_bva.md`, `01_Black_Box/EP_Test_Cases.md`, `01_Black_Box/defect_log.md` and `03_Special_Testing/usability_observations.md`. We did not change any app code. We only test our local copy at 127.0.0.1. The API results come from our PyTest run on the Flask test client.

## 1. Introduction

The web pages and the API do the same jobs, so they should follow the same rules. Some rules only exist in the browser, for example the HTML `required` attribute or the date picker. A browser check can be skipped by calling the API (or the web route) directly, so the server has to check again. We compare the two to find rules that are missing on the server, and cases where the web form and the API give different answers.

## 2. Rules table

"Server" means a check in the Python code. "HTML" means an attribute in a template, such as `required` or `type="date"`. "JS" means JavaScript in the page. The last column says whether the UI and the API behave the same.

| Feature | Rule | Enforced in UI? (HTML / JS / server) | Enforced in API? | Code location | Same or different? |
|---|---|---|---|---|---|
| Register | Username is 3 to 20 characters, letters, numbers or underscore | Server. The hint text is only a label. There is no `pattern` or `maxlength` in the HTML | Server, same function | `helpers.py::is_valid_username`, used by `app.py::register_page` and `api_register` | Same. Error text differs ("Username must be 3-20 characters..." vs `invalid username`) |
| Register | Password is at least 8 characters (spec) | Server, but the code needs more than 8, so 8 is rejected (D-004). Hint says "min 8" | Server, same function, same bug | `helpers.py::is_valid_password` | Same (both wrong). Error text differs |
| Register | Username and password are required | HTML `required` and server (empty fails the checks) | Server (missing key fails the checks, API-REG-05 to 07) | `templates/register.html`, `register_page`, `api_register` | Same |
| Register | Username is a string | Always true from a text box | Not checked. An integer crashes `.strip()` (DEF-API-01) | `api_register` line `(data.get("username") or "").strip()` | Different. The form cannot send an integer, the API can |
| Register | Username must be unique | Not enforced (comment "no uniqueness check") | Not enforced (DEF-API-02, API-REG-09) | `register_page`, `api_register`, `users` table has no UNIQUE | Same (both missing, D-013) |
| Login | Username and password are required | HTML `required` only. Server just fails the lookup | Not checked. Empty values give 401 | `templates/login.html`, `login_page`, `api_login` | Same result, but the UI check is only in the browser |
| Login | Wrong username or wrong password gives one message | Server: "Invalid username or password." | Server: 401 `invalid credentials` | `login_page`, `api_login` | Same |
| Login | Username is a string | Always true from a text box | Not checked. Integer crashes (DEF-API-03) | `api_login` | Different |
| Login required | Logged-out users cannot use task pages | Server: redirect to `/login` | Server: 401 JSON | `login_required_web`, `login_required_api` | Same rule, different response |
| Create task | Title is required | HTML `required` only. The server does not check | Server: blank title gives 400 `title is required` | `templates/task_form.html`, `new_task`, `api_create_task` | Different. The API is stricter |
| Create task | Title with only spaces is rejected | Not enforced. HTML `required` accepts spaces and the server only strips (D-011) | Server: stripped, then rejected | `new_task` (`.strip()` only), `api_create_task` (`if not title`) | Different. The API is stricter |
| Create task | Title has a maximum length | Not enforced (no `maxlength`) | Not enforced | `task_form.html`, `new_task`, `api_create_task` | Same (both missing, D-012) |
| Create task | Category is one of the 4 categories | HTML `select` only. The server does not check | Not checked. A bad id is saved and shows category `null` | `task_form.html`, `new_task`, `api_create_task` | Different, but both server sides are missing the check |
| Create task | Due date is a real date | HTML `type="date"` only | Not checked (D-006 shows a bad date then breaks the list) | `task_form.html`, `new_task`, `api_create_task`, `helpers.py::compute_urgency` | Different. UI check is browser only |
| Create task | Past or today's date is allowed | No rule. Accepted | No rule. Accepted | same | Same. Today shows "Overdue" in both (D-001) because `compute_urgency` is shared |
| Edit task | Task must exist and belong to the user | Server. If not, silent redirect to `/` | Server. 404 `not found` | `edit_task`, `api_update_task` | Different. UI says nothing (US-14), API says 404 |
| Edit task | Title is required and not blank | HTML `required` only. Server does not check | Not checked. `data.get("title", ...)` accepts anything | `edit_task`, `api_update_task` | Different. API edit is weaker than API create |
| Toggle done | Task must exist and belong to the user | Server. If not, silent redirect | Server. 404 | `toggle_task`, `api_update_task` | Different |
| Toggle done | Value of `done` | The server flips the current state itself. No input | `done` is used as sent. The string `"false"` counts as done | `toggle_task`, `api_update_task` | Different by design. There is no toggle endpoint |
| Delete task | Only the owner can delete | Server: query has `AND user_id = ?` | Not enforced. Query is `WHERE id = ?` | `delete_task_web`, `api_delete_task` | Different. The API is weaker |
| Delete task | Missing task id gives a clear answer | Silent redirect | Always 200 `ok` | same | Different |
| Delete task | Ask before deleting | JS `confirm()` popup only | None | `templates/index.html` | Different. Browser only |
| Search and filter | Search text is matched as plain text | Server: parameterised `LIKE ?`, but `%` and `_` are wildcards (D-014) | Server: text pasted into the SQL, wildcards also work, and a quote can change the query | `index`, `api_list_tasks` | Different. The API is weaker (SQL injection risk) |
| Search and filter | Unknown category or status is ignored | Server | Server | `index`, `api_list_tasks` | Same |
| Search and filter | Dropdowns submit by themselves | JS `onchange` only | Not relevant | `templates/index.html` | UI only, no rule |
| List | Page size limit | No paging at all | `per_page` has no maximum | `index`, `api_list_tasks` | Different (Week 5 performance topic) |

## 3. Comparison test cases

**How to read this table**
- "Expected" is the rule we think both should follow. Where the spec and the code disagree (for example the 8-character password) we use the spec.
- **UI Actual** comes from our earlier results. We cite the ID (US-xx from `usability_observations.md`, TC-BB or D- from Week 1). "Checked by hand" means we ran it in the browser with our two test accounts. We did not take screenshots for these, so we should add them.
- **API Actual** comes from running `tests/test_ui_vs_api.py`. The output is in `evidence_ui_vs_api.txt`.
- **Match?** means the UI and the API behave the same. Yes = same, No = different, Partly = same result but the rule is in a different place, N/A = the form cannot send this input.
- **Defect ID** is an existing ID where one fits. "New, to log" means we found it in this comparison and nobody has logged it yet.
- **Evidence** lists the UI screenshot, and the pytest output for the API side. UI screenshots are in `03_Special_Testing/evidence/usability_testing/` and `01_Black_Box/evidence/BVA/`.

| ID | Feature | Input | Expected (same rule in both) | UI Actual | API Actual | Match? | Evidence | Defect ID |
|---|---|---|---|---|---|---|---|---|
| TC-API-UI-01 | Register | Password `1234567` (7 chars) | Rejected with an error | Rejected (TC-BB-BVA-F01-01, Pass) | Rejected (400) | Yes | TC-BB-BVA-F01-01_Actual.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-02 | Register | Password `12345678` (exactly 8 chars) | Accepted (spec says min 8) | Rejected with "Password must be at least 8 characters." (US-05, D-004) | Rejected (400), same bug as the UI | Yes | US-05.png, evidence_ui_vs_api.txt | D-004 |
| TC-API-UI-03 | Register | Password `123456789` (9 chars) | Accepted | Accepted (TC-BB-BVA-F01-03, Pass) | Accepted (201) | Yes | TC-BB-BVA-F01-03-1_Actual.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-04 | Register | Username that already exists, same password | Rejected with an error such as "username already in use" | Accepted, no warning (US-04, D-013). Week 1 TC-BB-002 said Pass, but the retest showed it was wrong | Accepted (201), duplicate user created | Yes | No screenshot for US-04, evidence_ui_vs_api.txt | D-013, DEF-API-02 |
| TC-API-UI-05 | Register | Username of 2 characters (`ab`) | Rejected | Rejected with "Username must be 3-20 characters (letters, numbers, underscore)." (US-03) | Rejected (400) | Yes | US-03a.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-06 | Register | Username sent as a number (`12345`) | Rejected with an error, no crash | Cannot be sent from the form, it only sends text | Crash, 500 (`AttributeError` on `.strip()`) | N/A | evidence_ui_vs_api.txt | DEF-API-01 |
| TC-API-UI-07 | Login | Existing username, empty password | Rejected, not logged in | Blocked by the browser: "Please fill out this field." and the form is not sent (US-08). The server was not reached | Rejected, not logged in (401 or 400) | Yes | US-08.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-08 | Login | Existing username, wrong password | Rejected with one general message | "Invalid username or password." (US-06) | Rejected (401) `invalid credentials` | Yes | US-06a.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-09 | Create task | Title empty (`""`) | Rejected | Blocked only by the browser's required popup (US-11, TC-BB-005, TC-BB-BVA-F08-01). Per code, the server would save it if the browser check was skipped | Rejected (400) `title is required` | Partly | TC-BB-BVA-F08-01_Actual.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-10 | Create task | Title of only spaces (`"   "`) | Rejected | Accepted. The list shows a row with no visible title (US-11, D-011) | Rejected (400) | No | US-11b.png, evidence_ui_vs_api.txt | D-011 (UI side) |
| TC-API-UI-11 | Create task | Title `A` (1 character) | Accepted | Accepted (TC-BB-BVA-F08-02, Pass) | Accepted (201) | Yes | TC-BB-BVA-F08-02-1_Actual.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-12 | Create task | Title of 500 characters | Same answer in both. No length rule in the spec, we expect some limit | Long title accepted with no limit, it squashes the table (US-11, D-012). We did not test exactly 500 characters in the UI | Accepted (201), no length limit | Yes | US-11c.png, evidence_ui_vs_api.txt | D-012 |
| TC-API-UI-13 | Create task | Due date in the past (`today - 30 days`) | Accepted, badge "Overdue" | Accepted with no warning, shows "Overdue" (US-11, US-11d) | Accepted (201), urgency `Overdue` | Yes | US-11d.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-14 | Create task | Due date today | Badge "Due Today" (spec) | Shows "Overdue" (US-18, D-001) | Accepted (201), urgency `Overdue`, not `Due Today` | Yes | US-18.png, evidence_ui_vs_api.txt | D-001 |
| TC-API-UI-15 | Create task | Due date in a wrong format (`04-11-2026`) | Rejected | Cannot be sent from the form. The date picker only sends `YYYY-MM-DD` | Crash, 500 (`ValueError` in `compute_urgency`). The task is saved before the crash | N/A | evidence_ui_vs_api.txt | D-006 |
| TC-API-UI-16 | Create task | Category id that does not exist (`999`) | Rejected | Cannot be sent from the form. The dropdown only has the 4 categories | Accepted (201), no category check | N/A | evidence_ui_vs_api.txt | New, to log |
| TC-API-UI-17 | Edit task | Task id that does not exist | A clear "not found" answer, nothing changes | Silently goes back to My Tasks with no message (US-14) | 404 `not found` | No | None (US-14 has no screenshot), evidence_ui_vs_api.txt | None (US-14 is Minor, not logged) |
| TC-API-UI-18 | Edit task | Existing task, title changed to empty | Rejected | Checked by hand: blocked by the browser's required popup, the server was not reached | Accepted (200), title became empty | No | evidence_ui_vs_api.txt (UI: no screenshot yet) | New, to log |
| TC-API-UI-19 | Edit task | Another user's task id (two test accounts) | Not changed, same answer as "not found" | Checked by hand: silent redirect to My Tasks, the task is not changed (TH-22) | 404, the title did not change | Partly | evidence_ui_vs_api.txt (UI: no screenshot yet) |  |
| TC-API-UI-20 | Toggle done | Own open task, mark done, then reopen | Done with a completion time, then open again with no completion time | Works. Tick, crossed out, "Done", then back to the urgency badge (US-17) | Works. Done gives `completed_at`, reopen clears it | Yes | US-17a.png, US-17b.png, evidence_ui_vs_api.txt |  |
| TC-API-UI-21 | Toggle done | Task id that does not exist | A clear "not found" answer | Checked by hand: silent redirect to My Tasks, no message | 404 | No | evidence_ui_vs_api.txt (UI: no screenshot yet) |  |
| TC-API-UI-22 | Toggle done | `done` sent as the text `"false"` on an open task | Task stays open, or the request is rejected | Cannot be sent from the form, the button has no value | Accepted (200), task became done | N/A | evidence_ui_vs_api.txt | New, to log |
| TC-API-UI-23 | Delete task | Task id that does not exist | A clear "not found" answer | Checked by hand: silent redirect to My Tasks, no message | 200 `ok`, no 404 | No | evidence_ui_vs_api.txt (UI: no screenshot yet) | New, to log |
| TC-API-UI-24 | Delete task | Another user's task id (two test accounts) | Not deleted, same answer as "not found" | Checked by hand: nothing is deleted, silent redirect (TH-22) | 200, not refused. The test stopped at the status, so we still have to check that the task is gone | No | evidence_ui_vs_api.txt (UI: no screenshot yet) | New, to log. See also TH-21 |
| TC-API-UI-25 | Search | Text `due_today` with a task titled `due_today` and one titled `due today` | Only the exact `due_today` task | Both tasks match, `_` is a wildcard (US-24, D-014) | Both tasks returned, `_` is a wildcard | Yes | US-24.png, evidence_ui_vs_api.txt | D-014 |
| TC-API-UI-26 | Search | Text `100%` with a task titled `100% done` and one titled `100 done` | Only `100% done` | Checked by hand: both tasks match, `%` is a wildcard | Both tasks returned, `%` is a wildcard | Yes | evidence_ui_vs_api.txt (UI: no screenshot yet) | D-014 |
| TC-API-UI-27 | Search | Text `a'` (one quote) | No error, treated as plain text | Checked by hand: no error, the quote is treated as text | Crash, 500 (`sqlite3.OperationalError: unrecognized token`) | No | evidence_ui_vs_api.txt (UI: no screenshot yet) | New, to log. See also TH-07 |
| TC-API-UI-28 | No login | Create a task without logging in | Refused | Checked by hand: redirected to `/login` | Refused (401) | Yes | evidence_ui_vs_api.txt (UI: no screenshot yet) |  |
| TC-API-UI-29 | No login | Edit a task without logging in | Refused | Checked by hand: redirected to `/login` | Refused (401) | Yes | evidence_ui_vs_api.txt (UI: no screenshot yet) |  |
| TC-API-UI-30 | No login | Delete a task without logging in | Refused | Checked by hand: redirected to `/login` | Refused (401) | Yes | evidence_ui_vs_api.txt (UI: no screenshot yet) |  |

Notes on the test cases:
- For TC-API-UI-06, 15, 16 and 22 the web form has no way to send the input. The UI column shows what the form allows, so a mismatch there says the API trusts input that the form would never send.
- All cases now have a UI result, or cannot be sent from the form (4 cases, see above). The 10 cases marked "Checked by hand" were tested in the browser with two test accounts (`syasya_test1`, `syasya_test2`). They have no screenshots yet.

### What the run showed

Match? count: Yes 17, No 7, Partly 2, N/A 4.

- **Same in both (17):** the password and username length checks, duplicate usernames being accepted, no title length limit, "Due Today" shown as "Overdue", `_` and `%` as wildcards, and refusing requests with no login (the UI redirects, the API returns 401). Most of these are shared bugs. Fixing the shared code (`helpers.py`, the `users` table) fixes both sides.
- **Different (7):**
  - The API is stricter than the UI for a whitespace title (10).
  - The API gives a clear 404 for a missing task on edit and toggle (17, 21), where the UI redirects with no message. The API delete returns 200 for a missing task (23).
  - Empty title on edit: the UI blocks it only in the browser, the API saves it (18).
  - Delete another user's task: the UI refuses it, the API returns 200 (24, TH-21).
  - A single quote in search: the UI treats it as text, the API crashes with a 500 SQL error (27, TH-07).
- **API-only problems we confirmed (N/A, 4):** an integer username crashes register (06, DEF-API-01), a bad date crashes the request after saving the task (15, D-006), an unknown category is accepted (16), and `done` as the text `"false"` completes the task (22).
- **API edit is weaker than API create (18).** `PUT` with an empty title returns 200 and saves it. `POST` rejects the same title.
- **Search (27).** A single quote gives a 500 SQL error in the API only. This confirms the SQL injection risk (TH-07).
- **Partly (2).** A blank title on create (09) and another user's task on edit (19): the result is the same, but the UI and the API get there in different ways.

## 4. Automated tests

Our Automation/Tool Coordinator's setup exists. It is in `04_Web_API/tests/` (not in a `tests/` folder at the project root). It uses PyTest and the Flask test client, so there are no real network calls.

We wrote `04_Web_API/tests/test_ui_vs_api.py` and ran it: **16 passed, 14 failed** (output in `evidence_ui_vs_api.txt`). Things to know:

- There is one test for each case from TC-API-UI-01 to TC-API-UI-30. The ID is in the test name, for example `test_tc_api_ui_02_password_8_chars_accepted`.
- Each test checks the **Expected** column, not what the app does now. A failing test means the API does not follow the shared rule, which may be a defect. The 14 that failed are 02, 04, 06, 12, 14, 15, 16, 18, 22, 23, 24, 25, 26 and 27.
- Each test starts with a fresh temporary database. The existing `client` fixture in `conftest.py` uses the real `pytodo_pro.db`, so we did not reuse it. This way our tests do not add rows to the real file.
- Our first run showed five wrong failures (04, 07, 08, 19, 24) with "Cannot operate on a closed database". This was a mistake in our test fixture, not an app defect. We fixed it and ran again. The results below are from the second run.
- We set `PROPAGATE_EXCEPTIONS` to `False` inside the fixture. This turns a crash into a 500 response, so the test fails on the status code and does not stop with an exception.
- Run it with `pytest 04_Web_API/tests/test_ui_vs_api.py -v`.

## 5. Rules that exist only in the UI

These rules are only in the browser, or the UI and the API disagree. We have not confirmed any of them yet, so all are **likely defect, confirm by testing**.

1. **Title is required (HTML `required` only).** `new_task` and `edit_task` do not check for an empty title. If the browser check is skipped, the web server saves a blank title. The API create route does check it. Likely defect in the web routes. Confirm by posting to `/tasks/new` with the Flask test client.
2. **Title with only spaces.** The web form accepts it (D-011). The API create route rejects it. Likely defect in the web routes. The API edit route (`PUT`) has no title check at all, so it is also likely a defect.
3. **Category choice (HTML `select` only).** No server check in the web form or in the API. Likely defect. Confirm with `category_id` 999.
4. **Due date format (HTML `type="date"` only).** No server check anywhere. A bad date can break the task list with a 500 error (D-006). Likely defect in both the web routes and the API.
5. **Delete confirmation (JS `confirm()` only).** The API deletes straight away. This is by design for an API, but the API also does not check the owner, which is a bigger problem (TH-21).
6. **Delete, edit and toggle for a missing id.** The web routes redirect silently and the API delete always returns 200. Only the API edit returns 404. Likely defect, because the user and the caller are not told that nothing happened.
7. **Hints in the labels.** The username hint and the password hint ("min 8") are only text. The server does enforce a rule, but the password rule is different from the hint (D-004).

Rules that are **missing in both** the UI and the API: unique usernames (D-013) and a maximum title length (D-012).

Rules that exist **only in the API**: the blank-title check on create, and the 404 for a missing task on edit. The web forms do not have these.

## 6. Limitations

- UI Actual comes from Week 1 and Week 3 results. 10 of the 30 cases were checked by hand in the browser and have no screenshots yet.
- The Flask test client calls the app directly. It does not test the real HTTP server, browsers or cookies over the network.
- For the web routes we only compare against what the browser did. We did not post to the web routes without the browser. We would like to add this to see the web server rules on their own.
- Ratings and "likely defect" notes are from reading the code. They are not confirmed.
