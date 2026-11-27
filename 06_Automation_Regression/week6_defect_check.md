# Week 6 Defect Check - Automated Runs vs Defect Log

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Version:** 3 (final), 27 Nov 2026. Version 1 was a pre-check on 25 Nov; version 2 checked 85 tests on 26 Nov, before `test_state_transition.py` was added.
**Week 6 task:** 6. Log failures as defects or script issues, and check whether known defects (8-character password, due today) are caught.

---

## 1. Runs checked

| Run | What it covers | Source |
| :--- | :--- | :--- |
| A. Week 6 suite | Everything in `06_Automation_Regression/tests/` (Nisrina, Aida, Nafiesa) | `logs/week6_suite.txt`, `logs/week6_regression.txt`; `logs/full_suite.log` (Nisrina) for the 2 Selenium tests |
| B. Earlier automated tests | Test files from Weeks 2, 4 and 5 | `logs/precheck_all_existing_tests.txt` (re-run on 26 Nov with the same results) |

**Environment (my runs):** Linux, Python 3.13, Flask 3.0.3, pytest 9.1.1, fresh `pytodo_pro.db` created with `python -c "import app; app.init_db()"`, app running at `http://127.0.0.1:5000` for the UI folder.

**Selenium note:** the 2 Selenium tests could not start a browser on my machine, because its Chrome (153) and ChromeDriver (147) versions do not match. This is an environment problem, not a test or app problem. Their result is taken from Nisrina's `logs/full_suite.log` (both passed, headless Chrome on Windows).

## 2. Results

### 2.1 Run A: Week 6 suite (`06_Automation_Regression/tests/`)

| Test file | Owner | Tests | Passed | Failed |
| :--- | :--- | :---: | :---: | :---: |
| `unit/test_bva_unit.py` | Nisrina | 3 | 2 | 1 |
| `api/test_api_auth.py` | Nisrina | 18 | 15 | 3 |
| `ui/test_ui_auth.py`, `ui/test_ui_tasks.py` (Selenium) | Nisrina | 2 | 2 | 0 |
| `unit/test_ep_urgency_unit.py` | Aida | 6 | 5 | 1 |
| `api/test_ep_and_core_api.py` | Aida | 13 | 4 | 9 |
| `unit/test_reg_decision_table.py` | Nafiesa | 19 | 13 | 6 |
| `api/test_reg_api_delete_dashboard.py` | Nafiesa | 10 | 6 | 4 |
| `ui/test_reg_accessibility_markup.py` | Nafiesa | 14 | 4 | 10 |
| `api/test_state_transition.py` | Syasya | 18 | 18 | 0 |
| **Total** | | **103** | **69** | **34** |

**Regression subset** (`pytest 06_Automation_Regression/tests -m regression`): **51 tests, 22 passed, 29 failed.** The Selenium tests are not marked, as `regression_suite.md` explains. These match Nisrina's `execution_report.md` and `07_Test_Management/execution_status.md`.

### 2.2 Run B: earlier automated tests (Weeks 2, 4, 5)

| Folder | Tests | Passed | Failed |
| :--- | :---: | :---: | :---: |
| `02_White_Box_Coverage` (3 files) | 31 | 29 | 2 |
| `04_Web_API` (5 files) | 97 | 67 | 30 |
| `05_Security_Performance` | 22 | 3 | 19 |
| **Total** | **150** | **99** | **51** |

### 2.3 All automated tests together

| Tests | Passed | Failed | Errors | Pass rate |
| :---: | :---: | :---: | :---: | :---: |
| **253** | **168** | **85** | **0** | **66.4%** |

## 3. Failure analysis: defect or script issue?

| Question | Answer |
| :--- | :--- |
| Failures checked | 85 (34 in Run A + 51 in Run B). The 18 state transition tests all pass. |
| Real product defects | **85** |
| Script issues | **0** |
| New defects found | **0**. Every failure matches a defect already in the log. The next new ID was **D-036** (used in Week 7 for `TC-BB-067`, then closed as a duplicate of D-032); the next free ID is now **D-037**. |
| Unexpected passes (a known defect not seen) | **0**. No defect looks fixed. |

### 3.1 Run A failures mapped to defects

| Defect | Severity | Failing tests in the Week 6 suite |
| :--- | :---: | :--- |
| D-001 Due today shown as Overdue | Moderate | `test_tc_bb_008_due_today_urgency` (Aida), `test_tc_bb_f14_02`, `test_reg_d001_01`, `test_reg_d001_02` (Nafiesa) |
| D-004 8-character password rejected | Major | `test_tc_bb_bva_f01_02` (Nisrina), `test_reg_d004_01[12345678]`, `test_reg_d004_02`, `test_reg_d004_03` (Nafiesa) |
| D-005 Dashboard misses 7-day boundary | Moderate | `test_api_dd_08` (Nafiesa) |
| D-006 Bad due date gives 500 | Major | `test_tc_wb_f14_10_bad_due_date_api_rejected` (Aida), `test_api_dd_10` (Nafiesa) |
| D-008 Wrong empty-list message | Minor | `test_gui_08` (Nafiesa) |
| D-009 No form labels | Moderate | `test_acc_01_form_labels_have_for_attribute` (Aida), `test_acc_01` ×4, `test_acc_08` (Nafiesa) |
| D-010 Stored XSS | Major | `test_tc_sec_05_stored_xss_escaped_in_task_list` (Aida) |
| D-011 Spaces-only title accepted | Major | `test_tc_bb_005_web_whitespace_title_rejected` (Aida) |
| D-013 Duplicate usernames | Major | `test_api_reg_09_duplicate_username` (Nisrina) |
| D-015 Low contrast | Moderate | `test_acc_03` ×2 (Nafiesa) |
| D-016 Toggle has no name | Moderate | `test_acc_02_toggle_button_has_aria_label` (Aida), `test_acc_02` (Nafiesa) |
| D-017 No viewport / reflow | Moderate | `test_acc_09_viewport_meta_tag_present` (Aida), `test_acc_09` (Nafiesa) |
| D-019 Wrong data type gives 500 | Moderate | `test_api_reg_08`, `test_api_log_06` (Nisrina) |
| D-020 SQL injection | Critical | `test_tc_sec_07_sql_injection_in_search_handled` (Aida) |
| D-022 PUT accepts empty title | Major | `test_api_tsk_put_03_empty_title_on_edit_rejected` (Aida) |
| D-024 DELETE returns 200 for missing task | Minor | `test_api_dd_02` (Nafiesa) |
| D-025 Cross-user delete | Critical | `test_tc_sec_21_cross_user_delete_blocked` (Aida), `test_api_dd_01` (Nafiesa) |

**17 of the 32 valid defects** are guarded by the Week 6 suite, including **2 of the 3 Critical** ones. D-027 (hard-coded secret key) is still guarded by `05_Security_Performance/tests/test_security.py`.

## 4. Known defects check (task 6)

| Known defect | Caught by the Week 6 suite? |
| :--- | :--- |
| **D-004** 8-character password rejected | **Yes, by 4 tests at 3 levels:** helper (`test_tc_bb_bva_f01_02`, `test_reg_d004_01`), web `/register` (`test_reg_d004_02`), API (`test_reg_d004_03`) |
| **D-001** Task due today shown as Overdue | **Yes, by 4 tests:** helper (`test_tc_bb_008`, `test_reg_d001_01`), API urgency (`test_tc_bb_f14_02`), dashboard count (`test_reg_d001_02`) |

Note: Nisrina's `execution_report.md` lists only 23 tests, so on its own it catches **D-004 but not D-001**. D-001 is caught once Aida's and Nafiesa's files are included.

## 5. Defect coverage by automation (all folders)

Out of **32 valid defects**, **31 (96.9%)** fail at least one automated test when every folder is run. Only **D-018** (target size) has no automated test, because it needs a real browser to measure.

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

- `static/style.css` line 1 is `* { box-sizing: border-box; }`. The `*` selector is valid.
- `git log` shows `style.css` has not changed since the first commit (12 Oct 2026).
- In `GUI-01.png` the inputs line up inside the card, with the same 32 px gap on both sides.

**Status:** `Closed (Not reproducible)` in `07_Test_Management/defect_log.md`. The Test Design Coordinator should re-run `GUI-01`.

## 7. Issues found in the Week 6 files (not app defects)

| # | File | Issue | Suggested fix | Owner |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `execution_report.md` | Covered only 23 tests | Updated to 103 tests (69 passed, 34 failed) and regression 51 (22 passed, 29 failed). **Resolved 26 Nov** | Nisrina |
| 2 | `regression_suite.md` | Lists 10 defects | With all marked tests, the regression suite guards 17 defects (section 3.1) | Nisrina |
| 3 | `06_Automation_Regression/README.md` | File is empty | Add the setup section (task 2) and the automation reflection (task 7) | Nisrina, Syasya |
| 4 | `tests/conftest.py` | The `client` fixture uses the real `pytodo_pro.db`. On a fresh clone the tests fail unless `init_db()` is run first, and a second run can behave differently | Use a temporary database per test, as `test_reg_*.py` files do | Nisrina |
| 5 | Selenium tests | They need the app running at `127.0.0.1:5000` and a ChromeDriver that matches Chrome. On Linux (and GitHub Actions in Week 9) Chrome also needs `--no-sandbox` | Write the steps in the README; add `--no-sandbox` and `--disable-dev-shm-usage` to the `browser` fixture | Nisrina |
| 6 | `manual_to_automated_traceability.md` | Nafiesa's 43 automated tests were not listed | Now included (103 tests). **Resolved 26 Nov** | Aida |
| 7 | `automation_candidates.md` | Says the web `/login` route has no test | `test_reg_decision_table.py` now covers web login (TC-BB-F03-01..04) | Syasya |
| 8 | Overlap | Aida's `test_acc_01/02/09` and Nafiesa's `test_acc_01/02/09` check the same defects | Not wrong, but say in `regression_suite.md` that they overlap, so counts are not read as extra defects | Nisrina |

## 8. What changes in the defect log

- No new defects. No status changes: every defect that was `Confirmed` on 25 Nov failed again on 26 Nov.
- D-018 stays `Open` until a browser retest.
