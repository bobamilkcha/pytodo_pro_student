# Week 6: Automation Candidates

**Prepared by:** QA Test Lead

## 1. Introduction

We do not automate every test. Automation takes time to write and fix, and a test we run once or twice is cheaper to do by hand. We also cannot automate judgement, such as "is this page easy to understand?". So we picked the tests that repeat often, give the same answer each time, cover important features, and catch bugs that could come back.

This file is selection only. We did not write any new test code. We read the test files from Weeks 1 to 5 and the central defect log (`01_Black_Box/defect_log.md`).

Things we noticed while reading, so nobody is surprised later:
- The brief mentions `tc_ep` and `tc_decision_table`. In our repo these are `EP_Test_Cases.md` and `tc_defect_coordinator.md`.
- There is no `tests/` folder in the repo root. Our PyTest files are in `02_White_Box_Coverage/`, `04_Web_API/tests/` and `05_Security_Performance/tests/`.
- We did not run any test this week. The "already automated" status comes from the evidence files and the Week 2 and Week 4 metrics. We should re-run everything once before we trust it.
- Selenium is not installed in our `venv` (only Flask and pytest are). Locust is not installed there either. We have not tried a browser driver yet.

## 2. Scoring method

Each test gets 1 to 3 on four criteria. The total is 4 to 12.

| Criterion | 3 | 2 | 1 |
|---|---|---|---|
| Repetition: how often we would run it | Every change | Sometimes | Once or twice |
| Stability: does it give the same answer each time, and does the page or rule stay the same? | Always the same | Mostly | Changes often, or depends on the browser, clock or machine |
| Criticality: how bad is it if this breaks? | Data loss, security, login, core task flow | A normal feature | Looks or wording only |
| Regression value: could this bug come back, or has it already happened? | Known defect or area that broke before | Normal feature that could break | Unlikely to break again |

Rules we used:
- Total 9 or more: Automate = Y.
- Total 8 or less: Automate = N. The test stays manual, or we leave an old test as it is.
- A known defect gets 3 for regression value. These are exactly the tests a regression suite should catch.
- We used the lowest level that can check the rule. A rule in `helpers.py` goes to PyTest unit. A rule in a route goes to PyTest API. Selenium is used only when we need a real browser.

Tool names in the table:
- PyTest unit: calls a function in `helpers.py` directly.
- PyTest API: uses the Flask test client. This covers `/api/...` routes and also the web routes (`/login`, `/tasks/new` and so on), because the test client sends the same requests as a browser form. No browser needed.
- Selenium UI: drives a real browser.

Two honest limits. The scores are our own judgement, so another group could score some rows differently. And one point is not settled: many tests for known defects fail today on purpose (see section 7).

## 3. Candidate table

Week means the week the manual test or test file was written. "Already automated?" says which PyTest test covers it now. Some rows group several test IDs that have the same score and the same reason.

### 3.1 Week 1: EP (Test Design Coordinator)

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-BB-001 | 1 | F-01 Register | EP | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes: API-REG-01 | Sign-up must always work. |
| TC-BB-002 | 1 | F-01 Register | EP | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-API-UI-04, API-REG-09, TC-SEC-02 (fail today, D-013) | The manual result was Pass but D-013 shows it should Fail. Re-run the manual case and keep the automated one. |
| TC-BB-003 | 1 | F-03 Login | EP | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes: API-LOG-02, TC-API-UI-08 | Wrong password must always be refused. |
| TC-BB-004 | 1 | F-08 Create task | EP | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes: API-TSK-POST-01, 02, TC-API-UI-11 | Creating a task is the main action. |
| TC-BB-005 | 1 | F-08 Create task | EP | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: TC-API-UI-09 (API), TC-SEC-09 (web, spaces) | The manual test only checked the browser `required` tag. The server rule is what matters (D-011). |
| TC-BB-006 | 1 | F-14 Urgency | EP | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-01, 02 | Pure function. Fast and stable. |
| TC-BB-007 | 1 | F-14 Urgency | EP | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-03 | Same function, past date. |
| TC-BB-008 | 1 | F-14 Urgency | EP | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes: TC-WB-F14-04 (fails, D-001), TC-API-UI-14 | Known defect: due today shows Overdue. |
| TC-BB-009 | 1 | F-14 Urgency | EP | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-05, 06 | Due Soon range. |
| TC-BB-010 | 1 | F-14 Urgency | EP | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-07 | Upcoming range. The manual case used fixed dates in October 2026. The PyTest tests use dates relative to today, which is better. |

### 3.2 Week 1: BVA (Automation/Tool Coordinator)

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-BB-BVA-F01-01 | 1 | F-01 Register | BVA | 3 | 3 | 3 | 3 | 12 | Y | PyTest unit | Partly: TC-API-UI-01 (API). No direct test of `is_valid_password` yet | 7 characters must be rejected. A unit test is fastest, and the web form and the API share this function. |
| TC-BB-BVA-F01-02 | 1 | F-01 Register | BVA | 3 | 3 | 3 | 3 | 12 | Y | PyTest unit | Partly: TC-API-UI-02 (fails, D-004) | Known defect: 8 characters are rejected. |
| TC-BB-BVA-F01-03 | 1 | F-01 Register | BVA | 3 | 3 | 3 | 2 | 11 | Y | PyTest unit | Partly: TC-API-UI-03 | 9 characters must work. If someone "fixes" D-004 the wrong way, this test catches it. |
| TC-BB-BVA-F08-01 | 1 | F-08 Create task | BVA | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-API-UI-09 | Empty title must be rejected. |
| TC-BB-BVA-F08-02 | 1 | F-08 Create task | BVA | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: TC-API-UI-11 | One-character title must work. |
| TC-BB-BVA-F14-01 | 1 | F-14 Urgency | BVA | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-03, TC-API-UI-13 | Yesterday is Overdue. |
| TC-BB-BVA-F14-02 | 1 | F-14 Urgency | BVA | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes: TC-WB-F14-04, TC-API-UI-14 (fail, D-001) | Known defect. Same boundary as TC-BB-008. |
| TC-BB-BVA-F15-01 | 1 | F-15 Dashboard | BVA | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes: `test_completed_exactly_n_days_ago` in `test_helpers.py`, API-DD-08 (D-005) | Known defect. In Week 1 we had to change the system clock by hand. The PyTest test passes a `now` value instead. |

### 3.3 Week 1: Decision table (Defect & Metrics Coordinator)

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-BB-F03-01 | 1 | F-03 Login | Decision table | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-LOG-01 (API only). The web `/login` route has no test | Valid login. Use the web route through the test client. |
| TC-BB-F03-02 to 04 | 1 | F-03 Login | Decision table | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-LOG-02, 03, TC-API-UI-08 (API only) | Three "login refused" rules. One test with three data rows. |
| TC-BB-F11-01 | 1 | F-11 Filter | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: TC-WB-F11-03 | No filters shows all own tasks. |
| TC-BB-F11-02 | 1 | F-11 Filter | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: TC-WB-F11-10 | Category, status and search together. |
| TC-BB-F11-03 | 1 | F-11 Filter | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: TC-WB-F11-06 | Done filter. |
| TC-BB-F11-04 | 1 | F-11 Filter | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Partly: TC-WB-F11-09 | No match gives an empty list. We should also check the message text. |
| TC-BB-F14-01 | 1 | F-14 Urgency | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-03 | Overdue. |
| TC-BB-F14-02 | 1 | F-14 Urgency | Decision table | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes: TC-WB-F14-04 (fails, D-001) | Known defect. |
| TC-BB-F14-03 | 1 | F-14 Urgency | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: TC-WB-F14-05, 07 | See the problem below. |
| TC-BB-F14-04 | 1 | F-14 Urgency | Decision table | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Partly: API-DD-05 | Done tasks must not show as overdue. |

Problem to fix before we use TC-BB-F14-03: it says a task due tomorrow shows "Upcoming". But `TC-BB-009` and the code (`compute_urgency`, tests `TC-WB-F14-05` and `06`) say tomorrow is "Due Soon". Both manual cases were marked Pass, so one of them is wrong. We should settle the expected result first. We did not change the case ourselves.

### 3.4 Week 1: State transition (QA/Test Lead)

None of these 20 cases was run by hand yet (the Actual Result columns are empty), and `toggle_task` has no white-box tests. So they are all new automation. We use the Flask test client for the route cases.

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-BB-060 | 1 | F-05 Session | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-LOG-01 | Login moves us to Logged In. |
| TC-BB-061 | 1 | F-05 Session | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-REG-01 | Register logs us in straight away. |
| TC-BB-062 | 1 | F-05 Session | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | No (TC-SEC-04 and 20 only touch logout) | Logout ends the session. |
| TC-BB-063 | 1 | F-05 Session | State transition | 2 | 2 | 2 | 1 | 7 | N | none | No | We do not know what the app should do when a logged-in user opens `/login`. Decide first, then automate. |
| TC-BB-064 | 1 | F-05 Session | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: TC-API-UI-08 | Wrong password keeps us out. |
| TC-BB-065 | 1 | F-05 Session | State transition | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: TC-WB-F11-01 (task list only), TC-API-UI-28 to 30 (API only) | Protected pages must redirect. Web `/dashboard` and `/tasks/new` have no test yet. |
| TC-BB-066 | 1 | F-05 Session | State transition | 3 | 3 | 1 | 1 | 8 | N | none | No | Low value. We can add it as one extra line in the TC-BB-062 test. |
| TC-BB-067 | 1 | F-05 Session | State transition | 2 | 1 | 2 | 2 | 7 | N | none | Header only: TC-SEC-12 | The Back button depends on the browser cache, so it must be checked by hand in each browser. |
| TC-BB-068 | 1 | F-05 Session | State transition | 2 | 3 | 3 | 2 | 10 | Y | PyTest API | No | Old page action after logout. In the test client this is one POST after logout. |
| TC-BB-069 | 1 | F-12 Task state | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-TSK-POST-01 | New task starts Open. Also check the dashboard counts. |
| TC-BB-070 | 1 | F-12 Task state | State transition | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: API-TSK-PUT-02 (API only). `toggle_task` has no tests (Week 2 gap) | Open to Done, and the dashboard "Completed" count. |
| TC-BB-071 | 1 | F-12 Task state | State transition | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: TC-API-UI-20 (API only) | Done to Open, and `completed_at` is cleared. |
| TC-BB-072 | 1 | F-10 Edit task | State transition | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | No | Editing must not change Open or Done. |
| TC-BB-073 | 1 | F-10 Edit task | State transition | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | No | Same for a Done task. |
| TC-BB-074 | 1 | F-13 Delete task | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-TSK-DEL-01 (API only) | Delete an Open task. |
| TC-BB-075 | 1 | F-13 Delete task | State transition | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Partly: API-DD-03 (API only) | Delete a Done task, and the dashboard counts. |
| TC-BB-076 | 1 | F-13 Delete task | State transition | 2 | 2 | 2 | 1 | 7 | N | none | No | This is the browser confirm popup. It passed by hand in three browsers (GUI-11). We cover it inside the Selenium flow in 3.6, not on its own. |
| TC-BB-077 | 1 | F-12 Task state | State transition | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | No | Toggle on a deleted task must not crash or create a task. |
| TC-BB-078 | 1 | F-10 Edit task | State transition | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | No | Edit page of a deleted task. We only check that it does not crash. The silent redirect may be a usability issue, which we judge by hand. |
| TC-BB-079 | 1 | F-10 Edit task | State transition | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-SEC-22 | Another user's task must stay untouched. |

### 3.5 Week 2: White-box (existing PyTest)

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-WB-F14-01 to 03 | 2 | F-14 `compute_urgency` | White-box | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes: `test_compute_urgency.py` | Fast, no setup. Keep. |
| TC-WB-F14-04 | 2 | F-14 `compute_urgency` | White-box | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes (fails, D-001) | Known defect. |
| TC-WB-F14-05 to 08 | 2 | F-14 `compute_urgency` | White-box | 3 | 3 | 2 | 2 | 10 | Y | PyTest unit | Yes | Branches and the boundary at 2 and 3 days. |
| TC-WB-F14-09 | 2 | F-14 `compute_urgency` | White-box | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes (4 data values) | Bad date format raises an error. This is the root of D-006. |
| TC-WB-F14-10 | 2 | F-14 `compute_urgency` | White-box | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-006) | A bad date saved by the API breaks the list. |
| TC-WB-F11-01 to 10 | 2 | F-09, F-11 `index` | White-box | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: `test_index.py` | Filters and user isolation on the task list. Keep. |
| TC-WB-F11-11 | 2 | F-11 `index` | White-box | 2 | 3 | 1 | 3 | 9 | Y | PyTest API | Yes | Known defect (D-014): `%` is a wildcard. Low severity but cheap. |
| `completed_in_last_n_days` (7 tests, no TC ID yet) | 2 | F-15 helper | White-box | 3 | 3 | 2 | 3 | 11 | Y | PyTest unit | Yes: `test_helpers.py` | Includes D-005. The Week 2 metrics say the tests still need TC IDs in their docstrings. |
| `toggle_task` (no tests, no TC ID) | 2 | F-12 | White-box | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | No (Week 2 "not started") | Covered by the new TC-BB-070, 071 and 077 above, so we do not write a separate set. |

### 3.6 Week 3: GUI, compatibility, usability, accessibility

Most of Week 3 is judgement or browser-specific, so it stays manual (section 4). These are the parts we can automate.

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US-04, US-05, US-11, US-18, US-24 | 3 | F-01, F-08, F-11, F-14 | Usability (defect-linked) | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-API-UI-04, 02, 10, 12, 14, 25 and TC-SEC-02, 09 | These five usability issues are really the defects D-013, D-004, D-011, D-012, D-001 and D-014. The server rules are already tested. We do not need a second test for the wording. |
| GUI-02, ACC-01, ACC-08 | 3 | F-01, F-03, F-08, F-11 | GUI, accessibility | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | No | D-009: labels have no `for`. We can read the page HTML and check each label points to an input. |
| ACC-02 | 3 | F-12 | Accessibility | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | No | D-016: the toggle button needs a name. Check the HTML for `aria-label` or text. |
| GUI-08 | 3 | F-09 | GUI | 2 | 3 | 1 | 3 | 9 | Y | PyTest API | No | D-008: empty list message. Check the page text for a user with no tasks. |
| GUI-01 | 3 | All pages | GUI | 2 | 3 | 1 | 3 | 9 | Y | PyTest API | No | D-007: line 1 of `style.css` is `-` instead of `*`. A one-line file check. |
| ACC-09 (viewport tag only) | 3 | All pages | Accessibility | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | No | D-017: check the `<meta name="viewport">` tag exists. This does not prove the page reflows. That part stays manual. |
| WTS-01, WTS-02, WTS-08 | 4 | F-01, F-03, F-05 | End-to-end | 3 | 2 | 3 | 3 | 11 | Y | Selenium UI | No | One browser script: register, log out, log in, log out. Only a real browser tests cookies and redirects together. |
| WTS-03, WTS-06, WTS-07, TC-BB-076, GUI-11 | 3, 4 | F-08, F-12, F-13 | End-to-end | 3 | 2 | 3 | 3 | 11 | Y | Selenium UI | No | One browser script: create a task, mark it done, delete it. It also answers the confirm popup, first Cancel and then OK. |

### 3.7 Week 4: Web and API

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WTS-04, WTS-05 | 4 | F-11, F-10 | Web workflow | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Partly: TC-WB-F11-04 to 10. Edit by TC-BB-072 (new) | Filters and edit through the web routes. No Selenium needed. |
| WTS-VAL-01 | 4 | F-01 | Validation | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: TC-API-UI-01, 02, 05 (API only) | Web register with a bad username or 7 and 8 character passwords. |
| WTS-VAL-02 | 4 | F-01 | Validation | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-SEC-02 (fails, D-013) | Duplicate username on the web route. |
| WTS-VAL-03 | 4 | F-08, F-10 | Validation | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Partly: TC-SEC-09 (create only) | Whitespace title, D-011. The edit route has no test yet. |
| WTS-VAL-04 | 4 | F-08 | Validation | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-SEC-17 (fails, D-006) | Bad due date through the web form. |
| WTS-VAL-05 | 4 | F-08 | Validation | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | No (API version: TC-API-UI-16) | Category id 9999 on the web route. |
| WTS-VAL-06 | 4 | F-13 | Validation | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes: TC-SEC-22 | Web delete checks the owner. |
| API-REG-01 to 07, API-LOG-01 to 05, 07 | 4 | F-02, F-04 | API | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes: `test_api_auth.py` | Register and login rules. Passing now. |
| API-REG-08, API-LOG-06, API-TSK-POST-07 | 4 | F-02, F-04, F-19 | API | 3 | 3 | 2 | 3 | 11 | Y | PyTest API | Yes (fail, D-019) | A number sent as a text field gives a 500 error. |
| API-REG-09 | 4 | F-02 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-013) | Same as TC-API-UI-04. |
| API-CAT-01 to 03 | 4 | F-17 | API | 2 | 3 | 1 | 2 | 8 | N | none | Yes: `test_api_auth.py` | Low value (a public list of four names). We leave the existing tests alone and do not add more. |
| API-TSK-GETALL-01, 02, 05, 06, 07 | 4 | F-18 | API | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes: `test_api_tasks.py` | List, filters, login needed, paging. |
| API-TSK-GETALL-03, 04 | 4 | F-18 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (04 fails, D-020) | SQL injection in `q`. Same rule as TC-SEC-07. |
| API-TSK-GETONE-01 to 04 | 4 | F-20 | API | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes | Get one task. |
| API-TSK-GETONE-05, API-TSK-PUT-07 | 4 | F-20, F-21 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes | Cross-user read and edit must give 404. |
| API-TSK-POST-01 to 06 | 4 | F-19 | API | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes. 04 fails (D-006) | Create task rules. |
| API-TSK-POST-08 | 4 | F-19 | API | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | Yes (fails, D-021) | Category that does not exist. |
| API-TSK-PUT-01, 02, 04, 05 | 4 | F-21 | API | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes | Update, toggle, not found, empty body. |
| API-TSK-PUT-03 | 4 | F-21 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-022) | Empty title on edit. |
| API-TSK-PUT-06 | 4 | F-21 | API | 2 | 3 | 2 | 3 | 10 | Y | PyTest API | Yes (fails, D-023) | `"done": "false"` completes the task. |
| API-TSK-DEL-01, 03, 04 | 4 | F-22 | API | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes | Delete, login needed, wrong id type. |
| API-TSK-DEL-02, API-DD-02 | 4 | F-22 | API | 2 | 3 | 1 | 3 | 9 | Y | PyTest API | Yes (fail, D-024) | Delete of a missing task returns 200. |
| API-TSK-DEL-05, API-DD-01 | 4 | F-22 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail, D-025) | Another user can delete our task. Critical defect. Same rule as TC-SEC-21. |
| API-DASH-01 to 04, API-DD-03 to 07, 09 | 4 | F-16 | API | 3 | 3 | 2 | 2 | 10 | Y | PyTest API | Yes | Dashboard counts and boundaries. |
| API-DD-08 | 4 | F-16 | API | 3 | 3 | 2 | 3 | 11 | Y | PyTest API | Yes (fails, D-005) | Completed exactly 7 days ago. |
| API-DD-10 | 4 | F-16 | API | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-006) | A bad date also breaks the dashboard. |
| TC-API-UI-01, 03, 05, 07, 08, 09, 10, 11, 13, 17, 19, 20, 21, 28, 29, 30 | 4 | Web vs API rules | Comparison | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes: `test_ui_vs_api.py` (16 pass) | These rules agree between the UI and the API today. They protect against the API drifting away from the UI. Many repeat the `API-...` tests above. |
| TC-API-UI-02, 04, 12 | 4 | Web vs API rules | Comparison | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail: D-004, D-013, D-012) | Known defects. |
| TC-API-UI-14, 15, 16 | 4 | Web vs API rules | Comparison | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail: D-001, D-006, D-021) | Known defects. |
| TC-API-UI-06, 18, 22, 23, 24 | 4 | Web vs API rules | Comparison | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail: D-019, D-022, D-023, D-024, D-025) | Known defects. The test for 24 only checks the status code, so it does not yet prove the task is really deleted (see section 7). |
| TC-API-UI-25, 26, 27 | 4 | Web vs API rules | Comparison | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail: D-014, D-020) | Search treats `_` and `%` as wildcards, and `'` breaks the SQL. |

### 3.8 Week 5: Security and performance

The `test_security.py` tests assert the secure behaviour. A test that fails today means the weakness is still there.

| Original TC ID | Week | Feature | Test type | Rep | Stab | Crit | Reg | Total | Automate? | Tool | Already automated? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-SEC-01, TC-SEC-19 | 5 | F-03, F-16 Login | Security | 2 | 3 | 3 | 2 | 10 | Y | PyTest API | Yes (fail, D-026) | No limit on password guesses. 10 and 20 requests only. |
| TC-SEC-02 | 5 | F-01 Register | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-013) | Duplicate usernames. |
| TC-SEC-03 | 5 | F-04 Session | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-027) | Forged cookie from the hard-coded key. If the key is changed, the test must read the new key from the app config. |
| TC-SEC-04 | 5 | F-05 Logout | Security | 2 | 3 | 3 | 2 | 10 | Y | PyTest API | Yes (fails, D-028) | Old cookie still works after logout. |
| TC-SEC-05 | 5 | F-09 Task list | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-010) | Stored XSS from the `safe` filter. |
| TC-SEC-06 | 5 | F-08, F-10, F-13 | Security | 2 | 3 | 3 | 3 | 11 | Y | PyTest API | Yes (fails, D-029) | No CSRF token. |
| TC-SEC-07, TC-SEC-14 | 5 | F-19 API search | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fail, D-020) | SQL injection. TC-SEC-14 is the cross-user version. |
| TC-SEC-08 | 5 | F-11 Search | Security | 2 | 3 | 1 | 3 | 9 | Y | PyTest API | Yes (fails, D-014) | `%` wildcard on the web route. |
| TC-SEC-09 | 5 | F-08 Create task | Security | 3 | 3 | 2 | 3 | 11 | Y | PyTest API | Yes (fails, D-011) | Whitespace title on the web route. |
| TC-SEC-10 | 5 | F-13 Delete | Security | 1 | 3 | 1 | 2 | 7 | N | none | Yes (fails, D-030) | There is no audit table. That is a missing feature, not something that will break again. We leave the test as it is and do not put it in the suite. |
| TC-SEC-11 | 5 | Server config | Security | 2 | 3 | 3 | 3 | 11 | Y | PyTest unit | Yes (fails, D-031) | Reads `app.py` for `debug=True`. Cheap, and it fails loudly if debug stays on. |
| TC-SEC-12 | 5 | F-15 Dashboard | Security | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | Yes (fails, D-032) | `Cache-Control` header. |
| TC-SEC-13 | 5 | F-01 Passwords | Security | 3 | 3 | 3 | 2 | 11 | Y | PyTest API | Yes (passes) | Passwords stay hashed. If this ever fails, it is serious. |
| TC-SEC-15 | 5 | F-04 Session | Security | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | Yes (fails, D-033) | Cookie flags. |
| TC-SEC-16 | 5 | F-17 Categories | Security | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | Yes (passes) | Public list shows no user data. |
| TC-SEC-17 | 5 | F-08, F-09 | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-006) | A bad date breaks the task list. |
| TC-SEC-18 | 5 | F-19 API list | Security | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | Yes (fails, D-034) | No cap on `per_page`. |
| TC-SEC-20 | 5 | F-05 Logout | Security | 2 | 3 | 2 | 2 | 9 | Y | PyTest API | Yes (fails, D-035) | Logout by GET. |
| TC-SEC-21 | 5 | F-22 API delete | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (fails, D-025) | Another user can delete our task. |
| TC-SEC-22 | 5 | F-10, F-12, F-13 | Security | 3 | 3 | 3 | 3 | 12 | Y | PyTest API | Yes (passes) | The web routes check the owner. This must not break when we fix the API. |
| Performance stages 1 to 3 (`locustfile.py`) | 5 | API load | Performance | 1 | 1 | 2 | 2 | 6 | N | none (Locust script already exists) | Scripted only | Times change between machines and runs. See section 4. |

## 4. Not automated (kept manual)

- Usability observations US-01 to US-31 (other than the defect-linked ones above): they are about wording and how the app feels, so only a person can judge them.
- Visual layout checks, GUI-01 (the look), GUI-07, GUI-09, GUI-12, GUI-15: colours, spacing and alignment are easy for a person to see and hard to assert.
- Cross-browser checks COMP-01 to COMP-09 and GUI-16: they need real Chrome, Edge, Firefox and device views. The results can vary by browser version, so we repeat them by hand before release.
- Colour contrast (ACC-03), touch target size (ACC-11), reflow at 320 px (ACC-09, the layout part), keyboard and screen reader use (ACC-13 and similar): these need a person, or a tool like Lighthouse that we run by hand.
- Lighthouse scores (ACC-10): the scores change with the machine and the Chrome version.
- Back button after logout (TC-BB-067, US-29): depends on browser cache. The header itself is checked by TC-SEC-12.
- Browser required tooltip (GUI-13, TC-BB-005 manual part): this only exists in the browser. The server rule is automated.
- Performance runs: we already have a Locust script, but the times depend on the machine, so we run it by hand before release and compare to the same-machine baseline.
- Login while logged in (TC-BB-063): we have not decided what the correct behaviour is.
- Low-value or missing-feature checks (TC-BB-066, API-CAT-01 to 03, TC-SEC-10): not worth more work.

## 5. Assignment

The brief gives four groups. These are the "Automate = Y" rows grouped that way. "New work" means a test that is not written yet.

| Owner | Rows (Automate = Y) | New work | Already written |
|---|---|---|---|
| Test Design Coordinator (EP) | TC-BB-001 to TC-BB-010 | Add a direct test for the web whitespace title (TC-BB-005, with TC-SEC-09). Make sure each existing test has its TC ID. | Most of it |
| Automation/Tool Coordinator (BVA and all Selenium) | TC-BB-BVA-F01-01 to 03, F08-01, 02, F14-01, 02, F15-01. Selenium scripts: WTS-01, 02, 08 and WTS-03, 06, 07 (with TC-BB-076 and GUI-11) | 3 unit tests for `is_valid_password`. Install and set up Selenium. 2 browser scripts. | Most BVA rows are covered through the API or `compute_urgency` |
| Defect & Metrics Coordinator (decision table) | TC-BB-F03-01 to 04, F11-01 to 04, F14-01 to 04 | Web login tests through the test client. Check the "no tasks match" message text. First settle the F14-03 expected result. | F11 and F14 mostly |
| QA/Test Lead (state transition) | TC-BB-060, 061, 062, 064, 065, 068 to 075, 077, 078, 079 (16 rows) | About 14 new route tests. This is the biggest group. It includes the missing `toggle_task` tests. | TC-BB-079 only (TC-SEC-22) |

The brief does not assign the other Y rows (the white-box tests, the API tests, the TC-API-UI tests, TC-SEC, and the Week 3 static checks). They are already written, so we suggest the original author keeps them up to date: Week 2 units by their unit owners, Week 4 API tests by the Automation/Tool Coordinator and the Test Design Coordinator, Week 5 security tests by the Test Design Coordinator. The Week 3 static checks (D-007, D-008, D-009, D-016, D-017) are new and unassigned. We suggest the Test Design Coordinator, because they own `gui_checklist.md`. This needs the group to agree.

Workload note: the QA/Test Lead has the most new tests, and the Automation/Tool Coordinator has the Selenium setup, which we have not tried. We may need to move some state transition cases to others.

## 6. Proposed regression suite

These 19 tests should run after every change. All are PyTest and fast. Selenium is left out of this list because it is slower and more likely to fail for reasons that are not bugs. We suggest running the two Selenium scripts before each release or demo.

For each known defect we listed only one test, even when two or three files check the same thing.

| # | Test | Why we include it |
|---|---|---|
| 1 | TC-API-UI-01 (7 characters rejected) | Lower side of the password boundary. Passes today and must keep passing. |
| 2 | TC-API-UI-02 (8 characters accepted, D-004) | The known password bug. |
| 3 | TC-API-UI-04 (duplicate username, D-013) | The known account bug. Accounts are the base of everything else. |
| 4 | TC-BB-F03-01 (valid login, new) | If login breaks, nothing else can be used. |
| 5 | TC-BB-065 (protected pages redirect, new) | Stops someone seeing pages without logging in. |
| 6 | TC-API-UI-28 to 30 (no login on create, edit, delete) | Same rule for the API. |
| 7 | TC-SEC-09 (whitespace title, D-011) | Known bug on the web form. |
| 8 | TC-WB-F14-04 (due today, D-001) | Known bug in the date rule. Also feeds the dashboard. |
| 9 | TC-WB-F14-10 (bad due date, D-006) | A bad date breaks the list and the dashboard. |
| 10 | `test_completed_exactly_n_days_ago` (D-005) | Known bug in the 7-day counter. |
| 11 | TC-WB-F11-10 (all filters together) | One test that touches category, status and search. |
| 12 | TC-BB-070 (Open to Done, new) | The main task action, including the dashboard counts. |
| 13 | TC-BB-071 (Done to Open, new) | Checks `completed_at` is cleared. |
| 14 | TC-BB-074 (delete own task, new) | Delete is permanent, so it must work and only touch the right task. |
| 15 | TC-SEC-22 (web checks the owner) | Passes today. Protects the one place we get this right. |
| 16 | TC-SEC-21 (API delete by another user, D-025) | Critical defect. Data loss. |
| 17 | TC-SEC-07 (SQL injection in search, D-020) | Critical defect. |
| 18 | TC-SEC-05 (stored XSS, D-010) | Major defect, in the display code that changes often. |
| 19 | TC-API-UI-18 (empty title on edit, D-022) | Major defect in the edit rule. |

## 7. Open questions for the group

- Most of the known-defect tests in this suite fail today. A suite that is red from day one is easy to ignore. We suggest marking them as expected failures (PyTest `xfail`) until the fix is made, so the suite is green when nothing new breaks and a fix shows up as a surprise pass. We have not used `xfail` anywhere yet, and nobody has decided this.
- TC-API-UI-24 only checks the status code of the other user's delete. We could add one line to check that the owner's task is really gone. We left it as it is.
- Both TC-BB-F14-03 and TC-BB-009 cannot be right (tomorrow is "Upcoming" in one and "Due Soon" in the other). We need to decide which one the spec says.
- Some tests overlap (for example, API-TSK-DEL-05, TC-API-UI-24 and TC-SEC-21 all check the same bug). We keep them for now, but the suite lists only one of each.
- The `.coverage` and `coverage.json` files are tracked in git. That is outside this task, but we should probably stop tracking them.
