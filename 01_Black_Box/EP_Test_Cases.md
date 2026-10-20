# Black-Box Test Design: Equivalence Partitioning (EP)

**Role:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro  
**ID Scheme:** `TC-BB-xxx`  

---

## 1. Master Test Case Template Structure

All team members must structure their black-box test cases using the following standard fields required by the QA framework:

| Field | Description |
| :--- | :--- |
| **Test Case ID** | Unique identifier following `TC-BB-xxx`[cite: 2, 5] |
| **Feature/Requirement** | The specific feature or system capability under test[cite: 5] |
| **Technique/Test Type** | Black-box design technique applied (EP, BVA, Decision Table, State-Transition)[cite: 5] |
| **Objective** | Concise statement of what the test verifies[cite: 5] |
| **Preconditions** | Initial system state required before test execution[cite: 5] |
| **Test Data** | Input parameters and data values used[cite: 5] |
| **Steps** | Sequential procedure to execute the test[cite: 5] |
| **Expected Result** | Defined system behavior expected before execution[cite: 5] |
| **Actual Result** | Observed behavior during manual execution[cite: 5] |
| **Status** | Pass / Fail / Blocked / Not Run[cite: 5] |
| **Evidence** | Reference link or filename to screenshot/log proof[cite: 5] |
| **Defect ID** | Linked ID from Defect Log if test status is Fail[cite: 5] |

---

## 2. Technique Justification & Test Data

### Technique Justification: Equivalence Partitioning (EP)
Equivalence Partitioning (EP) was selected to test input validation and task urgency classification because it systematically divides the input domain into disjoint classes (valid and invalid)[cite: 2]. The core premise of EP is that if one test case in a partition reveals a defect, all other inputs in that same partition will behave similarly[cite: 2]. Applying EP reduces redundant test execution while ensuring thorough coverage across key logical boundaries in PyTodo Pro[cite: 2].

### Test Data & Partitioning Strategy

#### A. Task Due Date & Urgency Classification Partitions
- **Partition 1 (Past Date):** Dates earlier than today $\rightarrow$ Expected Urgency: `Overdue`
- **Partition 2 (Current Date):** Today's date (`2026-10-20`) $\rightarrow$ Expected Urgency: `Due Today`
- **Partition 3 (Near Future):** Tomorrow or within 2 days (`2026-10-21` to `2026-10-22`) $\rightarrow$ Expected Urgency: `Due Soon`
- **Partition 4 (Far Future):** Dates 3 or more days in advance (`2026-10-23` or later) $\rightarrow$ Expected Urgency: `Upcoming`
- **Partition 5 (Null/Empty Date):** No due date provided $\rightarrow$ Expected Urgency: `No due date`

#### B. Text Input Partitions (Task Title)
- **Valid String Partition:** Standard non-empty string (e.g., `"Complete STQA Report"`)
- **Invalid Empty Partition:** Blank string `""` or whitespace-only `" "`

#### C. User Authentication Partitions
- **Valid Account Creation:** Unregistered username + non-empty password
- **Invalid Duplicate Registration:** Already existing username
- **Valid Login Credentials:** Correct username + correct password
- **Invalid Login Credentials:** Correct username + incorrect password

---

## 3. Equivalence Partitioning (EP) Test Cases

| Test Case ID | Feature/Requirement | Technique | Objective | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Evidence | Defect ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-BB-001** | Account Management | EP | Verify registration with valid new account details | User is on `/register` page | Username: `aida_tester`<br>Password: `Pass123!` | 1. Go to `/register`<br>2. Enter username & password<br>3. Click Register | Account created successfully; redirected to login/dashboard | Account created; redirected to login page | Pass | `evidence/TC-BB-001.png` | N/A |
| **TC-BB-002** | Account Management | EP | Verify registration fails when username already exists | User `aida_tester` already exists | Username: `aida_tester`<br>Password: `Pass123!` | 1. Go to `/register`<br>2. Enter existing username<br>3. Click Register | Registration rejected; explicit error message displayed | Registration fails with error message | Pass | `evidence/TC-BB-002.png` | N/A |
| **TC-BB-003** | Account Management | EP | Verify login with incorrect password fails | Account `aida_tester` exists | Username: `aida_tester`<br>Password: `WrongPass` | 1. Go to `/login`<br>2. Enter username & incorrect password<br>3. Click Login | Access denied; error message "Invalid credentials" shown | Login rejected with error message | Pass | `evidence/TC-BB-003.png` | N/A |
| **TC-BB-004** | Task Creation | EP | Verify task creation with valid title and category | User logged in | Title: `"Finish EP Test Design"`<br>Category: `Study`<br>Due Date: None | 1. Click "+ New Task"<br>2. Fill Title & Category<br>3. Click Save | Task appears in list with correct category | Task successfully saved and listed | Pass | `evidence/TC-BB-004.png` | N/A |
| **TC-BB-005** | Task Creation | EP | Verify task creation fails when Title is empty | User logged in | Title: `""`<br>Category: `Personal`<br>Due Date: None | 1. Click "+ New Task"<br>2. Leave Title blank<br>3. Click Save | Form validation prevents submission; task not created | Submission blocked; field error shown | Pass | `evidence/TC-BB-005.png` | N/A |
| **TC-BB-006** | Task Urgency | EP | Verify urgency classification for empty due date | User logged in | Title: `"Buy Groceries"`<br>Due Date: `""` | 1. Create task with no due date<br>2. View task in list | Urgency status displays `No due date` | Urgency displays `No due date` | Pass | `evidence/TC-BB-006.png` | N/A |
| **TC-BB-007** | Task Urgency | EP | Verify urgency classification for past due date | User logged in | Title: `"Past Assignment"`<br>Due Date: `2026-10-15` | 1. Create task with past date<br>2. View task in list | Urgency status displays `Overdue` | Urgency displays `Overdue` | Pass | `evidence/TC-BB-007.png` | N/A |
| **TC-BB-008** | Task Urgency | EP | Verify urgency classification for today's due date | User logged in | Title: `"Submit Daily Standup"`<br>Due Date: `2026-10-20` | 1. Create task with today's date<br>2. View task in list | Urgency status displays `Due Today` | Urgency displays `Due Today` | Pass | `evidence/TC-BB-008.png` | N/A |
| **TC-BB-009** | Task Urgency | EP | Verify urgency classification for date within 2 days | User logged in | Title: `"Review PR"`<br>Due Date: `2026-10-21` | 1. Create task with tomorrow's date<br>2. View task in list | Urgency status displays `Due Soon` | Urgency displays `Due Soon` | Pass | `evidence/TC-BB-009.png` | N/A |
| **TC-BB-010** | Task Urgency | EP | Verify urgency classification for date 3+ days out | User logged in | Title: `"Final Exam Prep"`<br>Due Date: `2026-10-28` | 1. Create task with future date<br>2. View task in list | Urgency status displays `Upcoming` | Urgency displays `Upcoming` | Pass | `evidence/TC-BB-010.png` | N/A |
