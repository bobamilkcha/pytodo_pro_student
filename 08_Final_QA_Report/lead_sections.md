# Final Report Sections: QA/Test Lead

**Date:** 26 Nov 2026
**For:** the final QA report (we copy these three sections into it)

Numbers come from `07_Test_Management/defect_log.md` (final defect log), `07_Test_Management/execution_status.md`, `07_Test_Management/test_plan.md`, the files in `05_Security_Performance/`, and `08_Final_QA_Report/metrics.md`. `metrics.md` is older. It still says 35 defect IDs and 193 automated tests, and it has no performance table. Where the files differ, we used the later files and say so.

---

## 1. Security evidence summary

### 1.1 Threats identified, tested and only analysed

We wrote a STRIDE table with 22 threats (`05_Security_Performance/stride_table.md`). We then wrote one test for each (TC-SEC-01 to TC-SEC-22) and ran them all.

| STRIDE category | Identified | Tested | Only analysed | Confirmed (test failed) | Control worked (test passed) |
|---|---|---|---|---|---|
| Spoofing | 4 | 4 | 0 | 4 | 0 |
| Tampering | 5 | 5 | 0 | 5 | 0 |
| Repudiation | 1 | 1 | 0 | 1 | 0 |
| Information disclosure | 6 | 6 | 0 | 4 | 2 |
| Denial of service | 4 | 4 | 0 | 4 | 0 |
| Elevation of privilege | 2 | 2 | 0 | 1 | 1 |
| Total | 22 | 22 | 0 | 19 | 3 |

No threat was left as analysis only. But "tested" does not mean "tested deeply". 10 of the 22 tests prove only part of the threat. For example, the CSRF test looks for a token in the form but does not use a real cross-site page. The XSS test checks that the script tag is in the page but does not see it run in a browser. The SQL injection test shows the query changes but does not show that another user's data can be read. The full list is in section 3.4 of `05_Security_Performance/README.md`.

A Fail is a good result for the test, because it found a weakness. The 3 passes are TC-SEC-13 (passwords stored as salted hashes), TC-SEC-16 (`GET /api/categories` shows only category names) and TC-SEC-22 (the web edit, toggle and delete routes check the owner).

### 1.2 Security defects found

The 19 failed tests point to 17 different defects: 10 new ones (D-026 to D-035) and 7 found earlier in other weeks. None is fixed.

| Severity | Defects |
|---|---|
| Critical (3) | D-020 SQL injection in `GET /api/tasks?q=`. D-025 any user can delete another user's task through the API. D-027 hard-coded secret key lets anyone forge a login cookie. |
| Major (7) | D-006 a bad due date makes pages return 500. D-010 stored XSS in task titles. D-011 whitespace-only title accepted. D-013 duplicate usernames. D-026 no rate limit on login. D-029 no CSRF protection. D-031 debug mode on. |
| Moderate (4) | D-028 old session cookie works after logout. D-032 no `Cache-Control` header on logged-in pages. D-033 cookie has no `SameSite` or `Secure`. D-034 no upper limit on `per_page`. |
| Minor (3) | D-014 `_` and `%` act as wildcards in search. D-030 no audit trail. D-035 logout works through GET. |

D-036 (Back button after logout) was logged first and then closed as a duplicate of D-032.

### 1.3 What our security testing can and cannot tell us

What it can tell us:
- 19 specific weaknesses exist, and each one has a test that fails today.
- The web pages and the JSON API follow different rules. The web delete checks the owner and the web search is safe. The API versions of both are not. Testing only the web pages would have missed both Critical API defects.
- The most urgent problems are the three Critical defects.
- Three controls worked.

What it cannot tell us:
- That the app is secure. Passing a test means the control worked for the input we tried.
- How far a real attacker could go. We used safe, simple inputs (one quote, `' OR 1=1 --`, `<script>alert(1)</script>`). It is not penetration testing, and we used no scanners and no password cracking.
- How the app behaves on a real server. All tests ran on our local copy, with the Flask test client and a temporary database. We did not test HTTPS, a proxy or a production server, so the `Secure` cookie flag was never tested in a real setup.
- What happens in browsers for CSRF, XSS and the Back button. Only the Back button was tried by hand, in one browser.
- Threats that are not in our table: HTTPS, session timeout and password strength.
- How serious each threat really is. The likelihood and impact ratings in the STRIDE table are our own guesses from reading the code. One was wrong: TH-13 said the database is committed to git, and it is not (the table is corrected, the ratings were not).
- Whether fixes work. No defect has been fixed and we have not retested anything.

---

## 2. Residual risk assessment

These are the risks that are still there at the end of testing. Likelihood (L) and impact (I) are H, M or L. For rows linked to a threat, we used the ratings from the STRIDE table. For the other rows the ratings are our own judgement. All the defects below are still open (31 Confirmed, 1 Open, 0 fixed).

| Risk ID | Area / feature | Risk | Why it remains | L | I | Related defect or threat | Recommended action |
|---|---|---|---|---|---|---|---|
| RR-01 | Delete task (API), F-22 | Any logged-in user can delete another user's task. The data is lost. | Open defect | H | H | D-025, TH-21 | Add `AND user_id = ?` to the delete query and return 404 if nothing is deleted. Re-run TC-SEC-21 and API-DD-01. |
| RR-02 | Task search (API), F-18 | SQL injection can change the query. | Open defect. Only partly tested: we showed an error and a changed query, but not that another user's data can be read. | H | H | D-020, TH-07, TH-14 | Use a parameterised query. Then test again with two accounts to see if data could be read. |
| RR-03 | Session handling | Anyone who has read the source can sign a login cookie as any user. | Open defect | M | H | D-027, TH-03 | Load the key from an environment variable and change the old key, because it is already public. |
| RR-04 | Server settings, NFR-02 | Debug mode shows error pages with code. The `/console` page may run Python code. | Open defect. Only partly tested: we read `app.py`, we did not open `/console`. | M | H | D-031, TH-11 | Turn debug off by default and use a production server. |
| RR-05 | Task title display, F-08 and F-09 | A script in a title is stored and shown without escaping. | Open defect. Only partly tested: we did not see the script run in a browser. | M | H | D-010, TH-05 | Remove the `safe` filter from the title. |
| RR-06 | Web forms | Another site could make a logged-in user's browser create, edit or delete tasks. | Open defect. Only partly tested: we looked for a token, we did not use a cross-site page. | M | M | D-029, TH-06 | Add CSRF tokens and set `SameSite`. |
| RR-07 | Login and register | Unlimited password guesses. Many logins use a lot of CPU because of password hashing. | Open defect. Only partly tested: we sent 10 and 20 requests, not a real attack. | M | H | D-026, TH-01, TH-19, PERF-OBS-01 | Add a rate limit. Then run the Locust stages again, because login times will change. |
| RR-08 | Logout and cookies, F-05 | An old cookie still works after logout. Back shows a cached page. Logout works through GET. The cookie has no `SameSite` or `Secure`. | Open defect. Only partly tested: Back was tried in one browser, and nothing was tested over HTTPS. | M | M | D-028, D-032, D-035, D-033, TH-04, TH-12, TH-15, TH-20 | End sessions on the server, send `Cache-Control: no-store`, make logout POST only, set the cookie flags. |
| RR-09 | Register, F-01 and F-02 | Two users can have the same name. A valid 8-character password is refused. | Open defect | H | M | D-013, D-004, TH-02 | Add a UNIQUE rule on usernames. Accept 8 characters. |
| RR-10 | Dates, F-14 and F-16 | One bad due date saved through the API makes the task list and dashboard return 500. The user cannot reach their tasks. | Open defect | M | H | D-006, TH-17 | Check the date on the server. |
| RR-11 | Urgency and dashboard, F-14 and F-15 | A task due today shows as Overdue. The 7-day counter leaves out day 7. Every user sees wrong numbers. | Open defect | H | M | D-001, D-005 | Add the "Due Today" case. Change the 7-day check to include day 7. |
| RR-12 | API input checks | Wrong data types give a 500 error. An unknown category is accepted. An empty title is accepted on edit. `"done": "false"` completes a task. Deleting a missing task returns 200. | Open defect | M | M | D-019, D-021, D-022, D-023, D-024 | Check input in the API, as the web forms do. |
| RR-13 | Accessibility, all pages | Missing labels, no accessible name on the done button, low contrast, no reflow at 320 px, small Edit and Delete links. | Open defect. Only partly tested: we used tools and one keyboard script, not a real screen reader. | H | M | D-009, D-015, D-016, D-017, D-018 | Fix them. Run axe and Lighthouse again. Test with a screen reader. |
| RR-14 | Larger data sets | The web list has no paging. `per_page` has no limit. A long title squashes the table. We only used small lists. | Open defect. Not tested with large data. | M | M | D-034, D-012, TH-18 | Cap `per_page`, limit title length, and test with hundreds of tasks. |
| RR-15 | Speed under load, NFR-03 | Overall P95 is 520 ms at 100 users, above our 500 ms target. Login and register slow down most. | Tested only locally: API only, up to 100 users, 30 seconds per stage, Flask dev server on a laptop. | M | M | PERF-OBS-01, PERF-OBS-02 | Repeat on a second machine, run longer, and add web pages. Decide a final target. |
| RR-16 | Real deployment | Behaviour with HTTPS, a production server and a proxy is unknown. | Not tested. Tested only locally. | M | H | TH-11, TH-15 | Test on a real setup before any real use. |
| RR-17 | Usability with real users | Our ratings are one person's view, and that person already knew the app. | Only partly tested | M | M | US-04, US-05, US-11, US-18 | Test with 3 to 5 new users. |
| RR-18 | Browsers and devices | Safari and real phones and tablets were not tested. | Only partly tested. Phone and tablet were simulated. | L | M | NFR-01 | Test on real devices and Safari. |
| RR-19 | Fixes and regression | No defect is fixed, so we do not know if fixes work or break something else. 29 of 51 regression tests fail today. | Not tested (no retest yet) | H | M | All open defects | Run the full suite after each fix. Retest each defect. |
| RR-20 | Threat model gaps | HTTPS, session timeout and password strength are not in the STRIDE table. | Not tested | M | M | none | Add them in the next round of threat modelling. |

### Important areas we did not test

- Browsers and devices: Safari, older browser versions, real phones and tablets. We tested Chrome 157, Edge 157 and Firefox 127 on Windows, plus a simulated phone and tablet.
- Real deployment: HTTPS, a production web server, a proxy, a real database server. We only used the Flask dev server and SQLite on our own machines.
- Larger data sets: long task lists, many users, long titles. The performance tests used very small lists.
- Longer or heavier load: more than 100 users, runs longer than 30 seconds, and the web pages. We load tested only 7 API endpoints.
- Real users: usability was one tester who knew the app. Accessibility had no real screen reader test.
- Real attacks: a real brute force, a real cross-site page, a script running in a browser, and reading another user's data through the SQL injection.
- Different machines: our results come from Windows and Linux, and from Python 3.10, 3.11 and 3.13. A second performance run on another machine was slower (login average 1,521 ms).
- Fixes: nothing was retested, because nothing was fixed.
- White-box tests for `toggle_task`: never written. The state transition tests cover how it behaves (TC-BB-070, 071 and 077), but not its code branches.

---

## 3. Overall quality assessment

### 3.1 Verdict

PyTodo Pro is not ready for real users. The normal paths work. The app fails where it matters for safety: checking input, checking who owns data, and server settings. We would not release it until the three Critical defects are fixed.

The numbers behind this:
- Weeks 1 to 5: 286 unique tests and checks. Of the 254 that give pass or fail, 177 passed and 77 failed (`execution_status.md`). The 31 usability observations were rated 6 Good, 21 Minor issue and 4 Major issue.
- Defects: 36 IDs logged, 32 valid. That is 3 Critical, 9 Major, 14 Moderate and 6 Minor. 12 of the 32 are Critical or Major. None is fixed.
- Automation: 103 automated tests, 69 pass and 34 fail. Every failure is a known defect, and none is a script problem. The regression suite has 51 tests, 22 pass and 29 fail.
- Load: 3,416 requests, 0 failed. The average response time was 24, 47 and 95 ms at 10, 50 and 100 users.

The pass rate falls from 92.9% in Week 2 to 13.6% in Week 5. This is because we aimed our tests at invalid input and attacks, not because the app got worse.

### 3.2 Strengths and weaknesses

| Quality characteristic (ISO/IEC 25010) | Strengths | Weaknesses |
|---|---|---|
| Functional suitability | Register (9 or more characters), login, create, edit, filter, mark done and delete all work. All 20 state transition cases give the expected result, except the Back button after logout. | A task due today shows as Overdue (D-001). The 8-character password is refused (D-004). The 7-day counter is wrong (D-005). Duplicate usernames are accepted (D-013). |
| Usability | Easy to find things. The nav bar is the same on every page. Compatibility passed 45 of 45 results on 5 configurations. | No success messages. Edit and Delete look the same. 8 of 16 accessibility checks failed, with missing labels and low contrast. |
| Security | Passwords are stored as salted hashes. The web routes check the task owner. | 19 of 22 security tests failed. The 3 Critical defects are all security defects (D-020, D-025, D-027). The web and the API follow different rules. |
| Performance efficiency | No errors in 3,416 requests. Throughput grew with the users (7.55, 36.92 and 72.19 requests per second). | Login and register are slow under load. The overall P95 is 520 ms at 100 users, over our 500 ms target. We only tested small data on a dev server. |
| Reliability | The app did not fail under our load test. | A bad due date makes pages return 500 (D-006). The wrong data type gives 500 in the API (D-019). Debug mode is on (D-031). |
| Maintainability | The regression suite checks 31 of 32 valid defects in seconds, so a fix is easy to check. | We did not test maintainability directly. The same feature has different rules in the web and the API, which suggests the code is hard to keep consistent. |

### 3.3 Exit criteria

We set 11 exit criteria in `07_Test_Management/test_plan.md`. We met 5, mostly met 1, partly met 1 and did not meet 4.

- Met: every feature has an executed test (EX-1), High priority features were executed (EX-2), every failed test links to a logged defect (EX-5), the regression suite fails only for known defects (EX-8), and one defect log exists (EX-10).
- Mostly met: the master test repository matches the weekly files (EX-11). Small items are still open in `cross_check_defects.md`.
- Partly met: performance (EX-9). Average time, error rate and throughput met the targets. The overall P95 at 100 users did not.
- Not met: no planned test left Not Run (EX-3), 100% coverage on every selected unit (EX-4, `toggle_task` is at 0%), no open Critical defects (EX-6, 3 are open), and no open Major defects without a decision (EX-7, 9 are open).

EX-6 and EX-7 need the developers to fix the defects. We cannot do that in this course.

### 3.4 What we cannot claim

Testing shows that defects are present. It does not show that there are none. We found 32 valid defects, and there are almost certainly more that we did not find. We cannot say the app is defect-free. High coverage does not change this. Our automated tests ran 94.8% of statements and 89.0% of branches (`metrics.md`, 25 Nov), but running a line is not the same as checking it. For example, every line of the delete API ran in the passing test API-TSK-DEL-01, and only a test with a second user showed the missing owner check (D-025).
