# PyTodo Pro: Test Scope Matrix (Week 1)

This matrix shows which features from `feature_inventory.md` we will test in Week 1, which black-box technique we will use, and who in the group is responsible. Week 1 only covers black-box testing through the web pages, so the API features are marked out of scope for now. The risk and priority values are a first draft and will change once we start testing.

## Scope Matrix

| Feature ID | Feature | In Scope (Y/N) | Technique(s) | Risk (draft) | Priority | Assigned To | Reason |
|---|---|---|---|---|---|---|---|
| F-01 | Register (web) | Y | EP, BVA | H | High | Test Design Coordinator (EP), Automation/Tool Coordinator (BVA) | Username and password have clear length limits, and the code seems to reject a password of exactly 8 characters. |
| F-02 | Register (API) | N | None for Week 1 | M | Medium | Not assigned yet | It is an API endpoint, so it waits for Week 4. We test the same rules through F-01 first. |
| F-03 | Login (web) | Y | Decision Table | M | High | Defect & Metrics Coordinator | The result depends on two things (user exists, password correct), and users cannot do anything without login. |
| F-04 | Login (API) | N | None for Week 1 | L | Low | Not assigned yet | It is an API endpoint, so it waits for Week 4. |
| F-05 | Logout | Y | State Transition | L | Medium | QA/Test Lead | The user goes from logged in to logged out, and we want to check the pages are blocked afterwards. |
| F-06 | Page protection (web) | Y | EP | M | Medium | Test Design Coordinator | There are only two groups (logged in or not), so we pick a few protected pages from each. |
| F-07 | Endpoint protection (API) | N | None for Week 1 | M | Medium | Not assigned yet | It only applies to API calls, so it waits for Week 4. |
| F-08 | Create task | Y | EP, BVA | H | High | Test Design Coordinator (EP), Automation/Tool Coordinator (BVA) | The title has no server check and no length limit, and the category and due date have different valid groups. |
| F-09 | View task list | Y | EP | M | Medium | Test Design Coordinator | We test the groups "no tasks" and "some tasks", and check that we only see our own tasks. |
| F-10 | Edit task | Y | EP | M | Medium | Test Design Coordinator | It uses the same fields as create, and a task id that is not ours or does not exist is a separate group. |
| F-11 | Filter and search | Y | Decision Table | M | Medium | Defect & Metrics Coordinator | Category, status and search text combine in many ways, so a table keeps the cases organised. |
| F-12 | Mark done / reopen | Y | State Transition | M | High | QA/Test Lead | A task moves between open and done, and the dashboard numbers depend on it. |
| F-13 | Delete task (web) | Y | EP | M | Medium | Test Design Coordinator | Deleting loses data, so we test own task, someone else's task and a missing task. |
| F-14 | Urgency badge | Y | BVA, Decision Table | H | High | Automation/Tool Coordinator (BVA), Defect & Metrics Coordinator (Decision Table) | The label changes at day boundaries around today, and "Due Today" seems to be missing. We also combine done status with due date type. |
| F-15 | Dashboard (web) | Y | BVA | H | High | Automation/Tool Coordinator | The 7 day cutoff is a boundary, and the code seems to leave out tasks completed exactly 7 days ago. We are not sure yet how to make a task that old from the UI, so we will check during testing. |
| F-16 | Dashboard (API) | N | None for Week 1 | L | Low | Not assigned yet | It is an API endpoint, so it waits for Week 4. We compare it with F-15 then. |
| F-17 | List categories | N | None for Week 1 | L | Low | Not assigned yet | It is an API endpoint with no input, so it waits for Week 4. |
| F-18 | List tasks (API) | N | None for Week 1 | M | Medium | Not assigned yet | It is an API endpoint, so it waits for Week 4. Page and per_page limits will be tested then. |
| F-19 | Create task (API) | N | None for Week 1 | H | High | Not assigned yet | It is an API endpoint, so it waits for Week 4. It has little validation, so we expect problems there. |
| F-20 | Get one task | N | None for Week 1 | L | Low | Not assigned yet | It is an API endpoint, so it waits for Week 4. |
| F-21 | Update task | N | None for Week 1 | M | Medium | Not assigned yet | It is an API endpoint, so it waits for Week 4. |
| F-22 | Delete task (API) | N | None for Week 1 | H | High | Not assigned yet | It is an API endpoint, so it waits for Week 4. It does not check the owner, which is also a Week 5 security topic. |

## Out of Scope for Week 1

- API endpoints (F-02, F-04, F-07, F-16 to F-22): Week 4.
- Security problems we noticed in the code, such as SQL injection in the API search, stored XSS in task titles, deleting other users' tasks, hard-coded secret key, debug mode and missing CSRF protection: Week 5.
- Performance and load behaviour: Week 5.
- Cookie flags and session settings: Week 5.
- Browser compatibility and page layout: we have not been told which week covers this, so we are not testing it for now.
- Code-level checks of the helper functions (for example `compute_urgency` and `is_valid_password` on their own): this is white-box work, so it belongs to a later phase and not black-box testing.
