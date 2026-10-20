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
| **Passed Test Cases** | 16 | 80.00% |
| **Failed Test Cases** | 4 | 20.00% |
| **Block / Not Run Test Cases** | 0 | 0.00% |

- **Execution Completion Rate:** 100% (20 / 20 executed)
- **Overall Pass Rate:** **80.00%** 
- **Overall Failure Rate:** **20.00%** 

### Breakdown by Technique
- **Decision Table (Nafiesa):** 12 Executed | 11 Passed | 1 Failed
- **Boundary Value Analysis (Nisrina):** 8 Executed | 5 Passed | 3 Failed

---

## 2. Defect Breakdown & Summary

| Defect ID | Associated Test Case | Feature / Area | Severity | Priority | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **D-001** | `TC-BB-F14-02` | F-14: Urgency Badge | Moderate | Medium | Open |
| **D-003** | `TC-BB-BVA-F14-02` | F-14: Urgency Badge | Moderate | Medium | Open |
| **D-004** | `TC-BB-BVA-F01-02` | F-01: Register (web) | High | High | Open |
| **D-005** | `TC-BB-BVA-F15-01` | F-15: Dashboard (web) | Moderate | Medium | Open |

### Defect Distribution Metrics
- **Total Defects Found:** 4
- **Defects by Status:** Open (4), Resolved (0)
- **Defects by Source / Feature:** 
  - F-01 (Register): 1 defect (`D-004`)
  - F-14 (Urgency Badge): 2 defects (`D-001`, `D-003`)
  - F-15 (Dashboard): 1 defect (`D-005`)

---

## 3. Week 1 Summary & Conclusion
- **Test Completion:** All planned black-box test cases for Week 1 across Decision Table and BVA (20/20) have been fully executed.
- **Quality Status:** Core functionality for Login (F-03), Search/Filter (F-11), and basic Task Creation (F-08) passed boundary constraints successfully.
- **Key Risks Identified:** 
  1. **Task Urgency Logic:** Defects (`D-001`, `D-003`) logged where tasks due exactly today incorrectly show "Overdue".
  2. **Boundary Validation Flaws:** Registration incorrectly rejects valid 8-character passwords (`D-004`), and the dashboard's 7-day counter entirely excludes tasks completed exactly 7 days ago (`D-005`).