# Week 7: Master Test Repository (`master_test_repository.md`)

**Prepared by:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro  
**Consolidation Scope:** All unique test cases, checks, and usability observations across **Weeks 1–5** (`286` unique items), plus **Week 6** automated regression execution runs (`103` automated runs across `10` scripts, reported separately below so re-executed cases are not double-counted).

---

## 1. Repository Summary & ID Reconciliation Log

### 1.1 Consolidated Test Inventory by Week & Technique

| Week | Folder | Technique / Test Type | Count | Passed | Failed | Ratings / Observations |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **Week 1** | `01_Black_Box` | Equivalence Partitioning (`TC-BB-001` to `010`) | 10 | 8 | 2 | 0 |
| **Week 1** | `01_Black_Box` | Boundary Value Analysis (`TC-BB-BVA-*`) | 8 | 5 | 3 | 0 |
| **Week 1** | `01_Black_Box` | Decision Table (`TC-BB-F03-*`, `F11-*`, `F14-*`) | 12 | 11 | 1 | 0 |
| **Week 1** | `01_Black_Box` | State Transition (`TC-BB-060` to `079`) | 20 | 19 | 1 | 0 |
| **Week 2** | `02_White_Box_Coverage` | White-Box Path & Branch Coverage (`TC-WB-*`) | 28 | 24 | 4 | 0 |
| **Week 3** | `03_Special_Testing` | GUI Checklist (`GUI-01` to `18`) | 18 | 14 | 4 | 0 |
| **Week 3** | `03_Special_Testing` | Cross-Browser & Device Compatibility (`COMP-01` to `09`) | 9 | 9 | 0 | 0 *(45/45 config results passed)* |
| **Week 3** | `03_Special_Testing` | Accessibility Testing (`ACC-01` to `16`) | 16 | 8 | 8 | 0 |
| **Week 3** | `03_Special_Testing` | Usability Evaluation (`US-01` to `31`) | 31 | — | — | **6 Good, 21 Minor issue, 4 Major issue** *(source ratings)* |
| **Week 4** | `04_Web_API` | End-to-End Web Workflows (`WTS-01` to `08`) | 8 | 8 | 0 | 0 |
| **Week 4** | `04_Web_API` | Client–Server Validation (`WTS-VAL-01` to `06`) | 6 | 1 | 5 | 0 |
| **Week 4** | `04_Web_API` | Core REST API Endpoints (`API-*`) | 55 | 43 | 12 | 0 |
| **Week 4** | `04_Web_API` | Extra Delete & Dashboard API (`API-DD-01` to `10`) | 10 | 6 | 4 | 0 |
| **Week 4** | `04_Web_API` | UI vs. API Parity Comparison (`TC-API-UI-01` to `30`) | 30 | 16 | 14 | 0 |
| **Week 5** | `05_Security_Performance` | STRIDE Security Tests (`TC-SEC-01` to `22`) | 22 | 3 | 19 | 0 |
| **Week 5** | `05_Security_Performance` | Locust Load & Performance Stages (`PERF-01` to `03`) | 3 | 2 | 0 | **1 Observation** (`PERF-03` Stage 3 P95 520 ms; `PERF-OBS-01/02`) |
| **Subtotal** | **Weeks 1–5** | **Unique Test Cases, Checks & Observations** | **286** | **177** | **77** | **31 Usability Ratings + 1 Performance Observation** |
| **Week 6** | `06_Automation_Regression` | Automated Regression & Verification Runs (`10` scripts) | **103** | **69** | **34** | Re-runs mapped cases from Weeks 1–5 (see Section 7) |

### 1.2 Duplicate & Inconsistent ID Fixes Applied (Order 1 & Order 5 Reconciliation)

| Issue Found Across Weeks 1–6 | Source File(s) | Resolution Applied in Master Repository |
| :--- | :--- | :--- |
| **Missing TC IDs for `completed_in_last_n_days`** | `02_White_Box_Coverage/test_helpers.py` | Assigned standardized IDs **`TC-WB-F15-01` through `TC-WB-F15-07`** in exact unit-test order mapped to Feature `F-15`. |
| **Missing TC IDs for Locust load stages** | `05_Security_Performance/performance_plan.md`, `performance_results.md` | Assigned standardized IDs **`PERF-01` (10 users)**, **`PERF-02` (50 users)**, and **`PERF-03` (100 users)**. |
| **Status conflict on `TC-BB-002` (Duplicate username)** | `01_Black_Box/EP_Test_Cases.md` vs `07_Test_Management/defect_log.md` | Updated status from `Pass` to **`Fail`** and linked to **`D-013`** (confirmed by `US-04`, `API-REG-09`, `TC-SEC-02`). |
| **Status separation on `TC-BB-005` (Empty title)** | `01_Black_Box/EP_Test_Cases.md` | Kept **`Pass`** (empty title blocked by HTML5 `required`); spaces-only title (`D-011`) is tested separately in `US-11`, `WTS-VAL-03`, and `TC-SEC-09`. |
| **Spec conflict on `TC-BB-F14-03` (1 day ahead)** | `01_Black_Box/tc_defect_coordinator.md` vs `EP_Test_Cases.md` | Kept distinct Decision Table ID `TC-BB-F14-03` (separate from `TC-BB-BVA-F14-*`) and standardized expected result to **`Due Soon`** per spec. |
| **State Transition execution & `D-036` duplicate rule** | `01_Black_Box/tc_state_transition.md`, `07_Test_Management/defect_log.md` | Recorded `19 Pass, 1 Fail` (`TC-BB-067` linked to **`D-032`**, with `D-036` closed as `Closed (Duplicate of D-032)`). |
| **Unreproducible defect `D-007` on `GUI-01`** | `03_Special_Testing/gui_checklist.md` vs `week6_defect_check.md` | Updated `GUI-01` to **`Pass`** and marked `D-007` as **`Closed (Not reproducible)`** after code and screenshot verification. |
| **Draft Defect IDs across Weeks 1, 4, and 5** | `tc_bva.md`, `web_test_scenarios.md`, `04_Web_API/defect_log.md`, `security_test_cases.md` | Standardized `DEF-001` → `D-001`; `DEF-API-01`/`03` → `D-019`; `DEF-API-02` → `D-013`; Week 4 draft `D-009` → `D-011`; Week 5 drafts `D-015`–`026` → `D-026`–`035`. |

---

## 2. Week 1: Black-Box Test Cases (`50` Cases)

### 2.1 Equivalence Partitioning (`TC-BB-001` to `TC-BB-010`, `10` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-BB-001` | F-01 | Black-Box (EP) | Register new user with valid username (`3–20` chars) and valid password (`9+` chars) | Pass | — |
| `TC-BB-002` | F-01 | Black-Box (EP) | Register with an already existing username (reconciled from Week 1 `Pass` to `Fail` per `D-013`) | Fail | D-013 |
| `TC-BB-003` | F-03 | Black-Box (EP) | Log in with valid username and incorrect password | Pass | — |
| `TC-BB-004` | F-08 | Black-Box (EP) | Create task with valid non-empty title, optional description, category, and due date | Pass | — |
| `TC-BB-005` | F-08 | Black-Box (EP) | Submit New Task form with empty title (`""` blocked by HTML5 `required` attribute) | Pass | — |
| `TC-BB-006` | F-14 | Black-Box (EP) | Urgency classification when due date is `None` or empty | Pass | — |
| `TC-BB-007` | F-14 | Black-Box (EP) | Urgency classification for past due date (`< today`) returns `Overdue` | Pass | — |
| `TC-BB-008` | F-14 | Black-Box (EP) | Urgency classification when due date equals `today` returns `Due Today` | Fail | D-001 |
| `TC-BB-009` | F-14 | Black-Box (EP) | Urgency classification for due date `1–2` days ahead returns `Due Soon` | Pass | — |
| `TC-BB-010` | F-14 | Black-Box (EP) | Urgency classification for due date `3+` days ahead returns `Upcoming` | Pass | — |

### 2.2 Boundary Value Analysis (`TC-BB-BVA-*`, `8` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-BB-BVA-F01-01` | F-01 | Black-Box (BVA) | Password just below minimum length (`7` characters) rejected | Pass | — |
| `TC-BB-BVA-F01-02` | F-01 | Black-Box (BVA) | Password at exact minimum boundary (`8` characters) accepted | Fail | D-004 |
| `TC-BB-BVA-F01-03` | F-01 | Black-Box (BVA) | Password just above minimum boundary (`9` characters) accepted | Pass | — |
| `TC-BB-BVA-F08-01` | F-08 | Black-Box (BVA) | Task title at `0` characters (empty) rejected | Pass | — |
| `TC-BB-BVA-F08-02` | F-08 | Black-Box (BVA) | Task title at `1` character (minimum non-empty boundary) accepted | Pass | — |
| `TC-BB-BVA-F14-01` | F-14 | Black-Box (BVA) | Task due yesterday (`today - 1 day`) displays `Overdue` | Pass | — |
| `TC-BB-BVA-F14-02` | F-14 | Black-Box (BVA) | Task due exact today (`today + 0 days`) displays `Due Today` (standardized from `DEF-001`) | Fail | D-001 |
| `TC-BB-BVA-F15-01` | F-15 | Black-Box (BVA) | Task completed exactly `7` days ago included in dashboard 7-day counter | Fail | D-005 |

### 2.3 Decision Table Testing (`TC-BB-F03-*`, `TC-BB-F11-*`, `TC-BB-F14-*`, `12` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-BB-F03-01` | F-03 | Black-Box (DT) | Login Rule 1: Existing user + correct password → authenticated session | Pass | — |
| `TC-BB-F03-02` | F-03 | Black-Box (DT) | Login Rule 2: Existing user + wrong password → generic error message | Pass | — |
| `TC-BB-F03-03` | F-03 | Black-Box (DT) | Login Rule 3: Non-existent user + valid password format → generic error message | Pass | — |
| `TC-BB-F03-04` | F-03 | Black-Box (DT) | Login Rule 4: Non-existent user + wrong password → generic error message | Pass | — |
| `TC-BB-F11-01` | F-11 | Black-Box (DT) | Filter Rule 1: No category, status, or search filter → shows all user's tasks | Pass | — |
| `TC-BB-F11-02` | F-11 | Black-Box (DT) | Filter Rule 2: Category + Status + Search keyword combined (`AND` logic) | Pass | — |
| `TC-BB-F11-03` | F-11 | Black-Box (DT) | Filter Rule 3: Status `done` filter only → shows completed tasks only | Pass | — |
| `TC-BB-F11-04` | F-11 | Black-Box (DT) | Filter Rule 4: Filter combination with zero matches → displays empty-state message | Pass | — |
| `TC-BB-F14-01` | F-14 | Black-Box (DT) | Urgency Rule 1: Open task with past due date → `Overdue` | Pass | — |
| `TC-BB-F14-02` | F-14 | Black-Box (DT) | Urgency Rule 2: Open task due today → `Due Today` | Fail | D-001 |
| `TC-BB-F14-03` | F-14 | Black-Box (DT) | Urgency Rule 3: Open task due tomorrow (`+1 day`) → `Due Soon` | Pass | — |
| `TC-BB-F14-04` | F-14 | Black-Box (DT) | Urgency Rule 4: Completed (`done=1`) task with past due date → `Done` | Pass | — |

### 2.4 State Transition Testing (`TC-BB-060` to `TC-BB-079`, `20` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-BB-060` | F-05 | Black-Box (ST) | Session transition (`S1`): Anonymous → Logged In via `/login` | Pass | — |
| `TC-BB-061` | F-05 | Black-Box (ST) | Session transition (`S2`): Anonymous → Logged In automatically via `/register` | Pass | — |
| `TC-BB-062` | F-05 | Black-Box (ST) | Session transition (`S6`): Logged In → Anonymous via `/logout` | Pass | — |
| `TC-BB-063` | F-05 | Black-Box (ST) | Session transition (`S7`): Logged In user logs in as another user via `/login` | Pass | — |
| `TC-BB-064` | F-05 | Black-Box (ST) | Session transition (`S3`): Anonymous → stays Anonymous on failed login | Pass | — |
| `TC-BB-065` | F-06 | Black-Box (ST) | Session guard (`S4`): Anonymous user redirected to `/login` on `/`, `/dashboard`, `/tasks/new` | Pass | — |
| `TC-BB-066` | F-05 | Black-Box (ST) | Repeated `/logout` request while already Anonymous (`S5`) redirects cleanly | Pass | — |
| `TC-BB-067` | F-05 | Black-Box (ST) | Browser Back button after `/logout` (`S8`) shows cached previous task page | Fail | D-032 *(D-036 dup)* |
| `TC-BB-068` | F-05 | Black-Box (ST) | Stale tab toggle action after logout (`S9`) is refused and redirects to `/login` | Pass | — |
| `TC-BB-069` | F-12 | Black-Box (ST) | Task transition (`T1`): `(None)` → `Open` upon creation (`completed_at` is `None`) | Pass | — |
| `TC-BB-070` | F-12 | Black-Box (ST) | Task transition (`T2`): `Open` → `Done` via `/tasks/<id>/toggle` sets `completed_at` | Pass | — |
| `TC-BB-071` | F-12 | Black-Box (ST) | Task transition (`T3`): `Done` → `Open` via `/tasks/<id>/toggle` clears `completed_at` | Pass | — |
| `TC-BB-072` | F-10 | Black-Box (ST) | Task transition (`T4`): Editing an `Open` task preserves `Open` state | Pass | — |
| `TC-BB-073` | F-10 | Black-Box (ST) | Task transition (`T5`): Editing a `Done` task preserves `Done` state | Pass | — |
| `TC-BB-074` | F-13 | Black-Box (ST) | Task transition (`T6`): `Open` → `Deleted` via `/tasks/<id>/delete` | Pass | — |
| `TC-BB-075` | F-13 | Black-Box (ST) | Task transition (`T7`): `Done` → `Deleted` updates dashboard counters | Pass | — |
| `TC-BB-076` | F-13 | Black-Box (ST) | Delete confirmation dialog Cancel (`T8`) keeps task in list as `Open` | Pass | — |
| `TC-BB-077` | F-12 | Black-Box (ST) | Toggle request on already `Deleted` task ID (`T9`) redirects safely without crash | Pass | — |
| `TC-BB-078` | F-10 | Black-Box (ST) | Edit request on already `Deleted` task ID (`T10`) redirects safely without crash | Pass | — |
| `TC-BB-079` | F-10 | Black-Box (ST) | Cross-user edit attempt (`T11`) leaves target user's task state unchanged | Pass | — |

---

## 3. Week 2: White-Box Unit & Route Coverage (`28` Cases)

### 3.1 `index()` Route White-Box Suite (`TC-WB-F11-01` to `TC-WB-F11-11`, `11` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-WB-F11-01` | F-06, F-09 | White-Box (Branch) | Unauthenticated `GET /` redirects to `/login` (`302`) | Pass | — |
| `TC-WB-F11-02` | F-09 | White-Box (Path) | Authenticated user with zero tasks renders empty task view | Pass | — |
| `TC-WB-F11-03` | F-09, F-11 | White-Box (Path) | Authenticated user with no filters sees all own tasks ordered by `id DESC` | Pass | — |
| `TC-WB-F11-04` | F-11 | White-Box (Branch) | Valid `category` query parameter filters by matching `category_id` | Pass | — |
| `TC-WB-F11-05` | F-11 | White-Box (Branch) | Unknown `category` parameter is ignored without error | Pass | — |
| `TC-WB-F11-06` | F-11 | White-Box (Branch) | `status=done` branch adds `AND done = 1` to query | Pass | — |
| `TC-WB-F11-07` | F-11 | White-Box (Branch) | `status=open` branch adds `AND done = 0` to query | Pass | — |
| `TC-WB-F11-08` | F-11 | White-Box (Branch) | Unknown `status` parameter is ignored without error | Pass | — |
| `TC-WB-F11-09` | F-11 | White-Box (Branch) | Search query `q` with no matching title returns empty task list | Pass | — |
| `TC-WB-F11-10` | F-11 | White-Box (Path) | Combined `category`, `status`, and `q` filters execute compound `AND` clause | Pass | — |
| `TC-WB-F11-11` | F-11 | White-Box (Edge) | Literal `%` in search `q` acts as unescaped SQL `LIKE` wildcard | Fail | D-014 |

### 3.2 `compute_urgency()` White-Box Suite (`TC-WB-F14-01` to `TC-WB-F14-10`, `10` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-WB-F14-01` | F-14 | White-Box (Branch) | `due_date_str=None` returns `"No due date"` | Pass | — |
| `TC-WB-F14-02` | F-14 | White-Box (Branch) | `due_date_str=""` returns `"No due date"` | Pass | — |
| `TC-WB-F14-03` | F-14 | White-Box (Branch) | `due < today` branch returns `"Overdue"` | Pass | — |
| `TC-WB-F14-04` | F-14 | White-Box (Boundary) | `due == today` hits `due <= today` branch (`"Overdue"`) instead of `"Due Today"` | Fail | D-001 |
| `TC-WB-F14-05` | F-14 | White-Box (Boundary) | `delta == 1` (`due == today + 1`) returns `"Due Soon"` | Pass | — |
| `TC-WB-F14-06` | F-14 | White-Box (Boundary) | `delta == 2` (`due == today + 2`) returns `"Due Soon"` | Pass | — |
| `TC-WB-F14-07` | F-14 | White-Box (Boundary) | `delta == 3` (`due == today + 3`) returns `"Upcoming"` | Pass | — |
| `TC-WB-F14-08` | F-14 | White-Box (Path) | Default `today=None` argument resolves `date.today()` properly | Pass | — |
| `TC-WB-F14-09` | F-14 | White-Box (Exception) | Malformed date string raises `ValueError` in `datetime.strptime` | Pass | — |
| `TC-WB-F14-10` | F-14, F-19 | White-Box (Integration) | Bad `due_date` saved via `POST /api/tasks` causes `500` crash on `GET /api/tasks` | Fail | D-006 |

### 3.3 `completed_in_last_n_days()` White-Box Suite (`TC-WB-F15-01` to `TC-WB-F15-07`, `7` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-WB-F15-01` | F-15 | White-Box (Path) | `test_completed_within_bounds`: Task completed `3` days ago returns `True` | Pass | — |
| `TC-WB-F15-02` | F-15 | White-Box (Boundary) | `test_completed_older_than_n_days`: Task completed `8` days ago returns `False` | Pass | — |
| `TC-WB-F15-03` | F-15 | White-Box (Boundary) | `test_completed_exactly_n_days_ago`: Reproduces `D-005` (exact `7` days returns `False` instead of `True`) | Fail | D-005 |
| `TC-WB-F15-04` | F-15 | White-Box (Branch) | `test_completed_in_future`: Future completion timestamp (`+1` day) returns `False` | Pass | — |
| `TC-WB-F15-05` | F-15 | White-Box (Exception) | `test_invalid_date_format`: Malformed `completed_at` string raises `ValueError` | Pass | — |
| `TC-WB-F15-06` | F-15 | White-Box (Branch) | `test_empty_date`: `completed_at=None` and `""` return `False` | Pass | — |
| `TC-WB-F15-07` | F-15 | White-Box (Path) | `test_completed_default_now`: Default `now=None` resolves `datetime.now()` properly | Pass | — |

---

## 4. Week 3: Special Testing — GUI, Compatibility, Accessibility & Usability (`74` Items)

### 4.1 GUI Checklist (`GUI-01` to `GUI-18`, `18` Items — `14` Pass, `4` Fail)

| TC ID | Feature | Technique | Test Scenario / Summary (from `03_Special_Testing/gui_checklist.md`) | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `GUI-01` | F-03 | Special (GUI) | Verify `.auth-card` container centering, padding, and input box alignment (re-verified Pass in W6; `D-007` closed) | Pass | D-007 *(Closed)* |
| `GUI-02` | F-03 | Special (GUI) | Click the `"Username"` label text to verify input focus behavior | Fail | D-009 |
| `GUI-03` | F-03 | Special (GUI) | Submit invalid credentials and inspect error banner styling | Pass | — |
| `GUI-04` | F-03 | Special (GUI) | Verify `"Register"` link below login button navigates to registration page | Pass | — |
| `GUI-05` | F-01 | Special (GUI) | Inspect label hints and submit an 8-character password matching the displayed hint | Fail | D-004 |
| `GUI-06` | F-01 | Special (GUI) | Verify `"Log in"` link below registration form returns to login page | Pass | — |
| `GUI-07` | F-05, F-06 | Special (GUI) | Verify top navbar layout, contrast, and user context when logged in | Pass | — |
| `GUI-08` | F-09 | Special (GUI) | Inspect empty-state table message when a user has 0 tasks and no filters selected | Fail | D-008 |
| `GUI-09` | F-11 | Special (GUI) | Verify filter bar controls (category dropdown, status dropdown, search input, Filter button) | Pass | — |
| `GUI-10` | F-09, F-12, F-14 | Special (GUI) | Verify task table rows, done toggle (`○`/`✓`), urgency badges, and title text rendering (`\|safe`) | Fail | D-010 |
| `GUI-11` | F-13 | Special (GUI) | Click **Delete** on a task row to verify destructive action confirmation | Pass | — |
| `GUI-12` | F-08 | Special (GUI) | Verify form layout and visual alignment between **Create Task** button and **Cancel** link | Pass | — |
| `GUI-13` | F-08 | Special (GUI) | Submit New Task form with an empty **Title** field | Pass | — |
| `GUI-14` | F-10 | Special (GUI) | Open Edit Task and verify pre-filled values, **Save Changes** button, and **Cancel** link | Pass | — |
| `GUI-15` | F-15 | Special (GUI) | Verify 5 summary stat cards layout, typography, and semantic color coding | Pass | — |
| `GUI-16` | F-15 | Special (GUI) | Inspect responsive card grid behavior at narrow width (`375px` via Edge DevTools) | Pass | — |
| `GUI-17` | F-05 | Special (GUI) | Click **Log out** in navbar and verify session termination and UI state | Pass | — |
| `GUI-18` | F-06 | Special (GUI) | Click **PyTodo Pro** brand link while logged out | Pass | — |

### 4.2 Compatibility Matrix (`COMP-01` to `COMP-09`, `9` Pages/Components across `5` Configurations = `45` Results)

| TC ID | Feature | Technique | Page / Component Tested (Chrome, Edge, Firefox, Galaxy A55, iPad Pro 13) | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `COMP-01` | F-01 | Special (Compat) | Register (`/register`) across all 5 browser and viewport configurations (`5/5 Pass`) | Pass | — |
| `COMP-02` | F-03 | Special (Compat) | Log in (`/login`) across all 5 browser and viewport configurations (`5/5 Pass`) | Pass | — |
| `COMP-03` | F-05 | Special (Compat) | Log out (`/logout`) across all 5 browser and viewport configurations (`5/5 Pass`) | Pass | — |
| `COMP-04` | F-05, F-06 | Special (Compat) | Navigation Bar (All logged-in pages) across all 5 configurations (`5/5 Pass`) | Pass | — |
| `COMP-05` | F-09, F-11 | Special (Compat) | Task List — Layout & Filters (`/`) across all 5 configurations (`5/5 Pass`) | Pass | — |
| `COMP-06` | F-12, F-13, F-14 | Special (Compat) | Task List — Controls & Popup (`/`) across all 5 configurations (`5/5 Pass`) | Pass | — |
| `COMP-07` | F-08 | Special (Compat) | New Task — Form & Date Picker (`/tasks/new`) across all 5 configurations (`5/5 Pass`) | Pass | — |
| `COMP-08` | F-10 | Special (Compat) | Edit Task (`/tasks/<id>/edit`) across all 5 configurations (`5/5 Pass`) | Pass | — |
| `COMP-09` | F-15 | Special (Compat) | Dashboard — Stat Cards (`/dashboard`) across all 5 configurations (`5/5 Pass`) | Pass | — |

### 4.3 Accessibility Checklist (`ACC-01` to `ACC-16`, `16` Items — `8` Pass, `8` Fail)

| TC ID | Feature | Technique | Test Scenario / Summary (from `03_Special_Testing/accessibility_findings.md`) | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `ACC-01` | F-01, F-03, F-08, F-10 | Special (A11y) | Click each form label; check whether the label is linked to its input (`for`/`id`) | Fail | D-009 |
| `ACC-02` | F-12 | Special (A11y) | Read the accessible name of the done toggle button (`○` / `✓`) | Fail | D-016 |
| `ACC-03` | F-09, F-12 | Special (A11y) | Measure text contrast of done task titles and the empty-list message (`>= 4.5:1`) | Fail | D-015 |
| `ACC-04` | All Pages | Special (A11y) | Every control can be reached in a logical Tab order and focused control has a visible outline | Pass | — |
| `ACC-05` | All Pages | Special (A11y) | Each page has its own unique browser tab `<title>` and one main `<h1>` heading | Pass | — |
| `ACC-06` | F-01 | Special (A11y) | Submit invalid username (`ab`) on Register; error is shown in text and says what is wrong | Pass | — |
| `ACC-07` | All Pages | Special (A11y) | `<html lang="en">` is set in `base.html` so screen readers use the right voice | Pass | — |
| `ACC-08` | F-11 | Special (A1y) | Check accessible names (`label`/`aria-label`) of category dropdown, status dropdown, and search box | Fail | D-009 |
| `ACC-09` | All Pages | Special (A11y) | Set window to `320 px` wide and check whether content reflows without sideways scrolling | Fail | D-017 |
| `ACC-10` | All Pages | Special (A11y) | Run Lighthouse accessibility audit on each page (scores: 85, 85, 72, 74, 95; avg 82.2) | Fail | — *(See ACC-01, 03, 08, 11, 15)* |
| `ACC-11` | F-10, F-13 | Special (A11y) | Measure click target size of Edit (`24×16 px`) and Delete (`39×15 px`) links (`>= 24×24 px`) | Fail | D-018 |
| `ACC-12` | F-14 | Special (A11y) | Check whether urgency badges convey meaning in text rather than colour alone | Pass | — |
| `ACC-13` | F-12, F-13 | Special (A11y) | Use done toggle and Delete confirm popup with keyboard only (`Enter` activates and answers) | Pass | — |
| `ACC-14` | All Pages | Special (A11y) | Check images across all pages for alt text | Pass | — |
| `ACC-15` | All Pages | Special (A11y) | Check pages for `<main>` landmark region and non-empty task table column headers | Fail | — *(Rec. R-04, not a defect)* |
| `ACC-16` | All Pages | Special (A11y) | Look for flashing or moving content (`> 3` flashes per second) across all pages | Pass | — |

### 4.4 Usability Evaluation (`US-01` to `US-31`, `31` Observations — `6` Good, `21` Minor issue, `4` Major issue)

*(Note: Usability observations in `03_Special_Testing/usability_observations.md` use qualitative ratings — `Good`, `Minor issue`, `Major issue` — rather than binary Pass/Fail.)*

| TC ID | Feature | Technique | Test Scenario / Summary | Source Rating | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `US-01` | F-01 | Special (Usability) | Finding the Register page link from the initial `/login` screen | Minor issue | — |
| `US-02` | F-01 | Special (Usability) | Clarity and visibility of inline hints under Username and Password fields | Minor issue | See US-05 (`D-004`) |
| `US-03` | F-01 | Special (Usability) | Error box feedback and field clearing after failed/successful registration | Minor issue | — |
| `US-04` | F-01 | Special (Usability) | Registering again with a username that already exists | Major issue | D-013 |
| `US-05` | F-01 | Special (Usability) | Misleading error message when entering an exact 8-character password | Major issue | D-004 |
| `US-06` | F-03 | Special (Usability) | Generic error feedback and username field clearing on failed login | Minor issue | — |
| `US-07` | F-03 | Special (Usability) | Visual and layout consistency between Login and Register pages | Good | — |
| `US-08` | F-03 | Special (Usability) | Password masking and HTML5 empty-field prevention on Login | Good | — |
| `US-09` | F-08 | Special (Usability) | Prominence of `+ New Task` button and Cancel navigation on task form | Good | — |
| `US-10` | F-08 | Special (Usability) | Absence of confirmation flash banner after creating a task | Minor issue | — |
| `US-11` | F-08 | Special (Usability) | Whitespace-only title, very long title, and past due date handling | Major issue | D-011, D-012 |
| `US-12` | F-08 | Special (Usability) | Required/optional field indicators and date format consistency | Minor issue | — |
| `US-13` | F-10 | Special (Usability) | Edit Task form layout consistency and pre-filled values | Good | — |
| `US-14` | F-10 | Special (Usability) | Silent redirect without message when opening `/tasks/9999/edit` | Minor issue | — |
| `US-15` | F-12 | Special (Usability) | Visual prominence and differentiation of stacked Edit and Delete links | Minor issue | — |
| `US-16` | F-12 | Special (Usability) | Circle toggle button (`○`) lacks tooltip, label, or column heading | Minor issue | — |
| `US-17` | F-12 | Special (Usability) | Immediate visual feedback when marking a task done and undoing | Good | — |
| `US-18` | F-14 | Special (Usability) | Task due today displays `"Overdue"` instead of `"Due Today"` | Major issue | D-001 |
| `US-19` | F-13 | Special (Usability) | Browser confirmation prompt on Delete (omits specific task title) | Minor issue | — |
| `US-20` | F-13 | Special (Usability) | Delete link styling identical to Edit link without danger color | Minor issue | — |
| `US-21` | F-13 | Special (Usability) | Absence of confirmation message after deleting a task | Minor issue | — |
| `US-22` | F-11 | Special (Usability) | Empty filter message shown even for new user with zero tasks | Minor issue | — |
| `US-23` | F-11 | Special (Usability) | Dropdowns auto-submit while search box requires clicking Filter; no Clear button | Minor issue | — |
| `US-24` | F-11 | Special (Usability) | Underscore `_` in search acts as single-character wildcard | Minor issue | D-014 |
| `US-25` | F-15 | Special (Usability) | Dashboard counter readability and inflated Overdue count (`D-001`) | Minor issue | See US-18 (`D-001`) |
| `US-26` | F-15 | Special (Usability) | Dashboard stat cards are not clickable links to filtered task views | Minor issue | — |
| `US-27` | F-05 | Special (Usability) | Visibility and consistent placement of `Log out` link in top navbar | Good | — |
| `US-28` | F-05 | Special (Usability) | Absence of `"You have been logged out."` message after logout | Minor issue | — |
| `US-29` | F-05 | Special (Usability) | Browser Back button after logout shows cached Dashboard page | Minor issue | D-032 *(D-036 dup)* |
| `US-30` | All Pages | Special (Usability) | Cross-page styling consistency (button colors, fonts, date formats) | Minor issue | — |
| `US-31` | All Pages | Special (Usability) | Brand link home routing and lack of active page indicator in navbar | Minor issue | — |

---

## 5. Week 4: Web Workflows & REST API Testing (`109` Items)

### 5.1 End-to-End Web Workflows (`WTS-01` to `WTS-08`, `8` Scenarios)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `WTS-01` | F-01, F-02, F-06 | Web E2E Workflow | New user registration (`GET /register` → `POST /register` → `GET /`) & auto-login | Pass | — |
| `WTS-02` | F-03, F-04 | Web E2E Workflow | Existing user login & session persistence across `/` and `/dashboard` | Pass | — |
| `WTS-03` | F-08, F-09, F-14 | Web E2E Workflow | End-to-end task creation and urgency badge classification | Pass | — |
| `WTS-04` | F-11 | Web E2E Workflow | Multi-criteria task filtering (`category`, `status`, `q`) and state retention | Pass | — |
| `WTS-05` | F-10 | Web E2E Workflow | Task modification via `/tasks/<id>/edit` and database persistence | Pass | — |
| `WTS-06` | F-12, F-15 | Web E2E Workflow | Task completion toggle and `/dashboard` counter synchronization | Pass | — |
| `WTS-07` | F-13 | Web E2E Workflow | Own task deletion and cross-user web route isolation | Pass | — |
| `WTS-08` | F-05, F-06 | Web E2E Workflow | Logout (`GET /logout`) and unauthenticated route redirect guard | Pass | — |

### 5.2 Client-Side vs. Server-Side Validation (`WTS-VAL-01` to `WTS-VAL-06`, `6` Checks)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `WTS-VAL-01` | F-01 | Web Validation | Bypass HTML5 attributes on `POST /register` with short username/password | Pass *(with D-004)* | D-004 |
| `WTS-VAL-02` | F-01 | Web Validation | Submit duplicate username on `POST /register` (no server uniqueness check) | Fail | D-013 |
| `WTS-VAL-03` | F-08, F-10 | Web Validation | Submit whitespace-only title on `POST /tasks/new` and `/tasks/<id>/edit` (reconciled from draft `D-009` to `D-011`) | Fail | D-011 |
| `WTS-VAL-04` | F-08, F-10 | Web Validation | Bypass `<input type="date">` and submit malformed `due_date` string | Fail | D-006 |
| `WTS-VAL-05` | F-08, F-10 | Web Validation | Submit non-existent `category_id=9999` on web task form | Fail | D-021 |
| `WTS-VAL-06` | F-13 | Web Validation | Direct `POST /tasks/<id>/delete` enforces `user_id` ownership (lacks CSRF token) | Fail | D-029 |

### 5.3 Core REST API Endpoints (`55` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `API-REG-01` | F-02 | API Testing | `POST /api/register` with valid username & password returns `201 Created` | Pass | — |
| `API-REG-02` | F-02 | API Testing | `POST /api/register` trims leading/trailing whitespace in username | Pass | — |
| `API-REG-03` | F-02 | API Testing | `POST /api/register` rejects username `< 3` chars with `400` | Pass | — |
| `API-REG-04` | F-02 | API Testing | `POST /api/register` rejects short password with `400` | Pass | — |
| `API-REG-05` | F-02 | API Testing | `POST /api/register` with missing `username` returns `400` | Pass | — |
| `API-REG-06` | F-02 | API Testing | `POST /api/register` with missing `password` returns `400` | Pass | — |
| `API-REG-07` | F-02 | API Testing | `POST /api/register` with empty JSON `{}` returns `400` | Pass | — |
| `API-REG-08` | F-02 | API Testing | `POST /api/register` with integer `username` crashes with `500 AttributeError` | Fail | D-019 |
| `API-REG-09` | F-02 | API Testing | `POST /api/register` with duplicate username returns `201` instead of `400`/`409` | Fail | D-013 |
| `API-LOG-01` | F-04 | API Testing | `POST /api/login` with valid credentials returns `200 OK` and sets session | Pass | — |
| `API-LOG-02` | F-04 | API Testing | `POST /api/login` with wrong password returns `401 invalid credentials` | Pass | — |
| `API-LOG-03` | F-04 | API Testing | `POST /api/login` with non-existent username returns `401` | Pass | — |
| `API-LOG-04` | F-04 | API Testing | `POST /api/login` with missing `password` returns `401` | Pass | — |
| `API-LOG-05` | F-04 | API Testing | `POST /api/login` with empty JSON `{}` returns `401` | Pass | — |
| `API-LOG-06` | F-04 | API Testing | `POST /api/login` with integer `username` crashes with `500 AttributeError` | Fail | D-019 |
| `API-LOG-07` | F-04 | API Testing | `POST /api/login` with non-JSON plain text body returns `401` | Pass | — |
| `API-CAT-01` | F-17 | API Testing | Unauthenticated `GET /api/categories` returns `200 OK` with category list | Pass | — |
| `API-CAT-02` | F-17 | API Testing | `GET /api/categories` returns categories sorted alphabetically | Pass | — |
| `API-CAT-03` | F-17 | API Testing | Unsupported `POST /api/categories` returns `405 Method Not Allowed` | Pass | — |
| `API-TSK-GETALL-01` | F-18 | API Testing | Authenticated `GET /api/tasks` returns user's tasks ordered by `id DESC` | Pass | — |
| `API-TSK-GETALL-02` | F-18 | API Testing | `GET /api/tasks` filters by `category`, `status`, `q`, `page`, and `per_page` | Pass | — |
| `API-TSK-GETALL-03` | F-18 | API Testing | `GET /api/tasks?q=' OR '1'='1` returns `200 OK` `[]` | Pass | — |
| `API-TSK-GETALL-04` | F-18 | API Testing | `GET /api/tasks?q=test'` causes `500 sqlite3.OperationalError` (SQL injection) | Fail | D-020 |
| `API-TSK-GETALL-05` | F-07, F-18 | API Testing | Unauthenticated `GET /api/tasks` returns `401 authentication required` | Pass | — |
| `API-TSK-GETALL-06` | F-18 | API Testing | Non-integer `page`/`per_page` safely defaults to `0` and `10` | Pass | — |
| `API-TSK-GETALL-07` | F-18 | API Testing | Out-of-range `page=99` returns `200 OK` `[]` | Pass | — |
| `API-TSK-GETONE-01` | F-20 | API Testing | Authenticated `GET /api/tasks/<own_id>` returns `200 OK` task object | Pass | — |
| `API-TSK-GETONE-02` | F-20 | API Testing | `GET /api/tasks/99999` returns `404 not found` | Pass | — |
| `API-TSK-GETONE-03` | F-07, F-20 | API Testing | Unauthenticated `GET /api/tasks/1` returns `401 authentication required` | Pass | — |
| `API-TSK-GETONE-04` | F-20 | API Testing | Non-integer `GET /api/tasks/abc` returns `404 Not Found` | Pass | — |
| `API-TSK-GETONE-05` | F-20 | API Testing | Cross-user `GET /api/tasks/<other_id>` blocked with `404 not found` | Pass | — |
| `API-TSK-POST-01` | F-19 | API Testing | `POST /api/tasks` with all valid fields returns `201 Created` | Pass | — |
| `API-TSK-POST-02` | F-19 | API Testing | `POST /api/tasks` with minimal `title` only applies defaults and returns `201` | Pass | — |
| `API-TSK-POST-03` | F-19 | API Testing | `POST /api/tasks` with whitespace-only `title` returns `400 title is required` | Pass | — |
| `API-TSK-POST-04` | F-19 | API Testing | `POST /api/tasks` with malformed `due_date` crashes with `500 ValueError` | Fail | D-006 |
| `API-TSK-POST-05` | F-19 | API Testing | `POST /api/tasks` omitting `title` returns `400 title is required` | Pass | — |
| `API-TSK-POST-06` | F-07, F-19 | API Testing | Unauthenticated `POST /api/tasks` returns `401 authentication required` | Pass | — |
| `API-TSK-POST-07` | F-19 | API Testing | `POST /api/tasks` with integer `title` crashes with `500 AttributeError` | Fail | D-019 |
| `API-TSK-POST-08` | F-19 | API Testing | `POST /api/tasks` accepts non-existent `category_id=9999` (`201 Created`) | Fail | D-021 |
| `API-TSK-PUT-01` | F-21 | API Testing | `PUT /api/tasks/<id>` updates `title` and `due_date` (`200 OK`) | Pass | — |
| `API-TSK-PUT-02` | F-21 | API Testing | `PUT /api/tasks/<id>` toggles `done: true` / `false` and updates `completed_at` | Pass | — |
| `API-TSK-PUT-03` | F-21 | API Testing | `PUT /api/tasks/<id>` accepts empty `title: ""` and overwrites title (`200 OK`) | Fail | D-022 |
| `API-TSK-PUT-04` | F-21 | API Testing | `PUT /api/tasks/99999` returns `404 not found` | Pass | — |
| `API-TSK-PUT-05` | F-21 | API Testing | `PUT /api/tasks/<id>` with empty `{}` preserves existing fields (`200 OK`) | Pass | — |
| `API-TSK-PUT-06` | F-21 | API Testing | `PUT /api/tasks/<id>` with string `"done": "false"` marks task `done: true` | Fail | D-023 |
| `API-TSK-PUT-07` | F-21 | API Testing | Cross-user `PUT /api/tasks/<other_id>` blocked with `404 not found` | Pass | — |
| `API-TSK-DEL-01` | F-22 | API Testing | `DELETE /api/tasks/<own_id>` deletes task and returns `200 {"result": "ok"}` | Pass | — |
| `API-TSK-DEL-02` | F-22 | API Testing | `DELETE /api/tasks/99999` returns `200` instead of `404 not found` | Fail | D-024 |
| `API-TSK-DEL-03` | F-07, F-22 | API Testing | Unauthenticated `DELETE /api/tasks/1` returns `401 authentication required` | Pass | — |
| `API-TSK-DEL-04` | F-22 | API Testing | Non-integer `DELETE /api/tasks/abc` returns `404 Not Found` | Pass | — |
| `API-TSK-DEL-05` | F-22 | API Testing | Cross-user `DELETE /api/tasks/<other_id>` succeeds (`200`) and deletes victim's task | Fail | D-025 |
| `API-DASH-01` | F-16 | API Testing | `GET /api/dashboard` counts task due today as `overdue` instead of `due_soon` | Fail | D-001 |
| `API-DASH-02` | F-16 | API Testing | `GET /api/dashboard` for user with 0 tasks returns all zeros (`200 OK`) | Pass | — |
| `API-DASH-03` | F-07, F-16 | API Testing | Unauthenticated `GET /api/dashboard` returns `401 authentication required` | Pass | — |
| `API-DASH-04` | F-16 | API Testing | Unsupported `POST /api/dashboard` returns `405 Method Not Allowed` | Pass | — |

### 5.4 Extra Delete & Dashboard API Cases (`API-DD-01` to `API-DD-10`, `10` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `API-DD-01` | F-22 | API Security (IDOR) | Verify User A's task returns `404` after User B executes `DELETE /api/tasks/<id>` | Fail | D-025 |
| `API-DD-02` | F-22 | API Invalid Input | Deleting the same task ID twice returns `200` both times instead of `404` | Fail | D-024 |
| `API-DD-03` | F-22, F-16 | API Functional | Deleting 1 of 2 tasks decrements `GET /api/dashboard` `total` from `2` to `1` | Pass | — |
| `API-DD-04` | F-16 | API Isolation | `GET /api/dashboard` counts only authenticated user's own tasks | Pass | — |
| `API-DD-05` | F-16 | API Functional | Completed task with past due date is not counted as `overdue` | Pass | — |
| `API-DD-06` | F-16 | API (BVA) | Due Soon upper boundary: `today + 2` counted in `due_soon`, `today + 3` excluded | Pass | — |
| `API-DD-07` | F-16 | API (BVA) | Overdue/Due Soon boundary: `today - 1` is `overdue`, `today + 1` is `due_soon` | Pass | — |
| `API-DD-08` | F-16 | API (BVA) | Task completed exactly `7` days ago excluded (`completed_this_week: 0`) | Fail | D-005 |
| `API-DD-09` | F-16 | API (BVA) | Task completed `8` days ago properly excluded (`completed_this_week: 0`) | Pass | — |
| `API-DD-10` | F-16 | API Edge Case | Task with malformed `due_date` causes `GET /api/dashboard` to return `500` | Fail | D-006 |

### 5.5 UI vs. API Parity Comparison (`TC-API-UI-01` to `TC-API-UI-30`, `30` Cases)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-API-UI-01` | F-01, F-02 | UI vs API Parity | 7-character password rejected in both UI and API | Pass | — |
| `TC-API-UI-02` | F-01, F-02 | UI vs API Parity | 8-character password rejected in both UI and API | Fail | D-004 |
| `TC-API-UI-03` | F-01, F-02 | UI vs API Parity | 9-character password accepted in both UI and API | Pass | — |
| `TC-API-UI-04` | F-01, F-02 | UI vs API Parity | Duplicate username accepted in both UI and API | Fail | D-013 |
| `TC-API-UI-05` | F-01, F-02 | UI vs API Parity | 2-character username (`ab`) rejected in both UI and API | Pass | — |
| `TC-API-UI-06` | F-02 | UI vs API Parity | Numeric username (`12345`) crashes API with `500` | Fail | D-019 |
| `TC-API-UI-07` | F-03, F-04 | UI vs API Parity | Empty password on login rejected in both UI and API | Pass | — |
| `TC-API-UI-08` | F-03, F-04 | UI vs API Parity | Wrong password on login rejected with generic error in both | Pass | — |
| `TC-API-UI-09` | F-08, F-19 | UI vs API Parity | Empty task title (`""`) rejected in UI (browser) and API (`400`) | Pass | — |
| `TC-API-UI-10` | F-08, F-19 | UI vs API Parity | Whitespace-only title rejected by API (`400`), accepted by UI (`D-011`) | Pass *(API)* | D-011 |
| `TC-API-UI-11` | F-08, F-19 | UI vs API Parity | 1-character title (`"A"`) accepted in both UI and API | Pass | — |
| `TC-API-UI-12` | F-08, F-19 | UI vs API Parity | 500-character title accepted without length cap in both UI and API | Fail | D-012 |
| `TC-API-UI-13` | F-14 | UI vs API Parity | Past due date (`today - 30d`) shows `Overdue` in both UI and API | Pass | — |
| `TC-API-UI-14` | F-14 | UI vs API Parity | Task due today shows `Overdue` instead of `Due Today` in both | Fail | D-001 |
| `TC-API-UI-15` | F-19 | UI vs API Parity | Malformed date (`04-11-2026`) causes `500` crash in API | Fail | D-006 |
| `TC-API-UI-16` | F-19 | UI vs API Parity | Non-existent `category_id=999` accepted by API (`201`) | Fail | D-021 |
| `TC-API-UI-17` | F-10, F-21 | UI vs API Parity | Edit non-existent task ID (`404` in API, silent redirect in UI) | Pass | — |
| `TC-API-UI-18` | F-21 | UI vs API Parity | Edit task with empty title accepted by API (`200`), blocked in browser | Fail | D-022 |
| `TC-API-UI-19` | F-10, F-21 | UI vs API Parity | Cross-user edit blocked in both UI and API (`404`) | Pass | — |
| `TC-API-UI-20` | F-12, F-21 | UI vs API Parity | Toggle `done` sets `completed_at` and reopen clears it in both | Pass | — |
| `TC-API-UI-21` | F-12, F-21 | UI vs API Parity | Toggle non-existent task ID handled cleanly (`404` API / redirect UI) | Pass | — |
| `TC-API-UI-22` | F-21 | UI vs API Parity | `done: "false"` string completes task in API (`200`) | Fail | D-023 |
| `TC-API-UI-23` | F-22 | UI vs API Parity | Delete non-existent task ID returns `200` in API instead of `404` | Fail | D-024 |
| `TC-API-UI-24` | F-13, F-22 | UI vs API Parity | Cross-user delete blocked in UI, succeeds (`200`) in API | Fail | D-025 |
| `TC-API-UI-25` | F-11, F-18 | UI vs API Parity | Underscore `_` in search acts as wildcard in both UI and API | Fail | D-014 |
| `TC-API-UI-26` | F-11, F-18 | UI vs API Parity | Percent `%` in search acts as wildcard in both UI and API | Fail | D-014 |
| `TC-API-UI-27` | F-11, F-18 | UI vs API Parity | Single quote `a'` in search causes `500` SQL error in API only | Fail | D-020 |
| `TC-API-UI-28` | F-06, F-07 | UI vs API Parity | Unauthenticated task creation blocked in both UI (`302`) and API (`401`) | Pass | — |
| `TC-API-UI-29` | F-06, F-07 | UI vs API Parity | Unauthenticated task edit blocked in both UI (`302`) and API (`401`) | Pass | — |
| `TC-API-UI-30` | F-06, F-07 | UI vs API Parity | Unauthenticated task deletion blocked in both UI (`302`) and API (`401`) | Pass | — |

---

## 6. Week 5: Security & Performance Testing (`25` Items)

### 6.1 STRIDE Security Test Cases (`TC-SEC-01` to `TC-SEC-22`, `22` Cases — `3` Pass, `19` Fail)

*(Note: `Fail` indicates the STRIDE vulnerability was confirmed on the local environment and logged in `07_Test_Management/defect_log.md`; `Pass` indicates the security control prevented the attack.)*

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `TC-SEC-01` | F-03 | Security (STRIDE `TH-01`) | Login brute-force protection across 10 consecutive failed `POST /login` attempts | Fail | D-026 |
| `TC-SEC-02` | F-01 | Security (STRIDE `TH-02`) | Duplicate username registration prevention on `POST /register` | Fail | D-013 |
| `TC-SEC-03` | F-04 | Security (STRIDE `TH-03`) | Session cookie forgery using hardcoded `SECRET_KEY` in `app.py` | Fail | D-027 |
| `TC-SEC-04` | F-05 | Security (STRIDE `TH-04`) | Server-side session cookie invalidation after `GET /logout` | Fail | D-028 |
| `TC-SEC-05` | F-08, F-09 | Security (STRIDE `TH-05`) | Stored XSS escaping for `<script>alert(1)</script>` in task title on `/` | Fail | D-010 |
| `TC-SEC-06` | F-08, F-10, F-13 | Security (STRIDE `TH-06`) | Anti-CSRF token verification on state-changing web forms | Fail | D-029 |
| `TC-SEC-07` | F-18 | Security (STRIDE `TH-07`) | SQL injection syntax handling for `GET /api/tasks?q=a'` | Fail | D-020 |
| `TC-SEC-08` | F-11 | Security (STRIDE `TH-08`) | Literal `%` wildcard escaping in web search `GET /?q=%` | Fail | D-014 |
| `TC-SEC-09` | F-08 | Security (STRIDE `TH-09`) | Server-side rejection of whitespace-only title on `POST /tasks/new` | Fail | D-011 |
| `TC-SEC-10` | F-13 | Security (STRIDE `TH-10`) | Database audit trail verification upon task deletion | Fail | D-030 |
| `TC-SEC-11` | NFR-02 | Security (STRIDE `TH-11`) | Inspection of `app.py` for hardcoded `app.run(debug=True)` | Fail | D-031 |
| `TC-SEC-12` | F-05, F-09, F-15 | Security (STRIDE `TH-12`) | `Cache-Control: no-store` header verification on authenticated pages | Fail | D-032 |
| `TC-SEC-13` | F-01 | Security (STRIDE `TH-13`) | Password cryptographic hashing (`scrypt:`/`pbkdf2:`) in `users` table | Pass | — |
| `TC-SEC-14` | F-18 | Security (STRIDE `TH-14`) | Boolean SQL injection (`' OR 1=1 --`) cross-user isolation check | Fail | D-020 |
| `TC-SEC-15` | F-04 | Security (STRIDE `TH-15`) | Session cookie `HttpOnly`, `SameSite`, and `Secure` flags check | Fail | D-033 |
| `TC-SEC-16` | F-17 | Security (STRIDE `TH-16`) | Unauthenticated `GET /api/categories` exposes no user data | Pass | — |
| `TC-SEC-17` | F-08, F-09 | Security (STRIDE `TH-17`) | Malformed `due_date` (`04-11-2026`) DoS check on `GET /` | Fail | D-006 |
| `TC-SEC-18` | F-18 | Security (STRIDE `TH-18`) | Upper bound cap on `GET /api/tasks?per_page=1000` | Fail | D-034 |
| `TC-SEC-19` | F-04 | Security (STRIDE `TH-19`) | Burst request throttling across 20 sequential `POST /api/login` calls | Fail | D-026 |
| `TC-SEC-20` | F-05 | Security (STRIDE `TH-20`) | HTTP method enforcement requiring `POST` rather than `GET /logout` | Fail | D-035 |
| `TC-SEC-21` | F-22 | Security (STRIDE `TH-21`) | Cross-user IDOR delete check on `DELETE /api/tasks/<id>` | Fail | D-025 |
| `TC-SEC-22` | F-10, F-12, F-13 | Security (STRIDE `TH-22`) | Cross-user access control across web `/edit`, `/toggle`, and `/delete` | Pass | — |

### 6.2 Locust Load & Performance Stages (`PERF-01` to `PERF-03`, `3` Stages)

| TC ID | Feature | Technique | Test Scenario / Summary | Status | Linked Defect / Obs |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `PERF-01` | F-02, F-04, F-16–F-22 | Performance (Load) | Stage 1 Baseline: `10` concurrent users (`221` reqs, `24 ms` avg, `140 ms` P95, `0.00%` errors) | Pass | — |
| `PERF-02` | F-02, F-04, F-16–F-22 | Performance (Load) | Stage 2 Moderate: `50` concurrent users (`1,073` reqs, `47 ms` avg, `310 ms` P95, `0.00%` errors) | Pass | — |
| `PERF-03` | F-02, F-04, F-16–F-22 | Performance (Load) | Stage 3 High Load: `100` concurrent users (`2,122` reqs, `95 ms` avg, `520 ms` P95, `0.00%` errors) | Observation | `PERF-OBS-01`, `PERF-OBS-02` |

---

## 7. Week 6: Automated Regression & Verification Runs (`103` Automated Runs across `10` Scripts)

All 103 automated test runs in `06_Automation_Regression/tests/` (`69 Passed`, `34 Failed`, `0 Errors`) re-execute cases from Weeks 1–5 and map one-to-one in `06_Automation_Regression/manual_to_automated_traceability.md`.

| Script File | Layer | Automated Runs | `@pytest.mark.regression` | Passed | Failed | Defects Caught |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `tests/unit/test_bva_unit.py` | PyTest Unit | 3 | 1 | 2 | 1 | `D-004` |
| `tests/unit/test_ep_urgency_unit.py` | PyTest Unit | 6 | 1 | 5 | 1 | `D-001` |
| `tests/unit/test_reg_decision_table.py` | PyTest Unit / Route | 19 | 13 | 13 | 6 | `D-001`, `D-004` |
| `tests/api/test_api_auth.py` | PyTest API | 18 | 2 | 15 | 3 | `D-013`, `D-019` |
| `tests/api/test_ep_and_core_api.py` | PyTest API / Route | 13 | 9 | 4 | 9 | `D-006`, `D-009`, `D-010`, `D-011`, `D-016`, `D-017`, `D-020`, `D-022`, `D-025` |
| `tests/api/test_reg_api_delete_dashboard.py` | PyTest API | 10 | 7 | 6 | 4 | `D-005`, `D-006`, `D-024`, `D-025` |
| `tests/api/test_state_transition.py` | PyTest API / Route | 18 | 6 | 18 | 0 | — |
| `tests/ui/test_ui_auth.py` | Selenium Browser UI | 1 | 0 | 1 | 0 | — |
| `tests/ui/test_ui_tasks.py` | Selenium Browser UI | 1 | 0 | 1 | 0 | — |
| `tests/ui/test_reg_accessibility_markup.py` | PyTest HTML/CSS | 14 | 12 | 4 | 10 | `D-008`, `D-009`, `D-015`, `D-016`, `D-017` |
| **Total Automated Runs** | **All Layers** | **103** | **51** | **69** | **34** | **16 Unique Defects Confirmed** |