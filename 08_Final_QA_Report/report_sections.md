# Final Report Sections - Nafiesa (Defect & Metrics Coordinator)

**Date:** 25 Nov 2026
**For:** `final_qa_report.md` (QA/Test Lead integrates)

This file holds my three written sections for the final report:

| Section | Brief requirement | Week task |
| :--- | :--- | :--- |
| A. Security evidence | "Consolidate API, usability, security and performance evidence" | Week 8, task 3b |
| B. One process improvement | "Evaluate which QA activities could prevent recurrence" | Week 8, task 5 |
| C. QA and process improvements for Agile/DevOps | "Identify QA/process improvements that could be incorporated into an Agile/DevOps workflow" | Week 9, task 2b |

The metrics tables and charts are in `metrics.md`, and the defect analysis is in `07_Test_Management/defect_log.md`. Please copy, do not rewrite, the numbers, so they stay consistent.

---

## A. Security evidence

### A.1 What we did

We built a STRIDE threat table of 22 threats (TH-01 to TH-22) for the app's main assets: accounts, sessions, tasks and the server. From it we wrote 22 security test cases (TC-SEC-01 to TC-SEC-22) and automated all of them with pytest. Every test ran on our own local copy, with a temporary database and our own test accounts. We did not use external scanners, password cracking tools or real traffic floods, as the brief asks for safe, controlled testing.

### A.2 What we found

Of the 22 threats, **19 were confirmed** (the test failed because the app did not block the threat) and **3 were blocked**. The 19 failures point to **17 unique defects**: 10 new ones (D-026 to D-035) and 7 found earlier through other techniques (D-006, D-010, D-011, D-013, D-014, D-020, D-025).

| STRIDE category | Threats | Confirmed | Blocked | Main defects |
| :--- | :---: | :---: | :---: | :--- |
| Spoofing | 4 | 4 | 0 | D-027 (Critical), D-026, D-013, D-028 |
| Tampering | 5 | 5 | 0 | D-020 (Critical), D-010, D-029, D-011, D-014 |
| Repudiation | 1 | 1 | 0 | D-030 |
| Information disclosure | 6 | 4 | 2 | D-031, D-032, D-033, D-020 |
| Denial of service | 4 | 4 | 0 | D-006, D-026, D-034, D-035 |
| Elevation of privilege | 2 | 1 | 1 | D-025 (Critical) |
| **Total** | **22** | **19** | **3** | **17 unique** |

The three most serious findings are all **Critical**:

1. **D-025:** any logged-in user can permanently delete another user's task through `DELETE /api/tasks/<id>`, because the query checks only the task id.
2. **D-020:** the API search places the user's text straight into the SQL query. A single quote breaks the query, and `' OR 1=1 --` changes its structure.
3. **D-027:** the session secret key is written in the source code, so anyone who reads the code can forge a valid login cookie.

Three controls **did** work, and the report should say so to stay balanced:
- passwords are stored as salted hashes, not plain text (TC-SEC-13);
- the public categories endpoint returns no private data (TC-SEC-16);
- the **web** edit, toggle and delete routes check that the task belongs to the user (TC-SEC-22).

### A.3 What the evidence means

The clearest pattern is that **the web pages and the JSON API apply different rules** to the same feature. The web delete checks the owner and the web search uses a safe query, but the API versions do neither (D-025, D-020). The API also crashes with HTTP 500 on unexpected data types (D-019), which the web forms cannot send. Week 4 API testing found the first signs of this, and Week 5 confirmed it as a security problem. Testing only through the web pages would have missed both Critical API defects. Broken access control and injection are two of the most common web application risks (OWASP Foundation, 2021), and both appear here.

The second pattern is **missing defaults for a real deployment**: a hard-coded secret key, debug mode on, no rate limiting, no CSRF tokens and weak cookie flags (D-026, D-027, D-029, D-031, D-033). Each is common in a development build, but together they mean the app is not ready to be put on the internet as it is.

All 19 security failures are re-checked automatically by `05_Security_Performance/tests/test_security.py`, and the two Critical ones (D-020, D-025) are also in the Week 6 regression suite, so each fix can be checked again in seconds.

### A.4 Limitations

- These were targeted tests, one per threat, not a full penetration test. Passing TC-SEC-13, 16 and 22 means those specific checks worked, not that those areas are secure.
- In TC-SEC-14, the SQL injection payload changed the query but did not return another user's data. We did not try harder payloads, which keeps the test safe. So we can show the risk, but not the full damage an attacker could do.
- Tests ran with the Flask test client, not over HTTPS on a real server, so transport security (TLS) and server hardening were not tested.

---

## B. One process improvement (Defect & Metrics area)

**Idea: give every logged defect a "regression test" field, and do not set a defect to `Closed` until that test passes.**

**Why, from our own evidence.** Several defects were found again and again by different people in later weeks before anyone had an automated check for them:
- D-001 was found in Weeks 1, 2, 4 and 6;
- D-004 in Weeks 1, 3, 4 and 6;
- D-013 in Weeks 3, 4, 5 and 6.

Each rediscovery cost time, and in Week 1 it also produced two duplicate IDs (D-002, D-003). Until Week 6, D-004 had no automated test at the web or helper level at all. In Week 6, linking every defect to an automated test raised automated defect coverage from 81.3% to 96.9% (`metrics.md`, section 2).

**How it would work.**
1. When a defect is logged, the reporter adds a failing test that reproduces it, and puts its name in the log.
2. The test stays in the regression suite.
3. When the developers report a fix, the status moves to `Retest`. Only a passing run of that test moves it to `Closed`. This follows the usual practice of confirmation testing after a fix, plus regression testing to check that nothing else broke (International Software Testing Qualifications Board [ISTQB], 2023).

**What it prevents:** duplicate reports, a fix that quietly breaks again later, and "closed" defects with no proof that they were fixed.

---

## C. QA and process improvements for an Agile/DevOps workflow

In Agile and DevOps, a team delivers small changes often, so quality checks have to run continuously, not once at the end (Forsgren et al., 2018). Our project tested a finished app in weekly phases, which is closer to a traditional test stage. Below are five improvements that would move this QA work into an Agile/DevOps workflow. Each one is based on something we observed.

| # | Improvement | Where it fits | Evidence from our project | Defects it would have prevented or caught earlier |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Definition of Done includes tests and a security check.** A user story is "done" only when it has automated tests for its normal path, invalid input and another user's data. | Sprint planning and review | Both Critical API defects come from a missing check that the web version of the same feature has | D-020, D-025, D-022 |
| 2 | **Shift-left review of risky code.** A short peer review checklist for every pull request: parameterised SQL, owner check on every query by id, no secrets in code, no `debug=True`. | Pull request, before merge | D-020, D-027 and D-031 are each one visible line in `app.py` that a checklist would catch | D-020, D-025, D-027, D-031 |
| 3 | **Static analysis in the pipeline.** Run a Python security linter (for example Bandit) and an accessibility check (for example axe or Lighthouse CI) on every push. | CI pipeline (with the regression suite) | Week 3 accessibility defects were found with axe and Lighthouse but are checked only once; secrets and debug mode are findings a linter reports automatically | D-009, D-015, D-016, D-017, D-027, D-031 |
| 4 | **Defect-to-test rule** (section B). Every defect gets a failing regression test, and it is closed only when that test passes in the pipeline. | Defect workflow, linked to CI | Same defects rediscovered across 3–4 weeks; 2 duplicate IDs in Week 1 | Duplicates and re-opened defects in general |
| 5 | **Shared definition of the rules between web and API.** Validation (title, password, due date, category) lives in one function, used by both web and API routes, and is tested once. | Design and code review | The same rule is applied differently by web and API in D-006, D-011/D-022, D-019, D-020 and D-025 | D-006, D-011, D-019, D-021, D-022 |

Improvement 3 matters because accessibility is easy to break again with any template change. WCAG 2.2 (World Wide Web Consortium, 2023) gives testable success criteria, such as labels and contrast, so most of the checks we did by hand in Week 3 can run automatically on each push.

**Metrics to track each sprint.** These continue the metrics we already calculate, so the team can see whether quality is improving:
- defects found per sprint by severity, and how many were found **before** merge rather than after;
- the pass rate of the regression suite (it should rise as fixes arrive; today it is 43.1%: 22 of the 51 regression tests pass);
- automated defect coverage (96.9% today; the target is 100%);
- the time from a defect being logged to it being `Closed`.

These metrics only help if the team reads them as signals, not targets. For example, a falling defect count could mean that testing has stopped, not that the app got better.

**Link to the other sections.** These improvements are process rules: what must be tested before code is merged, and how defects move through their lifecycle. They assume a CI step that runs `pytest 06_Automation_Regression/tests -m regression` on every push or pull request, as recommended in `section_3_5_automation_performance.md`. We did not build that pipeline in this project, so it is a recommendation, not something we tested.

---

## References

Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean software and DevOps: Building and scaling high performing technology organizations*. IT Revolution Press.

International Software Testing Qualifications Board. (2023). *Certified Tester Foundation Level syllabus* (Version 4.0). ISTQB.

OWASP Foundation. (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. W3C. https://www.w3.org/TR/WCAG22/
