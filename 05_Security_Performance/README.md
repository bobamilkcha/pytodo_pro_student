# Week 5: Security and Performance Testing

**Prepared by:** QA Test Lead

## 1. Introduction

In Week 5 we looked at PyTodo Pro from a security and a speed point of view. First we went through the app with the STRIDE checklist and wrote down 22 threats without attacking anything. Then we wrote one safe test for each threat and ran them on our local copy with two test accounts. Last, we ran a small controlled load test against the JSON API with Locust, at 10, 50 and 100 users. We did not change any app code. Most threats turned out to be real (19 of 22), and the API held up under load without a single error, but the login and register requests got slow.

## 2. Deliverables

| Deliverable | File | Owner (role) |
|---|---|---|
| Threat / STRIDE table | `stride_table.md` | QA/Test Lead |
| Security test cases and findings | `security_test_cases.md`, `tests/test_security.py`, `evidence_security.txt` (test cases and results) | Test Design Coordinator |
| | `security_findings.md` (findings, defects, recommendations) | Defect & Metrics Coordinator |
| Performance test objective and workload | `performance_plan.md` (objectives, targets), `locustfile.py` (the workload) | Automation/Tool Coordinator |
| Performance results | `performance_results.md` | Automation/Tool Coordinator |
| Performance interpretation | `performance_interpretation.md`, `evidence_performance_rerun.txt` (second run) | Defect & Metrics Coordinator |
| Security and performance limitations and recommendations | `security_findings.md` (sections 5 and 6), `performance_interpretation.md` (sections 6 and 7), and sections 5 and 6 of this file | Defect & Metrics Coordinator, QA/Test Lead |

The official defect IDs are in `../01_Black_Box/defect_log.md`.

## 3. Security summary

### 3.1 Threats per STRIDE category

Counted from the table in `stride_table.md`.

| STRIDE category | Threat IDs | Threats | Tested | Confirmed (test failed) | Control worked (test passed) |
|---|---|---|---|---|---|
| Spoofing | TH-01 to TH-04 | 4 | 4 | 4 | 0 |
| Tampering | TH-05 to TH-09 | 5 | 5 | 5 | 0 |
| Repudiation | TH-10 | 1 | 1 | 1 | 0 |
| Information disclosure | TH-11 to TH-16 | 6 | 6 | 4 | 2 (TH-13, TH-16) |
| Denial of service | TH-17 to TH-20 | 4 | 4 | 4 | 0 |
| Elevation of privilege | TH-21, TH-22 | 2 | 2 | 1 | 1 (TH-22) |
| Total | | 22 | 22 | 19 | 3 |

The top five by Likelihood times Impact in the STRIDE table: TH-21 (API delete has no owner check), TH-07 and TH-14 (SQL injection in the API search), TH-03 (hard-coded secret key), TH-05 with TH-06 (HTML in titles and no CSRF token), TH-11 (debug mode). All five were confirmed by a test.

### 3.2 Security test cases

From `security_test_cases.md` (22 cases, TC-SEC-01 to TC-SEC-22) and the last lines of `evidence_security.txt` ("19 failed, 3 passed").

| Result | Count |
|---|---|
| Pass (the app blocked the threat) | 3 (TC-SEC-13, 16, 22) |
| Fail (the threat was confirmed) | 19 |
| Blocked | 0 |
| Not run | 0 |
| Total | 22 |

Check: 3 + 19 = 22. The Fail column adds up from the table above: 4 + 5 + 1 + 4 + 4 + 1 = 19.

A Fail here is a good result for the test, because it found a weakness. So a pass rate of 13.64% (3 of 22) says the app is weak, not that our testing went badly. What passed: passwords are stored as salted hashes (TC-SEC-13), `GET /api/categories` shows only ids and names (TC-SEC-16), and the web edit, toggle and delete routes check the task owner (TC-SEC-22).

### 3.3 Security defects

The 19 failed cases point to 17 different defects: 10 new ones (D-026 to D-035) and 7 that were already logged. Titles and severities are from the central defect log.

| Defect ID | Title (short) | Severity | Threat |
|---|---|---|---|
| D-020 | SQL injection in `GET /api/tasks?q=` (found Week 4) | Critical | TH-07, TH-14 |
| D-025 | Any user can delete another user's task through the API (found Week 4) | Critical | TH-21 |
| D-027 | Hard-coded `SECRET_KEY` lets anyone forge a session | Critical | TH-03 |
| D-006 | A bad due date makes the task list return 500 (found Week 2) | Major | TH-17 |
| D-010 | Task title shown as HTML, stored XSS (found Week 3) | Major | TH-05 |
| D-011 | Whitespace-only title accepted (found Week 3) | Major | TH-09 |
| D-013 | Duplicate usernames (found Week 3) | Major | TH-02 |
| D-026 | No rate limit or lockout on login | Major | TH-01, TH-19 |
| D-029 | No CSRF protection on web forms | Major | TH-06 |
| D-031 | `debug=True` hard-coded | Major | TH-11 |
| D-028 | Old session cookie works after logout | Moderate | TH-04 |
| D-032 | No `Cache-Control` on logged-in pages | Moderate | TH-12 |
| D-033 | Cookie has no `SameSite` or `Secure` | Moderate | TH-15 |
| D-034 | No upper limit on API `per_page` | Moderate | TH-18 |
| D-014 | `_` and `%` act as wildcards in search (found Week 3) | Minor | TH-08 |
| D-030 | No audit trail | Minor | TH-10 |
| D-035 | Logout works through GET | Minor | TH-20 |

Count: 3 Critical, 7 Major, 4 Moderate, 3 Minor, 17 in total. No defect is fixed.

### 3.4 Tested and only analysed

All 22 threats have a test case, so none is left as "analysis only". But the depth of the tests is different. Some tests confirm the weakness from code or from a response, not from a real attack. Our own list:

| Threat | What the test did | What it did not do |
|---|---|---|
| TH-03 | Signed a cookie with the key from `app.py` and the app accepted it | Nothing missing (the full test) |
| TH-06 CSRF | Looked for a token in the `/tasks/new` form | We did not build a cross-site page or try different browsers |
| TH-11 debug | Searched `app.py` for `debug=True` | We did not open `/console` or look at a real error page |
| TH-12 cache | Checked the `Cache-Control` header | We did not press Back in a browser (the Week 3 note US-29 did) |
| TH-14 | Showed the query can be changed (500 error) | It did not return another user's tasks, so reading other data is not proven |
| TH-07 | Showed a syntax error with one quote | Nothing more |
| TH-05 XSS | Checked the raw `<script>` tag is in the page | We did not see the script run in a browser |
| TH-01, TH-19 | Sent 10 and 20 requests and saw no limit | A real brute force, and the CPU load from password hashing |
| TH-15 | Read the `Set-Cookie` header after register | Not checked under HTTPS |
| TH-13 | Checked the hash format in a temporary database | See limitation 7 in section 5 |
| TH-20 | Confirmed `GET /logout` logs us out | We did not use an image on another page |

## 4. Performance summary

All numbers in this section are from `performance_results.md`.

### 4.1 What we tested

- **Endpoints (7):** `POST /api/register`, `POST /api/login`, `GET /api/tasks`, `GET /api/dashboard`, `GET /api/categories`, `POST /api/tasks`, `DELETE /api/tasks/<id>`. We did not test any web page, `GET /api/tasks/<id>` or `PUT /api/tasks/<id>`.
- **Workload** (from `locustfile.py`): each simulated user registers and logs in once, then waits 1 to 2 seconds between actions. The actions are weighted: list tasks 4, dashboard 3, categories 2, create-and-delete a task 1.
- **Load levels:** 10, 50 and 100 users, with a spawn rate of 2, 10 and 20 users per second. Each stage ran for 30 seconds.
- **Environment** (from `performance_plan.md`): Locust 2.46.0, Python 3.10.11 on Windows, local loopback (`127.0.0.1:5000`), SQLite, `python app.py` (the Flask development server).
- **Targets** (from `performance_plan.md`): average below 200 ms, P95 below 500 ms, error rate below 1%, and throughput that grows with the number of users.

### 4.2 Key numbers

| Stage | Users | Requests | Failed | Error rate | Avg (ms) | Median (ms) | P95 (ms) | Max (ms) | Throughput (req/s) |
|---|---|---|---|---|---|---|---|---|---|
| 1 Baseline | 10 | 221 | 0 | 0.00% | 24 | 10 | 140 | 204 | 7.55 |
| 2 Moderate | 50 | 1,073 | 0 | 0.00% | 47 | 13 | 310 | 770 | 36.92 |
| 3 High load | 100 | 2,122 | 0 | 0.00% | 95 | 19 | 520 | 1,478 | 72.19 |

Check: 221 + 1,073 + 2,122 = 3,416 requests, 0 failed.

Slowest endpoints (average at 10, 50 and 100 users):

| Endpoint | 10 users | 50 users | 100 users |
|---|---|---|---|
| `POST /api/register` | 147 ms | 412 ms | 662 ms |
| `POST /api/login` | 148 ms | 289 ms | 427 ms |
| Other 5 endpoints (range of averages) | 9 to 19 ms | 13 to 22 ms | 40 to 78 ms |

Against the targets: the average and error targets were met in all three stages. The P95 target was met at 10 and 50 users, and missed at 100 users (520 ms against 500 ms).

### 4.3 What happened as load grew

Nothing failed: no errors and no timeouts in 3,416 requests. Throughput rose almost in line with the users (7.55 to 36.92 to 72.19 req/s), so the server was not yet full at 100 users. The average and P95 times grew with the load, and most of that came from login and register, which hash passwords on purpose. The task, dashboard and category endpoints stayed fast (median 14 to 26 ms at 100 users). `performance_interpretation.md` explains that the 520 ms P95 comes from login and register at the start of the run, and that a real group of users would not all log in in the same few seconds.

A second run on a different machine (`evidence_performance_rerun.txt`, 2 CPU cores, Linux) had no errors and the same pattern, but it was slower at 100 users (login average 1,521 ms, overall P95 1,600 ms). So the exact times depend on the machine.

## 5. Limitations

Security:
1. All tests ran on our local copy, through the Flask test client and a temporary database. We did not test a real web server, a proxy or HTTPS. So we could not test the `Secure` cookie flag in a real HTTPS setup.
2. We used safe, simple inputs only (one quote, `' OR 1=1 --`, `<script>alert(1)</script>`). These show that a weakness exists. They do not show how far a real attacker could go.
3. This is not penetration testing. We used no external scanners and no password cracking. Rate-limit tests sent only 10 and 20 requests.
4. Some threats are only partly tested (see section 3.4). A passed test shows a control worked for the input we tried, not that the feature is secure.
5. Our likelihood and impact ratings in the STRIDE table are our own guesses from reading the code. Another group could rate them differently.
6. `stride_table.md` still has a "Test now or Week 4" column. That was the plan when we wrote it. All 22 tests were run in Week 5.
7. The STRIDE table (TH-13) says `pytodo_pro.db` is committed to git. It is not. `.gitignore` lists it and `git ls-files` shows no `.db` file. The risk in TH-13 is smaller than the table says. We did not change the table. TC-SEC-13 tested a temporary database, not our real file.

Performance:
1. Locust and the app ran on the same laptop, so they compete for the same CPU.
2. The app ran on Flask's development server with debug mode on, not on a production server.
3. The database was SQLite with very little data. Each user creates a task and deletes it straight away, so lists are short. SQLite allows one writer at a time, and our writes were light.
4. Each stage ran once, for 30 seconds. We have no repeat runs and no long run, so we cannot say how much the numbers vary.
5. We only tested the API, and only up to 100 users, so we do not know where the app starts to fail.
6. The results file does not list the CPU or RAM of the machine. `performance_plan.md` also stops after `python app.py`, so its workload and load stages are missing, and it names the database `pytodo.db` (the app uses `pytodo_pro.db`). The workload is defined in `locustfile.py` and the stage settings are in the headings of `performance_results.md`. `performance_interpretation.md` already lists these fixes. They are not done yet.
7. The results do not predict a real production setup.
8. The load test creates `perf_` users in the app's database. We should delete `pytodo_pro.db` afterwards, as in the STRIDE safe testing rules.

## 6. Recommendations

Priority is from the severity and priority in the defect log. These are proposals. We do not fix the app.

| Priority | Recommendation | Linked to |
|---|---|---|
| High | Load `SECRET_KEY` from an environment variable. The old key is public, so change it | D-027, TH-03 |
| High | Add `AND user_id = ?` to the API delete, and return 404 if nothing was deleted | D-025, TH-21 |
| High | Use a parameterised query for the API search | D-020, TH-07, TH-14 |
| High | Rate-limit `/login` and `/api/login`. This also protects the slow password hashing step | D-026, TH-01, TH-19. Performance: login averaged 427 ms and register 662 ms at 100 users |
| High | Turn off `debug=True` by default. Run the app on a production server for any real use | D-031, TH-11. Performance: our load test ran in debug mode |
| High | Remove `\|safe` from task titles. Validate the due date on the server | D-010, TH-05. D-006, TH-17 |
| Medium | Add CSRF tokens to the web forms and set `SameSite=Lax` | D-029, D-033, TH-06, TH-15 |
| Medium | Make old session cookies stop working after logout, and make logout POST-only | D-028, D-035, TH-04, TH-20 |
| Medium | Send `Cache-Control: no-store` on logged-in pages | D-032, TH-12 |
| Medium | Reject duplicate usernames and whitespace-only titles on the server | D-013, D-011, TH-02, TH-09 |
| Medium | Decide a final response time target. The 100-user P95 (520 ms) is only 20 ms over our own 500 ms target | PERF-OBS-02 |
| Low | Cap `per_page` | D-034, TH-18 |
| Low | Add an audit log for create, edit and delete | D-030, TH-10 |
| Low | Escape `%` and `_` in the search | D-014, TH-08 |
| Low | Next time: run Locust on a second machine, repeat each stage 3 times, log users in before the timed part, and add a longer run | Performance limitations 1, 4 and 5 |

## 7. What to pass on

Threats not fully tested (for a later week, if time allows):
- TH-06: a real cross-site page in more than one browser.
- TH-11: whether `/console` opens and what an error page shows.
- TH-12 and TH-04: Back button and cookie reuse in a real browser.
- TH-14: whether the SQL injection can return another user's tasks. We only proved the query changes.
- TH-01 and TH-19: the CPU cost of many logins. We did not test it. The performance results suggest it could matter.
- Not in the STRIDE table at all: HTTPS, session timeout and password strength (the 9-character rule, D-004).

Retests for Week 6 regression:
- Run all 22 `test_security.py` tests after each fix. Of the three that pass today, TC-SEC-22 and TC-SEC-13 are the most important to keep green. TC-SEC-16 is a lower priority.
- Re-run D-006 (TC-SEC-17) and the API delete (TC-SEC-21) first. These two are the easiest to break again.
- Re-run the Locust stages after rate limiting is added, because it will change the login times. `06_Automation_Regression/automation_candidates.md` lists which of these tests we propose to automate.
- Most of the 19 failing tests are expected to fail until a fix is made. The group has not yet decided whether to mark them as expected failures.

Residual risks for the Week 8 final report:
- All 17 security defects are open, including 3 Critical ones (D-020, D-025, D-027).
- Anyone who has read the source has the secret key, even after we change it in the code.
- We have no real data on production behaviour. The speed results come from a development server on a laptop.
- Performance observations PERF-OBS-01 and PERF-OBS-02 are not logged as defects. The next free defect ID is D-036. The group should agree if PERF-OBS-02 becomes one.
