# Week 7: Execution and Regression Status Summary

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Project:** PyTodo Pro (`pytodo_pro_student`)  
**Reconciled Against:** `07_Test_Management/master_test_repository.md`, `05_Security_Performance/performance_results.md`, `06_Automation_Regression/execution_report.md`

---

## 1. Consolidated Execution Status Across Weeks 1–5 (Unique Items)

Across Weeks 1–5, **286 unique test cases, checks, and usability evaluations** were executed (**177 Passed**, **77 Failed**, **31 Usability Source Ratings**, and **1 Performance Observation**). Week 6 automated runs (`103` executions) are reported separately in Section 2 to avoid double-counting re-executed cases.

| Week | Folder | Technique / Test Type | Execution Mode | Count | Passed | Failed | Ratings / Observations |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Week 1** | `01_Black_Box` | Equivalence Partitioning (`TC-BB-001`–`010`) | Manual | 10 | 8 | 2 | 0 |
| **Week 1** | `01_Black_Box` | Boundary Value Analysis (`TC-BB-BVA-*`) | Manual | 8 | 5 | 3 | 0 |
| **Week 1** | `01_Black_Box` | Decision Table (`TC-BB-F03-*`, `F11-*`, `F14-*`) | Manual | 12 | 11 | 1 | 0 |
| **Week 1** | `01_Black_Box` | State Transition (`TC-BB-060`–`079`) | Scripted + Browser | 20 | 19 | 1 | 0 |
| **Week 2** | `02_White_Box_Coverage` | White-Box Path & Branch Coverage (`TC-WB-*`) | Automated (PyTest) | 28 | 24 | 4 | 0 |
| **Week 3** | `03_Special_Testing` | GUI Checklist (`GUI-01`–`18`) | Manual | 18 | 14 | 4 | 0 |
| **Week 3** | `03_Special_Testing` | Cross-Browser & Device Compatibility (`COMP-01`–`09`) | Manual | 9 | 9 | 0 | 0 *(45/45 config results passed)* |
| **Week 3** | `03_Special_Testing` | Accessibility Testing (`ACC-01`–`16`) | Manual + Lighthouse | 16 | 8 | 8 | 0 |
| **Week 3** | `03_Special_Testing` | Usability Evaluation (`US-01`–`31`) | Manual | 31 | — | — | **6 Good, 21 Minor issue, 4 Major issue** *(source ratings)* |
| **Week 4** | `04_Web_API` | End-to-End Web Workflows (`WTS-01`–`08`) | Manual + Selenium | 8 | 8 | 0 | 0 |
| **Week 4** | `04_Web_API` | Client–Server Validation (`WTS-VAL-01`–`06`) | Manual + PyTest | 6 | 1 | 5 | 0 |
| **Week 4** | `04_Web_API` | Core REST API Endpoints (`API-*`) | Automated (PyTest) | 55 | 43 | 12 | 0 |
| **Week 4** | `04_Web_API` | Extra Delete & Dashboard API (`API-DD-01`–`10`) | Automated (PyTest) | 10 | 6 | 4 | 0 |
| **Week 4** | `04_Web_API` | UI vs. API Parity Comparison (`TC-API-UI-01`–`30`) | Automated (PyTest) | 30 | 16 | 14 | 0 |
| **Week 5** | `05_Security_Performance` | STRIDE Security Tests (`TC-SEC-01`–`22`) | Automated (PyTest) | 22 | 3 | 19 | 0 |
| **Week 5** | `05_Security_Performance` | Locust Load & Performance (`PERF-01`–`03`) | Automated (Locust) | 3 | 2 | 0 | **1 Observation** (`PERF-03` Stage 3 P95 520 ms; `PERF-OBS-01/02`) |
| **Subtotal** | **Weeks 1–5** | **Unique Test Cases, Checks & Observations** | **Manual + Automated** | **286** | **177** | **77** | **31 Usability Ratings + 1 Performance Observation** |

---

## 2. Week 6 Automation Execution Summary (`103` Re-Execution Runs)

All **103 automated tests** across **10 test scripts** in `06_Automation_Regression/tests/` execute with **0 collection or setup errors** (`logs/full_suite.log`):

| Test Layer | Test Modules (`10` Files) | Total | Passed | Failed | Errors | Status Summary |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Unit (`tests/unit/`)** | `test_bva_unit.py`, `test_ep_urgency_unit.py`, `test_reg_decision_table.py` | 14 | 6 | 8 | 0 | Failures isolate password length boundary (`D-004`) and due-today urgency (`D-001`). |
| **API / Route (`tests/api/`)** | `test_api_auth.py`, `test_ep_and_core_api.py`, `test_reg_api_delete_dashboard.py`, `test_state_transition.py` | 77 | 61 | 16 | 0 | Core CRUD, auth, and state transitions pass; failures confirm `D-005`, `D-006`, `D-009`, `D-010`, `D-013`, `D-016`, `D-017`, `D-019`, `D-020`, `D-022`, `D-024`, `D-025`. |
| **Browser UI (`tests/ui/`)** | `test_ui_auth.py`, `test_ui_tasks.py`, `test_reg_accessibility_markup.py` | 12 | 2 | 10 | 0 | Both Selenium E2E flows pass; 10 markup/accessibility checks fail (`D-008`, `D-009`, `D-015`/`ACC-03`, `D-016`, `D-017`). |
| **Full Suite Total** | **`pytest 06_Automation_Regression/tests/ -v`** | **103** | **69** | **34** | **0** | **100% of failures map to documented open defects.** |

---

## 3. Focused Regression Suite Status (`@pytest.mark.regression`)

* **Execution Command:** `pytest 06_Automation_Regression/tests/ -m regression -v`
* **Evidence Log:** `06_Automation_Regression/logs/regression_suite.log`
* **Execution Duration:** `14.61s`
* **Selection Scope:** **51 marked regression tests** (`52` deselected) — **22 Passed (43.1%)**, **29 Failed (56.9%)**, **0 Errors**

### Regression Health Assessment
* **Passing Baseline Protection (22 tests):** Confirms core positive user flows and state transitions remain functional—registration, login, task creation/editing/deletion, completion toggling (`Open` ↔ `Done`), combined filtering, session guards, and web-route ownership checks (`TC-SEC-22`).
* **Active Defect Coverage (29 failing tests):** Uses standard assertions (rather than `xfail`) so unpatched defects remain visible as caught failures across **16 distinct defect IDs** (`D-001`, `D-004`, `D-005`, `D-006`, `D-008`, `D-009`, `D-010`, `D-013`, `D-015`/`ACC-03`, `D-016`, `D-017`, `D-019`, `D-020`, `D-022`, `D-024`, `D-025`).

---

## 4. Week 5 Performance Execution Status (`PERF-01` to `PERF-03`)

| Test ID | Load Stage | Virtual Users | Total Requests | Error Rate | Avg Latency | P95 Latency | Throughput | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `PERF-01` | Stage 1 (Baseline) | 10 (`-r 2 -t 30s`) | 221 | 0.00% | 24 ms | 140 ms | 7.55 req/s | **Pass** (Avg `< 200 ms`, P95 `< 500 ms`) |
| `PERF-02` | Stage 2 (Moderate) | 50 (`-r 10 -t 30s`) | 1,073 | 0.00% | 47 ms | 310 ms | 36.92 req/s | **Pass** (Avg `< 200 ms`, P95 `< 500 ms`) |
| `PERF-03` | Stage 3 (High Load) | 100 (`-r 20 -t 30s`) | 2,122 | 0.00% | 95 ms | 520 ms | 72.19 req/s | **Observation** (0% errors, Avg `< 200 ms`; P95 `520 ms` due to auth hashing burst, `PERF-OBS-01/02`) |

---

## 5. Order 5 Cross-Check & Release Readiness

* **Owned Weeks ID Verification (Automation/Tool Coordinator):**
  * **Week 1 BVA (`TC-BB-BVA-F01-01`–`03`, `F08-01`–`02`, `F14-01`–`02`, `F15-01`):** All 8 IDs and linked defects (`D-001`, `D-004`, `D-005`) match `master_test_repository.md` and `rtm.md`.
  * **Week 4 REST API (`API-REG-01`–`09`, `API-LOG-01`–`07`, `API-CAT-01`–`03`):** All 19 IDs and linked defects (`D-013`, `D-019`) match `master_test_repository.md` and `rtm.md`.
  * **Week 5 Performance (`PERF-01`–`03`):** Standardized stage IDs and `0.00%` error metrics across 3,416 requests match `master_test_repository.md`.
  * **Week 6 Automation (`103` runs across `10` scripts):** Synchronized with `master_test_repository.md` (`69` Pass, `34` Fail).
* **Release Gate Verdict:** **Not Ready for Production Release** — 29 regression tests and critical security/data-loss defects (`D-020` SQL injection, `D-025` cross-user API deletion, `D-010` stored XSS) remain `Open`.