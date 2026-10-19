# Boundary Value Analysis (BVA) Test Designs

**Designer:** Nisrina (Automation/Tool Coordinator)
**Technique Justification:** BVA targets the edge cases of input ranges (minimum, just below minimum, maximum, just above maximum) where logic errors and database crashes most frequently occur.

## Test Cases

| Test ID | Feature / Endpoint | Boundary Condition | Input Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-BB-BVA-001** | Create Task (Web UI) | Title: Minimum valid length | `Title: "A"` (1 character) | Task is created successfully and appears in the list. |
| **TC-BB-BVA-002** | Create Task (Web UI) | Title: Just below minimum | `Title: ""` (0 characters / blank) | Application rejects the task and displays a validation error message. |
| **TC-BB-BVA-003** | Create Task (API) | Title: Extremely long string | `Title: [String of 300 characters]` | Application gracefully handles or truncates the input without throwing a 500 Internal Server Error. |
| **TC-BB-BVA-004** | API Pagination | Page: Minimum valid | `GET /api/tasks?page=1` | Returns the first page of the task list. |
| **TC-BB-BVA-005** | API Pagination | Page: Just below minimum | `GET /api/tasks?page=0` | API returns a clear 400 Bad Request error or safely defaults to page 1. |
| **TC-BB-BVA-006** | API Pagination | Per Page: Below minimum | `GET /api/tasks?per_page=0` | API returns a 400 Bad Request error or safely defaults to standard pagination. |
| **TC-BB-BVA-007** | Task Urgency Logic | Date: Boundary to Overdue | `Due Date: [Yesterday's Date]` | System categorizes and labels the task strictly as "Overdue". |
| **TC-BB-BVA-008** | Task Urgency Logic | Date: Boundary to Due Today | `Due Date: [Today's Date]` | System categorizes and labels the task strictly as "Due Today". |
