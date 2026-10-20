# Central Defect Log - PyTodo Pro

## Summary
- **Total Defects Logged:** 5
- **Open Defects:** 5
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

### Defect ID: D-003
- **Title:** Task due today incorrectly displays "Overdue" badge instead of "Due Today"
- **Affected Feature:** F-14: Urgency badge
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
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F14-02_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F14-02`

### Defect ID: D-004
- **Title:** Registration incorrectly rejects valid 8-character passwords
- **Affected Feature:** F-01: Register (web)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is on the registration page.
- **Steps to Reproduce:**
  1. Navigate to `http://127.0.0.1:5000/register`.
  2. Enter a unique, valid username.
  3. Enter exactly 8 characters for the password (e.g., `12345678`).
  4. Click the register button.
- **Expected Result:** The registration should be successful and the account created.
- **Actual Result:** The registration is rejected with a validation error message.
- **Severity:** High
- **Priority:** High
- **Status:** Open
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F01-02_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F01-02`

### Defect ID: D-005
- **Title:** Dashboard 7-day counter excludes tasks completed exactly 7 days ago
- **Affected Feature:** F-15: Dashboard (web)
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in and has a task completed exactly 7 days prior.
- **Steps to Reproduce:**
  1. Change the system clock to exactly 7 days in the past.
  2. Create a new task and mark it as "Done".
  3. Revert the system clock to the current date.
  4. Navigate to `/dashboard` and observe the "completed in the last 7 days" counter.
- **Expected Result:** The counter should include the task that was completed exactly 7 days ago.
- **Actual Result:** The counter ignores the task, though the task list still shows its status as "Done".
- **Severity:** Moderate
- **Priority:** Medium
- **Status:** Open
- **Evidence:** `/01_Black_Box/evidence/BVA/TC-BB-BVA-F15-01_Actual.png`
- **Related Test Case:** `TC-BB-BVA-F15-01`