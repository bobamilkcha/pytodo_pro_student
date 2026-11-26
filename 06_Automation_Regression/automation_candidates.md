# Automation Candidates and Traceability - Nafiesa's Tests

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)

**Week 6 tasks:** 1 (suggest candidates from my own tests), 3b (automate them), and input for 3c (manual-to-automated traceability)

This file is my input for `automation_candidates.md` (QA/Test Lead) and `manual_to_automated_traceability.md` (Test Design Coordinator). Copy the rows you need.

---

## 1. Scoring method

Each test group is scored from 1 (low) to 3 (high) on the four criteria in the brief:

| Criterion | 3 means |
| :--- | :--- |
| Repetition | It must be re-run after almost any change to the app |
| Stability | Same result every run; no timing, screen or human judgement needed |
| Criticality | Guards a Critical/Major defect or a core feature (login, saving or deleting user data) |
| Regression value | A future change is likely to break it, and a failure would be easy to miss by hand |

**Decision rule:** total 9 or more out of 12 = automate and add to the regression suite. 7–8 = automate, full suite only. 6 or less = keep manual.

## 2. Scores

| Source (week, technique) | Test IDs | Rep. | Stab. | Crit. | Reg. | Total | Decision |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| W1 Decision table, F-03 Login | TC-BB-F03-01, 02 | 3 | 3 | 3 | 3 | 12 | Automate, **regression** |
| W1 Decision table, F-03 Login | TC-BB-F03-03, 04 | 3 | 3 | 2 | 1 | 9 | Automate, full suite (same code path as F03-02, so low extra regression value) |
| W1 Decision table, F-11 Filter | TC-BB-F11-02 (all 3 filters combined) | 3 | 3 | 2 | 3 | 11 | Automate, **regression** |
| W1 Decision table, F-11 Filter | TC-BB-F11-01, 03, 04 | 2 | 3 | 1 | 2 | 8 | Automate, full suite |
| W1 Decision table, F-14 Urgency | TC-BB-F14-02, 03, 04 | 3 | 3 | 3 | 3 | 12 | Automate, **regression** (F14-02 guards D-001) |
| W1 Decision table, F-14 Urgency | TC-BB-F14-01 (no due date) | 2 | 3 | 1 | 1 | 7 | Automate, full suite |
| Known defects (Week 6 task 6) | REG-D004-01..03, REG-D001-01..02 | 3 | 3 | 3 | 3 | 12 | Automate, **regression** |
| W2 White-box, `compute_urgency` | TC-WB-F14-01..10 | 3 | 3 | 3 | 3 | 12 | Already automated in Week 2. Keep in the suite; mark TC-WB-F14-04 and -10 as regression (Automation/Tool Coordinator's file layout) |
| W3 Accessibility, markup checks | ACC-01, 02, 03, 07, 08, 09, GUI-08 | 3 | 3 | 2 | 3 | 11 | Automate (HTML/CSS checks, no browser), **regression** |
| W3 Accessibility, passed checks | ACC-05, ACC-12 | 2 | 3 | 1 | 2 | 8 | Automate, full suite |
| W3 Accessibility, target size | ACC-11 (D-018) | 2 | 2 | 1 | 2 | 7 | Automate later with **Selenium** (needs real element size). Suggested for `tests/ui/` |
| W3 Accessibility, Lighthouse audit | ACC-10 | 2 | 2 | 2 | 2 | 8 | Automate later in CI (Lighthouse CI). Not done this week: needs Chrome and Node |
| W3 Accessibility, human judgement | ACC-04, 06, 13 (keyboard, error message, popup) | 1 | 1 | 2 | 1 | 5 | **Keep manual**: a person must judge focus order and how clear a message is |
| W3 Accessibility, nothing to check | ACC-14 (no images), ACC-16 (no animation) | 1 | 3 | 1 | 1 | 6 | **Keep manual**: one look per release is enough |
| W3 Accessibility, best practice | ACC-15 (no `<main>`) | 1 | 3 | 1 | 1 | 6 | Keep manual: a recommendation (R-04), not a logged defect |
| W4 API, delete/dashboard | API-DD-01, 02, 08, 10 | 3 | 3 | 3 | 3 | 12 | Automate, **regression** (guard D-025, D-024, D-005, D-006) |
| W4 API, dashboard boundaries | API-DD-04, 06, 07 | 3 | 3 | 2 | 3 | 11 | Automate, **regression** (data isolation and the 2-day / 0-day limits) |
| W4 API, other dashboard | API-DD-03, 05, 09 | 2 | 3 | 2 | 2 | 9 | Automate, full suite (covered in part by the regression tests above) |

## 3. What I automated (task 3b)

| Script | Tests | Regression-marked | Result (25 Nov) |
| :--- | :---: | :---: | :--- |
| `tests/unit/test_reg_decision_table.py` | 19 | 13 | 13 pass, 6 fail (D-001, D-004) |
| `tests/api/test_reg_api_delete_dashboard.py` | 10 | 7 | 6 pass, 4 fail (D-005, D-006, D-024, D-025) |
| `tests/ui/test_reg_accessibility_markup.py` | 14 | 12 | 4 pass, 10 fail (D-008, D-009, D-015, D-016, D-017) |
| **Total** | **43** | **32** | **23 pass, 20 fail** |

All 20 failures are known open defects. Tests marked "EXPECTED TO FAIL" in their docstring should turn green once the developers fix that defect.

**Note for the Automation/Tool Coordinator:** the `tests/ui/` file uses the Flask test client and reads the HTML, not Selenium. It sits next to the Selenium scripts because it checks the user interface. Rename the folder if you prefer another layout. The `regression` marker is registered in `06_Automation_Regression/conftest.py`. Move it to your `pytest.ini` if you create one.

## 4. Manual-to-automated traceability (input for 3c)

| Automated test (function) | Original manual test | Requirement / feature | Defect guarded | Regression |
| :--- | :--- | :--- | :--- | :---: |
| `test_tc_bb_f03_01_rule1_user_exists_correct_password` | TC-BB-F03-01 | F-03 Login (web) | - | Yes |
| `test_tc_bb_f03_02_rule2_user_exists_wrong_password` | TC-BB-F03-02 | F-03 Login (web) | - | Yes |
| `test_tc_bb_f03_03_rule3_unknown_user_correct_password` | TC-BB-F03-03 | F-03 Login (web) | - | No |
| `test_tc_bb_f03_04_rule4_unknown_user_wrong_password` | TC-BB-F03-04 | F-03 Login (web) | - | No |
| `test_tc_bb_f11_01_no_filters_shows_all` | TC-BB-F11-01 | F-11 Filter and search | - | No |
| `test_tc_bb_f11_02_all_three_filters_combined` | TC-BB-F11-02 | F-11 Filter and search | - | Yes |
| `test_tc_bb_f11_03_status_done_only` | TC-BB-F11-03 | F-11 Filter and search | - | No |
| `test_tc_bb_f11_04_no_match_shows_empty_message` | TC-BB-F11-04 | F-11 Filter and search | - | No |
| `test_tc_bb_f14_01_open_task_no_due_date` | TC-BB-F14-01 | F-14 Urgency badge | - | No |
| `test_tc_bb_f14_02_open_task_due_today` | TC-BB-F14-02 | F-14 Urgency badge | D-001 | Yes |
| `test_tc_bb_f14_03_open_task_due_tomorrow` | TC-BB-F14-03 | F-14 Urgency badge | - | Yes |
| `test_tc_bb_f14_04_done_task_due_yesterday` | TC-BB-F14-04 | F-14 Urgency badge | - | Yes |
| `test_reg_d004_01_password_length_boundary` (7, 8, 9 chars) | TC-BB-BVA-F01-01..03 (Nisrina, BVA) | F-01 Register | D-004 | Yes |
| `test_reg_d004_02_web_register_accepts_8_char_password` | TC-BB-BVA-F01-02 | F-01 Register (web) | D-004 | Yes |
| `test_reg_d004_03_api_register_accepts_8_char_password` | TC-API-UI-02 | F-02 Register (API) | D-004 | Yes |
| `test_reg_d001_01_helper_due_today` | TC-WB-F14-04 | F-14 Urgency badge | D-001 | Yes |
| `test_reg_d001_02_dashboard_does_not_count_today_as_overdue` | API-DASH-01, TC-BB-F14-02 | F-16 Dashboard (API) | D-001 | Yes |
| `test_api_dd_01` … `test_api_dd_10` | API-DD-01 … API-DD-10 | F-22 Delete task (API), F-16 Dashboard (API) | D-025, D-024, D-005, D-006 | 01, 02, 04, 06, 07, 08, 10 |
| `test_acc_01_login_register_fields_have_labels` | ACC-01 | F-01, F-03 forms | D-009 | Yes |
| `test_acc_01_task_form_fields_have_labels` | ACC-01 | F-08, F-10 forms | D-009 | Yes |
| `test_acc_08_filter_controls_have_names` | ACC-08 | F-11 Filter and search | D-009 | Yes |
| `test_acc_02_done_toggle_has_accessible_name` | ACC-02 | F-12 Mark done | D-016 | Yes |
| `test_acc_03_grey_text_contrast` | ACC-03 | F-09 Task list | D-015 | Yes |
| `test_acc_05_each_page_has_unique_title_and_one_h1` | ACC-05 | All pages | - | No |
| `test_acc_07_page_language_set` | ACC-07 | All pages | - | Yes |
| `test_acc_09_viewport_meta_present` | ACC-09 | All pages | D-017 | Yes |
| `test_acc_12_badges_have_text` | ACC-12 | F-14 Urgency badge | - | No |
| `test_gui_08_empty_list_message_without_filters` | GUI-08 (Aida) | F-09 Task list | D-008 | Yes |

## 5. Small differences found while automating

| # | Finding | Action |
| :--- | :--- | :--- |
| 1 | TC-BB-F03-01 says the user is sent to `/dashboard` after login. The app sends the user to the task list `/`. The automated test checks `/`. | I will change the Expected Result in `tc_defect_coordinator.md` to "Redirected to the task list (`/`)". |
| 2 | ACC-03 contrast is 2.85:1 when calculated from `#999` in code. The Week 3 tool reported 2.84:1. This is a rounding difference only. Both fail 4.5:1. | None. |
