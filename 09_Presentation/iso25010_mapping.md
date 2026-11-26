# PyTodo Pro: ISO/IEC 25010 Mapping

**Prepared by:** QA/Test Lead
**Date:** 27 Nov 2026
**Based on:** [final_qa_report.md](../08_Final_QA_Report/final_qa_report.md) and [test_plan.md](../07_Test_Management/test_plan.md)

## 1. Introduction

ISO/IEC 25010 is a standard that describes software product quality. It splits quality into eight characteristics, and each one has sub-characteristics. We use it as a checklist to see what our testing covered and what it did not. We did not plan our weeks around it, so this mapping was done after testing.

How we rate the evidence in the table:
- Direct: we ran tests that were aimed at this sub-characteristic.
- Indirect: we only learnt something about it from tests aimed at something else.
- Not adequately evaluated: we did little or nothing, or the test was too weak to say anything.

Some sub-characteristics fit more than one place. We chose the place that seemed most honest and say so in the table.

## 2. Mapping table

| Characteristic | Sub-characteristic | How we evaluated it (week and artefact) | Evidence | Key finding |
|---|---|---|---|---|
| Functional suitability | Completeness | Weeks 1 to 7. Every feature F-01 to F-22 has at least one executed test (`rtm.md`, exit criterion EX-1). | Direct | 25 of 25 requirements are covered by a test. We checked against our own feature list. We had no written specification to compare with. |
| Functional suitability | Correctness | Week 1 black-box (EP, BVA, decision table, state transition), Week 2 white-box, Week 4 API, Week 6 regression. | Direct | The normal paths work. Wrong results in D-001 (due today shows Overdue), D-004 (8-character password rejected), D-005 (7-day counter) and D-013 (duplicate usernames). |
| Functional suitability | Appropriateness | Not tested on its own. | Not adequately evaluated | We did not check if the features fit what a user needs. We only tested that they behave as designed. |
| Performance efficiency | Time behaviour | Week 5, `PERF-01` to `PERF-03` with Locust on 7 API endpoints (`performance_results.md`). | Direct | Average 24, 47 and 95 ms at 10, 50 and 100 users. P95 was 520 ms at 100 users, over our 500 ms target. Login and register were slowest. |
| Performance efficiency | Capacity | Week 5, Locust up to 100 users, 30 seconds per stage. | Indirect | 3,416 requests, 0 failed. We never went above 100 users or ran longer than 30 seconds. We used small data. |
| Performance efficiency | Resource utilisation | Not tested. | Not adequately evaluated | We did not record CPU or memory (`test_plan.md`, section 5). We only know that login is slow because of password hashing. |
| Compatibility | Interoperability (browsers and devices) | Week 3, `COMP-01` to `COMP-09` in `compatibility_matrix.md`. Chrome 157, Edge 157, Firefox 127 on Windows, a simulated Galaxy A55 and a simulated iPad Pro 13. | Direct, but limited | 9 of 9 checks passed (45 of 45 results). Safari and real devices were not tested. Some people would put browser checks under portability. We put them here. |
| Compatibility | Interoperability (API clients) | Week 4, Flask test client. | Indirect | We only used the Flask test client and our own scripts. No other kind of client was tried. |
| Compatibility | Co-existence | Not tested. | Not adequately evaluated | We never ran the app next to other software on a shared server. |
| Usability | Learnability and recognisability | Week 3, `US-01` to `US-31` task walkthrough (`usability_observations.md`). | Indirect | 6 Good, 21 Minor issue, 4 Major issue. One tester who already knew the app, so we may have missed first-time problems (RR-17). |
| Usability | Operability | Week 3, GUI checklist `GUI-01` to `GUI-18`. | Direct | 14 passed, 4 failed. Layout is consistent, but the done toggle has no accessible name (D-016). |
| Usability | User error protection | Week 3 usability, Week 4 client-server validation (`WTS-VAL-01` to `06`). | Direct | A "Minimum 8 characters" hint that rejects 8 characters (D-004). Whitespace-only title accepted (D-011). A 500-character title breaks the table (D-012). No success or error messages after create, delete and logout. |
| Usability | User interface aesthetics | Week 3, GUI checklist and compatibility screenshots. | Indirect | Layout is consistent on 5 configurations. We did not do a design review. |
| Usability | Accessibility | Week 3, `ACC-01` to `ACC-16` with axe-core, Lighthouse and a Playwright keyboard script (`accessibility_findings.md`). | Direct, but no real screen reader | 8 passed, 8 failed. Missing labels (D-009), low contrast (D-015), no reflow at 320 px (D-017), small click targets (D-018). |
| Reliability | Maturity (does it fail in normal use) | Weeks 4 to 6, test failures and the load test. | Indirect | 0 errors in 3,416 requests. A bad due date makes the list and dashboard return 500 (D-006). |
| Reliability | Fault tolerance | Week 2 white-box, Week 4 API, Week 5 security. | Direct | The app does not handle bad input well. Wrong data types give 500 (D-019). Debug mode is on (D-031). |
| Reliability | Availability and recoverability | Not tested. | Not adequately evaluated | We did not test restart, crash, a locked or damaged database, or a backup. |
| Security | Confidentiality | Week 5, STRIDE (`stride_table.md`, `TC-SEC-01` to `22`). | Direct, some tests shallow | Passwords are stored as salted hashes (`TC-SEC-13`) and the categories endpoint shows no private data (`TC-SEC-16`). Pages are cached after logout (D-032). Debug mode is on (D-031). |
| Security | Integrity | Week 4 API, Week 5 STRIDE. | Direct, some tests shallow | Anyone logged in can delete another user's task through the API (D-025, Critical). SQL injection in API search (D-020, Critical). Stored XSS (D-010). No CSRF protection (D-029). |
| Security | Authenticity | Week 5 STRIDE. | Direct | The secret key is in the source code, so a cookie can be forged (D-027, Critical). No rate limit on login (D-026). An old cookie works after logout (D-028). |
| Security | Non-repudiation and accountability | Week 5, one threat for Repudiation. | Direct, but only one threat | There is no audit trail (D-030). |
| Maintainability | Analysability and testability | Week 2 white-box coverage, Week 6 automation. | Indirect | The Flask test client runs without a server. Coverage after Week 6 was 94.8% of statements and 89.0% of branches. Coverage is not the same as checking. |
| Maintainability | Modularity and reusability | Week 2 code reading of 4 units, and the web against API results in Week 4. | Indirect | The same rule is written twice for web and API, with different results (D-011 and D-022, D-020, D-025). This suggests poor reuse. We did not review the code design. |
| Maintainability | Modifiability | Not tested. | Not adequately evaluated | We did not change any code. |
| Portability | Adaptability (other OS and Python versions) | Our own machines: Windows 10 and 11, some Linux runs, Python 3.10.11, 3.11.5 and 3.13 (`test_plan.md`, section 5). | Indirect | Tests ran on different team machines. We did not plan this as a test, and we did not compare results between machines, except for the performance re-run. |
| Portability | Installability | Not planned. Found during Week 6. | Indirect | `requirements.txt` lists only Flask, so test tools must be installed by hand. A fresh clone fails some tests until `init_db()` has run (S-02). |
| Portability | Replaceability | Not tested. | Not adequately evaluated | We did not try another server or another database. |

## 3. Characteristics we did not evaluate well, and why it matters

1. **Reliability over time.** We ran 30 seconds per load stage and short test runs. We did not test a long run, restart, memory growth, a damaged database file or recovery. A task app keeps people's data, so we do not know if the data survives a crash. Good results in our short runs do not say the app stays up for days.

2. **Portability to other servers and databases.** We only used the Flask development server and SQLite on our own machines. Debug mode is on (D-031), which is not allowed for a real deployment. We did not test HTTPS, a production server, a proxy or another database. The `Secure` cookie flag (D-033) was never tested in a real setup. So we cannot say the app would work or stay safe after it is deployed (RR-16).

3. **Maintainability beyond our code reading.** Week 2 looked at 4 units, and we never judged the design or tried a change. We have only a sign: web and API repeat the same rules in different ways. If the team fixes one place, the other can stay wrong. We cannot say how costly changes will be.

4. **Performance capacity and resource use.** We stopped at 100 users and 30 seconds, used small data, and only tested the API. A second machine gave a login average of 1,521 ms, so the numbers depend on the host. We did not measure CPU or memory. We do not know how the app behaves with hundreds of tasks per user.

5. **Usability with real users and real assistive tools.** One tester who knew the app did the walkthrough, and the accessibility checks were done with tools. A first-time user or a screen reader user could find problems we did not (RR-17, RR-13).

6. **Compatibility beyond browsers.** Safari and real phones and tablets were not tested. Co-existence and other API clients were not tested.

7. **Security depth.** All 22 threats were tested, but 10 of the 22 tests prove only part of the threat. We did not see a script run in a browser, a real cross-site request or data read through the SQL injection. Passing a test means the control worked for the input we tried. It does not mean the area is secure.

What this means for our verdict: the evidence is strongest for functional suitability, security and accessibility. It is weakest for reliability over time, portability and maintainability. Our "not ready for real users" verdict is based on the strong areas. For the weak areas, we cannot say the app is fine. We can only say we did not check.
