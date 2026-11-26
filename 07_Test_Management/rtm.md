# Week 7: Requirements Traceability Matrix (`rtm.md`)

**Prepared by:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro  
**Scope:** End-to-end forward and backward traceability across all **22 Functional Requirements (`F-01` to `F-22`)** and **3 Cross-Cutting / Non-Functional Requirements (`NFR-01` to `NFR-03`)**, linking every requirement to its manual/white-box/special/security/performance test cases (`Weeks 1–5`), automated regression scripts (`Week 6`), and central defects (`D-001` to `D-036`).

---

## 1. Traceability Coverage Summary

| Requirement Group | Total Requirements | Requirements Passing | Requirements Failing (Open Defects) | Requirements Passing with Observations | Coverage Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **2.1 Authentication (`F-01` – `F-07`)** | 7 | 2 (`F-06`, `F-07`) | 5 (`F-01` – `F-05`) | 0 | 100% |
| **2.2 Task Management Web (`F-08` – `F-14`)** | 7 | 0 | 7 (`F-08` – `F-14`) | 0 | 100% |
| **2.3 Dashboard (`F-15` – `F-16`)** | 2 | 0 | 2 (`F-15`, `F-16`) | 0 | 100% |
| **2.4 Task & Category API (`F-17` – `F-22`)** | 6 | 2 (`F-17`, `F-20`) | 4 (`F-18`, `F-19`, `F-21`, `F-22`) | 0 | 100% |
| **2.5 Non-Functional / Server (`NFR-01` – `NFR-03`)** | 3 | 0 | 2 (`NFR-01`, `NFR-02`) | 1 (`NFR-03`) | 100% |
| **Total** | **25** | **4** | **20** | **1** | **100%** |

---

## 2. Requirements Traceability Matrix (`F-01` to `F-22` & `NFR-01` to `NFR-03`)

### 2.1 Authentication (`F-01` to `F-07`)

| Req ID | Requirement Name & Route | Manual / Exploratory / Security Test Cases (Weeks 1–5) | Automated Week 6 Test Scripts (`06_Automation_Regression/tests/`) | Linked Defect IDs | Requirement Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **F-01** | **Register (Web)**<br>`GET/POST /register` (`app.py::register_page`) | `TC-BB-001`, `TC-BB-002`, `TC-BB-BVA-F01-01`–`03`, `TC-BB-061`, `GUI-01`–`03`, `GUI-13`, `GUI-14`, `ACC-01`, `US-01`–`05`, `WTS-01`, `WTS-VAL-01`, `WTS-VAL-02`, `TC-API-UI-01`–`05`, `TC-SEC-02`, `TC-SEC-13` | `unit/test_bva_unit.py` (`test_tc_bb_bva_f01_01`–`03`)<br>`unit/test_reg_decision_table.py` (`test_reg_d004_01`, `02`)<br>`api/test_state_transition.py` (`test_TC_BB_061`)<br>`ui/test_ui_auth.py`<br>`ui/test_reg_accessibility_markup.py` (`test_acc_01_login_register`) | `D-004` (Major)<br>`D-009` (Moderate)<br>`D-013` (Major)<br>*(`D-007` Closed)* | **Fail** |
| **F-02** | **Register (API)**<br>`POST /api/register` (`app.py::api_register`) | `API-REG-01`–`09`, `WTS-01`, `TC-API-UI-01`–`06`, `PERF-01`–`03` | `api/test_api_auth.py` (`test_api_reg_01`–`09`)<br>`unit/test_reg_decision_table.py` (`test_reg_d004_03`) | `D-004` (Major)<br>`D-013` (Major)<br>`D-019` (Moderate) | **Fail** |
| **F-03** | **Login (Web)**<br>`GET/POST /login` (`app.py::login_page`) | `TC-BB-003`, `TC-BB-F03-01`–`04`, `TC-BB-060`, `TC-BB-063`, `TC-BB-064`, `GUI-01`–`03`, `GUI-13`, `GUI-14`, `ACC-01`, `US-06`–`08`, `WTS-02`, `TC-API-UI-07`, `TC-API-UI-08`, `TC-SEC-01` | `unit/test_reg_decision_table.py` (`test_tc_bb_f03_01`–`04`)<br>`api/test_state_transition.py` (`test_TC_BB_060`, `064`)<br>`ui/test_ui_auth.py`<br>`ui/test_reg_accessibility_markup.py` (`test_acc_01_login_register`) | `D-009` (Moderate)<br>`D-026` (Major)<br>*(`D-007` Closed)* | **Fail** |
| **F-04** | **Login & Session (API)**<br>`POST /api/login` (`app.py::api_login`) | `API-LOG-01`–`07`, `WTS-02`, `TC-API-UI-07`, `TC-API-UI-08`, `TC-SEC-03`, `TC-SEC-15`, `TC-SEC-19`, `PERF-01`–`03` | `api/test_api_auth.py` (`test_api_log_01`–`07`) | `D-019` (Moderate)<br>`D-026` (Major)<br>`D-027` (Critical)<br>`D-033` (Moderate) | **Fail** |
| **F-05** | **Logout**<br>`GET /logout` (`app.py::logout`) | `TC-BB-060`–`068`, `GUI-04`, `ACC-16`, `US-28`, `US-29`, `WTS-08`, `TC-SEC-04`, `TC-SEC-12`, `TC-SEC-20` | `api/test_state_transition.py` (`test_TC_BB_062`, `068`)<br>`ui/test_ui_auth.py` | `D-028` (Moderate)<br>`D-032` (Moderate)<br>`D-035` (Minor)<br>`D-036` (Moderate) | **Fail** |
| **F-06** | **Page Protection (Web)**<br>`app.py::login_required_web` | `TC-BB-065`, `TC-WB-F11-01`, `WTS-01`, `WTS-08`, `TC-API-UI-28`–`30` | `api/test_state_transition.py` (`test_TC_BB_065` ×3)<br>`ui/test_ui_auth.py` | — | **Pass** |
| **F-07** | **Endpoint Protection (API)**<br>`app.py::login_required_api` | `API-TSK-GETALL-05`, `API-TSK-GETONE-03`, `API-TSK-POST-06`, `API-TSK-DEL-03`, `API-DASH-03`, `TC-API-UI-28`–`30`, `TC-SEC-16` | `api/test_ep_and_core_api.py` (unauthenticated guard assertions) | — | **Pass** |

---

### 2.2 Task Management — Web Pages (`F-08` to `F-14`)

| Req ID | Requirement Name & Route | Manual / Exploratory / Security Test Cases (Weeks 1–5) | Automated Week 6 Test Scripts (`06_Automation_Regression/tests/`) | Linked Defect IDs | Requirement Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **F-08** | **Create Task (Web)**<br>`GET/POST /tasks/new` (`app.py::new_task`) | `TC-BB-004`, `TC-BB-005`, `TC-BB-BVA-F08-01`, `02`, `TC-BB-069`, `GUI-01`, `GUI-02`, `GUI-07`, `GUI-13`, `GUI-17`, `COMP-04`, `ACC-01`, `US-09`–`11`, `US-30`, `WTS-03`, `WTS-VAL-03`–`05`, `TC-API-UI-09`–`12`, `TC-SEC-05`, `TC-SEC-06`, `TC-SEC-09`, `TC-SEC-10`, `TC-SEC-17` | `api/test_ep_and_core_api.py` (`test_tc_bb_005_web_whitespace_title_rejected`)<br>`api/test_state_transition.py` (`test_TC_BB_069`)<br>`ui/test_ui_tasks.py`<br>`ui/test_reg_accessibility_markup.py` (`test_acc_01_task_form`) | `D-006` (Major)<br>`D-009` (Moderate)<br>`D-010` (Major)<br>`D-011` (Major)<br>`D-012` (Moderate)<br>`D-021` (Moderate)<br>`D-029` (Major)<br>`D-030` (Minor) | **Fail** |
| **F-09** | **View Task List (Web)**<br>`GET /` (`app.py::index`) | `TC-BB-069`, `TC-WB-F11-01`–`03`, `GUI-05`, `GUI-08`, `GUI-10`, `GUI-12`, `GUI-18`, `ACC-03`, `ACC-14`, `US-22`, `US-27`, `WTS-03`, `TC-SEC-05`, `TC-SEC-12`, `TC-SEC-17` | `api/test_ep_and_core_api.py` (`test_tc_sec_05_stored_xss_escaped_in_task_list`)<br>`ui/test_reg_accessibility_markup.py` (`test_acc_03_grey_text_contrast`, `test_gui_08_empty_list_message_without_filters`) | `D-006` (Major)<br>`D-008` (Minor)<br>`D-010` (Major)<br>`D-012` (Moderate)<br>`D-015` (Moderate)<br>`D-032` (Moderate) | **Fail** |
| **F-10** | **Edit Task (Web)**<br>`GET/POST /tasks/<id>/edit` (`app.py::edit_task`) | `TC-BB-072`, `TC-BB-073`, `TC-BB-078`, `TC-BB-079`, `GUI-01`, `GUI-02`, `GUI-07`, `COMP-04`, `ACC-01`, `ACC-11`, `US-12`–`14`, `WTS-05`, `WTS-VAL-03`–`05`, `TC-API-UI-17`, `TC-API-UI-19`, `TC-SEC-06`, `TC-SEC-10`, `TC-SEC-22` | `api/test_state_transition.py` (`test_TC_BB_072`, `073`, `078`, `079`)<br>`ui/test_reg_accessibility_markup.py` (`test_acc_01_task_form`) | `D-006` (Major)<br>`D-009` (Moderate)<br>`D-011` (Major)<br>`D-018` (Minor)<br>`D-021` (Moderate)<br>`D-029` (Major)<br>`D-030` (Minor) | **Fail** |
| **F-11** | **Filter and Search (Web)**<br>`GET /?category=&status=&q=` (`app.py::index`) | `TC-BB-F11-01`–`04`, `TC-WB-F11-03`–`11`, `GUI-15`, `COMP-05`, `ACC-08`, `US-20`, `US-21`, `US-23`, `US-24`, `WTS-04`, `TC-API-UI-25`–`27`, `TC-SEC-08` | `unit/test_reg_decision_table.py` (`test_tc_bb_f11_01`–`04`)<br>`api/test_ep_and_core_api.py` (`test_tc_wb_f11_10_combined_web_filters`)<br>`ui/test_reg_accessibility_markup.py` (`test_acc_08_filter_controls_have_names`) | `D-009` (Moderate)<br>`D-014` (Minor) | **Fail** |
| **F-12** | **Mark Done / Reopen (Web)**<br>`POST /tasks/<id>/toggle` (`app.py::toggle_task`) | `TC-BB-070`, `TC-BB-071`, `TC-BB-077`, `GUI-12`, `ACC-02`, `ACC-03`, `US-15`–`17`, `WTS-06`, `TC-API-UI-20`, `TC-API-UI-21`, `TC-SEC-06`, `TC-SEC-22` | `api/test_state_transition.py` (`test_TC_BB_070`, `071`, `077`)<br>`ui/test_ui_tasks.py`<br>`api/test_ep_and_core_api.py` (`test_acc_02`)<br>`ui/test_reg_accessibility_markup.py` (`test_acc_02`, `test_acc_03`) | `D-015` (Moderate)<br>`D-016` (Moderate)<br>`D-029` (Major) | **Fail** |
| **F-13** | **Delete Task (Web)**<br>`POST /tasks/<id>/delete` (`app.py::delete_task_web`) | `TC-BB-074`–`076`, `GUI-11`, `COMP-06`, `ACC-11`, `US-19`, `US-30`, `WTS-07`, `WTS-VAL-06`, `TC-API-UI-24`, `TC-SEC-06`, `TC-SEC-10`, `TC-SEC-22` | `api/test_state_transition.py` (`test_TC_BB_074`, `075`)<br>`ui/test_ui_tasks.py`<br>`api/test_ep_and_core_api.py` (`test_tc_sec_22_web_delete_enforces_owner_check`) | `D-018` (Minor)<br>`D-029` (Major)<br>`D-030` (Minor) | **Fail** |
| **F-14** | **Urgency Badge Calculation**<br>`helpers.py::compute_urgency`, `app.py::row_to_task` | `TC-BB-006`–`010`, `TC-BB-BVA-F14-01`, `02`, `TC-BB-F14-01`–`04`, `TC-WB-F14-01`–`10`, `GUI-06`, `ACC-04`, `ACC-12`, `US-18`, `WTS-03`, `TC-API-UI-13`–`15` | `unit/test_ep_urgency_unit.py` (6 tests)<br>`unit/test_reg_decision_table.py` (`test_tc_bb_f14_01`–`04`, `test_reg_d001_01`)<br>`api/test_ep_and_core_api.py` (`test_tc_wb_f14_10`)<br>`ui/test_reg_accessibility_markup.py` (`test_acc_12`) | `D-001` (Moderate)<br>`D-006` (Major)<br>*(`D-002`, `D-003` Dup)* | **Fail** |

---

### 2.3 Dashboard (`F-15` to `F-16`)

| Req ID | Requirement Name & Route | Manual / Exploratory / Security Test Cases (Weeks 1–5) | Automated Week 6 Test Scripts (`06_Automation_Regression/tests/`) | Linked Defect IDs | Requirement Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **F-15** | **Dashboard (Web)**<br>`GET /dashboard` (`app.py::dashboard`, `helpers.py::completed_in_last_n_days`) | `TC-BB-BVA-F15-01`, `TC-WB-F15-01`–`07`, `GUI-09`, `US-25`, `US-26`, `WTS-06`, `TC-SEC-12` | `api/test_state_transition.py` (`test_TC_BB_069`–`075` dashboard counter assertions) | `D-001` (Moderate)<br>`D-005` (Moderate)<br>`D-032` (Moderate) | **Fail** |
| **F-16** | **Dashboard (API)**<br>`GET /api/dashboard` (`app.py::api_dashboard`) | `API-DASH-01`–`04`, `API-DD-03`–`10`, `TC-API-UI-14`, `PERF-01`–`03` | `unit/test_reg_decision_table.py` (`test_reg_d001_02`)<br>`api/test_reg_api_delete_dashboard.py` (`test_api_dd_03`–`10`) | `D-001` (Moderate)<br>`D-005` (Moderate)<br>`D-006` (Major) | **Fail** |

---

### 2.4 Task & Category JSON API (`F-17` to `F-22`)

| Req ID | Requirement Name & Route | Manual / Exploratory / Security Test Cases (Weeks 1–5) | Automated Week 6 Test Scripts (`06_Automation_Regression/tests/`) | Linked Defect IDs | Requirement Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **F-17** | **List Categories (API)**<br>`GET /api/categories` (`app.py::api_categories`) | `API-CAT-01`–`03`, `TC-SEC-16`, `PERF-01`–`03` | `api/test_state_transition.py` (`category_id` lookup helper) | — | **Pass** |
| **F-18** | **List Tasks (API)**<br>`GET /api/tasks` (`app.py::api_list_tasks`) | `API-TSK-GETALL-01`–`07`, `TC-API-UI-25`–`27`, `TC-SEC-07`, `TC-SEC-14`, `TC-SEC-18`, `PERF-01`–`03` | `api/test_ep_and_core_api.py` (`test_tc_sec_07_sql_injection_in_search_handled`) | `D-006` (Major)<br>`D-014` (Minor)<br>`D-020` (Critical)<br>`D-034` (Moderate) | **Fail** |
| **F-19** | **Create Task (API)**<br>`POST /api/tasks` (`app.py::api_create_task`) | `API-TSK-POST-01`–`08`, `TC-API-UI-09`–`12`, `TC-API-UI-15`, `TC-API-UI-16`, `PERF-01`–`03` | `api/test_api_auth.py` (`test_tc_bb_bva_f08_01`, `02`)<br>`api/test_ep_and_core_api.py` (`test_tc_bb_004`, `test_tc_wb_f14_10`) | `D-006` (Major)<br>`D-012` (Moderate)<br>`D-019` (Moderate)<br>`D-021` (Moderate) | **Fail** |
| **F-20** | **Get One Task (API)**<br>`GET /api/tasks/<id>` (`app.py::api_get_task`) | `API-TSK-GETONE-01`–`05` | `api/test_ep_and_core_api.py` (task read assertions) | — | **Pass** |
| **F-21** | **Update Task (API)**<br>`PUT /api/tasks/<id>` (`app.py::api_update_task`) | `API-TSK-PUT-01`–`07`, `TC-API-UI-17`–`22` | `api/test_ep_and_core_api.py` (`test_api_tsk_put_03_empty_title_on_edit_rejected`) | `D-022` (Major)<br>`D-023` (Moderate) | **Fail** |
| **F-22** | **Delete Task (API)**<br>`DELETE /api/tasks/<id>` (`app.py::api_delete_task`) | `API-TSK-DEL-01`–`05`, `API-DD-01`–`03`, `TC-API-UI-23`, `TC-API-UI-24`, `TC-SEC-21`, `PERF-01`–`03` | `api/test_ep_and_core_api.py` (`test_tc_sec_21_cross_user_delete_blocked`)<br>`api/test_reg_api_delete_dashboard.py` (`test_api_dd_01`–`03`) | `D-024` (Minor)<br>`D-025` (Critical) | **Fail** |

---

### 2.5 Cross-Cutting & Non-Functional Requirements (`NFR-01` to `NFR-03`)

| Req ID | Requirement Name & Scope | Manual / Exploratory / Security Test Cases (Weeks 1–5) | Automated Week 6 Test Scripts (`06_Automation_Regression/tests/`) | Linked Defect IDs | Requirement Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **NFR-01** | **Responsive Reflow & Cross-Browser UI**<br>All Web Templates (`base.html`, `style.css`) | `GUI-01`, `GUI-04`, `GUI-16`, `COMP-01`–`09`, `ACC-05`–`07`, `ACC-09`, `ACC-10`, `ACC-13`, `ACC-16`, `US-31` | `ui/test_reg_accessibility_markup.py` (`test_acc_05`, `test_acc_07`, `test_acc_09`) | `D-017` (Moderate)<br>*(`D-007` Closed)* | **Fail** |
| **NFR-02** | **Server Configuration & Debug Hardening**<br>Application Entry Point (`app.py::__main__`) | `TC-SEC-11` | — *(Static source inspection)* | `D-031` (Major) | **Fail** |
| **NFR-03** | **API Throughput & Latency Under Load**<br>REST API Endpoints (`locustfile.py`) | `PERF-01` (10 users), `PERF-02` (50 users), `PERF-03` (100 users) | — *(Locust load benchmark)* | `PERF-OBS-01`<br>`PERF-OBS-02` | **Pass (with Observations)** |

---

## 3. Reverse Traceability: Defect-to-Requirement Mapping (`D-001` to `D-036`)

Every defect in the central log traces back to one or more requirements and test cases above:

| Defect ID | Severity | Status | Linked Requirement(s) | Primary Triggering Test Case(s) |
| :---: | :---: | :--- | :--- | :--- |
| **D-001** | Moderate | Confirmed | `F-14`, `F-15`, `F-16` | `TC-BB-008`, `TC-BB-BVA-F14-02`, `TC-BB-F14-02`, `TC-WB-F14-04`, `API-DASH-01` |
| **D-002** | Moderate | Closed (Dup of `D-001`) | `F-14` | `TC-BB-BVA-F14-02` |
| **D-003** | Moderate | Closed (Dup of `D-001`) | `F-14` | `TC-BB-BVA-F14-02` |
| **D-004** | Major | Confirmed | `F-01`, `F-02` | `TC-BB-BVA-F01-02`, `US-05`, `TC-API-UI-02` |
| **D-005** | Moderate | Confirmed | `F-15`, `F-16` | `TC-BB-BVA-F15-01`, `TC-WB-F15-03`, `API-DD-08` |
| **D-006** | Major | Confirmed | `F-08`, `F-09`, `F-10`, `F-14`, `F-16`, `F-18`, `F-19` | `TC-WB-F14-10`, `WTS-VAL-04`, `API-TSK-POST-04`, `API-DD-10`, `TC-SEC-17` |
| **D-007** | Minor | Closed (Not reproducible) | `NFR-01` (`F-01`, `F-03`, `F-08`, `F-10`) | `GUI-01` |
| **D-008** | Minor | Confirmed | `F-09` | `GUI-08`, `US-22` |
| **D-009** | Moderate | Confirmed | `F-01`, `F-03`, `F-08`, `F-10`, `F-11` | `GUI-02`, `ACC-01`, `ACC-08` |
| **D-010** | Major | Confirmed | `F-08`, `F-09` | `GUI-10`, `TC-SEC-05` |
| **D-011** | Major | Confirmed | `F-08`, `F-10` | `TC-BB-005`, `GUI-17`, `US-11`, `WTS-VAL-03`, `TC-SEC-09` |
| **D-012** | Moderate | Confirmed | `F-08`, `F-09`, `F-19` | `GUI-18`, `US-11`, `TC-API-UI-12` |
| **D-013** | Major | Confirmed | `F-01`, `F-02` | `TC-BB-002`, `US-04`, `WTS-VAL-02`, `API-REG-09`, `TC-SEC-02` |
| **D-014** | Minor | Confirmed | `F-11`, `F-18` | `TC-WB-F11-11`, `US-24`, `TC-API-UI-25`, `TC-API-UI-26`, `TC-SEC-08` |
| **D-015** | Moderate | Confirmed | `F-09`, `F-12` | `ACC-03` |
| **D-016** | Moderate | Confirmed | `F-12` | `ACC-02`, `US-16` |
| **D-017** | Moderate | Confirmed | `NFR-01` (All Web Pages) | `ACC-09`, `ACC-16` |
| **D-018** | Minor | Open | `F-10`, `F-13` | `ACC-11` |
| **D-019** | Moderate | Confirmed | `F-02`, `F-04`, `F-19` | `API-REG-08`, `API-LOG-06`, `API-TSK-POST-07`, `TC-API-UI-06` |
| **D-020** | Critical | Confirmed | `F-18` | `API-TSK-GETALL-04`, `TC-API-UI-27`, `TC-SEC-07`, `TC-SEC-14` |
| **D-021** | Moderate | Confirmed | `F-08`, `F-10`, `F-19` | `WTS-VAL-05`, `API-TSK-POST-08`, `TC-API-UI-16` |
| **D-022** | Major | Confirmed | `F-21` | `API-TSK-PUT-03`, `TC-API-UI-18` |
| **D-023** | Moderate | Confirmed | `F-21` | `API-TSK-PUT-06`, `TC-API-UI-22` |
| **D-024** | Minor | Confirmed | `F-22` | `API-TSK-DEL-02`, `API-DD-02`, `TC-API-UI-23` |
| **D-025** | Critical | Confirmed | `F-22` | `API-TSK-DEL-05`, `API-DD-01`, `TC-API-UI-24`, `TC-SEC-21` |
| **D-026** | Major | Confirmed | `F-03`, `F-04` | `TC-SEC-01`, `TC-SEC-19` |
| **D-027** | Critical | Confirmed | `F-04` | `TC-SEC-03` |
| **D-028** | Moderate | Confirmed | `F-05` | `TC-SEC-04` |
| **D-029** | Major | Confirmed | `F-08`, `F-10`, `F-12`, `F-13` | `WTS-VAL-06`, `TC-SEC-06` |
| **D-030** | Minor | Confirmed | `F-08`, `F-10`, `F-13` | `TC-SEC-10` |
| **D-031** | Major | Confirmed | `NFR-02` (Server Config) | `TC-SEC-11` |
| **D-032** | Moderate | Confirmed | `F-05`, `F-09`, `F-15` | `US-29`, `TC-SEC-12` |
| **D-033** | Moderate | Confirmed | `F-04` | `TC-SEC-15` |
| **D-034** | Moderate | Confirmed | `F-18` | `TC-SEC-18` |
| **D-035** | Minor | Confirmed | `F-05` | `TC-SEC-20` |
| **D-036** | Moderate | Open *(Related to `D-032`)* | `F-05` | `TC-BB-067` |