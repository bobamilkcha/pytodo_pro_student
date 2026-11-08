# Automation & Coverage Report (Week 2)
**Role:** Automation/Tool Coordinator (Nisrina)

## 1. Environment Setup
- **Testing Framework:** `pytest`
- **Coverage Tool:** `pytest-cov`
- **Configuration:** Both libraries installed in the local virtual environment and `requirements.txt` updated and pushed to the repository.

## 2. Test Implementation & Execution
- **Target Function:** `completed_in_last_n_days` (Unit 3, `helpers.py`)
- **Execution Strategy:** Designed and executed 6 PyTest cases in `test_helpers.py` to achieve full branch and boundary coverage. 
- **Time/State Management:** Handled dynamically changing dates by overriding the `now` parameter in tests, ensuring stable execution without relying on system clock manipulation.

## 3. Coverage Results
See `coverage_evidence.txt` for the raw output.
- **Module Coverage (`helpers.py`):** 90% overall statement coverage.
- **Unit 3 Coverage:** 100% coverage achieved for `completed_in_last_n_days`. 
- **Uncovered Lines Justification:** Lines 48, 55, and 57 remain uncovered. These belong to `is_valid_username` and `is_valid_password`, which were explicitly excluded from the Week 2 testing scope.

## 4. Automation Findings for Defect Coordination
- **Failed Tests:** Two tests failed in `test_compute_urgency.py`. These failures successfully captured the known "Due Today" bug (Defect D-003), proving the automation suite is effectively catching expected logic errors.
- **Logic Verification:** The boundary test for exactly 7 days ago correctly returned `False`, technically confirming the root cause of Defect D-005 (the application uses strict `<` instead of `<=` for the day boundary).