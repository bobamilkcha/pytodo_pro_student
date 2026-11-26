# Week 6 Defect Check - Automated Run vs Defect Log

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)

**Week 6 task:** 6. Log failures as defects or script issues, and check whether known defects (8-character password, due today) are caught.

This is a **pre-check**. I ran every test file in the repo on a fresh clone before the official run in `execution_report.md`. When Nisrina's official run is in, I compare the two and update this file if anything differs.

---

## 1. How the run was done

| Item | Value |
| :--- | :--- |
| Code | Fresh clone of `main`, 25 Nov 2026 |
| Environment | Python 3, Flask 3.0.3, pytest 9.1.1, Flask test client (no browser) |
| Database | `python -c "import app; app.init_db()"` run first (needed by `04_Web_API/tests/conftest.py`) |
| Command | `pytest <file> -v -rA`, one file at a time |
| Logs | `logs/precheck_all_existing_tests_2026-11-25.txt`, `logs/nafiesa_scripts_2026-11-25.txt` |

## 2. Results

### 2.1 Existing test files (Weeks 2, 4 and 5)

| Test file | Tests | Passed | Failed | Errors |
| :--- | :---: | :---: | :---: | :---: |
| `02_White_Box_Coverage/compute_urgency/tests/test_compute_urgency.py` | 13 | 11 | 2 | 0 |
| `02_White_Box_Coverage/index/tests/test_index.py` | 11 | 11 | 0 | 0 |
| `02_White_Box_Coverage/test_helpers.py` | 7 | 7 | 0 | 0 |
| `04_Web_API/test_api_smoke.py` | 2 | 2 | 0 | 0 |
| `04_Web_API/tests/test_api_auth.py` | 19 | 16 | 3 | 0 |
| `04_Web_API/tests/test_api_delete_dashboard.py` | 10 | 6 | 4 | 0 |
| `04_Web_API/tests/test_api_tasks.py` | 36 | 27 | 9 | 0 |
| `04_Web_API/tests/test_ui_vs_api.py` | 30 | 16 | 14 | 0 |
| `05_Security_Performance/tests/test_security.py` | 22 | 3 | 19 | 0 |
| **Total** | **150** | **99** | **51** | **0** |

### 2.2 New Week 6 scripts (my own technique areas)

| Test file | Tests | Passed | Failed | Regression-marked |
| :--- | :---: | :---: | :---: | :---: |
| `tests/unit/test_reg_decision_table.py` | 19 | 13 | 6 | 13 |
| `tests/api/test_reg_api_delete_dashboard.py` | 10 | 6 | 4 | 7 |
| `tests/ui/test_reg_accessibility_markup.py` | 14 | 4 | 10 | 12 |
| **Total** | **43** | **23** | **20** | **32** |

Note: `pytest 06_Automation_Regression -m regression` runs the 32 marked tests (12 pass, 20 fail).

## 3. Failure analysis: defect or script issue?

| Question | Answer |
| :--- | :--- |
| Failures checked | 71 (51 existing + 20 new) |
| Real product defects | **71** |
| Script issues | **0** |
| New defects found | **0**. Every failure matches a defect already in the log. |
| Unexpected passes (a known defect not seen) | **0**. No defect looks fixed. |

I read the failure message of every failed test. Each one fails on the app's behaviour (wrong status code, wrong label, data deleted, missing header), not on a broken step in the script.

### Script observations (not defects, but worth fixing)

| # | Observation | Files | Suggested action (Automation/Tool Coordinator) |
| :--- | :--- | :--- | :--- |
| S-01 | When the app crashes, some tests show a Python error (`AttributeError`, `ValueError`, `sqlite3.OperationalError`) instead of "HTTP 500". The test still fails correctly, but the log looks like a script error. | `test_api_auth.py`, `test_api_tasks.py`, `test_security.py` | Set `app.config["PROPAGATE_EXCEPTIONS"] = False` in the fixtures, as `test_ui_vs_api.py` already does. |
| S-02 | `04_Web_API/tests/conftest.py` uses the real `pytodo_pro.db`, so tests fail on a fresh clone unless `init_db()` is run first, and a second run can give different results (users from the first run still exist). | `04_Web_API/tests/conftest.py` | Use a temporary database per test (`monkeypatch` + `tmp_path`), as the Week 5 and Week 6 scripts do. |

## 4. Known defects check (task 6)

| Known defect | Caught before Week 6? | Caught after Week 6? |
| :--- | :--- | :--- |
| **D-004** 8-character password rejected | Only through the API (`TC-API-UI-02`). The web register route and the `is_valid_password()` helper had **no** automated test. | **Yes, at 3 levels.** `REG-D004-01` (helper: 7, 8, 9 characters; only 8 fails), `REG-D004-02` (web `/register`), `REG-D004-03` (API). |
| **D-001** Task due today shown as "Overdue" | Yes. `TC-WB-F14-04` (helper), `API-DASH-01` (dashboard), `TC-API-UI-14` (API). | **Yes.** Also `TC-BB-F14-02` (Week 1 decision table, now automated), `REG-D001-01` (fixed date, so it does not depend on today), `REG-D001-02` (dashboard Overdue count). |

Both known defects now fail in the regression suite, so a fix will show straight away as these tests turning green.

## 5. Defect coverage by automation

Out of **32 valid defects** (35 IDs, minus duplicates D-002, D-003, minus D-007, see section 6):

| | Defects caught by an automated test | Rate |
| :--- | :---: | :---: |
| Before Week 6 (existing tests only) | 26 / 32 | 81.3% |
| After Week 6 (with the new scripts) | **31 / 32** | **96.9%** |

The new scripts add D-008, D-009, D-015, D-016 and D-017, which were only checked by hand in Week 3. **D-018** (Edit and Delete links are too small) is the only defect with no automated test, because it needs a real browser to measure the size. A Selenium check could measure it (suggested for `tests/ui/`).

| Defect | Severity | Caught by existing tests (Weeks 2–5) | Caught by new Week 6 scripts (Nafiesa) | Automated? |
| :--- | :---: | :--- | :--- | :---: |
| D-001 | Moderate | TC-WB-F14-04 (test_compute_urgency), API-DASH-01, TC-API-UI-14 | TC-BB-F14-02, REG-D001-01, REG-D001-02 | Yes |
| D-004 | Major | TC-API-UI-02 | REG-D004-01 (8 chars), REG-D004-02, REG-D004-03 | Yes |
| D-005 | Moderate | API-DD-08 | API-DD-08 (W6 copy) | Yes |
| D-006 | Major | TC-WB-F14-10 (test_compute_urgency), API-DD-10, API-TSK-POST-04, TC-API-UI-15, TC-SEC-17 | API-DD-10 (W6 copy) | Yes |
| D-008 | Minor | - | GUI-08 | Yes |
| D-009 | Moderate | - | ACC-01 (/login), ACC-01 (/register), ACC-01 (/tasks/new), ACC-01 (edit), ACC-08 | Yes |
| D-010 | Major | TC-SEC-05 | - | Yes |
| D-011 | Major | TC-SEC-09 | - | Yes |
| D-012 | Moderate | TC-API-UI-12 | - | Yes |
| D-013 | Major | API-REG-09, TC-API-UI-04, TC-SEC-02 | - | Yes |
| D-014 | Minor | TC-API-UI-25, TC-API-UI-26, TC-SEC-08 | - | Yes |
| D-015 | Moderate | - | ACC-03 (done title), ACC-03 (.empty) | Yes |
| D-016 | Moderate | - | ACC-02 | Yes |
| D-017 | Moderate | - | ACC-09 | Yes |
| D-018 | Minor | - | - | **No** |
| D-019 | Moderate | API-REG-08, API-LOG-06, API-TSK-POST-07, TC-API-UI-06 | - | Yes |
| D-020 | Critical | API-TSK-GETALL-04, TC-API-UI-27, TC-SEC-07, TC-SEC-14 | - | Yes |
| D-021 | Moderate | API-TSK-POST-08, TC-API-UI-16 | - | Yes |
| D-022 | Major | API-TSK-PUT-03, TC-API-UI-18 | - | Yes |
| D-023 | Moderate | API-TSK-PUT-06, TC-API-UI-22 | - | Yes |
| D-024 | Minor | API-DD-02, API-TSK-DEL-02, TC-API-UI-23 | API-DD-02 (W6 copy) | Yes |
| D-025 | Critical | API-DD-01, API-TSK-DEL-05, TC-API-UI-24, TC-SEC-21 | API-DD-01 (W6 copy) | Yes |
| D-026 | Major | TC-SEC-01, TC-SEC-19 | - | Yes |
| D-027 | Critical | TC-SEC-03 | - | Yes |
| D-028 | Moderate | TC-SEC-04 | - | Yes |
| D-029 | Major | TC-SEC-06 | - | Yes |
| D-030 | Minor | TC-SEC-10 | - | Yes |
| D-031 | Major | TC-SEC-11 | - | Yes |
| D-032 | Moderate | TC-SEC-12 | - | Yes |
| D-033 | Moderate | TC-SEC-15 | - | Yes |
| D-034 | Moderate | TC-SEC-18 | - | Yes |
| D-035 | Minor | TC-SEC-20 | - | Yes |

## 6. D-007 cannot be reproduced

While mapping failures, I checked D-007 ("invalid CSS selector `-` on line 1 of `style.css`").

- `static/style.css` line 1 is `* { box-sizing: border-box; }`. The `*` selector is valid.
- `git log` shows `style.css` has not changed since the first commit (12 Oct 2026), so it was never `-`.
- In `GUI-01.png` the inputs line up inside the card, with the same 32 px gap on both sides.

**Proposed status:** `Closed (Not reproducible)`. This is applied in the Week 7 final defect log. The Test Design Coordinator should re-run `GUI-01` and change its result if she agrees.

## 7. What changes in the defect log

- Every defect reproduced by an automated test in this run moves from `Open` to **`Confirmed`** (it has now been reproduced more than once). This is applied in `07_Test_Management/defect_log.md`.
- D-018 stays `Open` until a browser retest.
- No new D-IDs. The next new defect will be **D-036**.
