# Week 6: Manual-to-Automated Traceability Matrix (`manual_to_automated_traceability.md`)

**Prepared by:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro  
**Scope:** Full mapping of all 42 automated test functions across `06_Automation_Regression/tests/` (`unit/`, `api/`, `ui/`) back to their original manual/white-box/security Test Case IDs, Feature Requirements, and Linked Defects.

---

## 1. Traceability Summary by Automation Layer

| Automation Layer | Script File | Owner | Test Count | Regression Marked (`@pytest.mark.regression`) |
| :--- | :--- | :--- | :---: | :---: |
| **PyTest Unit** | `tests/unit/test_bva_unit.py` | Automation/Tool Coordinator | 3 | 1 |
| **PyTest Unit** | `tests/unit/test_ep_urgency_unit.py` | Test Design Coordinator | 6 | 1 |
| **PyTest API** | `tests/api/test_api_auth.py` | Automation/Tool Coordinator | 18 | 2 |
| **PyTest API / Route** | `tests/api/test_ep_and_core_api.py` | Test Design Coordinator | 13 | 9 |
| **Selenium Browser UI** | `tests/ui/test_ui_auth.py` | Automation/Tool Coordinator | 1 | 0 *(excluded by design)* |
| **Selenium Browser UI** | `tests/ui/test_ui_tasks.py` | Automation/Tool Coordinator | 1 | 0 *(excluded by design)* |
| **Total** | **6 Test Files** | | **42** | **13** |

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
| `test_gui_01_style_css_universal_box_sizing` | `GUI-01` | Week 3 (GUI) | F-01, F-03, F-08, F-10: CSS layout | No | D-007 |
| `test_acc_01_form_labels_have_for_attribute` | `GUI-02`, `ACC-01` | Week 3 (GUI / Accessibility) | F-01, F-03, F-08, F-10: Form labels | No | D-009 |
| `test_acc_02_toggle_button_has_aria_label` | `ACC-02` | Week 3 (Accessibility) | F-12: Mark done / reopen | No | D-016 |
| `test_acc_09_viewport_meta_tag_present` | `ACC-09` | Week 3 (Accessibility) | All Web Pages: Mobile reflow | No | D-017 |

---

## 4. End-to-End Browser UI Layer Traceability (`tests/ui/`)

### 4.1 `06_Automation_Regression/tests/ui/test_ui_auth.py` & `tests/ui/test_ui_tasks.py`

| Automated Test Function | Script File | Original TC ID(s) | Source Week / Technique | Feature / Requirement | Regression Marker | Linked Defect |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `test_wts_01_02_08_auth_lifecycle` | `tests/ui/test_ui_auth.py` | `WTS-01`, `WTS-02`, `WTS-08` | Week 4 (Web Workflow) | F-01, F-03, F-05, F-06: Auth lifecycle | No *(Selenium UI)* | — |
| `test_wts_03_06_07_task_lifecycle_and_confirm_dialog` | `tests/ui/test_ui_tasks.py` | `WTS-03`, `WTS-06`, `WTS-07`, `TC-BB-076`, `GUI-11` | Week 1 (State) / Week 3 (GUI) / Week 4 (Web Flow) | F-08, F-12, F-13: Task lifecycle & confirm dialog | No *(Selenium UI)* | — |