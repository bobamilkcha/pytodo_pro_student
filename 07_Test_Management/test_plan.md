# PyTodo Pro: Test Plan

**Prepared by:** QA/Test Lead
**Date:** 26 Nov 2026
**Based on:** the files in `01_Black_Box` to `06_Automation_Regression` and `07_Test_Management`

## 1. Introduction

This plan says how we test PyTodo Pro, what we covered, and whether we met our own exit criteria. The app is a small Flask 3.0.3 task manager with SQLite storage. It has web pages (register, login, task list, new and edit task, dashboard) and a JSON API under `/api`. We test the local copy only (`127.0.0.1:5000`). We do not change the app code.

We wrote this plan in Week 7, after testing. It is not the plan we started with. It records what we actually did and what we learnt. Some parts changed along the way. For example, Week 1 had only web features in scope, and the API, security and performance came later.

Numbers come from our own files. Where the files disagree, we say so. The file `07_Test_Management/cross_check_defects.md` lists the open disagreements. The brief also mentions an `execution_status` file, but there is no such file in `07_Test_Management/` yet. We used `cross_check_defects.md`, `06_Automation_Regression/execution_report.md` and the weekly metrics files instead.

## 2. Test objectives

1. Find defects in the web pages and in the API, and report each one with a severity, a priority and evidence.
2. Check every feature in `01_Black_Box/feature_inventory.md` (F-01 to F-22) with at least one test.
3. Compare the web pages with the API for the same rule, because we expected them to differ.
4. Check the main security threats with STRIDE, and check how the API behaves under load.
5. Automate the most useful tests and keep a regression suite that we can re-run after a fix.
6. Trace every requirement to its tests and defects (`rtm.md`).

## 3. Scope

### 3.1 In scope

| Area | Features | Where tested |
|---|---|---|
| Authentication (web) | F-01 Register, F-03 Login, F-05 Logout, F-06 Page protection | Weeks 1, 3, 4, 5, 6 |
| Authentication (API) | F-02 Register, F-04 Login, F-07 Endpoint protection | Weeks 4, 5, 6 |
| Task management (web) | F-08 Create, F-09 List, F-10 Edit, F-11 Filter and search, F-12 Mark done, F-13 Delete, F-14 Urgency badge | Weeks 1 to 6 |
| Dashboard | F-15 Dashboard (web), F-16 Dashboard (API) | Weeks 1, 2, 4, 6 |
| Task API | F-17 Categories, F-18 List tasks, F-19 Create, F-20 Get one, F-21 Update, F-22 Delete | Weeks 4, 5, 6 |
| Non-functional | NFR-01 Layout and browsers, NFR-02 Server configuration, NFR-03 Load and speed | Weeks 3, 5 |

Week 1 only covered the web features. All API features (F-02, F-04, F-07, F-16 to F-22) were marked out of scope for Week 1 in `test_scope_matrix.md` and tested in Week 4.

### 3.2 Out of scope

| Item | Reason |
|---|---|
| Fixing defects or changing app code | Course rule. We report and suggest fixes only. |
| Features the app does not have (password change, password reset, account deletion, category management, API logout) | Nothing to test. Listed in `feature_inventory.md`. |
| Real phones and tablets | We only had browser device mode (a simulation). |
| Browsers other than Chrome, Edge and Firefox | Not available to us. Safari was not tested. |
| More than 100 users, or tests longer than 30 seconds per stage | The Flask dev server on a laptop is not a real server. We kept the load small. |
| External scanners, password cracking, flooding, any host other than our own machine | Course safety rule. |
| Testing with real users | Usability was one tester who already knew the app. |
| Testing with a real screen reader | We used tools (Playwright keyboard script, axe-core, Lighthouse). We have no record of a real screen reader test. |
| Tests of the `/static/style.css` file by itself | We only checked it through how the pages look. |

## 4. Test strategy

### 4.1 Test levels

| Level | What we tested | How | Main files |
|---|---|---|---|
| Unit | Helper functions and route functions on their own: `compute_urgency`, `completed_in_last_n_days`, `is_valid_password`, the `index` route | PyTest, with coverage measured by pytest-cov | `02_White_Box_Coverage/`, `06_Automation_Regression/tests/unit/` |
| Integration and API | Routes, the database and the session working together. Both the JSON API and the web routes | PyTest with the Flask test client, which needs no running server | `04_Web_API/tests/`, `05_Security_Performance/tests/`, `06_Automation_Regression/tests/api/` |
| System and UI | The app in a real browser: layout, browsers, usability, accessibility, end-to-end flows | Manual testing, Playwright, axe-core, Lighthouse, 2 Selenium scripts | `03_Special_Testing/`, `06_Automation_Regression/tests/ui/` |
| Performance | The API under 10, 50 and 100 users | Locust against the Flask dev server | `05_Security_Performance/` |

The border between API and unit is not sharp. The Flask test client tests the web routes too, so we call those API-level tests as well.

### 4.2 Techniques, why we chose them, and what they found

We chose techniques from the first risk list in `feature_inventory.md` (section 5) and the scope matrix. After each week we checked what the technique really found. Defect counts below are from `07_Test_Management/defect_log.md` (32 valid defects).

| Technique | Features | Why we chose it | What it found for us |
|---|---|---|---|
| Equivalence partitioning (EP) | F-01, F-03, F-06, F-08, F-09, F-10, F-13, F-14 | Few input groups per feature, so cheap to cover. High risk on F-01, F-08 and F-14. | D-001 (due today shows Overdue). We also recorded TC-BB-002 as Pass, but it was wrong because duplicate usernames are accepted (D-013). |
| Boundary value analysis (BVA) | F-01 password, F-08 title, F-14 date, F-15 7-day cutoff | Clear numeric limits (8 characters, today, 7 days). Rated high risk. | D-004 (8-character password rejected) and D-005 (7-day counter). This was our best technique for off-by-one errors. |
| Decision table | F-03 login, F-11 filter, F-14 urgency | Several conditions give different results. | Nothing new. It repeated D-001. The F-14 table has only one condition, so it is weak. |
| State transition | F-05 logout and session, F-12 mark done, plus edit and delete | The session and a task both have states. The dashboard counts depend on task state. | 20 cases, 19 pass and 1 fail. The fail (Back button after logout) was merged into D-032. It also covered `toggle_task`, which had no white-box tests. |
| White-box (statement and branch) | `compute_urgency`, `completed_in_last_n_days`, `index`, `toggle_task` | We chose the units with the highest Week 1 risk. | D-006 (bad due date breaks the list) and the exact line behind D-005. `compute_urgency` had 100% branch coverage and still had D-001. Missing logic has no branch for a tool to show. |
| GUI, compatibility, usability, accessibility | All web pages | Black-box tests do not see layout or screen reader problems. | 11 defects (D-008 to D-018) in Week 3. Accessibility was the weakest area, 8 of 16 checks passed. Compatibility passed 9 of 9 checks on 5 configurations. |
| API testing | F-02, F-04, F-07, F-16 to F-22 | Week 1 notes said the API validates less. | 7 defects (D-019 to D-025), including two Critical ones that exist only in the API (D-020 SQL injection, D-025 delete other users' tasks). The comparison with the web pages (30 cases, 16 pass, 14 fail) showed that the web pages hide these problems. |
| Security (STRIDE) | Whole app | The first risk list had 4 security items. We wanted a structured list. | 22 threats, 22 tests, 3 pass and 19 fail. 10 new defects (D-026 to D-035). Some tests are shallow. For example, the CSRF test only looks for a token. |
| Performance (Locust) | 7 API endpoints | Nothing else in the plan checks speed. | No failed requests. Login and register slow down most. At 100 users the overall P95 was 520 ms against our 500 ms target (PERF-OBS-01, PERF-OBS-02). No defect was logged for this. |

What we learnt about technique choice:
- The web and the API apply different rules. Testing only through the browser would have missed both Critical API defects.
- Our Week 1 risk list already named SQL injection, deleting other users' tasks and stored XSS as Critical. We did not test them until Weeks 3 to 5, because they were out of scope for Week 1. In a real project we would test the highest risks first.
- EP and decision tables found little that BVA and white-box did not. Of the 32 valid defects, only 3 came from Week 1 black-box testing.

### 4.3 Manual and automated testing

We chose by score, as in `06_Automation_Regression/automation_candidates.md`. Each test group gets 1 to 3 points for four things: repetition, stability, criticality and regression value. A total of 9 or more out of 12 means we automate it and put it in the regression suite. A total of 7 or 8 means we automate it but only run it in the full suite. Lower than that, it stays manual.

We kept these manual:
- Tests that need human judgement, such as keyboard focus order, how clear an error message is, and usability.
- One-time checks, such as a page with no images.
- Browser-specific behaviour, such as the Back button after logout (TC-BB-067). A Selenium script could do some of this later.

We automated:
- Unit and API tests with PyTest and the Flask test client. These are fast and stable.
- HTML and CSS checks (labels, language, viewport tag, contrast) with the Flask test client, with no browser.
- 2 Selenium end-to-end scripts. They need Chrome, so they are not in the regression suite.

Week 6 result (`06_Automation_Regression/manual_to_automated_traceability.md`): 95 test functions that run as 103 tests, of which 69 pass and 34 fail. All 34 failures are known defects.

### 4.4 Regression approach

- Tests that belong in the regression suite carry the marker `@pytest.mark.regression`. The marker is registered in `pytest.ini`.
- Run it from the project root: `pytest 06_Automation_Regression/tests/ -m regression -v`.
- The suite is 51 tests (22 pass, 29 fail, counted in `cross_check_defects.md`). It takes a few seconds.
- It covers login, registration, page protection, task create, toggle and delete, and the known defects D-001, D-004, D-005, D-006, D-010, D-011, D-013, D-020, D-022 and D-025.
- Tests for a known defect assert the correct behaviour. They fail while the defect exists and turn green when it is fixed. A new failure that does not match a known defect is a new problem.
- Selenium scripts are excluded because they are slow and can fail for reasons that are not bugs. We run them before a release or a demo.
- We run the suite after every change to the app and after every claimed fix. We have not done a retest yet, because no defect has been fixed.
- Note: `06_Automation_Regression/execution_report.md` still shows 85 tests and 45 regression tests. It does not yet include `test_state_transition.py` (18 tests). `cross_check_defects.md` lists this as open.

## 5. Test environment

We did not all use the same machine. Each evidence file shows its own environment, so we list what the files show.

| Item | What we used | Source |
|---|---|---|
| Operating system | Windows 10 and 11 for most tests. Linux for some automated runs and for the accessibility tools. | Evidence files, `compatibility_matrix.md` |
| Python | 3.10.11, 3.11.5 and 3.13 (different team members) | Evidence file headers |
| App | Flask 3.0.3. This is the only line in `requirements.txt`. | `requirements.txt` |
| Server | Flask development server, `python app.py`, debug on, `http://127.0.0.1:5000` | `README.md`, `app.py` |
| Database | SQLite file `pytodo_pro.db`, with 4 categories created on first run: Work, Personal, Study, Urgent | `README.md` |
| PyTest | 9.2.0 on Windows, 9.1.1 on Linux | Evidence files |
| Coverage | pytest-cov 7.1.0, branch coverage | `coverage_evidence.txt` |
| Selenium | Headless Chrome. The Selenium version is not written in any file. | `execution_report.md` |
| Load tool | Locust 2.46.0 (Windows, Python 3.10.11). A re-run used Locust 2.47.0 on Linux with 2 CPU cores. | `performance_plan.md`, `evidence_performance_rerun.txt` |
| Browsers | Chrome 157.0.8103.79, Edge 157.0.4341.60, Firefox 127.0 on Windows 11. Mobile (Galaxy A55) and tablet (iPad Pro 13) were Chrome DevTools simulations. | `compatibility_matrix.md` |
| Accessibility tools | Chrome 153 headless on Linux, a Playwright keyboard script, axe-core, Lighthouse | `accessibility_findings.md` |

Problems with this setup:
- `requirements.txt` lists only Flask. PyTest, pytest-cov, Selenium and Locust are not in it, so a new team member has to install them by hand.
- The performance results come from a laptop, and the results file does not record the CPU or memory. The second run on a different machine was slower (login average 1,521 ms), so the numbers are only useful for comparing stages, not for judging the app.

## 6. Test data

| Data | How it is created | Where used |
|---|---|---|
| Fixed test accounts, for example `aida`, `ryulemontea`, `qa_user1` to `qa_user3`, `compat_user`, `syasya_test1` and `syasya_test2` | Registered by hand or by a test | Manual tests in Weeks 1, 3 and 5 |
| Random accounts, for example `st_` plus 8 random characters | Each automated test registers its own new user | `test_state_transition.py` and the other Week 6 tests |
| Task data | Created through the web form or the API during the test. Dates are set relative to today for urgency and dashboard tests. | Most tests |
| Categories | 4 categories, created when the database is made | All tests |
| Load test users | The Locust script registers and logs in each simulated user | Week 5 |

How we reset data:
- Manual tests: delete `pytodo_pro.db`. The app makes a new one on the next start.
- Most automated tests: a temporary database per test (`monkeypatch` and `tmp_path`). They do not touch `pytodo_pro.db`.
- Exceptions: `04_Web_API/tests/conftest.py` and `test_api_smoke.py` use the real `pytodo_pro.db`. On a fresh clone `test_api_auth.py` fails until `init_db()` has run, and the tests leave users in the real database. `week6_defect_check.md` lists this as script issue S-02. We have not fixed it.

Some Week 1 EP cases use fixed dates (2026-10-20 as "today"). They only match the app on that day.

## 7. Tools

| Tool | Used for |
|---|---|
| PyTest and the Flask test client | Unit, API and web route tests |
| pytest-cov (coverage.py) | Statement and branch coverage in Week 2 |
| Selenium with headless Chrome | 2 browser flows in Week 6 |
| Locust | Load tests in Week 5 |
| Browser DevTools | Layout, device mode, manual checks |
| Playwright, axe-core, Lighthouse | Accessibility checks in Week 3 |
| Git and GitHub | Version control and sharing files |
| Markdown files | Test cases, results, defect log, this plan |
| Mermaid | State diagrams in `tc_state_transition.md` |

## 8. Roles and responsibilities

We have four roles. The roles did not rotate. In Week 1 the roles were split by technique. In later weeks each role kept the same kind of work.

| Role | What this role did |
|---|---|
| QA/Test Lead | Feature inventory, scope matrix and risk list (Week 1). State transition cases (Week 1) and their run. White-box tests for `toggle_task` (assigned in Week 2, not done). Usability observations (Week 3). Web and API comparison (Week 4). STRIDE table (Week 5). State transition automation (Week 6). This plan. |
| Test Design Coordinator (Aida) | EP test cases (Week 1). White-box tests for `index` (Week 2). GUI checklist (Week 3). API tests for tasks (Week 4). Security test cases (Week 5). Traceability matrix, master test repository and RTM (Weeks 6 and 7). |
| Automation/Tool Coordinator (Nisrina) | BVA test cases (Week 1). Coverage setup and `completed_in_last_n_days` tests (Week 2). Compatibility matrix (Week 3). API auth tests (Week 4). Locust load tests (Week 5). Test layout, regression marker, Selenium scripts and execution report (Week 6). |
| Defect & Metrics Coordinator (Nafiesa) | Decision table cases (Week 1). `compute_urgency` tests (Week 2). Accessibility findings (Week 3). Delete and dashboard API tests (Week 4). Security findings (Week 5). The central defect log, test conventions, metrics files and the defect check (Weeks 1 to 7). |

Each week's folder has a file that shows which person owned which file.

## 9. Entry and exit criteria

### 9.1 Entry criteria

We use these before starting a test phase.

| # | Entry criterion | Met? |
|---|---|---|
| EN-1 | The app starts with `python app.py` on `127.0.0.1:5000` and a fresh database | Yes |
| EN-2 | The feature inventory and scope matrix exist | Yes (Week 1) |
| EN-3 | `test_conventions.md` exists (ID formats, severity scale, defect template) | Yes. It was written in Week 3, so Weeks 1 and 2 used draft IDs that we had to fix later. |
| EN-4 | Test accounts and a way to reset the database are known | Yes |
| EN-5 | The tools for that week are installed and run once | Mostly. Selenium and Locust had no setup note in `requirements.txt`. |
| EN-6 | The previous week's defects are logged with a D-number | Mostly. Draft IDs were used in Weeks 1, 4 and 5 and had to be corrected. |

### 9.2 Exit criteria and our result

| # | Exit criterion | Result | Evidence |
|---|---|---|---|
| EX-1 | Every feature F-01 to F-22 has at least one executed test | Met. The RTM shows 25 of 25 requirements covered. The RTM has 7 corrections pending (`cross_check_defects.md`, section 4). | `rtm.md` |
| EX-2 | All High priority features have all their planned tests executed (F-01, F-03, F-08, F-14, F-15) | Met | `master_test_repository.md`, weekly metrics |
| EX-3 | No planned test left Not Run | Not met. The white-box tests for `toggle_task` (F-12) were planned in Week 2 and never written. The state transition cases cover the same route, but the white-box coverage of that unit is 0%. | `Week2_Metrics.md` |
| EX-4 | Statement and branch coverage of 100% on each selected unit | Not met. 3 of 4 units reached 100%. `toggle_task` is at 0%. | `Week2_Metrics.md` |
| EX-5 | Every failed test is linked to a logged defect | Met. All 71 failures in the pre-check were product defects, with 0 script issues. | `week6_defect_check.md` |
| EX-6 | No open Critical defects | Not met. 3 are open: D-020, D-025 and D-027. No defect has been fixed. | `07_Test_Management/defect_log.md` |
| EX-7 | No open Major defects without a decision | Not met. 9 Major defects are open. We have no developer to decide. | `07_Test_Management/defect_log.md` |
| EX-8 | Regression suite passes, except known defects | Met in the sense that all 29 failures are known defects. It is not green. 22 of 51 pass. | `cross_check_defects.md` |
| EX-9 | Performance targets: average below 200 ms, P95 below 500 ms, errors below 1%, throughput grows with users | Partly met. At 100 users: average 95 ms, error rate 0%, throughput grows. The overall P95 is 520 ms, which is above target. | `performance_results.md` |
| EX-10 | One defect log with unique IDs, severity, priority and status | Met for `07_Test_Management/defect_log.md`. The copies in `01_Black_Box/` and `04_Web_API/` are older and differ. | `defect_log.md` |
| EX-11 | The master test repository matches the weekly files | Not met yet. It is cut off, and some test descriptions and statuses do not match their source. Aida has not applied the fixes yet. | `cross_check_defects.md` |

Summary: we met 5 of 11, partly met 1 (EX-9), and did not meet 5 (EX-3, EX-4, EX-6, EX-7, EX-11). EX-6 and EX-7 need defects to be fixed. That part is outside what we can do in this course.

## 10. Defect management

The rules are in `03_Special_Testing/test_conventions.md`. The final log applies them in `07_Test_Management/defect_log.md`.

### 10.1 Severity

| Severity | Meaning |
|---|---|
| Critical | Data is lost, or a security hole lets a user reach or change another user's data or session |
| Major | A main feature gives a wrong result or accepts invalid data, with no workaround |
| Moderate | Wrong behaviour with a workaround, or one group of users is blocked from part of the app |
| Minor | Cosmetic or wording, no effect on results |

### 10.2 Priority

Priority is separate from severity. The final log used one rule for every defect.

| Priority | Rule |
|---|---|
| High | All Critical defects, and Major defects that block a core flow for everyone or can be used directly |
| Medium | Other Major defects, and Moderate defects that give a wrong result, a crash or data exposure |
| Low | Moderate defects about missing limits with little harm, and all Minor defects |

### 10.3 Status lifecycle

`Open` then `Confirmed` then `Retest` then `Closed`.

- Open: found once.
- Confirmed: reproduced again, mostly by the Week 6 automated tests.
- Retest: a fix is delivered and we must re-run the linked tests.
- Closed: fixed. A duplicate is closed as `Closed (Duplicate of D-xxx)`. A defect we could not reproduce is closed as `Closed (Not reproducible)`.

### 10.4 How we used it

- Only the Defect & Metrics Coordinator gives out D-numbers. Other people use `DEF-TBC` until they get one.
- Same root cause means one defect. D-002 and D-003 are duplicates of D-001. D-036 (Back button after logout) is a duplicate of D-032. D-007 could not be reproduced and is closed.
- We logged 36 IDs. That makes 32 valid defects: 3 Critical, 9 Major, 14 Moderate and 6 Minor.
- 31 defects are Confirmed. 1 is Open (D-018, which needs a browser retest). None are in Retest or Closed as fixed.
- Draft IDs in Weeks 1, 4 and 5 clashed with real IDs. We mapped them in `01_Black_Box/defect_log.md`. We learnt to ask for the ID first.

## 11. Risks and mitigations

### 11.1 Project risks

| Risk | What happened | Mitigation |
|---|---|---|
| Not enough time | Weeks 4 to 7 were done within a few days (29 commits on 26 Nov alone). Some work was shallow, for example 11 of the 22 security tests only check part of the threat. | Keep the security depth table in `05_Security_Performance/README.md`. Plan more time next time. |
| Tool setup | Selenium, Locust and pytest-cov were set up on one machine each. Python versions differed. `requirements.txt` has only Flask. | Add the tools to `requirements.txt` (not done yet). Record versions in every evidence file. |
| One tester per area | Usability had one tester. `toggle_task` had one owner and was never done. A wrong Pass (TC-BB-002) lasted until Week 3. | Cross-checking in Week 7 (`cross_check_defects.md`). A second person should review each result. |
| Files overwritten or out of date | `automation_candidates.md` was overwritten after a merge. `execution_report.md` is behind. Several source files still show old results. | Pull before editing, and keep one source for each number. |
| Draft IDs and inconsistent IDs | Defect and test IDs clashed across weeks. | `test_conventions.md` and the ID mapping tables. |
| Missing evidence | Some screenshots are missing (for example `WTS-VAL-03.png`, the decision table screenshots, `TC-BB-067`). | Listed as open work. |

### 11.2 Product risks

These come from the risk list in `feature_inventory.md` and the scope matrix. The last column says what we found.

| Product risk | Where | What we found |
|---|---|---|
| SQL injection in API search | F-18 | D-020, Critical, confirmed. We only proved a syntax error, not data theft. |
| Any user can delete another user's task through the API | F-22 | D-025, Critical, confirmed |
| Stored XSS in task titles | F-08, F-09 | D-010, Major, confirmed |
| Password of exactly 8 characters rejected | F-01, F-02 | D-004, Major, confirmed |
| Due today shown as Overdue | F-14 | D-001, Moderate, confirmed. We first rated it High. |
| Duplicate usernames | F-01, F-02 | D-013, Major, confirmed |
| Bad dates break the list and dashboard | F-14, F-16, F-19 | D-006, Major, confirmed |
| Debug mode on | NFR-02 | D-031, Major, confirmed |
| Secret key in the source code | F-04 | D-027, Critical, confirmed |
| 7-day counter leaves out day 7 | F-15 | D-005, Moderate, confirmed |

All 10 risks turned out to be real defects. Because no defect is fixed, the product risk is still high.

## 12. Schedule

Dates come from git commit dates and file headers. We did not keep a separate schedule, so the dates are approximate. Some weeks overlap.

| Week | Dates (approx.) | What we did |
|---|---|---|
| 1 | 12 to 20 Oct | Feature inventory, scope matrix, risk list. EP, BVA, decision table and state transition design. First run of EP, BVA and decision table. Defects D-001 to D-005. |
| 2 | 4 to 16 Nov | White-box tests for 3 of 4 units with coverage. D-006. `toggle_task` not done. |
| 3 | 18 to 20 Nov | GUI checklist, compatibility, accessibility, usability. D-007 to D-018. |
| 4 | 23 to 25 Nov | Web scenarios, API tests, UI vs API comparison. D-019 to D-025. |
| 5 | 24 to 25 Nov | STRIDE table, 22 security tests, Locust load tests. D-026 to D-035. |
| 6 | 25 to 26 Nov | Automation candidates, 103 automated tests, regression suite, defect check. |
| 7 | 26 Nov | State transition run (D-036 raised, then merged into D-032). Master test repository, RTM, final defect log, cross-check, this plan. |
| 8 and 9 | After this plan | Final QA report (`08_Final_QA_Report/` has started). Agile and DevOps improvements. |

## 13. Limitations

- We found defects, but we did not retest any fix. No defect is fixed, so we cannot say how the app behaves after a fix.
- Black-box testing in Week 1 only covered web features. API tests came later.
- Some results are shallow. Examples: the CSRF test only looks for a token, the SQL injection test does not prove that data can be read, and the load test used only 30 seconds per stage.
- The testers used different machines, Python versions and operating systems. Some results may not repeat on another machine.
- Usability was tested by one person who already knew the app.
- Compatibility used device mode, not real devices.
- The master test repository has known mistakes and is cut off. Its total of 389 entries (286 distinct cases and 103 automated runs) is not reliable until it is fixed. The weekly files are more reliable.
- Some Week 1 results were wrong at first (TC-BB-002). Others may still be wrong. We rechecked the ones we noticed.
- Some state transition cases were run with the Flask test client, not in a browser. Two (TC-BB-067 and TC-BB-076) were run by hand in a browser.
- Defect ratings (severity, priority) are our own judgement. The defect log says the rule, but another group may rate them differently.
- `requirements.txt` does not list our test tools, so a reader cannot rebuild our setup from that file alone.

## 14. Deliverables

All paths are from the project root. Files in `07_Test_Management/` are in the same folder as this plan.

| Week | Deliverable | File |
|---|---|---|
| 1 | Feature inventory and risks | [feature_inventory.md](../01_Black_Box/feature_inventory.md) |
| 1 | Scope matrix | [test_scope_matrix.md](../01_Black_Box/test_scope_matrix.md) |
| 1 | EP test cases | [EP_Test_Cases.md](../01_Black_Box/EP_Test_Cases.md) |
| 1 | BVA test cases | [tc_bva.md](../01_Black_Box/tc_bva.md) |
| 1 | Decision table test cases | [tc_defect_coordinator.md](../01_Black_Box/tc_defect_coordinator.md) |
| 1 | State transition test cases | [tc_state_transition.md](../01_Black_Box/tc_state_transition.md) |
| 1 | Week 1 metrics and early defect log | [Week1_Metrics.md](../01_Black_Box/Week1_Metrics.md), [defect_log.md](../01_Black_Box/defect_log.md) |
| 2 | Selected units | [selected_units.md](../02_White_Box_Coverage/selected_units.md) |
| 2 | White-box tests and coverage | [test_helpers.py](../02_White_Box_Coverage/test_helpers.py), [coverage_evidence.txt](../02_White_Box_Coverage/coverage_evidence.txt), [automation_summary.md](../02_White_Box_Coverage/automation_summary.md) |
| 2 | Week 2 metrics | [Week2_Metrics.md](../02_White_Box_Coverage/Week2_Metrics.md) |
| 3 | GUI checklist | [gui_checklist.md](../03_Special_Testing/gui_checklist.md) |
| 3 | Compatibility matrix | [compatibility_matrix.md](../03_Special_Testing/compatibility_matrix.md) |
| 3 | Accessibility findings | [accessibility_findings.md](../03_Special_Testing/accessibility_findings.md) |
| 3 | Usability observations | [usability_observations.md](../03_Special_Testing/usability_observations.md) |
| 3 | Conventions and Week 3 metrics | [test_conventions.md](../03_Special_Testing/test_conventions.md), [Week3_Metrics.md](../03_Special_Testing/Week3_Metrics.md), [README.md](../03_Special_Testing/README.md) |
| 4 | Web test scenarios | [web_test_scenarios.md](../04_Web_API/web_test_scenarios.md) |
| 4 | API endpoints, cases and data | [api_endpoints.md](../04_Web_API/api_endpoints.md), [api_test_cases.md](../04_Web_API/api_test_cases.md), [api_test_cases_delete_dashboard.md](../04_Web_API/api_test_cases_delete_dashboard.md), [api_test_data.md](../04_Web_API/api_test_data.md) |
| 4 | UI vs API comparison | [ui_vs_api_comparison.md](../04_Web_API/ui_vs_api_comparison.md) |
| 4 | Week 4 summary and metrics | [README.md](../04_Web_API/README.md), [Week4_Metrics.md](../04_Web_API/Week4_Metrics.md) |
| 5 | STRIDE table | [stride_table.md](../05_Security_Performance/stride_table.md) |
| 5 | Security test cases and findings | [security_test_cases.md](../05_Security_Performance/security_test_cases.md), [security_findings.md](../05_Security_Performance/security_findings.md), [evidence_security.txt](../05_Security_Performance/evidence_security.txt) |
| 5 | Performance plan, script and results | [performance_plan.md](../05_Security_Performance/performance_plan.md), [locustfile.py](../05_Security_Performance/locustfile.py), [performance_results.md](../05_Security_Performance/performance_results.md), [performance_interpretation.md](../05_Security_Performance/performance_interpretation.md), [evidence_performance_rerun.txt](../05_Security_Performance/evidence_performance_rerun.txt) |
| 5 | Week 5 summary | [README.md](../05_Security_Performance/README.md) |
| 6 | Automation candidates | [automation_candidates.md](../06_Automation_Regression/automation_candidates.md) |
| 6 | Automated tests | [tests/](../06_Automation_Regression/tests/) |
| 6 | Manual-to-automated traceability | [manual_to_automated_traceability.md](../06_Automation_Regression/manual_to_automated_traceability.md) |
| 6 | Regression suite, execution report, defect check, logs | [regression_suite.md](../06_Automation_Regression/regression_suite.md), [execution_report.md](../06_Automation_Regression/execution_report.md), [week6_defect_check.md](../06_Automation_Regression/week6_defect_check.md), [logs/](../06_Automation_Regression/logs/) |
| 7 | Master test repository | [master_test_repository.md](master_test_repository.md) |
| 7 | Requirements traceability matrix | [rtm.md](rtm.md) |
| 7 | Final defect log | [defect_log.md](defect_log.md) |
| 7 | Cross-check of IDs and counts | [cross_check_defects.md](cross_check_defects.md) |
| 7 | This test plan | [test_plan.md](test_plan.md) |
