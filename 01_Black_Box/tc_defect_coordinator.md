# Week 1 Black-Box Test Cases: Decision Table Technique

**Author / Assigned To:** Defect & Metrics Coordinator  
**Technique:** Decision Table Testing  
**Target Features:** F-03 (Login web), F-11 (Filter and search), F-14 (Urgency badge)

---

## 1. Feature: F-03 - Login (Web)

### Decision Table
- **Conditions:**
  - C1: User account exists in database? (Y/N)
  - C2: Password matches user account? (Y/N)
- **Actions:**
  - A1: Grant access & redirect to dashboard (`/dashboard`)
  - A2: Display authentication error message ("Invalid username or password")

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: User Exists** | Y | Y | N | N |
| **C2: Correct Password** | Y | N | Y | N |
| **A1: Login Success (Redirect)** | **X** | | | |
| **A2: Display Error Message** | | **X** | **X** | **X** |

### Test Cases (F-03)

#### Test Case ID: TC-BB-F03-01
- **Feature/Requirement:** F-03: Login (web)
- **Technique/Test Type:** Decision Table / Black-box
- **Objective:** Verify successful login when user exists and password is correct (Rule 1).
- **Preconditions:** Registered user `ryulemontea` with password `Kimryulhensem` exists in DB.
- **Test Data:** Username: `ryulemontea`, Password: `Kimryulhensem`
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.
  2. Enter Username `ryulemontea` and Password `Kimryulhensem`.
  3. Click "Log in".
- **Expected Result:** Redirected to `/dashboard` with an active user session.
- **Actual Result:** * Redirected to `/dashboard` with an active user session*
- **Status:** PASS
- **Evidence:** ``
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F03-02
- **Feature/Requirement:** F-03: Login (web)
- **Technique/Test Type:** Decision Table / Black-box
- **Objective:** Verify failure when user exists but enters an incorrect password (Rule 2).
- **Preconditions:** Registered user `ryulemontea` exists in DB.
- **Test Data:** Username: `ryulemontea`, Password: `Kimryulhensom`
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.
  2. Enter Username `ryulemonteaa` and Password `Kimryulhensom`.
  3. Click "Log in".
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.
- **Actual Result:** ** Login denied, `/Invalid username and password` error message displayed
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F03-02.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F03-03
- **Feature/Requirement:** F-03: Login (web)
- **Technique/Test Type:** Decision Table / Black-box
- **Objective:** Verify failure when non-existent user tries to log in (Rule 3).
- **Preconditions:** Username `ryulemonteaa` does not exist in DB.
- **Test Data:** Username: `ryulemonteaa`, Password: `Kimryulhensem`
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.
  2. Enter Username `ryulemonteaa` and Password `Kimryulhensem`.
  3. Click "Log in".
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.
- **Actual Result:** ** Login denied, `invalid username or password` error message appeared
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F03-03.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F03-04
- **Feature/Requirement:** F-03: Login (web)
- **Technique/Test Type:** Decision Table / Black-box
- **Objective:** Verify failure when both username and password do not exist (Rule 4).
- **Preconditions:** Username `mingyuKim` does not exist in DB.
- **Test Data:** Username: `mingyuKim`, Password: `Abcdefgh`
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.
  2. Enter Username `mingyuKim` and Password `Abcdefgh`.
  3. Click "Log in".
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.
- **Actual Result:** ** Login denied, invalid username or password` error message appeared
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F03-04.png`
- **Defect ID:** N/A

---

## 2. Feature: F-11 - Filter and Search

### Decision Table
- **Conditions:**
  - C1: Category filter selected? (All / Specific Category "Work")
  - C2: Status filter selected? (All / Pending / Done)
  - C3: Search keyword provided? (Empty / Matches Task Title / No Match)
- **Actions:**
  - A1: Display matching tasks in task list
  - A2: Display "No tasks found" message

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Category** | All | Work | All | Work | All |
| **C2: Status** | All | Pending | Done | Pending | All |
| **C3: Search Keyword** | Empty | "Report" | Empty | "XYZ999" | "XYZ999" |
| **A1: Display Matching Tasks** | **X** | **X** | **X** | | |
| **A2: Display "No tasks found"** | | | | **X** | **X** |

### Test Cases (F-11)

#### Test Case ID: TC-BB-F11-01
- **Feature/Requirement:** F-11: Filter and search
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify that all tasks are displayed when filters are set to default/empty (Rule 1).
- **Preconditions:** User is logged in and has created multiple tasks in different categories.
- **Test Data:** Category: `All`, Status: `All`, Search Keyword: `""`
- **Steps:**
  1. Navigate to the task list page.
  2. Keep Category as `All`, Status as `All`, and Search input empty.
  3. Click "Search" or apply filter.
- **Expected Result:** All active tasks belonging to the logged-in user are displayed.
- **Actual Result:** ** All active tasks are displayed
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F11-01.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F11-02
- **Feature/Requirement:** F-11: Filter and search
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify filtering by specific category, pending status, and matching keyword (Rule 2).
- **Preconditions:** A Pending task titled "Submit Report" exists under category "Work".
- **Test Data:** Category: `Work`, Status: `Open`, Search Keyword: `"Report"`
- **Steps:**
  1. Select Category `Work`.
  2. Select Status `Open`.
  3. Enter `"Report"` in the search field.
  4. Click "Search".
- **Expected Result:** Only the task "Submit Report" is displayed in the list.
- **Actual Result:** ** "Submit Report" is the only task displayed in the list after done filter action
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F11-02.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F11-03
- **Feature/Requirement:** F-11: Filter and search
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify filtering completed tasks across all categories (Rule 3).
- **Preconditions:** User has both pending and completed tasks.
- **Test Data:** Category: `All`, Status: `Done`, Search Keyword: `""`
- **Steps:**
  1. Select Category `All`.
  2. Select Status `Done`.
  3. Click "Search".
- **Expected Result:** Only tasks marked as "Done" are listed.
- **Actual Result:** ** "Proposal decommissioning" is display when status marked as "Done"
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F11-03.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F11-04
- **Feature/Requirement:** F-11: Filter and search
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify system behavior when search keyword yields no matching results (Rule 4 & 5).
- **Preconditions:** User is logged in on the task list page.
- **Test Data:** Category: `Work`, Status: `Open`, Search Keyword: `"image scanner"`
- **Steps:**
  1. Select Category `Work`.
  2. Enter `"image scanner"` in the search input.
  3. Click "Search".
- **Expected Result:** Task list is empty and displays "No tasks found" feedback.
- **Actual Result:** ** Task list displays "No tasks match your filters"
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F11-04.png`
- **Defect ID:** N/A

---

## 3. Feature: F-14 - Urgency Badge

### Decision Table
- **Conditions:**
  - C1: Task status? (Open / Done)

- **Actions:**
  - A1: Display "Overdue" badge
  - A2: Display "Due Soon" badge
  - A3: Display "Upcoming" badge

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Task State** | Open | Open | Open | Open | Done |
| **A1: Badge = "Overdue"** | **X** | | | | |
| **A2: Badge = "Due Soon"** | | **X** | | | |
| **A3: Badge = "Upcoming"** | | | **X** | | |

### Test Cases (F-14)

#### Test Case ID: TC-BB-F14-01
- **Feature/Requirement:** F-14: Urgency badge
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify "Overdue" badge display on open tasks with a past due date (Rule 1).
- **Preconditions:** User is logged in.
- **Test Data:** Task Title: "Submit report", Status: `Open`
- **Steps:**
  1. Create an open task with yesterday's date as due date.
  2. View the task badge on the dashboard/task list.
- **Expected Result:** Task displays an "Overdue" badge (e.g., Red label).
- **Actual Result:** ** Task "Submit report" displays an "Overdue" badge
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F14-01.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F14-02
- **Feature/Requirement:** F-14: Urgency badge
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify "Due Today" badge display on open tasks due today (Rule 2).
- **Preconditions:** User is logged in.
- **Test Data:** Task Title: "Mock Interview", Status: `Open`, Due Date: `Today`
- **Steps:**
  1. Create an open task with today's date as due date.
  2. View the task badge on the dashboard/task list.
- **Expected Result:** Task displays a "Due Today" badge (Note: Check if label is missing as reported in Scope Matrix).
- **Actual Result:** Task displays a "Overdue" badge 
- **Status:** FAILED
- **Evidence:** `/evidence/TC-BB-F14-02.png`
- **Defect ID:** D-001

#### Test Case ID: TC-BB-F14-03
- **Feature/Requirement:** F-14: Urgency badge
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify "Dental appointment" badge display on open tasks due in the future (Rule 3).
- **Preconditions:** User is logged in.
- **Test Data:** Task Title: "Dental appointment", Status: `Open`, Due Date: `Tomorrow`
- **Steps:**
  1. Create an open task with tomorrow's date as due date.
  2. View the task badge on the dashboard/task list.
- **Expected Result:** Task displays an "Upcoming" badge.
- **Actual Result:** ** Task displays an "Upcoming" badge 
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F14-03.png`
- **Defect ID:** N/A

#### Test Case ID: TC-BB-F14-04
- **Feature/Requirement:** F-14: Urgency badge
- **Technique/Test Type:** Decision Table / Functional
- **Objective:** Verify completed tasks override urgency badge display (Rule 5).
- **Preconditions:** Task with a past due date exists.
- **Test Data:** Task Title: "Proposal decommissioning", Status: `Done`, Due Date: `Yesterday`
- **Steps:**
  1. Mark an overdue task as "Done".
  2. View the task badge on the task list.
- **Expected Result:** "Overdue" urgency warning is cleared/overridden by Completed status.
- **Actual Result:** ** Task title will strikethrough and "Done" urgency badge displayed
- **Status:** PASS
- **Evidence:** `/evidence/TC-BB-F14-04.png`
- **Defect ID:** N/A
