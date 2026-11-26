# Week 6: Manual-to-Automated Traceability Matrix (`manual_to_automated_traceability.md`)

**Prepared by:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro  
**Scope:** Full mapping of all 103 automated tests (95 test functions; 6 of them run more than once with different data) across `06_Automation_Regression/tests/` (`unit/`, `api/`, `ui/`) back to their original manual/white-box/security Test Case IDs, Feature Requirements, and Linked Defects.

---

## 1. Traceability Summary by Automation Layer

| Automation Layer | Script File | Owner | Test Count | Regression Marked (`@pytest.mark.regression`) |
| :--- | :--- | :--- | :---: | :---: |
| **PyTest Unit** | `tests/unit/test_bva_unit.py` | Automation/Tool Coordinator | 3 | 1 |
| **PyTest Unit** | `tests/unit/test_ep_urgency_unit.py` | Test Design Coordinator | 6 | 1 |
| **PyTest Unit / Route** | `tests/unit/test_reg_decision_table.py` | Defect & Metrics Coordinator | 19 | 13 |
| **PyTest API** | `tests/api/test_api_auth.py` | Automation/Tool Coordinator | 18 | 2 |
| **PyTest API / Route** | `tests/api/test_ep_and_core_api.py` | Test Design Coordinator | 13 | 9 |
| **PyTest API** | `tests/api/test_reg_api_delete_dashboard.py` | Defect & Metrics Coordinator | 10 | 7 |
| **PyTest API / Route** | `tests/api/test_state_transition.py` | QA/Test Lead | 18 | 6 |
| **Selenium Browser UI** | `tests/ui/test_ui_auth.py` | Automation/Tool Coordinator | 1 | 0 *(excluded by design)* |
| **Selenium Browser UI** | `tests/ui/test_ui_tasks.py` | Automation/Tool Coordinator | 1 | 0 *(excluded by design)* |
| **PyTest HTML/CSS (no browser)** | `tests/ui/test_reg_accessibility_markup.py` | Defect & Metrics Coordinator | 14 | 12 |
| **Total** | **10 Test Files** | | **103** | **51** |

*Note: `test_reg_d004_01` runs 3 times (7, 8, 9 characters), and `test_acc_01_login_register...`, `test_acc_01_task_form...`, `test_acc_03...`, and `test_acc_07...` run twice each, and `test_TC_BB_065...` runs 3 times (`/dashboard`, `/tasks/new`, `/`). That is why 95 functions give 103 tests.*

---

## 2. Unit Layer Traceability (`tests/unit/`)

### 2.1 `06_Automation_Regression/tests/unit/test_bva_unit.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_tc_bb_bva_f01_01_seven_char_password` | `TC-BB-BVA-F01-01` | Week 1 (BVA) | F-01: Register (web) | No | — |
| `test_tc_bb_bva_f01_02_eight_char_password` | `TC-BB-BVA-F01-02`, `TC-API-UI-02` | Week 1 (BVA) | F-01: Register (web) | Yes | D-004 |
| `test_tc_bb_bva_f01_03_nine_char_password` | `TC-BB-BVA-F01-03` | Week 1 (BVA) | F-01: Register (web) | No | — |

### 2.2 `06_Automation_Regression/tests/unit/test_ep_urgency_unit.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_tc_bb_006_no_due_date_none_and_empty` | `TC-BB-006`, `TC-WB-F14-01`, `TC-WB-F14-02` | Week 1 (EP) / Week 2 (White-Box) | F-14: Urgency badge | No | — |
| `test_tc_bb_007_past_due_date_overdue` | `TC-BB-007`, `TC-WB-F14-03` | Week 1 (EP) / Week 2 (White-Box) | F-14: Urgency badge | No | — |
| `test_tc_bb_008_due_today_urgency` | `TC-BB-008`, `TC-WB-F14-04`, `TC-BB-BVA-F14-02` | Week 1 (EP/BVA) / Week 2 (White-Box) | F-14: Urgency badge | Yes | D-001 |
| `test_tc_bb_009_near_future_due_soon` | `TC-BB-009`, `TC-WB-F14-05`, `TC-WB-F14-06` | Week 1 (EP) / Week 2 (White-Box) | F-14: Urgency badge | No | — |
| `test_tc_bb_010_far_future_upcoming` | `TC-BB-010`, `TC-WB-F14-07`, `TC-WB-F14-08` | Week 1 (EP) / Week 2 (White-Box) | F-14: Urgency badge | No | — |
| `test_tc_wb_f14_09_invalid_date_format_raises_value_error` | `TC-WB-F14-09` | Week 2 (White-Box) | F-14: Urgency badge | No | — |

### 2.3 `06_Automation_Regression/tests/unit/test_reg_decision_table.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_tc_bb_f03_01_rule1_user_exists_correct_password` | `TC-BB-F03-01` | Week 1 (Decision Table) | F-03: Login (web) | Yes | — |
| `test_tc_bb_f03_02_rule2_user_exists_wrong_password` | `TC-BB-F03-02` | Week 1 (Decision Table) | F-03: Login (web) | Yes | — |
| `test_tc_bb_f03_03_rule3_unknown_user_correct_password` | `TC-BB-F03-03` | Week 1 (Decision Table) | F-03: Login (web) | No | — |
| `test_tc_bb_f03_04_rule4_unknown_user_wrong_password` | `TC-BB-F03-04` | Week 1 (Decision Table) | F-03: Login (web) | No | — |
| `test_tc_bb_f11_01_no_filters_shows_all` | `TC-BB-F11-01` | Week 1 (Decision Table) | F-11: Filter and search | No | — |
| `test_tc_bb_f11_02_all_three_filters_combined` | `TC-BB-F11-02` | Week 1 (Decision Table) | F-11: Filter and search | Yes | — |
| `test_tc_bb_f11_03_status_done_only` | `TC-BB-F11-03` | Week 1 (Decision Table) | F-11: Filter and search | No | — |
| `test_tc_bb_f11_04_no_match_shows_empty_message` | `TC-BB-F11-04` | Week 1 (Decision Table) | F-11: Filter and search | No | — |
| `test_tc_bb_f14_01_open_task_no_due_date` | `TC-BB-F14-01` | Week 1 (Decision Table) | F-14: Urgency badge | No | — |
| `test_tc_bb_f14_02_open_task_due_today` | `TC-BB-F14-02`, `TC-BB-008` | Week 1 (Decision Table / EP) | F-14: Urgency badge | Yes | D-001 |
| `test_tc_bb_f14_03_open_task_due_tomorrow` | `TC-BB-F14-03` | Week 1 (Decision Table) | F-14: Urgency badge | Yes | — |
| `test_tc_bb_f14_04_done_task_due_yesterday` | `TC-BB-F14-04` | Week 1 (Decision Table) | F-14: Urgency badge | Yes | — |
| `test_reg_d004_01_password_length_boundary` (×3: 7, 8, 9 chars) | `TC-BB-BVA-F01-01`, `-02`, `-03` | Week 1 (BVA) / Week 6 (known-defect check) | F-01: Register | Yes | D-004 |
| `test_reg_d004_02_web_register_accepts_8_char_password` | `TC-BB-BVA-F01-02` | Week 1 (BVA) / Week 6 (known-defect check) | F-01: Register (web) | Yes | D-004 |
| `test_reg_d004_03_api_register_accepts_8_char_password` | `TC-API-UI-02` | Week 4 (UI vs API) / Week 6 (known-defect check) | F-02: Register (API) | Yes | D-004 |
| `test_reg_d001_01_helper_due_today` | `TC-WB-F14-04` | Week 2 (White-Box) / Week 6 (known-defect check) | F-14: Urgency badge | Yes | D-001 |
| `test_reg_d001_02_dashboard_does_not_count_today_as_overdue` | `API-DASH-01`, `TC-BB-F14-02` | Week 4 (API) / Week 6 (known-defect check) | F-16: Dashboard (API) | Yes | D-001 |

---

## 3. API & Web Route Layer Traceability (`tests/api/`)

### 3.1 `06_Automation_Regression/tests/api/test_api_auth.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_api_reg_01_valid_registration` | `API-REG-01`, `TC-BB-001` | Week 1 (EP) / Week 4 (API) | F-01, F-02: Registration | No | — |
| `test_api_reg_02_trimmed_username` | `API-REG-02` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_03_invalid_username` | `API-REG-03` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_04_invalid_password` | `API-REG-04` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_05_missing_username` | `API-REG-05` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_06_missing_password` | `API-REG-06` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_07_empty_json` | `API-REG-07` | Week 4 (API) | F-02: API Register | No | — |
| `test_api_reg_08_wrong_type_username` | `API-REG-08`, `TC-API-UI-06` | Week 4 (API) | F-02: API Register | No | D-019 |
| `test_api_reg_09_duplicate_username` | `API-REG-09`, `TC-BB-002`, `TC-SEC-02` | Week 1 (EP) / Week 4 (API) | F-01, F-02: Registration | Yes | D-013 |
| `test_api_log_01_valid_login` | `API-LOG-01` | Week 4 (API) | F-04: API Login | No | — |
| `test_api_log_02_wrong_password` | `API-LOG-02`, `TC-BB-003`, `TC-API-UI-08` | Week 1 (EP) / Week 4 (API) | F-03, F-04: Login | No | — |
| `test_api_log_03_nonexistent_user` | `API-LOG-03` | Week 4 (API) | F-04: API Login | No | — |
| `test_api_log_04_missing_password` | `API-LOG-04` | Week 4 (API) | F-04: API Login | No | — |
| `test_api_log_05_empty_json` | `API-LOG-05` | Week 4 (API) | F-04: API Login | No | — |
| `test_api_log_06_wrong_type_username` | `API-LOG-06` | Week 4 (API) | F-04: API Login | No | D-019 |
| `test_api_log_07_non_json_body` | `API-LOG-07` | Week 4 (API) | F-04: API Login | No | — |
| `test_tc_bb_bva_f08_01_empty_task_title` | `TC-BB-BVA-F08-01`, `TC-API-UI-09` | Week 1 (BVA) / Week 4 (UI vs API) | F-08, F-19: Create task | Yes | — |
| `test_tc_bb_bva_f08_02_single_char_task_title` | `TC-BB-BVA-F08-02`, `TC-API-UI-11` | Week 1 (BVA) / Week 4 (UI vs API) | F-08, F-19: Create task | No | — |

### 3.2 `06_Automation_Regression/tests/api/test_ep_and_core_api.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_tc_bb_004_create_valid_task_api` | `TC-BB-004`, `API-TSK-POST-01` | Week 1 (EP) / Week 4 (API) | F-08, F-19: Create task | Yes | — |
| `test_tc_bb_005_web_whitespace_title_rejected` | `TC-BB-005`, `WTS-VAL-03`, `TC-SEC-09` | Week 1 (EP) / Week 4 (Web Val) / Week 5 (Security) | F-08: Create task (web) | Yes | D-011 |
| `test_tc_wb_f11_10_combined_web_filters` | `TC-WB-F11-10`, `WTS-04` | Week 2 (White-Box) / Week 4 (Web Flow) | F-11: Filter and search | Yes | — |
| `test_tc_wb_f14_10_bad_due_date_api_rejected` | `TC-WB-F14-10`, `API-TSK-POST-04`, `TC-API-UI-15` | Week 2 (White-Box) / Week 4 (API) | F-14, F-19: Urgency / API Create | Yes | D-006 |
| `test_api_tsk_put_03_empty_title_on_edit_rejected` | `API-TSK-PUT-03`, `TC-API-UI-18` | Week 4 (API / UI vs API) | F-21: API update task | Yes | D-022 |
| `test_tc_sec_07_sql_injection_in_search_handled` | `TC-SEC-07`, `API-TSK-GETALL-04`, `TC-API-UI-27` | Week 4 (API) / Week 5 (Security) | F-18: API task list / search | Yes | D-020 |
| `test_tc_sec_21_cross_user_delete_blocked` | `TC-SEC-21`, `API-TSK-DEL-05`, `API-DD-01` | Week 4 (API) / Week 5 (Security) | F-22: API delete task (IDOR) | Yes | D-025 |
| `test_tc_sec_05_stored_xss_escaped_in_task_list` | `TC-SEC-05`, `GUI-10` | Week 3 (GUI) / Week 5 (Security) | F-09: Task list | Yes | D-010 |
| `test_tc_sec_22_web_delete_enforces_owner_check` | `TC-SEC-22`, `WTS-VAL-06` | Week 4 (Web Val) / Week 5 (Security) | F-13: Delete task (web) | Yes | — |
| `test_gui_01_style_css_universal_box_sizing` | `GUI-01` | Week 3 (GUI) | F-01, F-03, F-08, F-10: CSS layout | No | D-007 (Closed: not reproducible) |
| `test_acc_01_form_labels_have_for_attribute` | `GUI-02`, `ACC-01` | Week 3 (GUI / Accessibility) | F-01, F-03, F-08, F-10: Form labels | No | D-009 |
| `test_acc_02_toggle_button_has_aria_label` | `ACC-02` | Week 3 (Accessibility) | F-12: Mark done / reopen | No | D-016 |
| `test_acc_09_viewport_meta_tag_present` | `ACC-09` | Week 3 (Accessibility) | All Web Pages: Mobile reflow | No | D-017 |

### 3.3 `06_Automation_Regression/tests/api/test_reg_api_delete_dashboard.py`

| Automated Test Function | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_api_dd_01_cross_user_delete_loses_data` | `API-DD-01`, `TC-SEC-21` | Week 4 (API) / Week 5 (Security) | F-22: API delete task (IDOR) | Yes | D-025 |
| `test_api_dd_02_delete_same_task_twice` | `API-DD-02`, `API-TSK-DEL-02` | Week 4 (API) | F-22: API delete task | Yes | D-024 |
| `test_api_dd_03_delete_updates_dashboard` | `API-DD-03` | Week 4 (API) | F-22, F-16: Delete / Dashboard | No | — |
| `test_api_dd_04_dashboard_counts_only_own_tasks` | `API-DD-04` | Week 4 (API) | F-16: Dashboard (API) | Yes | — |
| `test_api_dd_05_done_task_not_overdue` | `API-DD-05` | Week 4 (API) | F-16: Dashboard (API) | No | — |
| `test_api_dd_06_due_soon_upper_boundary` | `API-DD-06` | Week 4 (API, BVA) | F-16: Dashboard (API) | Yes | — |
| `test_api_dd_07_overdue_lower_boundary` | `API-DD-07` | Week 4 (API, BVA) | F-16: Dashboard (API) | Yes | — |
| `test_api_dd_08_completed_exactly_7_days_ago` | `API-DD-08`, `TC-BB-BVA-F15-01` | Week 1 (BVA) / Week 4 (API) | F-16: Dashboard (API) | Yes | D-005 |
| `test_api_dd_09_completed_8_days_ago_not_counted` | `API-DD-09` | Week 4 (API, BVA) | F-16: Dashboard (API) | No | — |
| `test_api_dd_10_dashboard_with_bad_due_date` | `API-DD-10`, `TC-WB-F14-10` | Week 2 (White-Box) / Week 4 (API) | F-16: Dashboard (API) | Yes | D-006 |

### 3.4 `06_Automation_Regression/tests/api/test_state_transition.py`

Owner: QA/Test Lead. These tests use the web routes (`/login`, `/tasks/new`, ...) with the Flask test client, like the manual cases. The manual cases TC-BB-063, 066, 067 and 076 are not in this file (see the notes below the table).

| Original TC ID | Requirement / Feature | Automated test (file::function) | Level | In regression suite? | Result (26 Nov) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `TC-BB-060` | F-05 Logout / session: valid login | `test_state_transition.py::test_TC_BB_060_valid_login_reaches_logged_in` | API | No | Pass |
| `TC-BB-061` | F-05 Session: register logs in | `test_state_transition.py::test_TC_BB_061_register_goes_straight_to_logged_in` | API | No | Pass |
| `TC-BB-062` | F-05 Logout | `test_state_transition.py::test_TC_BB_062_logout_returns_to_anonymous` | API | No | Pass |
| `TC-BB-064` | F-05 Session: wrong password | `test_state_transition.py::test_TC_BB_064_wrong_password_keeps_us_anonymous` | API | No | Pass |
| `TC-BB-065` | F-06 Page protection (web) | `test_state_transition.py::test_TC_BB_065_protected_pages_blocked_after_logout` (x3: `/dashboard`, `/tasks/new`, `/`) | API | Yes | Pass (3 of 3) |
| `TC-BB-068` | F-05, F-12: old page action after logout | `test_state_transition.py::test_TC_BB_068_stale_page_action_after_logout` | API | No | Pass |
| `TC-BB-069` | F-08, F-12: new task starts Open | `test_state_transition.py::test_TC_BB_069_create_task_starts_as_open` | API | No | Pass |
| `TC-BB-070` | F-12 Mark done: Open to Done | `test_state_transition.py::test_TC_BB_070_open_to_done` | API | Yes | Pass |
| `TC-BB-071` | F-12 Reopen: Done to Open | `test_state_transition.py::test_TC_BB_071_done_back_to_open` | API | Yes | Pass |
| `TC-BB-072` | F-10 Edit task (Open stays Open) | `test_state_transition.py::test_TC_BB_072_edit_keeps_open_task_open` | API | No | Pass |
| `TC-BB-073` | F-10 Edit task (Done stays Done) | `test_state_transition.py::test_TC_BB_073_edit_keeps_done_task_done` | API | No | Pass |
| `TC-BB-074` | F-13 Delete task (Open) | `test_state_transition.py::test_TC_BB_074_delete_open_task` | API | Yes | Pass |
| `TC-BB-075` | F-13 Delete task (Done) | `test_state_transition.py::test_TC_BB_075_delete_done_task` | API | No | Pass |
| `TC-BB-077` | F-12: toggle on a deleted task | `test_state_transition.py::test_TC_BB_077_toggle_on_deleted_task` | API | No | Pass |
| `TC-BB-078` | F-10: edit page of a deleted task | `test_state_transition.py::test_TC_BB_078_edit_page_of_deleted_task` | API | No | Pass |
| `TC-BB-079` | F-10: edit page of another user's task | `test_state_transition.py::test_TC_BB_079_edit_page_of_another_users_task` | API | No | Pass |

Not automated here:
- `TC-BB-063` (login while logged in): the group has not decided what the app should do.
- `TC-BB-066` (logout page while logged out): low value.
- `TC-BB-067` (Back button after logout, defect D-036): needs a real browser.
- `TC-BB-076` (confirm popup): needs a real browser. It is covered in the Selenium script `test_ui_tasks.py` (section 4.1).

None of these 16 tests guards a known defect, so none is expected to fail. TC-BB-079 overlaps with `test_tc_sec_22_web_delete_enforces_owner_check` (section 3.2), which is the one in the regression suite.

---

## 4. End-to-End Browser & HTML/CSS UI Layer Traceability (`tests/ui/`)

### 4.1 `06_Automation_Regression/tests/ui/test_ui_auth.py` & `tests/ui/test_ui_tasks.py`

| Automated Test Function | Script File | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `test_wts_01_02_08_auth_lifecycle` | `tests/ui/test_ui_auth.py` | `WTS-01`, `WTS-02`, `WTS-08` | Week 4 (Web Workflow) | F-01, F-03, F-05, F-06: Auth lifecycle | No *(Selenium UI)* | — |
| `test_wts_03_06_07_task_lifecycle_and_confirm_dialog` | `tests/ui/test_ui_tasks.py` | `WTS-03`, `WTS-06`, `WTS-07`, `TC-BB-076`, `GUI-11` | Week 1 (State) / Week 3 (GUI) / Week 4 (Web Flow) | F-08, F-12, F-13: Task lifecycle & confirm dialog | No *(Selenium UI)* | — |

### 4.2 `06_Automation_Regression/tests/ui/test_reg_accessibility_markup.py`

These tests read the page HTML and CSS through the Flask test client. They do **not** open a browser, so they are fast and are included in the regression suite.

| Automated Test Function | Script File | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `test_acc_01_login_register_fields_have_labels` (×2: `/login`, `/register`) | `tests/ui/test_reg_accessibility_markup.py` | `ACC-01`, `GUI-02` | Week 3 (Accessibility) | F-01, F-03: Form labels | Yes | D-009 |
| `test_acc_01_task_form_fields_have_labels` (×2: new, edit) | `tests/ui/test_reg_accessibility_markup.py` | `ACC-01` | Week 3 (Accessibility) | F-08, F-10: Form labels | Yes | D-009 |
| `test_acc_08_filter_controls_have_names` | `tests/ui/test_reg_accessibility_markup.py` | `ACC-08` | Week 3 (Accessibility) | F-11: Filter and search | Yes | D-009 |
| `test_acc_02_done_toggle_has_accessible_name` | `tests/ui/test_reg_accessibility_markup.py` | `ACC-02` | Week 3 (Accessibility) | F-12: Mark done / reopen | Yes | D-016 |
| `test_acc_03_grey_text_contrast` (×2: done title, empty message) | `tests/ui/test_reg_accessibility_markup.py` | `ACC-03` | Week 3 (Accessibility) | F-09: Task list | Yes | D-015 |
| `test_acc_05_each_page_has_unique_title_and_one_h1` | `tests/ui/test_reg_accessibility_markup.py` | `ACC-05` | Week 3 (Accessibility) | All pages | No | — |
| `test_acc_07_page_language_set` (×2: `/login`, `/register`) | `tests/ui/test_reg_accessibility_markup.py` | `ACC-07` | Week 3 (Accessibility) | All pages | Yes | — |
| `test_acc_12_badges_have_text` | `tests/ui/test_reg_accessibility_markup.py` | `ACC-12` | Week 3 (Accessibility) | F-14: Urgency badge | No | — |
| `test_acc_09_viewport_meta_present` | `tests/ui/test_reg_accessibility_markup.py` | `ACC-09` | Week 3 (Accessibility) | All pages: mobile reflow | Yes | D-017 |
| `test_gui_08_empty_list_message_without_filters` | `tests/ui/test_reg_accessibility_markup.py` | `GUI-08` | Week 3 (GUI) | F-09: Task list | Yes | D-008 |

**Overlap note:** `test_acc_01`, `test_acc_02` and `test_acc_09` in section 3.2 check the same defects (D-009, D-016, D-017) as the tests above. Both are fine to keep. The section 3.2 tests do a quick text search; these check each field one by one.