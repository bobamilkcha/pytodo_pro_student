# Week 1 Testing Metrics Summary - PyTodo Pro

**Contributors:** 
- Nafiesa (Defect & Metrics Coordinator - Decision Table) 
- Nisrina (Automation/Tool Coordinator - BVA)

---

## 1. Test Execution Metrics (Combined)

| Metric Category | Count | Percentage |
| :--- | :---: | :---: |
| **Total Test Cases Planned** | 20 | 100% |
| **Total Test Cases Executed** | 20 | 100% |
| **Passed Test Cases** | 17 | 85.00% |
| **Failed Test Cases** | 3 | 15.00% |
| **Block / Not Run Test Cases** | 0 | 0.00% |

- **Execution Completion Rate:** 100% (20 / 20 executed)
- **Overall Pass Rate:** **85.00%** 
- **Overall Failure Rate:** **15.00%** 

### Breakdown by Technique
- **Decision Table (Nafiesa):** 12 Executed | 11 Passed | 1 Failed
- **Boundary Value Analysis (Nisrina):** 8 Executed | 6 Passed | 2 Failed

---

## 2. Defect Breakdown & Summary

| Defect ID | Associated Test Case | Feature / Area | Severity | Priority | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **D-001** | `TC-BB-F14-02` | F-14: Urgency Badge | Moderate | Medium | Open |
| **D-002** | `TC-BB-BVA-005` | API Pagination | Low | Low | Open |
| **D-003** | `TC-BB-BVA-008` | Task Urgency Logic | Moderate | Medium | Open |

### Defect Distribution Metrics
- **Total Defects Found:** 3
- **Defects by Status:** Open (3), Resolved (0)
- **Defects by Source / Feature:** 
  - F-03 (Login): 0 defects
  - F-11 (Filter & Search): 0 defects
  - API Pagination: 1 defect (`D-002`)
  - F-14 / Task Urgency Logic: 2 defects (`D-001`, `D-003`)

---

## 3. Week 1 Summary & Conclusion
- **Test Completion:** All planned black-box test cases for Week 1 across Decision Table and BVA (20/20) have been fully executed.
- **Quality Status:** The core functionality for Login (F-03) and Search/Filter (F-11) passed successfully. UI task creation boundary limits were also handled correctly.
- **Key Risks Identified:** 
  1. **Task Urgency / Date Logic:** Multiple defects (`D-001`, `D-003`) logged regarding date boundary logic, specifically where tasks due exactly today are incorrectly labeled as "Overdue".
  2. **API Input Validation:** The `/api/tasks` endpoint fails to validate `page=0` inputs, returning a blank response rather than a standard 400 Bad Request error (`D-002`).