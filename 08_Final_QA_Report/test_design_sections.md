# Final Report Sections: Test Design Coordinator (Aida)

**Date:** 26 Nov 2026
**For:** `08_Final_QA_Report/final_qa_report.md` (QA/Test Lead integrates)
**Sources:** `03_Special_Testing/usability_observations.md`, `04_Web_API/` (`web_test_scenarios.md`, `api_test_cases.md`, `ui_vs_api_comparison.md`), `07_Test_Management/` (`master_test_repository.md`, `rtm.md`, `defect_log.md`), and `08_Final_QA_Report/metrics.md`.

---

## 3.3 REST API and Usability Evidence Consolidation (Order 3b)

### A. REST API and UI-vs-API Parity Evidence (Week 4)

#### 1. What We Tested and Execution Results
In Week 4, we evaluated PyTodo Pro's seven REST API endpoints (`F-02`, `F-04`, `F-07`, `F-16` to `F-22`) alongside end-to-end web workflows and client-server validation rules (`109` total Week 4 items in `master_test_repository.md`, including the **`95` automated API and parity test cases** summarized in `metrics.md`):

| Week 4 Test Suite | Scope / Endpoints Covered | Executed | Passed | Failed | Pass Rate | Linked Defects |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Core REST API (`API-*`)** | `POST /api/register`, `POST /api/login`, `GET /api/categories`, `GET/POST/PUT/DELETE /api/tasks`, `GET /api/dashboard` | 55 | 43 | 12 | 78.2% | `D-001`, `D-006`, `D-013`, `D-019`–`D-025` |
| **Extra Delete & Dashboard (`API-DD-01`–`10`)** | IDOR delete checks, duplicate delete status, dashboard boundary counters & malformed dates | 10 | 6 | 4 | 60.0% | `D-005`, `D-006`, `D-024`, `D-025` |
| **UI vs. API Parity (`TC-API-UI-01`–`30`)** | Side-by-side validation, boundary, ownership, and error-handling comparison across web & API | 30 | 16 | 14 | 53.3% | `D-001`, `D-004`, `D-006`, `D-011`–`D-014`, `D-016`, `D-019`–`D-025` |
| **Subtotal (Automated API & Parity Suite)** | **Matches `metrics.md` Section 1.1 Week 4 row** | **95** | **65** | **30** | **68.4%** | **14 unique defects confirmed** |
| **Web E2E Workflows (`WTS-01`–`08`)** | Happy-path multi-step browser flows (register, login, create, filter, edit, toggle, delete, logout) | 8 | 8 | 0 | 100.0% | — |
| **Client–Server Validation (`WTS-VAL-01`–`06`)** | Bypassing HTML5 attributes on web forms (`required`, `type="date"`, category IDs, delete CSRF) | 6 | 1 | 5 | 16.7% | `D-004`, `D-006`, `D-011`, `D-013`, `D-021`, `D-029` |

Only two API requirements passed all tests with zero open defects: **`F-17` (`GET /api/categories`)** and **`F-20` (`GET /api/tasks/<id>`)**. The remaining four API endpoints (`F-18`, `F-19`, `F-21`, `F-22`), API authentication (`F-02`, `F-04`, `F-07`), and API dashboard (`F-16`) all failed due to open validation, authorization, or business-logic defects.

#### 2. Key Patterns Found in the API Evidence
1. **Severe Rule Divergence Between Web Routes and REST API Endpoints:**  
   PyTodo Pro implements validation and access checks separately for web forms and JSON endpoints rather than sharing server-side helpers:
   - **Broken Object-Level Authorization (`D-025`, Critical):** `POST /tasks/<id>/delete` verifies `user_id` ownership, whereas `DELETE /api/tasks/<id>` executes `DELETE FROM tasks WHERE id = ?` without checking `user_id`, allowing any logged-in user to delete another user's task (`API-TSK-DEL-05`, `API-DD-01`).
   - **SQL Injection in API Search (`D-020`, Critical):** Web search uses parameterized queries, whereas `GET /api/tasks?q=` interpolates user input directly into SQL, causing `500 sqlite3.OperationalError` on unescaped quotes (`API-TSK-GETALL-04`, `TC-API-UI-27`).
   - **Contradictory Title Validation (`D-011` vs. `D-022`):** `POST /api/tasks` properly strips whitespace and rejects empty titles (`400`, `API-TSK-POST-03`), whereas `POST /tasks/new` accepts whitespace-only titles (`D-011`). Conversely, `PUT /api/tasks/<id>` allows overwriting an existing task's title with an empty string `""` (`D-022`, `API-TSK-PUT-03`).
2. **Unhandled Data-Type and Schema Errors (`HTTP 500` Crashes):**  
   The JSON API assumes callers send well-formed strings and booleans:
   - Sending non-string JSON types (such as integer `username: 12345` or integer `title`) raises uncaught `AttributeError` `500` responses across `/api/register`, `/api/login`, and `/api/tasks` (`D-019`).
   - Submitting a malformed `due_date` (e.g., `"04-11-2026"`) succeeds in `POST /api/tasks` (`500` on validation or stored invalid string) and subsequently crashes `GET /api/tasks` and `GET /api/dashboard` with `500 ValueError` (`D-006`).
   - Non-existent foreign keys (`category_id=9999`) are accepted without validation (`D-021`), sending string `"done": "false"` evaluates as truthy `True` (`D-023`), and `DELETE /api/tasks/99999` returns `200 OK` instead of `404 Not Found` (`D-024`).
3. **Shared Helper Defects Propagate Across Both Layers:**  
   Logic defects in `helpers.py`—classifying tasks due today as `"Overdue"` (`D-001`), rejecting valid 8-character passwords (`D-004`), and excluding day 7 from `completed_this_week` (`D-005`)—along with missing database `UNIQUE` constraints on usernames (`D-013`), fail identically in both the web interface and the REST API.

#### 3. Limitations of Our API Testing
- All API tests were executed locally against the Flask test client/development server using functional single-user and two-user payloads; we did not test concurrent race conditions (e.g., simultaneous `PUT`/`DELETE` requests), large paginated datasets (`> 100` tasks), or malformed `Content-Type` headers and oversized JSON payloads.

---

### B. Usability Evaluation Evidence (Week 3)

#### 1. What We Evaluated and Rating Breakdown
In Week 3, we conducted a structured task-walkthrough usability evaluation across all user-facing screens (`03_Special_Testing/usability_observations.md`, `US-01` to `US-31`). Because usability observations assess user experience quality rather than binary pass/fail assertions, they are reported separately from pass rates:

| Usability Rating | Count | Share | Key Observations & Linked Defects |
| :--- | :---: | :---: | :--- |
| **Good** | 6 | 19.4% | Consistent Login/Register card layout (`US-07`), password masking & HTML5 required checks (`US-08`), prominent `+ New Task` CTA (`US-09`), consistent Edit form layout (`US-13`), immediate visual strike-through on task toggle (`US-17`), consistent top-right `Log out` placement (`US-27`). |
| **Minor issue** | 21 | 67.7% | Missing confirmation banners after create/delete/logout (`US-10`, `US-21`, `US-28`), silent redirect on invalid edit ID (`US-14`), unlabelled circle toggle `○` (`US-16`, `D-016`), identical styling for `Edit` and `Delete` (`US-15`, `US-20`, `D-018`), unclickable dashboard stat cards (`US-26`), mixed filter auto-submit vs. manual submit without Clear (`US-23`), SQL wildcards `_`/`%` in search (`US-24`, `D-014`), cached dashboard on Back after logout (`US-29`, `D-032`). |
| **Major issue** | 4 | 12.9% | Duplicate username registration succeeds silently (`US-04`, `D-013`), exact 8-character password rejected despite `"Minimum 8 characters"` hint (`US-05`, `D-004`), whitespace-only title creates blank row & 500-char title breaks table layout (`US-11`, `D-011`, `D-012`), tasks due today display red `"Overdue"` badge (`US-18`, `D-001`). |
| **Total Observations** | **31** | **100.0%** | **7 distinct defects linked (`D-001`, `D-004`, `D-011`, `D-012`, `D-013`, `D-014`, `D-032`)** |

#### 2. Key Patterns Found in the Usability Evidence
1. **Misleading Labels and False Urgency Signals Erode User Trust:**  
   Two of the four Major usability issues directly contradict user expectations set by the UI itself: the registration form explicitly instructs `"Minimum 8 characters"` yet rejects an 8-character password (`US-05`, `D-004`), and tasks due today are flagged in red as `"Overdue"` (`US-18`, `D-001`), which also inflates the dashboard's `Overdue` counter (`US-25`).
2. **Weak Error Prevention and Missing System Feedback:**  
   While basic happy-path navigation is clean and consistent (`US-07`, `US-09`, `US-13`, `US-27`), PyTodo Pro provides no success flash banners after creating a task (`US-10`), deleting a task (`US-21`), or logging out (`US-28`), and silently redirects users without explanation when an invalid task ID is requested (`US-14`). Destructive `Delete` links share the same blue link styling as `Edit` (`US-20`) and trigger a generic browser confirmation prompt that omits the task title (`US-19`).
3. **Companion Special-Testing Context:**  
   Visual layout and cross-browser compatibility passed **45 of 45 checks** across Chrome, Edge, Firefox, Galaxy A55, and iPad Pro 13 (`COMP-01` to `COMP-09`), whereas WCAG accessibility checks passed **8 of 16** and failed **8 of 16** due to missing `<label for>` links (`D-009`), unlabelled icon buttons (`D-016`), low contrast (`D-015`), `320 px` horizontal overflow (`D-017`), and undersized click targets (`D-018`).

#### 3. Limitations of Our Usability Evaluation
- The 31 observations reflect a single QA team member's structured walkthrough rather than moderated usability testing with 3–5 first-time end users (tracked as residual risk `RR-17`), and screen-reader behavior was checked via DOM/ARIA inspection rather than live NVDA/VoiceOver user sessions.

---

## 5. Process Improvements to Prevent Recurring Defects (Test Design & Traceability Area)

- **Enforce Shared Web-and-API Acceptance Contracts Linked to the RTM Before Implementation:**  
  Across Weeks 1–7, requirements (`F-01` to `F-22`) were documented only as high-level feature descriptions without explicit boundary rules, data-type schemas, or cross-channel parity specifications. As a result, developers implemented input validation and ownership checks separately in web routes and REST API endpoints—producing **Web-vs-API parity defects** (`D-025` missing owner check in `DELETE /api/tasks/<id>`, `D-020` unparameterized SQL in `GET /api/tasks?q=`, `D-011` vs. `D-022` mismatched title rules) and **specification-vs-code mismatches** (`D-004` UI hint stating `"Minimum 8 characters"` while `is_valid_password()` checks `> 8`; `D-001` missing `"Due Today"` boundary; `D-005` excluding day 7). In addition, late formalization of the RTM in Week 7 revealed that `toggle_task()` had no white-box tests and 20 Week 1 state-transition cases had been designed without recorded execution statuses.
  - **How it works:** Before coding a feature, the Test Design Coordinator and developer co-author a concise **Feature Acceptance & Input-Contract Table** specifying exact boundaries (e.g., `len(password) >= 8`, `due == today -> "Due Today"`), allowed JSON/form types, HTTP status codes (`400`/`404`), and ownership checks—explicitly tagged **"Shared: Web & API"**. Every contract rule is mapped to a Test Case ID in `rtm.md` before implementation is marked complete, with mandatory status reconciliation (`Pass` / `Fail` / `Not Run`) at the end of every sprint.
  - **What it prevents:** Eliminates boundary and UI-hint contradictions (`D-001`, `D-004`, `D-005`), prevents Web-vs-API validation and authorization drift (`D-006`, `D-011`, `D-019`–`D-022`, `D-025`), and ensures no planned test cases or code units (`toggle_task()`) remain unexecuted or untracked.