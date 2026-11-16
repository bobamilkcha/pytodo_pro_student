# Week 2 Testing Metrics Summary - PyTodo Pro  (not done yet)

**Prepared by:** (Defect & Metrics Coordinator)
**Scope:** White-box testing of the 4 units in `selected_units.md`

**Contributors:**
- QA/Test Lead - `toggle_task`
- Aida (Test Design Coordinator) - `index`
- Nisrina (Automation/Tool Coordinator) - `completed_in_last_n_days`
- Nafiesa (Defect & Metrics Coordinator) - `compute_urgency`

---

## 1. Unit Traceability Matrix

This matrix links each selected unit to its feature, Week 1 risk, tests, results and defects.

| Unit | File (lines) | Feature | Week 1 risk | Owner | Test file | Cases | Passed | Failed | Statement cov. | Branch cov. | Defects | Status |
| :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `index` | app.py (189-222) | F-09, F-11 | M | Aida | `index/tests/test_index.py` | 11 | 11 | 0 | 100% | 100% (8/8) | None | Done |
| `compute_urgency` | helpers.py (12-39) | F-14 | H | Nafiesa | `compute_urgency/tests/test_compute_urgency.py` | 10 | 8 | 2 | 100% | 100% (8/8) | D-001, D-006 | Done |
| `completed_in_last_n_days` | helpers.py (61-75) | F-15, F-16 | H | Nisrina | `test_helpers.py` | 7 | 7 | 0 | 100% | 100% (4/4) | D-005 | Done |
| `toggle_task` | app.py (269-281) | F-12 | M | QA/Test Lead | Not in repo | 0 | 0 | 0 | 0% | 0% (0/2) | - | **Not started** |

---

## 2. Test Execution Metrics (Week 2)

| Metric Category | Count | Percentage |
| :--- | :---: | :---: |
| **Units Planned** | 4 | 100% |
| **Units Tested** | 3 | 75.00% |
| **Test Cases Executed** | 28 | - |
| **Passed Test Cases** | 26 | 92.86% |
| **Failed Test Cases** | 2 | 7.14% |
| **Block / Not Run Test Cases** | 0 | 0.00% |

- **Unit Completion Rate:** 75% (3 / 4 units)
- **Overall Pass Rate:** **92.86%** (26 / 28)
- **Overall Failure Rate:** **7.14%** (2 / 28)

Note: `compute_urgency` has 10 test cases but 13 pytest runs, because TC-WB-F14-09 uses 4 data values. We count it as 1 test case.

### Breakdown by Unit
- **`index` (Aida):** 11 Executed | 11 Passed | 0 Failed
- **`compute_urgency` (Nafiesa):** 10 Executed | 8 Passed | 2 Failed
- **`completed_in_last_n_days` (Nisrina):** 7 Executed | 7 Passed | 0 Failed
- **`toggle_task` (QA/Test Lead):** 0 Executed. Tests not yet pushed.

---

## 3. Coverage Metrics

| Scope | Statements | Statement % | Branches | Branch % |
| :--- | :---: | :---: | :---: | :---: |
| `index` | 22 / 22 | 100% | 8 / 8 | 100% |
| `compute_urgency` | 11 / 11 | 100% | 8 / 8 | 100% |
| `completed_in_last_n_days` | 7 / 7 | 100% | 4 / 4 | 100% |
| `toggle_task` | 0 / 8 | 0% | 0 / 2 | 0% |
| `helpers.py` (whole file) | 28 / 31 | 90.3% | 15 / 18 | 83.3% |
| `app.py` (whole file) | 164 / 299 | 54.8% | 26 / 64 | 40.6% |

How we measured: all Week 2 tests were run together on 16 Nov 2026 with:

```
pytest 02_White_Box_Coverage --cov=helpers --cov=app --cov-branch
```

The function figures come from the coverage JSON report. The whole-file figures for `app.py` are low because most routes (API, dashboard, register) were not selected for Week 2. They are not a target for this week.

The uncovered lines in `helpers.py` (48, 55, 57) belong to `is_valid_username` and `is_valid_password`. These were not selected for Week 2.

---

## 4. Defect Metrics

### 4.1 Defects linked to Week 2

| Defect ID | Associated Test Case | Unit | Severity | Priority | Status | Week 2 finding |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **D-001** | `TC-WB-F14-04` | `compute_urgency` | Moderate | Medium | Open | Confirmed. There is no "Due Today" branch in the code, so coverage cannot find it. |
| **D-005** | `TC-WB-F15-03` (`test_completed_exactly_n_days_ago`) | `completed_in_last_n_days` | Moderate | Medium | Open | Confirmed. Root cause is `age.days < n` on line 75. It should be `<=`. |
| **D-006** | `TC-WB-F14-10` | `compute_urgency` | [set] | [set] | **New** | A bad `due_date` saved through the API makes `GET /api/tasks` return HTTP 500. |

### 4.2 Defect Distribution (Week 1 + Week 2)

| Metric | Count |
| :--- | :---: |
| **Unique defects found** | 4 |
| **Found in Week 1** | 3 (D-001, D-004, D-005) |
| **Found in Week 2** | 1 (D-006) |
| **Open** | 4 |
| **Resolved** | 0 |
| **Duplicate reports** | 3 (D-002, D-003 and DEF-001 are the same bug as D-001) |

- **By feature:** F-14 Urgency badge: 2 (D-001, D-006) | F-01 Register: 1 (D-004) | F-15 Dashboard: 1 (D-005)
- **By technique that found it:** Black-box: 3 | White-box: 1

---

## 5. Cumulative Execution (Week 1 + Week 2)

`Week1_Metrics.md` only counted the Decision Table and BVA cases. This table adds the EP and State Transition cases so the totals are complete.

| Technique | Owner | Planned | Executed | Passed | Failed | Not Run |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Decision Table | Nafiesa | 12 | 12 | 11 | 1 | 0 |
| BVA | Nisrina | 8 | 8 | 5 | 3 | 0 |
| EP | Aida | 10 | 10 | 9 | 1 | 0 |
| State Transition | QA/Test Lead | 20 | 0 | 0 | 0 | 20 |
| White-box | All | 28 | 28 | 26 | 2 | 0 |
| **Total** | | **78** | **58** | **51** | **7** | **20** |

- **Execution Rate:** 74.36% (58 / 78)
- **Pass Rate of executed cases:** 87.93% (51 / 58)

---

## 6. Outstanding Actions

| Owner | Action |
| :--- | :--- |
| QA/Test Lead | Run the 20 State Transition cases (TC-BB-060 to TC-BB-079) and fill in Actual Result and Status. |
| QA/Test Lead | Push white-box tests and write-up for `toggle_task`. |
| Nafiesa | Add D-006 to `01_Black_Box/defect_log.md`. |
| Nafiesa | Mark D-002, D-003 and DEF-001 as Duplicate of D-001 in the defect log. |
| Aida, Nisrina | Add TC IDs to the docstrings in `test_index.py` and `test_helpers.py`, so each test can be traced. |

---

## 7. Week 2 Summary & Conclusion

- **Progress:** 3 of the 4 selected units are fully tested. Each reached 100% statement and branch coverage. `toggle_task` has not started.
- **Quality status:** 26 of 28 white-box tests passed. Both failures are in `compute_urgency` and point to real defects.
- **Key findings:**
  1. **Full coverage does not mean correct code.** `compute_urgency` reached 100% branch coverage but still has two defects. D-001 is missing logic, so there is no branch for a tool to report.
  2. **New defect D-006.** The API accepts any text as a due date. The task list then crashes for that user.
  3. **D-005 root cause confirmed.** White-box testing found the exact line (75), which black-box testing could not show.
- **Risk for next week:** F-12 (Mark done / reopen) has no executed tests in Week 1 or Week 2, so its quality is unknown.
