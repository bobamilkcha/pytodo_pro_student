# Central Defect Log - PyTodo Pro

## Summary
- **Total Defects Logged:** 2
- **Open Defects:** 2
- **Resolved Defects:** 0

---

## Defect Details

### Defect ID: D-001
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** F-14 Urgency Badge
- **Environment:** Localhost (http://127.0.0.1:5000), Browser: Chrome / Edge
- **Preconditions:** User is logged in and viewing the task list or dashboard.
- **Steps to Reproduce:**
  1. Navigate to Create Task page (`/tasks/new`).
  2. Create an open task titled "Mock Interview" with **today's date** as the due date.
  3. Save the task and view the task list/dashboard.
- **Expected Result:** The task should display a "Due Today" urgency badge.
- **Actual Result:** The task displays an "Overdue" badge (red label).
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Open
- **Evidence:** `/evidence/TC-BB-F14-02.png`
- **Related Test Case:** `TC-BB-F14-02`

### Defect ID: D-002
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** Task Urgency Logic (`helpers.py`)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in.
- **Steps to Reproduce:**
  1. Navigate to the Create Task page (`/tasks/new`).
  2. Create an open task and set the due date exactly to **today's date**.
  3. Save the task and view the task list or dashboard.
- **Expected Result:** The task should display a **"Due Today"** badge.
- **Actual Result:** The task displays an **"Overdue"** badge.
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Open
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F14-02-2_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F14-02`