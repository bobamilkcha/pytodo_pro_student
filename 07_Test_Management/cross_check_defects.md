# Week 7 Cross-Check - Defect IDs, Statuses and Counts

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Version:** 2,(Order 5 check of `master_test_repository.md`, `rtm.md` and the final defect log)
**Week 7 task:** 5. Check that every TC ID, defect ID and status matches across the repository, RTM and defect log.

## 1. How I checked

1. Compared the **status of every test ID** in `master_test_repository.md` with its source: the weekly files (`EP_Test_Cases.md`, `tc_bva.md`, `tc_defect_coordinator.md`, `tc_state_transition.md`, `gui_checklist.md`, `accessibility_findings.md`) and the real pytest results for the API, white-box and security tests (logs in `06_Automation_Regression/logs/`).
2. Compared the **test description** of each GUI, ACC and COMP row with the source file.
3. Compared every **defect ID, status and linked test** in `rtm.md` with `07_Test_Management/defect_log.md`.
4. Re-counted the **summary tables** against the rows below them.

**Result:** 178 test IDs could be checked automatically. All 79 API and UI-vs-API tests match pytest, and all BVA, decision table and state transition rows match. The problems are listed below.

## 2. Decision on D-036 (Defect & Metrics Coordinator)

**D-036 is `Closed (Duplicate of D-032)`** in the final defect log.

- D-036 (Back button after logout shows a cached page, `TC-BB-067`) and D-032 (no `Cache-Control` header, so Back shows cached pages after logout, `TC-SEC-12`, `US-29`) have the **same root cause, same feature (F-05) and same fix** (`Cache-Control: no-store`).
- Rule used: one root cause = one defect, the same rule as D-002 and D-003 (duplicates of D-001).
- `TC-BB-067` is now listed as a related test of **D-032**.
- Valid unique defects stay at **32**. Defect IDs logged: **36**. Duplicates: **3**.

## 3. `master_test_repository.md` (owner: Aida)

### 3.1 The file is cut off

The file ends in the middle of the `TC-API-UI-24` row (no Defect ID cell, no line ending). Missing:

| Missing part | Rows |
| :--- | :---: |
| `TC-API-UI-24` (last cell: `D-025`) and `TC-API-UI-25` to `TC-API-UI-30` | 7 |
| Week 5: `TC-SEC-01` to `TC-SEC-22` and `PERF-01` to `PERF-03` | 25 |
| Week 6: the 103 automated tests (or a pointer to `06_Automation_Regression/manual_to_automated_traceability.md`) | - |

The summary table in section 1.1 counts these, so the summary and the rows do not match. Correct results for the missing rows: `TC-API-UI-25`, `26`, `27` **Fail** (D-014, D-014, D-020); `28`, `29`, `30` **Pass**. Security: only `TC-SEC-13`, `16`, `22` **Pass**; the other 19 **Fail** (defects as in `security_test_cases.md`).

### 3.2 Test descriptions that do not match the source

For these IDs, the master repository describes a **different test** from the one in the Week 3 file. The ID must keep the meaning it had when it was executed, or the result and evidence no longer belong to it. Please copy the title and result from the source file for each row.

| ID | What the original test checks (Week 3 file) | What the master repository says |
| :--- | :--- | :--- |
| ACC-04 | Every control can be reached in a logical order. The focused control has a visible outline. | Urgency badges meet contrast requirements |
| ACC-06 | The error is shown in text and says what is wrong. | Keyboard Tab focus order follows logical reading order |
| ACC-13 | Enter activates the button. The confirm popup can be answered by keyboard. | Visible keyboard focus indicators on links, inputs, and buttons |
| ACC-14 | Every meaningful image has alt text. | Task list uses semantic `<table>` with `<thead>` and `<th>` headers |
| ACC-15 | Pages have a `<main>` region. Every table column has a header. | Error messages rendered in visible text on failed login/register |
| ACC-16 | Nothing flashes more than 3 times per second. | Navbar contrast at narrow widths (`320 px`) keeps `Log out` legible |
| GUI-03 | Submit invalid credentials and inspect error banner styling | Auth card centered layout and visual hierarchy |
| GUI-04 | Verify "Register" link below login button navigates to registration page | Top navigation bar links (`Tasks`, `Dashboard`, `Log out`) visibility and alignment |
| GUI-05 | Inspect label hints and submit an 8-character password matching the displayed hint | Task table column headers and row alignment |
| GUI-06 | Verify "Log in" link below registration form returns to login page | Color-coded urgency badges (`Overdue`, `Due Soon`, `Upcoming`, `Done`, `No due date`) |
| GUI-07 | Verify top navbar layout, contrast, and user context when logged in | Category dropdown and date picker rendering on task form |
| GUI-09 | Verify filter bar controls (category dropdown, status dropdown, search input, Filter button) | Dashboard 5-card grid alignment and typography |
| GUI-10 | Verify task table rows, done toggle (`○`/`✓`), urgency badges, and title text rendering | HTML tags in task title rendered as escaped text rather than raw HTML |
| GUI-12 | Verify form layout and visual alignment between Create Task button and Cancel link | Completed task row renders checkmark (`✓`) and strikethrough styling |
| GUI-13 | Submit New Task form with an empty Title field | HTML5 `required` validation tooltip appears on empty submission |
| GUI-14 | Open Edit Task and verify pre-filled values, Save Changes button, and Cancel link | Server validation error banner styling (`.error`) on invalid auth |
| GUI-15 | Verify 5 summary stat cards layout, typography, and semantic color coding | Filter bar dropdowns and search box layout on `/` |
| GUI-16 | Inspect responsive card grid behavior at narrow width (`375px` via Edge DevTools) | Cross-browser visual consistency across Chrome and Edge |
| GUI-17 | Click Log out in navbar and verify session termination and UI state | Whitespace-only task title creates blank-looking row in task table |
| GUI-18 | Click PyTodo Pro brand link while logged out | Long task title overflows/stretches table row height |

**COMP-01 to COMP-09:** in `compatibility_matrix.md` each COMP row is a **page** (Register, Log in, Log out, ...) checked on 5 configurations. In the master repository each COMP row is a **browser**. Please list them by page, as in the source.

### 3.3 Status errors

| Test ID | Master repository | Correct | Source / reason | Defect |
| :--- | :---: | :---: | :--- | :--- |
| `TC-BB-005` | Fail | **Pass** | `EP_Test_Cases.md`: empty title is blocked by `required`. The spaces-only title (D-011) is a different test (`US-11`, `WTS-VAL-03`, `TC-SEC-09`) | none |
| `GUI-05` | Pass | **Fail** | `gui_checklist.md`: 8-character password rejected although the hint says "min 8" | **D-004** |
| `GUI-17` | Fail | **Pass** | `gui_checklist.md`: Log out redirects and hides the navbar links | none |
| `GUI-18` | Fail | **Pass** | `gui_checklist.md`: brand link while logged out goes to `/login` | none |
| `ACC-10` | Pass | **Fail** | `accessibility_findings.md`: Lighthouse scores 72 to 95; 4 of 5 pages are below 90. The failed audits are the same problems as ACC-01, 03, 08, 11, 15 (D-009, D-015, D-018), so no separate defect | none |
| `ACC-15` | Pass | **Fail** | `accessibility_findings.md`: no `<main>` landmark (recommendation R-04, not logged as a defect) | none |
| `ACC-16` | Fail | **Pass** | `accessibility_findings.md`: nothing flashes | none (remove D-017) |

### 3.4 Summary table (section 1.1) after the fixes

| Row | Now | Should be |
| :--- | :---: | :---: |
| Equivalence Partitioning | 7 / 3 | **8 / 2** (`TC-BB-002`, `TC-BB-008` fail) |
| White-Box (28) | 25 / 3 | **24 / 4** (the rows already show 4 fails: `F11-11`, `F14-04`, `F14-10`, `F15-03`) |
| GUI Checklist (18) | 13 / 5 | **14 / 4** (`GUI-02`, `05`, `08`, `10` fail) |
| Accessibility (16) | 9 / 7 | **8 / 8** (`ACC-01`, `02`, `03`, `08`, `09`, `10`, `11`, `15` fail) |
| Usability (31) | 12 / 6 / 13 | The rows show 13 / 7 / 11. The source uses ratings, not Pass/Fail: **6 Good, 21 Minor issue, 4 Major issue**. Please report the ratings, or state the rule used to turn them into Pass/Fail |
| Week 6 automated suite | 103 / 69 / 34 | Correct (checked: 103 tests, 69 passed, 34 failed) |
| Total 389 | | The Week 6 automated tests re-run cases already counted in Weeks 1 to 5. Please show **unique test cases** and **automated runs** as two separate totals, so nothing is counted twice |

## 4. `rtm.md` (owner: Aida)

| # | Where | Now | Should be | Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Section 3, D-036 | Open *(Related to D-032)* | **Closed (Duplicate of D-032)** | Decision in section 2 |
| 2 | Section 3, D-032 | `US-29`, `TC-SEC-12` | add **`TC-BB-067`** | D-036 merged into D-032 |
| 3 | Section 3, D-004 | `TC-BB-BVA-F01-02`, `US-05`, `TC-API-UI-02` | add **`GUI-05`** | `GUI-05` failed because of D-004 |
| 4 | Section 3, D-011 | includes `TC-BB-005`, `GUI-17` | remove both | They passed and test other things (section 3.3) |
| 5 | Section 3, D-012 | includes `GUI-18` | remove | `GUI-18` passed and tests the brand link |
| 6 | Section 3, D-017; section 2.1 F-05 | includes `ACC-16` | remove | `ACC-16` passed (flashing content) |
| 7 | Section 3, D-027 and D-033 | linked to `F-04` | **`F-06`, `F-07`** (as in the final defect log) | A forged or weak session cookie defeats page and endpoint protection. Then F-06 and F-07 are **Failing**, not Passing, and the summary in section 1 changes to 0 passing in group 2.1 |

## 5. Other files

| # | File | Issue | Owner | Status |
| :--- | :--- | :--- | :--- | :---: |
| 1 | `06_Automation_Regression/execution_report.md` | Still 85 tests. With Syasya's `test_state_transition.py` (18 tests, all pass) it is **103 tests: 69 passed, 34 failed**; regression **51: 22 passed, 29 failed** | Nisrina | ☐ |
| 2 | `04_Web_API/web_test_scenarios.md` | `WTS-VAL-03` links `D-009` (form labels). It should be **`D-011`** (spaces-only title). Its screenshot `WTS-VAL-03.png` is still missing | Aida | ☐ |
| 3 | `03_Special_Testing/gui_checklist.md`, `01_Black_Box/EP_Test_Cases.md` | Source files still show `GUI-01` Fail and `TC-BB-002` Pass. The master repository has the correct values. Add a one-line note in each source file pointing to the master repository | Aida | ☐ |
| 4 | `02_White_Box_Coverage/Week2_Metrics.md` | Title said "(not done yet)"; `toggle_task` not recorded; F11-11 / F15-03 outcome not explained | Nafiesa | ☑ 26 Nov |
| 5 | `01_Black_Box/Week1_Metrics.md`, `tc_defect_coordinator.md`, `defect_log.md` | D-004 severity, TC-BB-F03-01 expected result, pointer to the final log | Nafiesa | ☑ 26 Nov |
| 6 | `01_Black_Box/tc_state_transition.md` | 20 cases now executed (19 Pass, 1 Fail) | Syasya | ☑ 26 Nov |
| 7 | `06_Automation_Regression/automation_candidates.md` | Syasya's file was overwritten by Nafiesa's upload on 26 Nov; restored from history | Nafiesa | ☐ |

## 6. Checks that passed

| Check | Result |
| :--- | :--- |
| Every `D-xxx` in the RTM exists in the final defect log | Pass (D-001 to D-036) |
| RTM statuses for D-001 to D-035 match the final defect log | Pass (35 of 35) |
| All 79 API and UI-vs-API rows match pytest | Pass |
| All BVA, decision table and state transition rows match their source | Pass (40 of 40) |
| D-007 `Closed (Not reproducible)` and `GUI-01` Pass | Pass |
| `TC-BB-002` Fail with D-013 in the master repository | Pass |
