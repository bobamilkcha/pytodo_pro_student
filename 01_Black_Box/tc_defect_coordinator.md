# Week 1 Black-Box Test Cases: Decision Table Technique

**Author / Assigned To:** Defect & Metrics Coordinator  
**Technique:** Decision Table Testing[cite: 2]  
**Target Features:** F-03 (Login web), F-11 (Filter and search), F-14 (Urgency badge)[cite: 2]

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
- **Technique/Test Type:** Decision Table / Black-box[cite: 2, 5]
- **Objective:** Verify successful login when user exists and password is correct (Rule 1).[cite: 5]
- **Preconditions:** Registered user `validUser` with password `Password123!` exists in DB.[cite: 5, 8]
- **Test Data:** Username: `validUser`, Password: `Password123!`[cite: 5, 8]
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.[cite: 5, 8]
  2. Enter Username `validUser` and Password `Password123!`.[cite: 5, 8]
  3. Click "Log in".[cite: 5, 8]
- **Expected Result:** Redirected to `/dashboard` with an active user session.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F03-01.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F03-02
- **Feature/Requirement:** F-03: Login (web)[cite: 5]
- **Technique/Test Type:** Decision Table / Black-box[cite: 2, 5]
- **Objective:** Verify failure when user exists but enters an incorrect password (Rule 2).[cite: 5]
- **Preconditions:** Registered user `validUser` exists in DB.[cite: 5, 8]
- **Test Data:** Username: `validUser`, Password: `WrongPassword123`[cite: 5, 8]
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.[cite: 5, 8]
  2. Enter Username `validUser` and Password `WrongPassword123`.[cite: 5, 8]
  3. Click "Log in".[cite: 5, 8]
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F03-02.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F03-03
- **Feature/Requirement:** F-03: Login (web)[cite: 5]
- **Technique/Test Type:** Decision Table / Black-box[cite: 2, 5]
- **Objective:** Verify failure when non-existent user tries to log in (Rule 3).[cite: 5]
- **Preconditions:** Username `unknownUser` does not exist in DB.[cite: 5, 8]
- **Test Data:** Username: `unknownUser`, Password: `Password123!`[cite: 5, 8]
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.[cite: 5, 8]
  2. Enter Username `unknownUser` and Password `Password123!`.[cite: 5, 8]
  3. Click "Log in".[cite: 5, 8]
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F03-03.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F03-04
- **Feature/Requirement:** F-03: Login (web)[cite: 5]
- **Technique/Test Type:** Decision Table / Black-box[cite: 2, 5]
- **Objective:** Verify failure when both username and password do not exist (Rule 4).[cite: 5]
- **Preconditions:** Username `invalidUser` does not exist in DB.[cite: 5, 8]
- **Test Data:** Username: `invalidUser`, Password: `WrongPassword123`[cite: 5, 8]
- **Steps:**
  1. Navigate to `http://127.0.0.1:5000/login`.[cite: 5, 8]
  2. Enter Username `invalidUser` and Password `WrongPassword123`.[cite: 5, 8]
  3. Click "Log in".[cite: 5, 8]
- **Expected Result:** Login denied, user remains on `/login` with an error message displayed.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F03-04.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

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
- **Feature/Requirement:** F-11: Filter and search[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify that all tasks are displayed when filters are set to default/empty (Rule 1).[cite: 5]
- **Preconditions:** User is logged in and has created multiple tasks in different categories.[cite: 5]
- **Test Data:** Category: `All`, Status: `All`, Search Keyword: `""`[cite: 5]
- **Steps:**
  1. Navigate to the task list page.[cite: 5]
  2. Keep Category as `All`, Status as `All`, and Search input empty.[cite: 5]
  3. Click "Search" or apply filter.[cite: 5]
- **Expected Result:** All active tasks belonging to the logged-in user are displayed.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F11-01.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F11-02
- **Feature/Requirement:** F-11: Filter and search[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify filtering by specific category, pending status, and matching keyword (Rule 2).[cite: 5]
- **Preconditions:** A Pending task titled "Submit Report" exists under category "Work".[cite: 5]
- **Test Data:** Category: `Work`, Status: `Pending`, Search Keyword: `"Report"`[cite: 5]
- **Steps:**
  1. Select Category `Work`.[cite: 5]
  2. Select Status `Pending`.[cite: 5]
  3. Enter `"Report"` in the search field.[cite: 5]
  4. Click "Search".[cite: 5]
- **Expected Result:** Only the task "Submit Report" is displayed in the list.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F11-02.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F11-03
- **Feature/Requirement:** F-11: Filter and search[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify filtering completed tasks across all categories (Rule 3).[cite: 5]
- **Preconditions:** User has both pending and completed tasks.[cite: 5]
- **Test Data:** Category: `All`, Status: `Done`, Search Keyword: `""`[cite: 5]
- **Steps:**
  1. Select Category `All`.[cite: 5]
  2. Select Status `Done`.[cite: 5]
  3. Click "Search".[cite: 5]
- **Expected Result:** Only tasks marked as "Done" are listed.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F11-03.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F11-04
- **Feature/Requirement:** F-11: Filter and search[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify system behavior when search keyword yields no matching results (Rule 4 & 5).[cite: 5]
- **Preconditions:** User is logged in on the task list page.[cite: 5]
- **Test Data:** Category: `Work`, Status: `Pending`, Search Keyword: `"XYZ999"`[cite: 5]
- **Steps:**
  1. Select Category `Work`.[cite: 5]
  2. Enter `"XYZ999"` in the search input.[cite: 5]
  3. Click "Search".[cite: 5]
- **Expected Result:** Task list is empty and displays "No tasks found" feedback.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F11-04.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

---

## 3. Feature: F-14 - Urgency Badge

### Decision Table
- **Conditions:**
  - C1: Task completion state? (Open / Done)
  - C2: Due Date status? (Past / Today / Future / None)
- **Actions:**
  - A1: Display "Overdue" badge
  - A2: Display "Due Today" badge
  - A3: Display "Upcoming" badge
  - A4: Display Neutral / Completed badge (No urgency warning)

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Task State** | Open | Open | Open | Open | Done |
| **C2: Due Date Status** | Past | Today | Future | None | Past / Today / Future |
| **A1: Badge = "Overdue"** | **X** | | | | |
| **A2: Badge = "Due Today"** | | **X** | | | |
| **A3: Badge = "Upcoming"** | | | **X** | | |
| **A4: Badge = Neutral / "Completed"** | | | | **X** | **X** |

### Test Cases (F-14)

#### Test Case ID: TC-BB-F14-01
- **Feature/Requirement:** F-14: Urgency badge[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify "Overdue" badge display on open tasks with a past due date (Rule 1).[cite: 5]
- **Preconditions:** User is logged in.[cite: 5]
- **Test Data:** Task Title: "Past Task", Status: `Open`, Due Date: `Yesterday`[cite: 5]
- **Steps:**
  1. Create an open task with yesterday's date as due date.[cite: 5]
  2. View the task badge on the dashboard/task list.[cite: 5]
- **Expected Result:** Task displays an "Overdue" badge (e.g., Red label).[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F14-01.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F14-02
- **Feature/Requirement:** F-14: Urgency badge[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify "Due Today" badge display on open tasks due today (Rule 2).[cite: 5]
- **Preconditions:** User is logged in.[cite: 5]
- **Test Data:** Task Title: "Today Task", Status: `Open`, Due Date: `Today`[cite: 5]
- **Steps:**
  1. Create an open task with today's date as due date.[cite: 5]
  2. View the task badge on the dashboard/task list.[cite: 5]
- **Expected Result:** Task displays a "Due Today" badge (Note: Check if label is missing as reported in Scope Matrix).[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F14-02.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F14-03
- **Feature/Requirement:** F-14: Urgency badge[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify "Upcoming" badge display on open tasks due in the future (Rule 3).[cite: 5]
- **Preconditions:** User is logged in.[cite: 5]
- **Test Data:** Task Title: "Future Task", Status: `Open`, Due Date: `Tomorrow`[cite: 5]
- **Steps:**
  1. Create an open task with tomorrow's date as due date.[cite: 5]
  2. View the task badge on the dashboard/task list.[cite: 5]
- **Expected Result:** Task displays an "Upcoming" badge.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F14-03.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]

#### Test Case ID: TC-BB-F14-04
- **Feature/Requirement:** F-14: Urgency badge[cite: 5]
- **Technique/Test Type:** Decision Table / Functional[cite: 2, 5]
- **Objective:** Verify completed tasks override urgency badge display (Rule 5).[cite: 5]
- **Preconditions:** Task with a past due date exists.[cite: 5]
- **Test Data:** Task Title: "Finished Task", Status: `Done`, Due Date: `Yesterday`[cite: 5]
- **Steps:**
  1. Mark an overdue task as "Done".[cite: 5]
  2. View the task badge on the task list.[cite: 5]
- **Expected Result:** "Overdue" urgency warning is cleared/overridden by Completed status.[cite: 5]
- **Actual Result:** *(To be filled after execution)*[cite: 5]
- **Status:** Not Run[cite: 5]
- **Evidence:** `/evidence/TC-BB-F14-04.png`[cite: 5]
- **Defect ID:** N/A[cite: 5]
