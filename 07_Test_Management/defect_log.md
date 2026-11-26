# Final Consolidated Defect Log - PyTodo Pro

**Maintained by:** Nafiesa (Defect & Metrics Coordinator)  
  
**Covers:** every defect raised in Weeks 1 to 7 (D-001 to D-036)  
**Rules used:** `03_Special_Testing/test_conventions.md` and the defect report template in the project brief

This is the **single source** for defect IDs, severity, priority and status. Earlier copies (`01_Black_Box/defect_log.md`, `04_Web_API/defect_log.md`) are kept as weekly history. If they differ from this file, this file is correct.

---

## 1. Summary

| Item | Count |
| :--- | :---: |
| Defect IDs logged | 36 |
| Closed as duplicate (D-002, D-003 → D-001; D-036 → D-032) | 3 |
| Closed as not reproducible (D-007) | 1 |
| **Valid unique defects** | **32** |
| Confirmed (reproduced again, mostly by automated regression in Week 6) | 31 |
| Open (found once, not yet retested) | 1 |
| Retest (fix delivered, waiting for retest) | 0 |
| Closed as fixed | 0 |

No defect has been fixed yet. Our role is to find and report defects and propose fixes. The developers decide on and make the changes, and then we retest.

### 1.1 Valid defects by severity

| Severity | Count | % | Defect IDs |
| :--- | :---: | :---: | :--- |
| Critical | 3 | 9.4% | D-020, D-025, D-027 |
| Major | 9 | 28.1% | D-004, D-006, D-010, D-011, D-013, D-022, D-026, D-029, D-031 |
| Moderate | 14 | 43.8% | D-001, D-005, D-009, D-012, D-015, D-016, D-017, D-019, D-021, D-023, D-028, D-032, D-033, D-034 |
| Minor | 6 | 18.8% | D-008, D-014, D-018, D-024, D-030, D-035 |
| **Total** | **32** | **100%** | |

### 1.2 Severity x priority check

Each cell counts valid defects. Severity is the impact; priority is how soon to fix (see section 2).

| Severity \ Priority | High | Medium | Low |
| :--- | :---: | :---: | :---: |
| Critical | 3 | 0 | 0 |
| Major | 6 | 3 | 0 |
| Moderate | 0 | 10 | 4 |
| Minor | 0 | 0 | 6 |

No Critical defect has Medium or Low priority, and no Minor defect has High or Medium priority, so the two scales agree.

### 1.3 Valid defects by module

| Module | Features | Count | Critical | Major | Moderate | Minor | Defect IDs |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Registration & login | F-01 to F-04 | 4 | 0 | 3 | 1 | 0 | D-004, D-013, D-019, D-026 |
| Session & logout | F-05 to F-07 | 5 | 1 | 0 | 3 | 1 | D-027, D-028, D-032, D-033, D-035 |
| Create / edit / mark done | F-08, F-10, F-12, F-19, F-21 | 6 | 0 | 3 | 3 | 0 | D-011, D-012, D-021, D-022, D-023, D-029 |
| Delete task | F-13, F-22 | 3 | 1 | 0 | 0 | 2 | D-024, D-025, D-030 |
| Task list, search & filter | F-09, F-11, F-18 | 5 | 1 | 1 | 1 | 2 | D-008, D-010, D-014, D-020, D-034 |
| Urgency & dashboard | F-14 to F-16 | 3 | 0 | 1 | 2 | 0 | D-001, D-005, D-006 |
| Accessibility & layout | All pages | 5 | 0 | 0 | 4 | 1 | D-009, D-015, D-016, D-017, D-018 |
| Server configuration | Whole app | 1 | 0 | 1 | 0 | 0 | D-031 |
| **Total** | | **32** | **3** | **9** | **14** | **6** | |

### 1.4 Valid defects by week found

| Week | Activity | Count | Defect IDs |
| :--- | :--- | :---: | :--- |
| 1 | Black-box | 3 | D-001, D-004, D-005 |
| 2 | White-box and coverage | 1 | D-006 |
| 3 | GUI, usability, accessibility | 11 | D-008, D-009, D-010, D-011, D-012, D-013, D-014, D-015, D-016, D-017, D-018 |
| 4 | Web and API | 7 | D-019, D-020, D-021, D-022, D-023, D-024, D-025 |
| 5 | Security | 10 | D-026, D-027, D-028, D-029, D-030, D-031, D-032, D-033, D-034, D-035 |
| 6 | Automation and regression | 0 | None (all failures matched existing defects) |
| 7 | State transition run (TC-BB-060 to 079) | 0 | None (D-036 closed as a duplicate of D-032) |
| | **Total** | **32** | |

---

## 2. How severity, priority and status were applied

**Severity** follows `test_conventions.md` section 3:

| Severity | Rule used |
| :--- | :--- |
| Critical | Data loss, or a security hole that lets a user reach or change another user's data or session |
| Major | A main feature gives a wrong result, accepts invalid data, or exposes a security weakness, with no workaround |
| Moderate | Wrong behaviour with a workaround, or one group of users (e.g. screen reader users) is blocked from part of the app |
| Minor | Cosmetic, wording, or a weakness with very small impact |

**Priority** was set with one rule for every defect:

| Priority | Rule used |
| :--- | :--- |
| High | All Critical defects, and Major defects that block a core flow for every user or can be exploited directly (register, login guessing, stored XSS, debug console, a page that crashes) |
| Medium | Other Major defects (blank titles, CSRF, which needs another site and a logged-in victim), and Moderate defects that give a wrong result, a crash, data exposure, or block a group of users |
| Low | Moderate defects about missing limits or checks with little harm (title length, unknown category, page size, cookie flags), and all Minor defects |

**Status** follows the lifecycle in the brief: `Open` → `Confirmed` → `Retest` → `Closed`.

| Status | Meaning in this log |
| :--- | :--- |
| Open | Found and logged once, not yet reproduced again |
| Confirmed | Reproduced again by a second test or a later week, here mainly by the Week 6 automated regression run |
| Retest | Developers report a fix; we must re-run the linked tests (none yet) |
| Closed (Duplicate of D-xxx) | Same bug as an older defect |
| Closed (Not reproducible) | Could not be reproduced and the evidence does not support it |

---

## 3. Changes made in this final version

| # | Change | Defects | Reason |
| :--- | :--- | :--- | :--- |
| 1 | Status `Open` → `Confirmed` | D-001, D-004, D-005, D-006, D-008, D-009, D-010, D-011, D-012, D-014, D-015, D-016, D-017, D-019, D-020, D-021, D-022, D-023, D-024, D-025, D-026, D-027, D-028, D-029, D-030, D-031, D-032, D-033, D-034, D-035 | Reproduced again by the automated run on 25 Nov 2026 (`06_Automation_Regression/week6_defect_check.md`) |
| 2 | Status `Open` → `Closed (Not reproducible)` | D-007 | `style.css` line 1 is a valid `*` selector and has never changed; the screenshot shows no overflow |
| 3 | Status kept `Open` | D-018 | Not retested yet; needs a browser |
| 3a | New ID logged, then `Closed (Duplicate of D-032)` | D-036 | Same root cause, feature and fix as D-032 (no `Cache-Control` header). `TC-BB-067` added to D-032 as a related test |
| 4 | Affected Feature now uses the API feature IDs from `feature_inventory.md` (F-02, F-04, F-16, F-18, F-19, F-21, F-22) | D-004, D-006, D-013, D-019 to D-026, D-034 | API defects were labelled with the web feature IDs (e.g. "F-13 Delete" for the API delete, which is F-22), and D-026 and D-034 used F-16/F-19 for the wrong features |
| 5 | "F-04 Session" replaced | D-027, D-033 | F-04 is "Login (API)". Session handling sits behind F-06 and F-07 |
| 6 | Evidence paths corrected | D-001, D-003, D-005, D-006 | The listed files did not exist in the repo; replaced with the files that do |
| 7 | Severity, priority, titles and steps | None changed | Already consistent with section 2 |

---

## 4. Defect register (one row per ID)

| ID | Short title | Module | Week found | Severity | Priority | Status | Automated regression |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| D-001 | Task due today shown as Overdue | Urgency & dashboard | 1 | Moderate | Medium | Confirmed | Yes (6) |
| D-002 | Duplicate of D-001 | Urgency & dashboard | 1 | Moderate | Medium | Closed (Duplicate of D-001) | - |
| D-003 | Duplicate of D-001 | Urgency & dashboard | 1 | Moderate | Medium | Closed (Duplicate of D-001) | - |
| D-004 | 8-character password rejected | Registration & login | 1 | Major | High | Confirmed | Yes (4) |
| D-005 | Dashboard misses task completed exactly 7 days ago | Urgency & dashboard | 1 | Moderate | Medium | Confirmed | Yes (2) |
| D-006 | Bad due date saved, then task list and dashboard return 500 | Urgency & dashboard | 2 | Major | High | Confirmed | Yes (6) |
| D-007 | CSS selector on line 1 breaks input width (not reproducible) | Accessibility & layout | 3 | Minor | Low | Closed (Not reproducible) | - |
| D-008 | Wrong empty-list message when user has no tasks | Task list, search & filter | 3 | Minor | Low | Confirmed | Yes (1) |
| D-009 | Form fields and filters have no label | Accessibility & layout | 3 | Moderate | Medium | Confirmed | Yes (5) |
| D-010 | Task title rendered as HTML (stored XSS) | Task list, search & filter | 3 | Major | High | Confirmed | Yes (1) |
| D-011 | Title of only spaces accepted | Create / edit / mark done | 3 | Major | Medium | Confirmed | Yes (1) |
| D-012 | No maximum title length | Create / edit / mark done | 3 | Moderate | Low | Confirmed | Yes (1) |
| D-013 | Same username can be registered twice | Registration & login | 3 | Major | High | Confirmed | Yes (3) |
| D-014 | _ and % act as wildcards in search | Task list, search & filter | 3 | Minor | Low | Confirmed | Yes (3) |
| D-015 | Grey text fails 4.5:1 contrast | Accessibility & layout | 3 | Moderate | Medium | Confirmed | Yes (2) |
| D-016 | Done toggle has no accessible name | Accessibility & layout | 3 | Moderate | Medium | Confirmed | Yes (1) |
| D-017 | No reflow at 320 px width | Accessibility & layout | 3 | Moderate | Medium | Confirmed | Yes (1) |
| D-018 | Edit/Delete links below 24 x 24 px | Accessibility & layout | 3 | Minor | Low | Open | No |
| D-019 | Wrong data type in API body gives 500 | Registration & login | 4 | Moderate | Medium | Confirmed | Yes (4) |
| D-020 | SQL injection in GET /api/tasks?q= | Task list, search & filter | 4 | Critical | High | Confirmed | Yes (4) |
| D-021 | Non-existent category_id accepted | Create / edit / mark done | 4 | Moderate | Low | Confirmed | Yes (2) |
| D-022 | PUT accepts empty title | Create / edit / mark done | 4 | Major | Medium | Confirmed | Yes (2) |
| D-023 | "done": "false" completes the task | Create / edit / mark done | 4 | Moderate | Medium | Confirmed | Yes (2) |
| D-024 | DELETE returns 200 for missing task | Delete task | 4 | Minor | Low | Confirmed | Yes (4) |
| D-025 | Any user can delete another user's task (IDOR) | Delete task | 4 | Critical | High | Confirmed | Yes (5) |
| D-026 | No login rate limit or lockout | Registration & login | 5 | Major | High | Confirmed | Yes (2) |
| D-027 | Hard-coded SECRET_KEY allows forged sessions | Session & logout | 5 | Critical | High | Confirmed | Yes (1) |
| D-028 | Old session cookie works after logout | Session & logout | 5 | Moderate | Medium | Confirmed | Yes (1) |
| D-029 | No CSRF protection on web forms | Create / edit / mark done | 5 | Major | Medium | Confirmed | Yes (1) |
| D-030 | No audit trail for changes | Delete task | 5 | Minor | Low | Confirmed | Yes (1) |
| D-031 | Debug mode hard-coded on | Server configuration | 5 | Major | High | Confirmed | Yes (1) |
| D-032 | No Cache-Control on logged-in pages | Session & logout | 5 | Moderate | Medium | Confirmed | Yes (1) |
| D-033 | Session cookie lacks SameSite/Secure | Session & logout | 5 | Moderate | Low | Confirmed | Yes (1) |
| D-034 | No upper limit on per_page | Task list, search & filter | 5 | Moderate | Low | Confirmed | Yes (1) |
| D-035 | Logout works through GET | Session & logout | 5 | Minor | Low | Confirmed | Yes (1) |
| D-036 | Duplicate of D-032 (Back button after logout) | Session & logout | 7 | Moderate | Medium | Closed (Duplicate of D-032) | - |

The number in brackets is how many automated tests fail because of that defect. These tests should pass once the defect is fixed.

---

## 5. Proposed fix order (for the developers)

We only propose this order. The developers decide what to fix and when, then we retest.

| Order | Defects | Why first |
| :--- | :--- | :--- |
| 1 | D-025, D-020, D-027 | Critical: another user's data can be deleted or read, and sessions can be forged |
| 2 | D-010, D-029, D-026, D-031, D-013 | Major security weaknesses; D-010 and D-029 together allow a cross-site attack |
| 3 | D-004, D-006, D-011, D-022 | Major functional defects: users cannot register with a valid password, and bad data breaks pages |
| 4 | D-001, D-005 and the other Moderate defects | Wrong results with a workaround |
| 5 | Minor defects | Cosmetic or very small impact |

---

## 6. Draft IDs from team files mapped to this log

### 6.1 Week 4 draft IDs mapped to this log

Week 4 files used temporary IDs. This table shows where each one is logged, so the same bug is not counted twice.

| Draft ID / Test Case | Source file | Logged as |
| :--- | :--- | :--- |
| DEF-API-01 (`API-REG-08`), DEF-API-03 (`API-LOG-06`) | `04_Web_API/defect_log.md` | **D-019** |
| DEF-API-02 (`API-REG-09`) | `04_Web_API/defect_log.md` | **D-013** (existing, confirmed through the API) |
| "D-009" draft (blank title on web create and edit, `WTS-VAL-03`) | `04_Web_API/web_test_scenarios.md` | **D-011** (existing). D-009 is already used for form labels |
| `API-TSK-GETALL-04`, `TC-API-UI-27` | `api_test_cases.md`, `ui_vs_api_comparison.md` | **D-020** |
| `API-TSK-POST-04`, `TC-API-UI-15`, `API-DD-10` | `api_test_cases.md`, `ui_vs_api_comparison.md`, `api_test_cases_delete_dashboard.md` | **D-006** (existing) |
| `API-TSK-POST-07` | `api_test_cases.md` | **D-019** |
| `API-TSK-POST-08`, `TC-API-UI-16` | `api_test_cases.md`, `ui_vs_api_comparison.md` | **D-021** |
| `API-TSK-PUT-03`, `TC-API-UI-18` | `api_test_cases.md`, `ui_vs_api_comparison.md` | **D-022** |
| `API-TSK-PUT-06`, `TC-API-UI-22` | `api_test_cases.md`, `ui_vs_api_comparison.md` | **D-023** |
| `API-TSK-DEL-02`, `API-DD-02`, `TC-API-UI-23` | `api_test_cases.md`, `api_test_cases_delete_dashboard.md`, `ui_vs_api_comparison.md` | **D-024** |
| `API-TSK-DEL-05`, `API-DD-01`, `TC-API-UI-24` | `api_test_cases.md`, `api_test_cases_delete_dashboard.md`, `ui_vs_api_comparison.md` | **D-025** |
| `API-DASH-01`, `TC-API-UI-14` | `api_test_cases.md`, `ui_vs_api_comparison.md` | **D-001** (existing) |
| `API-DD-08` | `api_test_cases_delete_dashboard.md` | **D-005** (existing) |
| `TC-API-UI-02` | `ui_vs_api_comparison.md` | **D-004** (existing) |
| `TC-API-UI-04` | `ui_vs_api_comparison.md` | **D-013** (existing) |
| `TC-API-UI-12` | `ui_vs_api_comparison.md` | **D-012** (existing) |
| `TC-API-UI-25`, `TC-API-UI-26` | `ui_vs_api_comparison.md` | **D-014** (existing, now also in the API) |

### 6.2 Week 5 security test cases mapped to this log

`05_Security_Performance/security_test_cases.md` first used draft IDs D-015 to D-026, which were already taken in this log. Its Defect ID column has now been corrected to the IDs below. This table is kept as a record of the change.

| Test Case | Threat | Draft ID in `security_test_cases.md` | Logged as |
| :--- | :--- | :--- | :--- |
| TC-SEC-01 | TH-01 | D-015 (New) | **D-026** (new) |
| TC-SEC-02 | TH-02 | D-013 | **D-013** (existing) |
| TC-SEC-03 | TH-03 | D-016 (New) | **D-027** (new) |
| TC-SEC-04 | TH-04 | D-017 (New) | **D-028** (new) |
| TC-SEC-05 | TH-05 | D-010 | **D-010** (existing) |
| TC-SEC-06 | TH-06 | D-018 (New) | **D-029** (new) |
| TC-SEC-07 | TH-07 | D-019 (New) | **D-020** (existing) |
| TC-SEC-08 | TH-08 | D-014 | **D-014** (existing) |
| TC-SEC-09 | TH-09 | D-011 | **D-011** (existing) |
| TC-SEC-10 | TH-10 | D-020 (New) | **D-030** (new) |
| TC-SEC-11 | TH-11 | D-021 (New) | **D-031** (new) |
| TC-SEC-12 | TH-12 | D-022 (New) | **D-032** (new) |
| TC-SEC-14 | TH-14 | D-023 (New) | **D-020** (existing, same unsafe query) |
| TC-SEC-15 | TH-15 | D-024 (New) | **D-033** (new) |
| TC-SEC-17 | TH-17 | D-006 | **D-006** (existing) |
| TC-SEC-18 | TH-18 | D-012 | **D-034** (new; D-012 is the title length limit) |
| TC-SEC-19 | TH-19 | D-015 (New) | **D-026** (new, same as TC-SEC-01) |
| TC-SEC-20 | TH-20 | D-025 (New) | **D-035** (new) |
| TC-SEC-21 | TH-21 | D-026 (New) | **D-025** (existing) |

---

## 7. Full defect reports

Each report follows the defect report template in the project brief.

### Defect ID: D-001
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** F-14 Urgency badge, F-15 Dashboard (web), F-16 Dashboard (API)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser: Chrome / Edge
- **Preconditions:** User is logged in and viewing the task list or dashboard.
- **Steps to Reproduce:**
  1. Navigate to Create Task page (`/tasks/new`).
  2. Create an open task titled "Mock Interview" with **today's date** as the due date.
  3. Save the task and view the task list/dashboard.
- **Expected Result:** The task should display a "Due Today" urgency badge.
- **Actual Result:** The task displays an "Overdue" badge (red label).
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `01_Black_Box/evidence/EP/TC-BB-008.png`, `01_Black_Box/evidence/BVA/TC-BB-BVA-F14-02-1_Actual.png`, `TC-BB-BVA-F14-02-2_Actual.png`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `TC-BB-F14-02`
- **Week 4 retest:** Confirmed through the API. `API-DASH-01` (dashboard counts a task due today as overdue) and `TC-API-UI-14` (API returns urgency `Overdue` for today).
- **Week 6 regression (25 Nov 2026):** Reproduced by 6 automated test(s): TC-WB-F14-04 (test_compute_urgency), API-DASH-01, TC-API-UI-14, TC-BB-F14-02, REG-D001-01, REG-D001-02. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-002
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** Task Urgency Logic (`helpers.py`)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Navigate to the Create Task page (`/tasks/new`).
  2. Create an open task and set the due date exactly to **today's date**.
  3. Save the task and view the task list or dashboard.
- **Expected Result:** The task should display a **"Due Today"** badge.
- **Actual Result:** The task displays an **"Overdue"** badge.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Closed (Duplicate of D-001)
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F14-02-2_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F14-02`

### Defect ID: D-003
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** F-14: Urgency badge
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Navigate to the Create Task page (`/tasks/new`).
  2. Create an open task and set the due date exactly to **today's date**.
  3. Save the task and view the task list or dashboard.
- **Expected Result:** The task should display a **"Due Today"** badge.
- **Actual Result:** The task displays an **"Overdue"** badge.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Closed (Duplicate of D-001)
- **Evidence:** `01_Black_Box/evidence/BVA/TC-BB-BVA-F14-02-1_Actual.png`, `TC-BB-BVA-F14-02-2_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F14-02`

### Defect ID: D-004
- **Title:** Registration incorrectly rejects valid 8-character passwords
- **Affected Feature:** F-01 Register (web), F-02 Register (API) (`is_valid_password()` in `helpers.py`)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is on the registration page.
- **Steps to Reproduce:**
  1. Navigate to `http://127.0.0.1:5000/register`.
  2. Enter a unique, valid username.
  3. Enter exactly 8 characters for the password (e.g., `12345678`).
  4. Click the register button.
- **Expected Result:** The registration should be successful and the account created.
- **Actual Result:** The registration is rejected with a validation error message.
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F01-02_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F01-02`
- **Week 4 retest:** Confirmed through the API. `TC-API-UI-02`: `POST /api/register` also rejects an 8-character password, because the UI and API share `is_valid_password()`.
- **Week 6 regression (25 Nov 2026):** Reproduced by 4 automated test(s): TC-API-UI-02, REG-D004-01 (8 chars), REG-D004-02, REG-D004-03. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-005
- **Title:** Dashboard 7-day counter excludes tasks completed exactly 7 days ago
- **Affected Feature:** F-15: Dashboard (web)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in and has a task completed exactly 7 days prior.
- **Steps to Reproduce:**
  1. Change the system clock to exactly 7 days in the past.
  2. Create a new task and mark it as "Done".
  3. Revert the system clock to the current date.
  4. Navigate to `/dashboard` and observe the "completed in the last 7 days" counter.
- **Expected Result:** The counter should include the task that was completed exactly 7 days ago.
- **Actual Result:** The counter ignores the task, though the task list still shows its status as "Done".
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `01_Black_Box/evidence/BVA/TC-BB-BVA-F15-01-1_Actual.png`, `TC-BB-BVA-F15-01-2_Actual.png`, `04_Web_API/evidence/evidence_api_delete_dashboard.txt`
- **Related Test Case:** `TC-BB-BVA-F15-01`
- **Week 4 retest:** Confirmed through the API. `API-DD-08`: `GET /api/dashboard` returns `completed_this_week: 0` for a task completed exactly 7 days ago.
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): API-DD-08, API-DD-08 (W6 copy). Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-006
- **Title:** A badly formatted due date sent through the API is saved, then makes the task list API return HTTP 500
- **Affected Feature:** F-14 Urgency badge, F-19 Create task (API), F-18 List tasks (API), F-16 Dashboard (API) (`helpers.py` line 31)
- **Environment:** Python 3, Flask test client (pytest), Localhost (http://127.0.0.1:5000)
- **Preconditions:** A registered user is logged in through the API.
- **Steps to Reproduce:**
  1. Send `POST /api/tasks` with `{"title": "Test", "due_date": "04-11-2026"}` (wrong date format).
  2. Send `GET /api/tasks`.
- **Expected Result:** Step 1 returns 400 with a validation message, or the list in step 2 still returns 200.
- **Actual Result:** Step 1 returns 500 after saving the task. Every later `GET /api/tasks` for that user returns 500, because `compute_urgency` calls `strptime` with no error handling.
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `02_White_Box_Coverage/compute_urgency/evidence/cu_terminal_results.jpg`, `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_api_delete_dashboard.txt`
- **Related Test Case:** `TC-WB-F14-10`
- **Suggested Fix:** Validate `due_date` on the server before saving, and catch `ValueError` in `compute_urgency`.
- **Week 4 retest:** Confirmed again by `API-TSK-POST-04` and `TC-API-UI-15`. New effect found by `API-DD-10`: once such a task exists, `GET /api/dashboard` also returns 500, so the user's dashboard stops working.
- **Week 5 retest:** `TC-SEC-17` (threat TH-17, Denial of service) confirms it through the web route as well: one task with due date `04-11-2026` makes `GET /` return 500, so the user can no longer open their task list.
- **Week 6 regression (25 Nov 2026):** Reproduced by 6 automated test(s): TC-WB-F14-10 (test_compute_urgency), API-DD-10, API-TSK-POST-04, TC-API-UI-15, TC-SEC-17, API-DD-10 (W6 copy). Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-007
- **Title:** Invalid CSS selector `-` on line 1 of `style.css` disables `box-sizing: border-box`, so form inputs overflow their container
- **Affected Feature:** F-01 Register, F-03 Login, F-08 Create Task, F-10 Edit Task (`static/style.css`)
- **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized), Localhost (http://127.0.0.1:5000)
- **Preconditions:** User opens `/login`, `/register` or `/tasks/new`.
- **Steps to Reproduce:**
  1. Navigate to `/login` or `/tasks/new`.
  2. Look at the right edge of the text inputs compared with the labels and card padding.
- **Expected Result:** Inputs, text areas and dropdowns line up on both edges inside their container.
- **Actual Result:** Line 1 is `- { box-sizing: border-box; }` instead of `* { ... }`, so inputs with `width: 100%` add padding and border on top and stick out past the right edge.
- **Severity:** Minor
- **Priority:** Low
- **Status:** Closed (Not reproducible)
- **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-01.png`
- **Related Test Case:** `GUI-01`
- **Week 6 review:** Could not be reproduced. `static/style.css` line 1 is `* { box-sizing: border-box; }` (a valid selector), and `git log` shows the file has not changed since the first commit on 12 Oct 2026. In `GUI-01.png` the inputs line up with the same 32 px gap on both sides. Closed on 25 Nov 2026. `GUI-01` should be re-run by its owner. See `06_Automation_Regression/week6_defect_check.md` section 6.

### Defect ID: D-008
- **Title:** Task list shows "No tasks match your filters." when the user has no tasks and no filters applied
- **Affected Feature:** F-09 Task list (`templates/index.html`)
- **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized), Localhost (http://127.0.0.1:5000)
- **Preconditions:** Logged-in user has 0 tasks. No category, status or search filter is set.
- **Steps to Reproduce:**
  1. Log in with an account that has no tasks.
  2. Open the home page (`/`) without choosing any filter.
- **Expected Result:** A clear empty-list message, e.g. "No tasks yet. Click + New Task to create one."
- **Actual Result:** "No tasks match your filters." is shown, which suggests filters are hiding tasks.
- **Severity:** Minor
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-08.png`, `03_Special_Testing/evidence/usability_testing/US-22a.png`
- **Related Test Case:** `GUI-08`, `US-22`
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): GUI-08. Log: `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-009
- **Title:** Form fields and filter controls have no programmatic label, so screen readers cannot name them
- **Affected Feature:** F-01 Register, F-03 Login, F-08 Create Task, F-10 Edit Task, F-11 Filter and search (`register.html`, `login.html`, `task_form.html`, `index.html`)
- **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized); Google Chrome 153 (headless, Linux), 1366 x 768. Localhost (http://127.0.0.1:5000)
- **Preconditions:** None (login needed only for the task pages).
- **Steps to Reproduce:**
  1. Open `/login` and click the word "Username".
  2. Open `/` and run an accessibility check (Lighthouse or axe) on the category, status and search controls.
- **Expected Result:** Clicking a label moves focus to its input. Every input, dropdown and search box has a label or `aria-label`.
- **Actual Result:** Clicking the label does nothing. Labels have no `for` attribute and inputs have no `id`. The two filter dropdowns and the search box have no label at all. axe reports "Form elements must have labels" and "Select element must have an accessible name" (critical) on 5 pages.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-02.png`, `03_Special_Testing/evidence/accessibility_testing/ACC-01.png`, `ACC-08.png`
- **Related Test Case:** `GUI-02`, `ACC-01`, `ACC-08`
- **Suggested Fix:** Add `id` to each input and `for` to each label. Add `aria-label` to the filters.
- **Week 6 regression (25 Nov 2026):** Reproduced by 5 automated test(s): ACC-01 (/login), ACC-01 (/register), ACC-01 (/tasks/new), ACC-01 (edit), ACC-08. Log: `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-010
- **Title:** Task title is rendered as HTML because `index.html` uses the `|safe` filter
- **Affected Feature:** F-09 Task list (`templates/index.html`)
- **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized), Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Create a task with the title `<b>Bold task</b>`.
  2. Open the task list (`/`).
- **Expected Result:** The title shows as plain text, including the `<b>` tags.
- **Actual Result:** The title shows in bold. The tags are run as HTML, not shown as text. This display problem is also the stored XSS risk noted in the feature inventory (to be covered in Week 5, Security).
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-10.png`
- **Related Test Case:** `GUI-10`
- **Week 5 retest:** `TC-SEC-05` (threat TH-05, Tampering) confirms **stored XSS**: a title of `<script>alert(1)</script>` is saved and rendered unescaped on `/`. Today it only runs in the owner's own browser, but together with the missing CSRF protection (D-029) another website could create such a task for a logged-in user.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-05. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-011
- **Title:** A task title made only of spaces is accepted, creating a row with no visible title
- **Affected Feature:** F-08 Create Task, F-10 Edit Task
- **Environment:** Windows 11, Google Chrome (Desktop), Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Open `/tasks/new`.
  2. Type only spaces in the Title box.
  3. Click "Create Task".
- **Expected Result:** The task is rejected with a message such as "Title is required."
- **Actual Result:** The task is saved and appears in the list with a blank title. The browser's `required` check only blocks a fully empty box, and the server does not trim the title.
- **Severity:** Major
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/usability_testing/US-11b.png` (blank row at the bottom of the table)
- **Related Test Case:** `US-11`
- **Week 4 retest:** `WTS-VAL-03` (Aida, draft "D-009") shows the same gap on the web **edit** route as well as create: `new_task()` and `edit_task()` only rely on the HTML `required` attribute. Evidence: `WTS-VAL-03.png` is referenced in `web_test_scenarios.md` but is not in the repo yet.
- **Week 5 retest:** `TC-SEC-09` (threat TH-09) confirms the web route returns 302 and saves a blank title.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-09. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-012
- **Title:** No maximum title length, so a very long title fills the task table with one huge row
- **Affected Feature:** F-08 Create Task, F-09 Task list
- **Environment:** Windows 11, Google Chrome (Desktop), Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Create a task with a title of several hundred characters (e.g. a pasted paragraph).
  2. Open the task list.
- **Expected Result:** The title is limited (e.g. 100 characters), or long titles are cut short with "..." in the list.
- **Actual Result:** The title is accepted with no limit. In the list it wraps into a very tall row, which pushes the other tasks far down and makes the table hard to scan.
- **Severity:** Moderate
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/usability_testing/US-11b.png`, `US-11c.png`, `US-11d.png`
- **Related Test Case:** `US-11`
- **Week 4 retest:** `TC-API-UI-12`: the API also accepts a 500-character title. No limit exists in the UI or the API.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-API-UI-12. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-013
- **Title:** The same username can be registered more than once
- **Affected Feature:** F-01 Register (web), F-02 Register (API) (`app.py` register routes)
- **Environment:** Windows, Google Chrome (Desktop); retested on Google Chrome 153 (headless, Linux). Localhost (http://127.0.0.1:5000)
- **Preconditions:** An account `acc_tester` already exists.
- **Steps to Reproduce:**
  1. Open `/register`.
  2. Enter the username `acc_tester` and a valid password.
  3. Click "Register".
- **Expected Result:** Registration is rejected with "This username is already in use."
- **Actual Result:** Registration succeeds and the user is logged in. The database now holds two users named `acc_tester` (ids 1 and 5). `app.py` line 150 notes that there is no uniqueness check, and the `users` table has no UNIQUE rule on the username.
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/accessibility_testing/ACC_scan_log.txt` (retest), usability notes `US-04`
- **Related Test Case:** `US-04`, `TC-BB-002`
- **Note:** Week 1 case `TC-BB-002` ("Registration fails when username already exists") is marked Pass. That result conflicts with this retest and should be re-run and changed to Fail.
- **Week 4 retest:** Confirmed through the API. `API-REG-09` (draft DEF-API-02) and `TC-API-UI-04`: `POST /api/register` returns 201 for an existing username.
- **Week 5 retest:** `TC-SEC-02` (threat TH-02, Spoofing) confirms it again. Two accounts with the same name can be mistaken for each other.
- **Week 6 regression (25 Nov 2026):** Reproduced by 3 automated test(s): API-REG-09, TC-API-UI-04, TC-SEC-02. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-014
- **Title:** Underscore `_` in the search box works as a wildcard and matches any single character
- **Affected Feature:** F-11 Filter and search (`app.py`, index route, `LIKE` query)
- **Environment:** Windows 11, Google Chrome (Desktop), Localhost (http://127.0.0.1:5000)
- **Preconditions:** User has a task titled "due today".
- **Steps to Reproduce:**
  1. Type `due_today` in the search box.
  2. Click "Filter".
- **Expected Result:** Only titles that contain the exact text `due_today` are shown.
- **Actual Result:** The task "due today" (with a space) is also shown, because `_` and `%` are not escaped before the `LIKE` query.
- **Severity:** Minor
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/usability_testing/US-24.png`
- **Related Test Case:** `US-24`, `TC-WB-F11-11`
- **Week 4 retest:** `TC-API-UI-25` and `TC-API-UI-26`: `GET /api/tasks?q=` also treats `_` and `%` as wildcards. In the API this comes from the same unsafe query as D-020.
- **Week 5 retest:** `TC-SEC-08` (threat TH-08) confirms `%` is also a wildcard in the web search.
- **Week 6 regression (25 Nov 2026):** Reproduced by 3 automated test(s): TC-API-UI-25, TC-API-UI-26, TC-SEC-08. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-015
- **Title:** Done task titles and the empty-list message fail the 4.5:1 colour contrast minimum (2.84:1)
- **Affected Feature:** F-09 Task list, F-12 Mark done (`static/style.css`, `.done .title-cell` and `.empty`)
- **Environment:** Google Chrome 153 (headless, Linux), 1366 x 768, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User has at least one done task (or no tasks, for the empty message).
- **Steps to Reproduce:**
  1. Mark a task as done and open `/`.
  2. Measure the contrast of the struck-through title (or the "No tasks match your filters." text) with Lighthouse or a contrast checker.
- **Expected Result:** Text contrast is at least 4.5:1 (WCAG 1.4.3, Level AA).
- **Actual Result:** Grey `#999999` on white gives 2.84:1.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/accessibility_testing/ACC-03a.png`, `ACC-03b.png`
- **Related Test Case:** `ACC-03`
- **Suggested Fix:** Use `#767676` or darker.
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): ACC-03 (done title), ACC-03 (.empty). Log: `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-016
- **Title:** Done toggle button has no meaningful accessible name (only "○" or "✓")
- **Affected Feature:** F-12 Mark done / reopen (`templates/index.html`)
- **Environment:** Google Chrome 153 (headless, Linux), 1366 x 768, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User has at least one task.
- **Steps to Reproduce:**
  1. Open `/`.
  2. Inspect the accessible name of the round button in the first column (or move to it with a screen reader).
- **Expected Result:** The button has a name such as "Mark as done" or "Mark as open".
- **Actual Result:** The name is only the symbol `○` or `✓`, with no `aria-label` or `title`. A screen reader reads "white circle, button".
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/accessibility_testing/ACC-02.png`, usability notes `US-16`
- **Related Test Case:** `ACC-02`, `US-16`
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): ACC-02. Log: `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-017
- **Title:** Pages do not reflow at 320 px wide; the page scrolls sideways and the "Log out" link becomes hard to see
- **Affected Feature:** All pages (`templates/base.html`, `static/style.css`)
- **Environment:** Google Chrome 153 (headless, Linux), window 320 x 640, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Resize the window (or use DevTools device mode) to 320 px wide.
  2. Open `/`.
- **Expected Result:** Content fits the width with no horizontal scrolling (WCAG 1.4.10 Reflow).
- **Actual Result:** The page is 510 px wide, so it scrolls sideways. The nav bar does not stretch, and "Log out" sits on the light background, where it is almost invisible. There is no `<meta name="viewport">` tag and no `@media` rule.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `03_Special_Testing/evidence/accessibility_testing/ACC-09.png`
- **Related Test Case:** `ACC-09`
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): ACC-09. Log: `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-018
- **Title:** Edit and Delete links are smaller than the 24 x 24 px minimum target size
- **Affected Feature:** F-10 Edit Task, F-13 Delete Task (`templates/index.html`, `.actions a`, `.link-btn`)
- **Environment:** Google Chrome 153 (headless, Linux), 1366 x 768, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User has at least one task.
- **Steps to Reproduce:**
  1. Open `/`.
  2. Measure the Edit and Delete links in any row.
- **Expected Result:** Each target is at least 24 x 24 px or has enough space around it (WCAG 2.2, 2.5.8).
- **Actual Result:** Edit is 24 x 16 px and Delete is 39 x 15 px, stacked close together. Lighthouse flags this as "Touch targets do not have sufficient size or spacing".
- **Severity:** Minor
- **Priority:** Low
- **Status:** Open
- **Evidence:** `03_Special_Testing/evidence/accessibility_testing/ACC-11.png`
- **Related Test Case:** `ACC-11`
- **Week 6 regression (25 Nov 2026):** Not automated. Measuring a target size needs a real browser. Stays `Open` until a Selenium or manual browser retest confirms it.

### Defect ID: D-019
- **Title:** JSON API returns HTTP 500 when a text field is sent as another data type or the body is not a JSON object
- **Affected Feature:** F-02 Register (API), F-04 Login (API), F-19 Create task (API) (`api_register`, `api_login`, `api_create_task` in `app.py`)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** For `POST /api/tasks`, the user is logged in through the API.
- **Steps to Reproduce:**
  1. Send `POST /api/register` with `{"username": 12345, "password": "Password123"}`.
  2. Send `POST /api/login` with `{"username": 12345, "password": "Password123"}`.
  3. Send `POST /api/tasks` with `{"title": 12345}`.
- **Expected Result:** Each request is rejected with 400 (or 401 for login) and a JSON `error` message.
- **Actual Result:** All three return 500 Internal Server Error. The code calls `.strip()` on the value without checking that it is text (`AttributeError: 'int' object has no attribute 'strip'`). The web forms cannot send these values, so only the API is affected.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_auth.txt`, `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-REG-08`, `API-LOG-06`, `API-TSK-POST-07`, `TC-API-UI-06` (drafts DEF-API-01, DEF-API-03)
- **Suggested Fix:** Check `isinstance(value, str)` before `.strip()`, and check the body is a JSON object, returning 400 otherwise.
- **Week 6 regression (25 Nov 2026):** Reproduced by 4 automated test(s): API-REG-08, API-LOG-06, API-TSK-POST-07, TC-API-UI-06. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-020
- **Title:** SQL injection in `GET /api/tasks?q=`: the search text is placed directly into the SQL query
- **Affected Feature:** F-18 List tasks (API), search parameter `q` (`app.py` line 379: `query += f" AND title LIKE '%{q}%'"`)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in through the API.
- **Steps to Reproduce:**
  1. Send `GET /api/tasks?q=test'` (one single quote).
- **Expected Result:** 200 with an empty list. The quote is treated as plain text, as the web search does.
- **Actual Result:** 500 Internal Server Error (`sqlite3.OperationalError: unrecognized token`). The quote breaks the SQL statement, which proves user input is run as SQL. The web route uses a safe parameterised query (`LIKE ?`), so only the API is affected.
- **Severity:** Critical
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-TSK-GETALL-04`, `TC-API-UI-27`, threat `TH-07` (Week 5)
- **Suggested Fix:** Use a parameterised query (`AND title LIKE ?` with `f"%{q}%"` as the parameter).
- **Week 5 retest:** `TC-SEC-07` confirms the syntax error. `TC-SEC-14` sent `' OR 1=1 --` as User 2: the payload changed the SQL statement (the `--` removed the `LIMIT ? OFFSET ?` part), which caused a 500 error (`Incorrect number of bindings`). User 1's data was **not** returned in this test, but the query structure can clearly be changed by the user, so the risk stays Critical.
- **Week 6 regression (25 Nov 2026):** Reproduced by 4 automated test(s): API-TSK-GETALL-04, TC-API-UI-27, TC-SEC-07, TC-SEC-14. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-021
- **Title:** `POST /api/tasks` accepts a `category_id` that does not exist
- **Affected Feature:** F-19 Create task (API)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in through the API.
- **Steps to Reproduce:**
  1. Send `POST /api/tasks` with `{"title": "Invalid category", "category_id": 9999}`.
- **Expected Result:** 400 with an error such as "invalid category".
- **Actual Result:** 201 Created. The task is saved with `category_id: 9999` and `category: null`.
- **Severity:** Moderate
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-TSK-POST-08`, `TC-API-UI-16`
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): API-TSK-POST-08, TC-API-UI-16. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-022
- **Title:** `PUT /api/tasks/<id>` accepts an empty title and overwrites the existing title with a blank
- **Affected Feature:** F-21 Update task (API, `api_update_task`)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in and owns a task.
- **Steps to Reproduce:**
  1. Create a task with a normal title.
  2. Send `PUT /api/tasks/<id>` with `{"title": ""}`.
- **Expected Result:** 400 `{"error": "title is required"}`, the same rule as `POST /api/tasks`. The old title is kept.
- **Actual Result:** 200 OK. The title becomes an empty string. The update route has no title check at all.
- **Severity:** Major
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-TSK-PUT-03`, `TC-API-UI-18`
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): API-TSK-PUT-03, TC-API-UI-18. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-023
- **Title:** `PUT /api/tasks/<id>` treats `"done": "false"` (text) as true and completes the task
- **Affected Feature:** F-21 Update task (API, `api_update_task`), done flag
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in and owns an open task.
- **Steps to Reproduce:**
  1. Send `PUT /api/tasks/<id>` with `{"done": "false"}`.
- **Expected Result:** 400 (wrong data type), or the task stays open.
- **Actual Result:** 200 OK and the task becomes done. Python's `bool("false")` is `True`, because any non-empty text counts as true.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-TSK-PUT-06`, `TC-API-UI-22`
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): API-TSK-PUT-06, TC-API-UI-22. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-024
- **Title:** `DELETE /api/tasks/<id>` returns 200 "ok" for a task that does not exist or was already deleted
- **Affected Feature:** F-22 Delete task (API, `api_delete_task`)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** User is logged in through the API.
- **Steps to Reproduce:**
  1. Send `DELETE /api/tasks/99999` (no such task).
  2. Or delete one of your tasks, then send the same `DELETE` again.
- **Expected Result:** 404 `{"error": "not found"}`, the same as `GET` and `PUT` for a missing task.
- **Actual Result:** 200 `{"result": "ok"}` every time. The caller is told the delete worked when nothing was deleted.
- **Severity:** Minor
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_api_delete_dashboard.txt`
- **Related Test Case:** `API-TSK-DEL-02`, `API-DD-02`, `TC-API-UI-23`
- **Week 6 regression (25 Nov 2026):** Reproduced by 4 automated test(s): API-DD-02, API-TSK-DEL-02, TC-API-UI-23, API-DD-02 (W6 copy). Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-025
- **Title:** Any logged-in user can permanently delete another user's task through `DELETE /api/tasks/<id>` (IDOR)
- **Affected Feature:** F-22 Delete task (API, `app.py` line 459: `DELETE FROM tasks WHERE id = ?` with no `user_id`)
- **Environment:** Python 3, pytest with Flask test client, Localhost (http://127.0.0.1:5000)
- **Preconditions:** Two accounts exist. User A owns a task.
- **Steps to Reproduce:**
  1. As User A, create a task and note its `id`.
  2. As User B, send `DELETE /api/tasks/<id of A's task>`.
  3. As User A, send `GET /api/tasks/<id>`.
- **Expected Result:** Step 2 returns 403 or 404 and the task is kept. Step 3 returns 200.
- **Actual Result:** Step 2 returns 200 `{"result": "ok"}`. Step 3 returns 404: User A's task is **permanently deleted** by another user. The web delete route checks the owner (`AND user_id = ?`), so only the API is affected. The code comment confirms it: "deletes by id only".
- **Severity:** Critical
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `04_Web_API/evidence/evidence_api_tasks.txt`, `04_Web_API/evidence/evidence_api_delete_dashboard.txt`, `04_Web_API/evidence/evidence_ui_vs_api.txt`
- **Related Test Case:** `API-TSK-DEL-05`, `API-DD-01`, `TC-API-UI-24`, threat `TH-21` (Week 5), risk R1
- **Suggested Fix:** Add `AND user_id = ?` to the delete query and return 404 when no row was deleted.
- **Week 5 retest:** `TC-SEC-21` (threat TH-21, Elevation of privilege) confirms it. In contrast, `TC-SEC-22` passed: the **web** edit, toggle and delete routes do check the owner.
- **Week 6 regression (25 Nov 2026):** Reproduced by 5 automated test(s): API-DD-01, API-TSK-DEL-05, TC-API-UI-24, TC-SEC-21, API-DD-01 (W6 copy). Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`, `06_Automation_Regression/logs/week6_suite.txt`.

### Defect ID: D-026
- **Title:** No rate limiting or lockout on login: unlimited password guesses are accepted on both `/login` and `/api/login`
- **Affected Feature:** F-03 Login (web), F-04 Login (API) (`login_page`, `api_login` in `app.py`)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** Test account `syasya_test1` exists and is logged out.
- **Steps to Reproduce:**
  1. Send 10 `POST /login` requests in a row with the wrong password.
  2. Send 20 `POST /api/login` requests in a row with the wrong password.
- **Expected Result:** After a few failed attempts the account is temporarily locked, slowed down, or the server returns `429 Too Many Requests`.
- **Actual Result:** All 10 web attempts return 200 with "Invalid username or password." and all 20 API attempts return 401. There is no delay, lockout or 429 response, so an attacker can keep guessing passwords.
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_01`, `test_sec_19`)
- **Related Test Case:** `TC-SEC-01`, `TC-SEC-19`, threats `TH-01` (Spoofing) and `TH-19` (Denial of service)
- **Suggested Fix:** Limit failed attempts per username and per IP (for example with Flask-Limiter) and return 429 after the limit.
- **Week 6 regression (25 Nov 2026):** Reproduced by 2 automated test(s): TC-SEC-01, TC-SEC-19. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-027
- **Title:** Hard-coded `SECRET_KEY` lets anyone who reads the source forge a valid session cookie and log in as any user
- **Affected Feature:** Session handling behind F-06 Page protection (web) and F-07 Endpoint protection (API) (`app.py` line 28: `app.config["SECRET_KEY"] = "pytodo-pro-dev-secret"`)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** Two test accounts exist (`syasya_test1` id 1, `syasya_test2` id 2). The tester is logged out.
- **Steps to Reproduce:**
  1. Using the key from `app.py`, sign a Flask session cookie with `{"user_id": 2, "username": "syasya_test2"}`.
  2. Send `GET /` with this cookie.
- **Expected Result:** The forged cookie is rejected and the user is sent to `/login`.
- **Actual Result:** 200 OK. The app loads `syasya_test2`'s session without any password. The key is in the public repository, so anyone can impersonate any user.
- **Severity:** Critical
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_03`)
- **Related Test Case:** `TC-SEC-03`, threat `TH-03` (Spoofing), asset A-05
- **Suggested Fix:** Load a long random key from an environment variable, never commit it, and change it if it has been exposed.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-03. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-028
- **Title:** A session cookie copied before logout still works after logout
- **Affected Feature:** F-05 Logout (`app.py` lines 179–181: `logout()` only calls `session.clear()`)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` is logged in.
- **Steps to Reproduce:**
  1. Copy the `session` cookie value after login.
  2. Call `GET /logout`.
  3. Send `GET /` again with the old cookie value.
- **Expected Result:** The old cookie is no longer accepted and the user is sent to `/login`.
- **Actual Result:** 200 OK. The old cookie still gives full access. Flask's default cookie is stored on the client and logout only clears the browser's copy, so a stolen cookie stays valid.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_04`)
- **Related Test Case:** `TC-SEC-04`, threat `TH-04` (Spoofing)
- **Suggested Fix:** Use server-side sessions or store a session version per user that is changed on logout, and set a session expiry time.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-04. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-029
- **Title:** Web forms have no CSRF protection, so another website can create, edit, toggle or delete tasks for a logged-in user
- **Affected Feature:** F-08 Create Task, F-10 Edit Task, F-12 Mark done, F-13 Delete Task (`task_form.html`, `index.html`)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` is logged in.
- **Steps to Reproduce:**
  1. Request `GET /tasks/new` and inspect the form HTML.
  2. Check the other POST forms in `index.html` (toggle, delete).
- **Expected Result:** Every state-changing form has a hidden anti-CSRF token that the server checks.
- **Actual Result:** No form has a CSRF token, and the server accepts POST requests without one. Because the session cookie also has no `SameSite` attribute (D-033), a page on another site could submit these forms using the user's session.
- **Severity:** Major
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_06`)
- **Related Test Case:** `TC-SEC-06`, threat `TH-06` (Tampering)
- **Suggested Fix:** Add CSRF tokens to all POST forms (for example Flask-WTF `CSRFProtect`) and set `SameSite=Lax` on the cookie.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-06. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-030
- **Title:** No audit trail: create, edit and delete actions are not recorded anywhere
- **Affected Feature:** F-08, F-10, F-13 (database has only `users`, `categories` and `tasks` tables)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` is logged in.
- **Steps to Reproduce:**
  1. Create a task, then delete it with `POST /tasks/1/delete`.
  2. Look in the database for any audit or activity log table.
- **Expected Result:** The delete is recorded with user id, action, task id and time.
- **Actual Result:** No audit table exists. A deleted task leaves no record, so the team cannot prove who deleted what (for example after D-025).
- **Severity:** Minor
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_10`)
- **Related Test Case:** `TC-SEC-10`, threat `TH-10` (Repudiation)
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-10. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-031
- **Title:** Debug mode is hard-coded on (`app.run(debug=True)`), which exposes the Werkzeug debugger and full error details
- **Affected Feature:** Server configuration (`app.py` line 482)
- **Environment:** Source code review of `app.py`; behaviour checked on the local copy only
- **Preconditions:** Read access to `app.py`.
- **Steps to Reproduce:**
  1. Open the last lines of `app.py`.
- **Expected Result:** Debug mode is off by default and can only be turned on for local development (for example through an environment variable).
- **Actual Result:** `app.run(debug=True)` is always on when the app is started with `python app.py`, which is how the team runs it. In that mode, any 500 error (such as D-006 or D-020) shows a full stack trace with code and file paths in the browser, and the interactive Werkzeug debugger can run code if someone can reach it.
- **Severity:** Major
- **Priority:** High
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_11`)
- **Related Test Case:** `TC-SEC-11`, threat `TH-11` (Information disclosure), asset A-07
- **Suggested Fix:** Read the debug setting from an environment variable that is off by default, and never run the development server in production.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-11. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-032
- **Title:** Logged-in pages send no `Cache-Control` header, so they can still be viewed with the Back button after logout
- **Affected Feature:** F-05 Logout, F-09 Task list, F-15 Dashboard
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` is logged in.
- **Steps to Reproduce:**
  1. Send `GET /dashboard` and read the response headers.
- **Expected Result:** The response includes `Cache-Control: no-store`, so the browser does not keep a copy.
- **Actual Result:** No `Cache-Control` header is sent. After logout, pressing Back can show the cached task list or dashboard on a shared computer (also seen as US-29 in Week 3).
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_12`)
- **Related Test Case:** `TC-SEC-12`, threat `TH-12` (Information disclosure), usability `US-29`, `TC-BB-067` (state transition, Week 7; logged as D-036, now closed as a duplicate)
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-12. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-033
- **Title:** Session cookie is missing the `SameSite` and `Secure` attributes
- **Affected Feature:** Session cookie behind F-06 Page protection and F-07 Endpoint protection (Flask cookie settings in `app.py`)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** None.
- **Steps to Reproduce:**
  1. Send `POST /register` with a new user.
  2. Read the `Set-Cookie` response header.
- **Expected Result:** The cookie has `HttpOnly`, `SameSite=Lax` (or `Strict`) and, when served over HTTPS, `Secure`.
- **Actual Result:** Only `HttpOnly` is set. Without `SameSite` the cookie is sent with cross-site requests (making D-029 possible), and without `Secure` it could be sent over plain HTTP.
- **Severity:** Moderate
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_15`)
- **Related Test Case:** `TC-SEC-15`, threat `TH-15` (Information disclosure)
- **Suggested Fix:** Set `SESSION_COOKIE_SAMESITE="Lax"` and, for HTTPS deployments, `SESSION_COOKIE_SECURE=True`.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-15. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-034
- **Title:** `GET /api/tasks` has no upper limit on `per_page`, so one request can return every task at once
- **Affected Feature:** F-18 List tasks (API) (`app.py` line 359)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` owns 25 tasks.
- **Steps to Reproduce:**
  1. Send `GET /api/tasks?per_page=1000`.
- **Expected Result:** The server caps the page size (for example at 20 or 100).
- **Actual Result:** All 25 tasks are returned. With many tasks, very large `per_page` values make the server load the whole table in one request, which wastes memory and time under load.
- **Severity:** Moderate
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_18`)
- **Related Test Case:** `TC-SEC-18`, threat `TH-18` (Denial of service)
- **Suggested Fix:** Use `per_page = min(max(per_page, 1), 100)`.
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-18. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-035
- **Title:** Logout works through a simple GET request, so any link or image on another site can log the user out
- **Affected Feature:** F-05 Logout (`app.py` line 179: `@app.route("/logout")` accepts GET)
- **Environment:** Python 3, pytest with Flask test client, isolated temporary SQLite database (local copy only)
- **Preconditions:** `syasya_test1` is logged in.
- **Steps to Reproduce:**
  1. Send `GET /logout` (as an `<img src>` on another page would).
- **Expected Result:** Logout requires a POST request with a CSRF token. `GET /logout` returns 405 and the session stays active.
- **Actual Result:** `GET /logout` clears the session and redirects (302) to `/login`.
- **Severity:** Minor
- **Priority:** Low
- **Status:** Confirmed
- **Evidence:** `05_Security_Performance/evidence_security.txt` (`test_sec_20`)
- **Related Test Case:** `TC-SEC-20`, threat `TH-20` (Denial of service)
- **Week 6 regression (25 Nov 2026):** Reproduced by 1 automated test(s): TC-SEC-20. Log: `06_Automation_Regression/logs/precheck_all_existing_tests.txt`.

### Defect ID: D-036
- **Title:** Back button after logout shows the previous task page from the browser cache
- **Affected Feature:** F-05 Logout (`app.py` has no `Cache-Control` header on authenticated pages)
- **Environment:** Browser, local copy (127.0.0.1)
- **Preconditions:** `qa_user1` is logged in on the task list.
- **Steps to Reproduce:**
  1. Click Log out.
  2. Press the browser Back button.
- **Expected Result:** The login page is shown, or the user is redirected to it. The old task list is not shown.
- **Actual Result:** Back returns to the previous page (the old task list), not the login page. We did not check whether actions on that page are refused. Not yet tested: step 4 of TC-BB-067 (click Dashboard or press F5).
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Closed (Duplicate of D-032)
- **Evidence:** `01_Black_Box/evidence/ST/st_check_output.txt` (no `Cache-Control`, `Expires` or `Pragma` header). Browser screenshot still to be added.
- **Related Test Case:** `TC-BB-067`
- **Suggested Fix:** Send `Cache-Control: no-store` on authenticated pages.
- **Week 7 review (26 Nov 2026):** Closed as a duplicate of **D-032**. Both describe the same bug: logged-in pages send no `Cache-Control` header, so the Back button shows a cached page after logout. Same root cause, same affected feature (F-05) and same fix (`Cache-Control: no-store`). D-036 was found by the state transition test `TC-BB-067`, which is now listed as a related test case of D-032. Rule used: the same rule as D-002 and D-003 (one root cause = one defect).
