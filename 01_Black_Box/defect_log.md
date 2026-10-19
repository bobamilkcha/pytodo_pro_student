# Central Defect Log - PyTodo Pro

## Summary
- **Total Defects Logged:** 2
- **Open Defects:** 1
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
- **Title:** API `/tasks` endpoint accepts `page=0` and returns an empty response instead of an error
- **Affected Feature:** JSON REST API - Pagination
- **Environment:** Localhost (http://127.0.0.1:5000), Browser
- **Preconditions:** User is logged in with an active session cookie.
- **Steps to Reproduce:**
  1. Log into the application via `/login`.
  2. Open a new tab in the same browser.
  3. Navigate to `http://127.0.0.1:5000/api/tasks?page=0`.
  4. Observe the response in the browser window.
- **Expected Result:** The API should reject `page=0` with a 400 Bad Request error or gracefully default to returning the data for page 1. 
- **Actual Result:** The API returns a completely blank page/empty response without throwing an error or defaulting to valid data.
- **Severity:** Low 
- **Priority:** Low
- **Status:** Open
- **Evidence:** `/evidence/BVA/TC-BB-BVA-005_Actual.png`
- **Related Test Case:** `TC-BB-BVA-005`
