# Boundary Value Analysis (BVA) Test Designs

**Designer:** Nisrina (Automation/Tool Coordinator)
**Technique Justification:** BVA targets the edge cases of input ranges (minimum, just below minimum, maximum, just above maximum) to catch logic errors at the boundaries.

## Test Cases

| Test ID | Feature | Boundary Condition | Input Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-BB-BVA-F01-01** | F-01: Register (web) | Password: Just below minimum | `Password: "1234567"` (7 chars) | Rejects registration with validation error. |
| **TC-BB-BVA-F01-02** | F-01: Register (web) | Password: Minimum valid length | `Password: "12345678"` (8 chars) | Registration successful. |
| **TC-BB-BVA-F01-03** | F-01: Register (web) | Password: Just above minimum | `Password: "123456789"` (9 chars) | Registration successful. |
| **TC-BB-BVA-F08-01** | F-08: Create task | Title: Just below minimum | `Title: ""` (0 chars) | Rejects creation with validation error. |
| **TC-BB-BVA-F08-02** | F-08: Create task | Title: Minimum valid length | `Title: "A"` (1 char) | Task created successfully. |
| **TC-BB-BVA-F14-01** | F-14: Urgency badge | Date: Just before today | `Due Date: [Yesterday]` | Badge displays as "Overdue". |
| **TC-BB-BVA-F14-02** | F-14: Urgency badge | Date: Exactly today | `Due Date: [Today]` | Badge displays as "Due Today". |
| **TC-BB-BVA-F15-01** | F-15: Dashboard | Date: Exact 7-day cutoff | Task marked done exactly 7 days ago | Task is included in the "completed in last 7 days" counter. |