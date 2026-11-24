# Week 5: Security Findings Summary

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Date:** 24 Nov 2026
**Based on:** `stride_table.md` (QA/Test Lead, threats TH-01 to TH-22), `security_test_cases.md` and `tests/test_security.py` (Aida, TC-SEC-01 to TC-SEC-22)
**Defect log:** `01_Black_Box/defect_log.md` (D-026 to D-035 added this week)

---

## 1. How the findings were checked

- Aida's security suite was run again on a fresh copy of the repository on 24 Nov 2026 with `pytest 05_Security_Performance/tests -v`. The result matched her report: **22 cases, 3 passed, 19 failed**.
- Every test ran against our **local copy only**, with an isolated temporary SQLite database and our own test accounts (`syasya_test1`, `syasya_test2`). No external scanners, password cracking or real flooding were used, and no system outside our own machine was touched. This follows the brief's rule not to do uncontrolled penetration testing.
- A **Fail** means the threat was confirmed: the app did not block it. A **Pass** means the app's security control worked.

---

## 2. Results by STRIDE category

| STRIDE category | Threats tested | Confirmed (Fail) | Blocked (Pass) | Defects |
| :--- | :---: | :---: | :---: | :--- |
| **S**poofing | 4 (TH-01 to TH-04) | 4 | 0 | D-026, D-013, D-027, D-028 |
| **T**ampering | 5 (TH-05 to TH-09) | 5 | 0 | D-010, D-029, D-020, D-014, D-011 |
| **R**epudiation | 1 (TH-10) | 1 | 0 | D-030 |
| **I**nformation disclosure | 6 (TH-11 to TH-16) | 4 | 2 | D-031, D-032, D-020, D-033 |
| **D**enial of service | 4 (TH-17 to TH-20) | 4 | 0 | D-006, D-034, D-026, D-035 |
| **E**levation of privilege | 2 (TH-21, TH-22) | 1 | 1 | D-025 |
| **Total** | **22** | **19 (86.36%)** | **3 (13.64%)** | **17 unique defects** |

**What passed (security controls that work):**
- **TC-SEC-13 (TH-13):** passwords are stored as salted hashes (`scrypt:` / `pbkdf2:`), never as plain text.
- **TC-SEC-16 (TH-16):** `GET /api/categories` returns only category ids and names, with no private data.
- **TC-SEC-22 (TH-22):** the **web** edit, toggle and delete routes check the task owner, so User B cannot change User A's tasks through the web pages.

---

## 3. Defects

The 19 failures point to **17 unique defects**: 10 new ones and 7 that were already in the log from earlier weeks.

### 3.1 New security defects (Week 5)

| Defect ID | Title (short) | STRIDE | Severity | Priority | Test Case |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **D-026** | No login rate limiting or lockout | Spoofing / DoS | Major | High | TC-SEC-01, TC-SEC-19 |
| **D-027** | Hard-coded `SECRET_KEY` lets anyone forge a session | Spoofing | **Critical** | High | TC-SEC-03 |
| **D-028** | Old session cookie still works after logout | Spoofing | Moderate | Medium | TC-SEC-04 |
| **D-029** | No CSRF protection on web forms | Tampering | Major | Medium | TC-SEC-06 |
| **D-030** | No audit trail for create, edit or delete | Repudiation | Minor | Low | TC-SEC-10 |
| **D-031** | `debug=True` hard-coded | Info disclosure | Major | High | TC-SEC-11 |
| **D-032** | No `Cache-Control` on logged-in pages | Info disclosure | Moderate | Medium | TC-SEC-12 |
| **D-033** | Cookie missing `SameSite` and `Secure` | Info disclosure | Moderate | Low | TC-SEC-15 |
| **D-034** | No upper limit on API `per_page` | DoS | Moderate | Low | TC-SEC-18 |
| **D-035** | Logout works through GET | DoS | Minor | Low | TC-SEC-20 |

### 3.2 Earlier defects confirmed as security threats

| Defect ID | First found | Week 5 test | Security view |
| :--- | :--- | :--- | :--- |
| D-006 | Week 2 | TC-SEC-17 | One bad date makes the task list unavailable (DoS) |
| D-010 | Week 3 | TC-SEC-05 | `<script>` in a title is stored and runs (stored XSS) |
| D-011 | Week 3 | TC-SEC-09 | Server trusts the browser's `required` check |
| D-013 | Week 3 | TC-SEC-02 | Duplicate usernames make accounts look the same (Spoofing) |
| D-014 | Week 3 | TC-SEC-08 | Search input is not escaped |
| D-020 | Week 4 | TC-SEC-07, TC-SEC-14 | User input changes the SQL query (SQL injection) |
| D-025 | Week 4 | TC-SEC-21 | Any user can delete another user's task (IDOR) |

### 3.3 Severity of the 17 security-related defects

| Severity | Count | Defect IDs |
| :--- | :---: | :--- |
| Critical | 3 | D-020, D-025, D-027 |
| Major | 7 | D-006, D-010, D-011, D-013, D-026, D-029, D-031 |
| Moderate | 4 | D-028, D-032, D-033, D-034 |
| Minor | 3 | D-014, D-030, D-035 |
| **Total** | **17** | |

---

## 4. Key findings

1. **Three ways to act as, or against, another user.** Anyone who reads the public source can forge a login cookie (D-027). Any logged-in user can delete another user's tasks through the API (D-025). And the API search runs user input as SQL (D-020). These are the three Critical defects and should be fixed first.
2. **Sessions are weak.** The cookie cannot be cancelled after logout (D-028), has no `SameSite` attribute (D-033), and forms have no CSRF tokens (D-029). Together, another website could act for a logged-in user, for example by creating a task with a `<script>` title (D-010).
3. **No protection against repeated attempts.** Login has no rate limit (D-026), and the API has no page-size limit (D-034).
4. **The web pages are safer than the API.** The web routes check the task owner (TC-SEC-22 passed) and use a safe search query, but the API does not (D-020, D-025). This matches the Week 4 finding.
5. **Some controls work well.** Passwords are hashed with a modern algorithm, and the public categories endpoint leaks nothing.

---

## 5. Limitations

- **Local and controlled only.** Tests ran on the Flask test client and a local copy. Behaviour behind a real web server, proxy or HTTPS (for example the `Secure` cookie flag) was not tested.
- **Safe payloads only.** Simple, well-known inputs were used (one quote, `' OR 1=1 --`, `<script>alert(1)</script>`). This shows a threat exists but does not measure how far an attacker could take it. For example, TC-SEC-14 changed the SQL query but did not return another user's data.
- **Small request counts.** Rate-limit tests sent 10 and 20 requests, which is enough to show there is no limit but is not a real brute-force or flooding test.
- **Not every threat was tested in the browser.** CSRF (D-029) was confirmed from the form HTML and cookie settings, not with a real cross-site page.
- **One pass is not proof of safety.** Passing cases show a control worked for the input we tried, not that the feature is fully secure.

## 6. Recommendations (priority order)

1. **Fix the three Critical defects first:** load `SECRET_KEY` from an environment variable (D-027), add `AND user_id = ?` to the API delete (D-025), and use a parameterised query for the API search (D-020).
2. **Protect sessions:** add CSRF tokens (D-029), set `SameSite=Lax` (D-033), make logout POST-only (D-035), and send `Cache-Control: no-store` on logged-in pages (D-032).
3. **Add limits:** rate-limit login (D-026) and cap `per_page` (D-034).
4. **Turn off debug mode by default** (D-031) and escape task titles by removing `|safe` (D-010).
5. **Retest** TC-SEC-01 to TC-SEC-21 after fixes, and keep `test_security.py` in the regression suite.
