# Week 6: Automated Test Execution Report (Final Combined Suite)

**Executed by:** Automation/Tool Coordinator (Nisrina)  
**Environment:** Windows, Python `3.10.11`, PyTest `9.2.0`, Selenium WebDriver (Headless Chrome)  
**Evidence Logs:** `06_Automation_Regression/logs/full_suite.log`, `06_Automation_Regression/logs/regression_suite.log`

---

## 1. Combined Execution Summary

| Suite / Run Type | PyTest Command | Total Collected | Passed | Failed | Errors | Duration | Log File |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Full Automated Suite** | `pytest 06_Automation_Regression/tests/ -v` | **85** | **51** | **34** | **0** | **25.67s** | `logs/full_suite.log` |
| **Regression Suite (`-m regression`)** | `pytest 06_Automation_Regression/tests/ -m regression -v` | **45** *(40 deselected)* | **16** | **29** | **0** | **10.27s** | `logs/regression_suite.log` |

---

## 2. Suite Inventory by Layer & Test File

| Layer | File Path | Coverage Scope |
| :--- | :--- | :--- |
| **Unit** | `tests/unit/test_bva_unit.py` | Password boundary checks (`TC-BB-BVA-F01-01` to `03`, catches `D-004`). |
| **Unit** | `tests/unit/test_ep_urgency_unit.py` | Urgency classification equivalence partitions (`TC-BB-006` to `010`, catches `D-001`). |
| **Unit** | `tests/unit/test_reg_decision_table.py` | Decision table urgency rules and `D-001` / `D-004` regression boundaries. |
| **API** | `tests/api/test_api_auth.py` | Register/login API rules and task title BVA (`API-REG-01`–`09`, `API-LOG-01`–`07`, catches `D-013`, `D-019`). |
| **API** | `tests/api/test_ep_and_core_api.py` | Core task CRUD, SQLi/XSS security checks, and HTML attribute checks (catches `D-009`, `D-010`, `D-016`, `D-017`, `D-020`, `D-022`, `D-025`). |
| **API** | `tests/api/test_reg_api_delete_dashboard.py` | Delete idempotency, cross-user deletion, and dashboard date boundaries (catches `D-005`, `D-006`, `D-024`, `D-025`). |
| **UI** | `tests/ui/test_ui_auth.py` | End-to-end Selenium browser registration, login, and logout (`WTS-01`, `WTS-02`, `WTS-08`). |
| **UI** | `tests/ui/test_ui_tasks.py` | End-to-end Selenium task creation, toggle completion, and confirm dialog (`WTS-03`, `WTS-06`, `WTS-07`, `TC-BB-076`, `GUI-11`). |
| **UI** | `tests/ui/test_reg_accessibility_markup.py` | Form label associations, ARIA names, contrast, viewport tag, and empty-list messaging (`ACC-01`–`03`, `ACC-08`–`09`, `GUI-08`). |

---

## 3. Summary of Caught Defects (34 Failures)

All 34 failures in `logs/full_suite.log` are expected failures confirming active defects in the application under test:

| Defect ID | Affected Feature / Rule | Representative Failing Automated Tests |
| :---: | :--- | :--- |
| **D-001** | Task due today marked Overdue instead of Due Soon | `test_tc_bb_008_due_today_urgency`, `test_tc_bb_f14_02_open_task_due_today`, `test_reg_d001_01_helper_due_today`, `test_reg_d001_02_dashboard_does_not_count_today_as_overdue` |
| **D-004** | Valid 8-character boundary password rejected | `test_tc_bb_bva_f01_02_eight_char_password`, `test_reg_d004_01_password_length_boundary`, `test_reg_d004_02_web_register_accepts_8_char_password`, `test_reg_d004_03_api_register_accepts_8_char_password` |
| **D-005** | Task completed exactly 7 days ago excluded from dashboard count | `test_api_dd_08_completed_exactly_7_days_ago` |
| **D-006** | Invalid due date causes server/dashboard failure | `test_api_dd_10_dashboard_with_bad_due_date` |
| **D-008** | Missing empty-list message when user has no tasks | `test_gui_08_empty_list_message_without_filters` |
| **D-009** | Form labels missing `for` attribute associations | `test_acc_01_form_labels_have_for_attribute`, `test_acc_01_login_register_fields_have_labels`, `test_acc_01_task_form_fields_have_labels`, `test_acc_08_filter_controls_have_names` |
| **D-010** | Stored XSS payload rendered unescaped in task list | `test_tc_sec_05_stored_xss_escaped_in_task_list` |
| **D-013** | Duplicate username accepted on registration | `test_api_reg_09_duplicate_username` |
| **D-016** | Task completion toggle button lacks accessible name | `test_acc_02_toggle_button_has_aria_label`, `test_acc_02_done_toggle_has_accessible_name` |
| **D-017** | Missing `<meta name="viewport">` tag on templates | `test_acc_09_viewport_meta_tag_present`, `test_acc_09_viewport_meta_present` |
| **D-019** | Non-string integer username causes HTTP 500 `AttributeError` | `test_api_reg_08_wrong_type_username`, `test_api_log_06_wrong_type_username` |
| **D-020** | SQL injection payload in search query unhandled | `test_tc_sec_07_sql_injection_in_search_handled` |
| **D-022** | Empty title accepted when editing a task | `test_api_tsk_put_03_empty_title_on_edit_rejected` |
| **D-024** | Deleting a non-existent or already-deleted task returns `200` | `test_api_dd_02_delete_same_task_twice` |
| **D-025** | Authenticated user can delete another user's task via API | `test_tc_sec_21_cross_user_delete_blocked`, `test_api_dd_01_cross_user_delete_loses_data` |
| **ACC-03** | Insufficient colour contrast on completed task & empty text | `test_acc_03_grey_text_contrast` |