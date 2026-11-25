# Week 4: Web and API Testing

**Prepared by:** QA Test Lead

## 1. Introduction

In Week 4 we tested PyTodo Pro from the web side and the API side. We wrote 8 web workflows and 6 checks that compare what the browser checks with what the server checks. We tested all 9 JSON API endpoints with PyTest and the Flask test client. Then we compared the web form and the API for the same rule, such as password length or an empty title, in 30 cases. We did not change any app code. The main result is that the API is weaker than the web pages. Both Critical defects of the week (D-020 and D-025) exist only in the API.

## 2. Deliverables

| Deliverable | File | Owner (role) |
|---|---|---|
| Web test scenarios | `web_test_scenarios.md` | Test Design Coordinator |
| API test suite: endpoint list | `api_endpoints.md` | Automation/Tool Coordinator |
| API test suite: test cases (register, login, categories, tasks, dashboard) | `api_test_cases.md` | Automation/Tool Coordinator (sections 1 to 3), Test Design Coordinator (sections 4 to 9) |
| API test suite: extra delete and dashboard cases | `api_test_cases_delete_dashboard.md` | Defect & Metrics Coordinator |
| API test suite: PyTest code | `tests/test_api_auth.py`, `tests/test_api_tasks.py`, `tests/test_api_delete_dashboard.py`, `tests/conftest.py` | Automation/Tool Coordinator (auth, `conftest.py`), Test Design Coordinator (tasks), Defect & Metrics Coordinator (delete and dashboard) |
| Request and test data | `api_test_data.md` | Test Design Coordinator |
| Expected versus actual status and response | The Expected and Actual columns in `api_test_cases.md` and `api_test_cases_delete_dashboard.md` | Same owners as the case files |
| Execution evidence | `evidence/evidence_api_auth.txt`, `evidence/evidence_api_tasks.txt`, `evidence/evidence_api_delete_dashboard.txt`, `evidence/evidence_ui_vs_api.txt` | Same owners as the test files |
| Defects | `defect_log.md` (draft IDs for the auth tests only). The official log is `../01_Black_Box/defect_log.md` | Automation/Tool Coordinator (draft), Defect & Metrics Coordinator (official log) |
| UI vs API comparison | `ui_vs_api_comparison.md`, `tests/test_ui_vs_api.py` | QA/Test Lead |
| Week 4 numbers | `Week4_Metrics.md` | Defect & Metrics Coordinator |

Also in the folder: `test_api_smoke.py` (2 setup checks, not part of the 95 cases).

Tool: PyTest with the Flask test client (`app.test_client()`). It sends requests straight to the app, so we need no running server, and it keeps the session cookie between calls.

## 3. How to run the API tests

Nothing needs to be running first. Do not start `python app.py`. The test client talks to the app directly.

Run every command from the project root (the folder that contains `app.py`), not from inside `04_Web_API`. We got a "file not found" error once by running from the wrong folder.

```powershell
.\venv\Scripts\Activate.ps1
pip install pytest
pytest 04_Web_API/tests/ -v
```

`pip install pytest` is only needed if `pytest` is not recognised. `requirements.txt` lists only Flask.

To run one file:

```powershell
pytest 04_Web_API/tests/test_api_auth.py -v
pytest 04_Web_API/tests/test_api_tasks.py -v
pytest 04_Web_API/tests/test_api_delete_dashboard.py -v
pytest 04_Web_API/tests/test_ui_vs_api.py -v
pytest 04_Web_API/test_api_smoke.py -v
```

Two things to know:
- Failures are expected. 30 of the 95 tests fail on purpose, because the app breaks the rule the test checks. A fail means a defect was confirmed, not that the test is broken.
- `test_api_auth.py` (through `conftest.py`) and `test_api_smoke.py` use the app's real database file (`pytodo_pro.db`). The other three files make a temporary database for each test. On a fresh clone the real database has no tables, so `Week4_Metrics.md` says 13 of the 19 auth tests fail with `no such table`. After `init_db()` has run once, the results match ours. We have not re-run this. These tests also leave test users in the real database. We suggest changing `conftest.py` to a temporary database (see section 6).

## 4. Execution summary

All numbers come from `Week4_Metrics.md`, the last lines of the four evidence files, and the case files. We did not run the tests again to write this page. The counts of tests in each file match the number of test functions in the files (19, 36, 10 and 30).

### 4.1 Cases per file

| File | Cases | Pass | Fail | Blocked / Not run | Pass rate |
|---|---|---|---|---|---|
| `test_api_auth.py` (register, login, categories) | 19 | 16 | 3 | 0 | 84.21% (16/19) |
| `test_api_tasks.py` (tasks and dashboard) | 36 | 27 | 9 | 0 | 75.00% (27/36) |
| `test_api_delete_dashboard.py` (extra delete and dashboard) | 10 | 6 | 4 | 0 | 60.00% (6/10) |
| `test_ui_vs_api.py` (UI vs API) | 30 | 16 | 14 | 0 | 53.33% (16/30) |
| Total | 95 | 65 | 30 | 0 | 68.42% (65/95) |

- API endpoint cases only (the first three rows): 65 cases, 49 passed, 16 failed, 75.38% (49/65).
- Execution rate: 100% (95 of 95 run).
- Lowest endpoint: `DELETE /api/tasks/<id>`, 4 of 8 passed (50%).
- Not counted: `test_api_smoke.py` (2 checks, both pass according to `Week4_Metrics.md`) and the web scenarios. The scenarios in `web_test_scenarios.md` have no Pass or Fail column. 8 workflows and 6 validation checks are written, but the file does not say if each was run in a browser. For the 6 checks it records 1 consistent result (with the D-004 note), 4 gaps (duplicate username, blank title, bad date, unknown category) and 1 passed owner check (delete, but no CSRF token).
- The tests ran in different places. The delete and dashboard evidence was made on Linux with Python 3.13. The others were made on Windows. The numbers agree with each other.

### 4.2 Defects found

New in Week 4 (IDs from the official log):

| Defect ID | Title (short) | Severity |
|---|---|---|
| D-019 | API returns HTTP 500 when a text field is sent as a number | Moderate |
| D-020 | SQL injection in `GET /api/tasks?q=` | Critical |
| D-021 | `POST /api/tasks` accepts a category id that does not exist | Moderate |
| D-022 | `PUT /api/tasks/<id>` accepts an empty title | Major |
| D-023 | `"done": "false"` completes the task | Moderate |
| D-024 | Delete returns 200 for a task that does not exist | Minor |
| D-025 | Any user can delete another user's task (IDOR) | Critical |

That is 7 new defects: 2 Critical, 1 Major, 3 Moderate, 1 Minor.

Earlier defects that Week 4 confirmed again through the API: D-001 (due today shows Overdue), D-004 (8-character password), D-005 (7-day counter), D-006 (bad due date, now also breaks the dashboard), D-011 (blank title, also on the web edit route), D-012 (no title length limit), D-013 (duplicate usernames), D-014 (`_` and `%` wildcards). D-011 comes from the web scenarios, the other seven from failing tests.

The 30 failed cases come from 14 different defects (the 7 new ones and D-001, D-004, D-005, D-006, D-012, D-013, D-014). Many failures are the same bug seen from two test files. `defect_log.md` in this folder still uses the draft IDs DEF-API-01 to 03. They are logged as D-019 and D-013.

### 4.3 UI vs API mismatches

From the 30 comparison cases in `ui_vs_api_comparison.md`: 17 match, 7 do not match, 2 match partly, 4 are not applicable (the web form cannot send that input, so only the API can be tested).

The 9 cases that do not match, or match partly:

| Case | What differs | Defect |
|---|---|---|
| TC-API-UI-09 (empty title on create), partly | The web form relies on the browser required popup. The API checks on the server and returns 400. | None |
| TC-API-UI-10 (spaces-only title), no | The web form accepts it. The API rejects it. | D-011 |
| TC-API-UI-17 (edit missing task), no | The web page silently goes back to the list. The API returns 404. | None (Minor, not logged) |
| TC-API-UI-18 (empty title on edit), no | The browser blocks it. The API accepts it. | D-022 |
| TC-API-UI-19 (edit another user's task), partly | Both leave the task unchanged. The web page redirects silently, the API returns 404. | None |
| TC-API-UI-21 (toggle missing task), no | The web page silently redirects. The API returns 404. | None |
| TC-API-UI-23 (delete missing task), no | The web page silently redirects. The API returns 200. | D-024 |
| TC-API-UI-24 (delete another user's task), no | The web page deletes nothing. The API does not refuse. | D-025 |
| TC-API-UI-27 (search with `'`), no | The web search treats it as text. The API crashes with 500. | D-020 |

In every case where the API is weaker, the web route was the stricter one. Only the web side hides the problem, because the browser blocks or redirects before the server is reached.

Limits of these numbers:
- 10 cases (18, 19, 21, 23, 24, 26, 27, 28, 29, 30) were checked by hand in the browser. We have no screenshots for them yet. `WTS-VAL-03.png` is also missing.
- In `ui_vs_api_comparison.md` the Defect ID column still says "New, to log" for cases 16, 18, 22, 23, 24 and 27. They are now D-021, D-022, D-023, D-024, D-025 and D-020. We left that file alone.
- The test for case 24 checks only the status code. It does not yet prove that the other user's task is really gone. The delete and dashboard test `test_api_dd_01` does check this.

## 5. What we learnt and what to pass on

The API is less safe than the web pages. The web routes use a safe search query and check the task owner. The API does not do either in two places, and these are the two Critical defects. Testing only through the browser would have missed both. We also learnt that the server must check every rule itself. The browser `required` tag is not a check, because the API and a changed form can skip it.

The API mostly does check that we are logged in. Every task and dashboard route returns 401 without a login (tests API-TSK-*, API-DASH-03 and TC-API-UI-28 to 30 pass). Reading and editing another user's task returns 404, as it should. Only `DELETE /api/tasks/<id>` has no ownership check. `GET /api/categories` is public on purpose and shows only four names.

For Week 5 (security and performance), we pass on:
- `DELETE /api/tasks/<id>` with no `user_id` in the query (D-025). Another user can delete our task.
- `GET /api/tasks?q=` with the search text pasted into the SQL (D-020). We only proved a syntax error. We did not test whether it can show another user's tasks, so Week 5 should check this safely with two test accounts.
- A bad due date saved through the API breaks the task list and the dashboard (D-006), which could be used to lock a user out.
- Every 500 error: with `debug=True` it may show internal details. This also applies to the type errors in D-019.
- Missing limits. We did not test login or register attempts, or `per_page`, for limits. We only know that no limit exists in the code.

Week 5 followed these up with `TC-SEC-07`, `TC-SEC-14`, `TC-SEC-17` and `TC-SEC-21`.

## 6. Open items

- Change `tests/conftest.py` to use a temporary database, as the other test files do. This stops tests from writing to the real database and fixes the `no such table` failures on a fresh clone. (Automation/Tool Coordinator)
- Add screenshots for the 10 hand-checked UI cases, and upload `WTS-VAL-03.png`.
- Change the draft ID "D-009" in `web_test_scenarios.md` to D-011.
- Update the Defect ID column in `ui_vs_api_comparison.md`.
- Add `pytest` to `requirements.txt`.
- No Week 4 defect is fixed. All 7 are open.

## 7. Endpoint division (corrected)

The old version of this README gave the task endpoints to three different people and named test files that do not exist (`test_api_tasks_read.py` and `test_api_tasks_write.py`). The files show this split.

| Role | Endpoints | Count | Test file |
|---|---|---|---|
| Automation/Tool Coordinator | `POST /api/register`, `POST /api/login`, `GET /api/categories` | 3 | `tests/test_api_auth.py` |
| Test Design Coordinator | `GET /api/tasks`, `GET /api/tasks/<id>`, `POST /api/tasks`, `PUT /api/tasks/<id>`, `DELETE /api/tasks/<id>`, `GET /api/dashboard` | 6 | `tests/test_api_tasks.py` |
| Defect & Metrics Coordinator | Extra checks on `DELETE /api/tasks/<id>` and `GET /api/dashboard` | (same 2) | `tests/test_api_delete_dashboard.py` |
| QA/Test Lead | UI vs API comparison across the endpoints | 30 cases | `tests/test_ui_vs_api.py` |
