# Week 6: Automated Test Execution Report

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Test Environment:** Windows, Python `3.10.11`, PyTest `9.2.0`, Selenium WebDriver (Headless Chrome)  
**Evidence Logs:** `06_Automation_Regression/logs/full_suite.log`, `06_Automation_Regression/logs/regression_suite.log`

---

## 1. Execution Summary

| Suite / Layer | Command | Total | Passed | Failed | Errors | Duration | Log File |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Unit (`tests/unit/`)** | `pytest 06_Automation_Regression/tests/unit -v` | 3 | 2 | 1 | 0 | ~0.05s | `logs/full_suite.log` |
| **API (`tests/api/`)** | `pytest 06_Automation_Regression/tests/api -v` | 18 | 15 | 3 | 0 | ~1.10s | `logs/full_suite.log` |
| **Selenium UI (`tests/ui/`)** | `pytest 06_Automation_Regression/tests/ui -v` | 2 | 2 | 0 | 0 | ~10.43s | `logs/full_suite.log` |
| **Full Automated Suite** | `pytest 06_Automation_Regression/tests/ -v` | **23** | **19** | **4** | **0** | **12.36s** | `logs/full_suite.log` |
| **Regression Suite (`-m regression`)** | `pytest 06_Automation_Regression/tests/ -m regression -v` | **3** *(20 deselected)* | **1** | **2** | **0** | **0.68s** | `logs/regression_suite.log` |

---

## 2. Test-by-Test Breakdown

### A. Unit Tests (`tests/unit/test_bva_unit.py`)

| Test Function | Manual TC ID | Regression Marker | Status | Notes |
| :--- | :--- | :---: | :---: | :--- |
| `test_tc_bb_bva_f01_01_seven_char_password` | `TC-BB-BVA-F01-01` | No | **PASSED** | Rejects 7-character password (`Pass123`). |
| `test_tc_bb_bva_f01_02_eight_char_password` | `TC-BB-BVA-F01-02` | Yes | **FAILED** | Caught **Defect D-004** (8-character password rejected). |
| `test_tc_bb_bva_f01_03_nine_char_password` | `TC-BB-BVA-F01-03` | No | **PASSED** | Accepts 9-character password (`Pass12345`). |

### B. API Tests (`tests/api/test_api_auth.py`)

| Test Function | Manual TC ID | Regression Marker | Status | Notes |
| :--- | :--- | :---: | :---: | :--- |
| `test_api_reg_01_valid_registration` | `API-REG-01` / `TC-BB-001` | No | **PASSED** | Returns `201 Created` with user ID and username. |
| `test_api_reg_02_trimmed_username` | `API-REG-02` | No | **PASSED** | Strips leading/trailing whitespace on registration. |
| `test_api_reg_03_invalid_username` | `API-REG-03` | No | **PASSED** | Returns `400` for usernames under 3 characters. |
| `test_api_reg_04_invalid_password` | `API-REG-04` | No | **PASSED** | Returns `400` for short passwords. |
| `test_api_reg_05_missing_username` | `API-REG-05` | No | **PASSED** | Returns `400` when `username` is omitted. |
| `test_api_reg_06_missing_password` | `API-REG-06` | No | **PASSED** | Returns `400` when `password` is omitted. |
| `test_api_reg_07_empty_json` | `API-REG-07` | No | **PASSED** | Returns `400` on empty JSON body. |
| `test_api_reg_08_wrong_type_username` | `API-REG-08` | No | **FAILED** | Caught **Defect D-019** (`AttributeError` / HTTP 500 on integer username). |
| `test_api_reg_09_duplicate_username` | `API-REG-09` / `TC-BB-002` | Yes | **FAILED** | Caught **Defect D-013** (duplicate username returns `201` instead of `400`/`409`). |
| `test_api_log_01_valid_login` | `API-LOG-01` | No | **PASSED** | Returns `200` and sets valid session cookie. |
| `test_api_log_02_wrong_password` | `API-LOG-02` / `TC-BB-003` | No | **PASSED** | Returns `401 invalid credentials`. |
| `test_api_log_03_nonexistent_user` | `API-LOG-03` | No | **PASSED** | Returns `401` for unregistered username. |
| `test_api_log_04_missing_password` | `API-LOG-04` | No | **PASSED** | Returns `401` when password is missing. |
| `test_api_log_05_empty_json` | `API-LOG-05` | No | **PASSED** | Returns `401` on empty JSON body. |
| `test_api_log_06_wrong_type_username` | `API-LOG-06` | No | **FAILED** | Caught **Defect D-019** (`AttributeError` / HTTP 500 on integer username). |
| `test_api_log_07_non_json_body` | `API-LOG-07` | No | **PASSED** | Returns `401` on `text/plain` payload. |
| `test_tc_bb_bva_f08_01_empty_task_title` | `TC-BB-BVA-F08-01` | Yes | **PASSED** | Rejects empty task title with `400`. |
| `test_tc_bb_bva_f08_02_single_char_task_title` | `TC-BB-BVA-F08-02` | No | **PASSED** | Accepts 1-character task title with `201`. |

### C. Selenium Browser UI Tests (`tests/ui/`)

| Test Function | Manual TC ID | Regression Marker | Status | Notes |
| :--- | :--- | :---: | :---: | :--- |
| `test_wts_01_02_08_auth_lifecycle` | `WTS-01`, `WTS-02`, `WTS-08` | No | **PASSED** | Verified register, logout redirect, login, and logout in headless Chrome. |
| `test_wts_03_06_07_task_lifecycle_and_confirm_dialog` | `WTS-03`, `WTS-06`, `WTS-07`, `TC-BB-076`, `GUI-11` | No | **PASSED** | Verified task creation, toggle completion, Cancel confirm alert, and OK delete alert. |

---

## 3. Failed Tests & Defect Handoff (For Order 6)

All 4 failures in `logs/full_suite.log` are genuine, reproducible application defects rather than test script errors:

| Failed Test | Manual TC ID | Linked Defect | Root Cause / Observed Behavior |
| :--- | :--- | :---: | :--- |
| `test_tc_bb_bva_f01_02_eight_char_password` | `TC-BB-BVA-F01-02` | **D-004** | `is_valid_password("Pass1234")` returns `False` (`len(pw) > 8` instead of `>= 8`), rejecting valid 8-character passwords. |
| `test_api_reg_09_duplicate_username` | `API-REG-09` / `TC-BB-002` | **D-013** | `POST /api/register` allows duplicate usernames and returns `201 Created` instead of rejecting with `400` or `409`. |
| `test_api_reg_08_wrong_type_username` | `API-REG-08` | **D-019** | `POST /api/register` calls `.strip()` directly on `data.get("username")`, raising `AttributeError: 'int' object has no attribute 'strip'` (HTTP 500) when given an integer. |
| `test_api_log_06_wrong_type_username` | `API-LOG-06` | **D-019** | `POST /api/login` calls `.strip()` directly on `data.get("username")`, raising `AttributeError: 'int' object has no attribute 'strip'` (HTTP 500) when given an integer. |