# Week 6: Automation & Regression Testing (`06_Automation_Regression`)

**Primary Coordinator:** Automation/Tool Coordinator (Nisrina)  
**Contributors:** QA/Test Lead, Test Design Coordinator (Aida), Defect & Metrics Coordinator (Nafiesa)

---

## 1. Documented Test Environment & Prerequisites

* **Operating System:** Windows 10/11 (primary execution) and Linux (cross-platform verification)
* **Python Runtime:** Python `3.10.11` / `3.11.5` (inside virtual environment `venv`)
* **Application Under Test:** Flask `3.0.3` (`app.py`, `helpers.py`) with SQLite (`pytodo_pro.db`)
* **Testing & Coverage Tools:**
  * `pytest` (`9.2.0`) — unit, route, and REST API test runner
  * `pytest-cov` (`7.1.0`) — statement and branch coverage instrumentation
  * `selenium` — end-to-end browser automation using Headless Chrome

### Dependency Installation (From Project Root)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest pytest-cov selenium
```

---

## 2. Folder Structure & Deliverables

| Path | Owner | Purpose |
| :--- | :--- | :--- |
| `tests/conftest.py` | Automation/Tool Coordinator | Shared PyTest fixtures isolating each test with a temporary SQLite database (`tmp_path`) so `pytodo_pro.db` stays clean. |
| `tests/unit/` | Nisrina, Nafiesa | Unit tests for `is_valid_password()`, `compute_urgency()`, and decision-table rules (`3` files, `14` tests). |
| `tests/api/` | Nisrina, Aida, Nafiesa, QA Lead | Flask test-client suites for auth, CRUD, security, delete/dashboard boundaries, and state transitions (`4` files, `77` tests). |
| `tests/ui/` | Nisrina, Nafiesa | Headless Chrome Selenium E2E flows (`test_ui_auth.py`, `test_ui_tasks.py`) and accessibility/markup checks (`3` files, `12` tests). |
| `automation_candidates.md` | QA/Test Lead & Team | Scoring matrix (`1`–`12` scale) selecting candidates for full automation (`>= 7`) and `@pytest.mark.regression` (`>= 9`). |
| `manual_to_automated_traceability.md` | Test Design Coordinator | Maps manual test case IDs from Weeks 1–5 to automated test functions. |
| `regression_suite.md` | Automation/Tool Coordinator | Selection criteria, execution command, and inventory for `@pytest.mark.regression`. |
| `execution_report.md` | Automation/Tool Coordinator | Detailed execution summary, per-layer breakdown, and defect mapping. |
| `week6_defect_check.md` | Defect & Metrics Coordinator | Verification confirming all automated failures map to valid logged defects (`0` script errors). |
| `logs/full_suite.log` | Automation/Tool Coordinator | Saved console output from the full `103`-test run. |
| `logs/regression_suite.log` | Automation/Tool Coordinator | Saved console output from the `51`-test `-m regression` run. |

---

## 3. How to Run the Automated Suites

Run all commands from the repository root (`pytodo_pro_student`) with `(venv)` active:

### A. Focused Regression Suite (`@pytest.mark.regression` — Fast Pre-Merge Check)
Runs unit, API, and markup regression checks without requiring a live server (`~14.6s`):
```powershell
pytest 06_Automation_Regression/tests/ -m regression -v
```

### B. Full Automated Suite (`103` Tests Across `10` Scripts)
Start the Flask server in **Terminal 1** first so the two Selenium browser tests in `tests/ui/` can connect to `http://127.0.0.1:5000`:
```powershell
# Terminal 1
python app.py

# Terminal 2
pytest 06_Automation_Regression/tests/ -v
```

### C. Combined Statement & Branch Coverage Check
```powershell
pytest 06_Automation_Regression/tests/unit 06_Automation_Regression/tests/api --cov=app --cov=helpers --cov-branch --cov-report=term-missing
```

---

## 4. Execution Summary & Coverage Metrics

| Metric / Suite | Total | Passed | Failed | Errors | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Full Automated Suite (`tests/`)** | **103** | **69** | **34** | **0** | Executed in `~26s`; all `34` failures confirm open defects (`logs/full_suite.log`). |
| **Focused Regression (`-m regression`)** | **51** | **22** | **29** | **0** | Executed in `14.61s` (`52` deselected); guards `16` distinct defect IDs (`logs/regression_suite.log`). |
| **Combined Coverage (`app.py` + `helpers.py`)** | `330` stmts / `82` branches | `313` stmts (**94.8%**) | `73` branches (**89.0%**) | — | Measured across all automated suites (`08_Final_QA_Report/metrics.md`). |

---

## 5. Automation & Regression Reflection

* **Value of Tiered Execution:** Separating fast Flask test-client and unit checks (`@pytest.mark.regression`) from slower browser-driven Selenium scripts keeps per-commit feedback under 15 seconds while preserving end-to-end UI verification before demos or releases.
* **Expected Failures as Defect Guards:** Using standard assertions instead of `xfail` keeps all 16 unpatched defect types visibly failing (`29` regression failures) so fixes can be verified automatically when they turn green.
* **Database Isolation:** Switching from shared `pytodo_pro.db` access to per-test `tmp_path` SQLite fixtures in `tests/conftest.py` eliminated state pollution and cross-test flakiness.