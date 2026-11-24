# Week 4: Extra API Test Cases - Delete and Dashboard

**Prepared & Executed by:** Defect & Metrics Coordinator (Nafiesa)
**Endpoints:** `DELETE /api/tasks/<int:task_id>`, `GET /api/dashboard`
**Test Script:** `tests/test_api_delete_dashboard.py`
**Evidence:** `evidence_api_delete_dashboard.txt`
**Run:** Python 3, pytest with Flask test client. Each test uses its own temporary database.
**Summary:** 10 Test Cases - **6 Passed, 4 Failed**

---

## 1. Why these extra cases

The basic cases for these two endpoints are already in `api_test_cases.md` (sections 8 and 9, `API-TSK-DEL-01` to `05` and `API-DASH-01` to `04`). These 10 cases add what those tests do not check:

- **After a cross-user delete, is the data really gone?** `API-TSK-DEL-05` only checked the status code. `ui_vs_api_comparison.md` (TC-API-UI-24) also noted this was still unconfirmed.
- **Does the dashboard only count the logged-in user's tasks?** This is the same access-control risk (R1) as the delete bug.
- **Are the dashboard date boundaries right?** We test each counter at its limits (BVA): yesterday/tomorrow, 2/3 days ahead, and 7/8 days ago.

The tests also create a fresh database for every test. They pass on a new clone without an existing `pytodo_pro.db`.

---

## 2. Test Cases: `DELETE /api/tasks/<int:task_id>`

| TC ID | Category | Test Case | Request / Steps | Expected Result | Actual Result | Result | Defect |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **API-DD-01** | Security (IDOR) | Is data lost after another user's delete? | User A creates a task. User B sends `DELETE /api/tasks/<A's id>`. User A sends `GET /api/tasks/<id>` | B gets 403/404. A still gets **200** | B got `200 {"result": "ok"}`. A got **404**: the task was **permanently deleted** by another user | **Fail** | D-025 |
| **API-DD-02** | Invalid Input | Delete the same task twice | `DELETE /api/tasks/<id>` two times | 1st: 200. 2nd: **404** `not found` | 1st: 200. 2nd: **200** `{"result": "ok"}` | **Fail** | D-024 |
| **API-DD-03** | Valid | Delete updates the dashboard | Create 2 tasks, delete 1, compare dashboard `total` before and after | `total` goes from 2 to 1. The kept task still returns 200 | 2 → 1. Kept task 200 | **Pass** | - |

## 3. Test Cases: `GET /api/dashboard`

| TC ID | Category | Test Case | Request / Steps | Expected Result | Actual Result | Result | Defect |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **API-DD-04** | Security | Dashboard counts only own tasks | A has 1 task. B has 3 overdue tasks. A sends `GET /api/dashboard` | A: `total: 1`, `overdue: 0` | `total: 1`, `overdue: 0` | **Pass** | - |
| **API-DD-05** | Valid | Done task with a past due date | Task due 5 days ago, marked done | `overdue: 0`, `open: 0`, `completed_this_week: 1` | As expected | **Pass** | - |
| **API-DD-06** | BVA (Due Soon upper limit) | Due in 2 days vs 3 days | One task due today+2, one due today+3 | `due_soon: 1` (only +2), `overdue: 0` | `due_soon: 1`, `overdue: 0` | **Pass** | - |
| **API-DD-07** | BVA (Overdue / Due Soon) | Due yesterday vs tomorrow | One task due today-1, one due today+1 | `overdue: 1`, `due_soon: 1` | `overdue: 1`, `due_soon: 1` | **Pass** | - |
| **API-DD-08** | BVA (7-day window, on boundary) | Completed exactly 7 days ago | Task with `completed_at` = now - 7 days | `completed_this_week: 1` (spec: last 7 days) | `completed_this_week: 0` | **Fail** | D-005 |
| **API-DD-09** | BVA (7-day window, outside) | Completed 8 days ago | Task with `completed_at` = now - 8 days | `completed_this_week: 0` | `completed_this_week: 0` | **Pass** | - |
| **API-DD-10** | Edge Condition | Dashboard after a task with a bad date is saved | `POST /api/tasks` with `"due_date": "31-12-2026"`, then `GET /api/dashboard` | Dashboard still returns 200 | **500** Internal Server Error (`ValueError` in `compute_urgency`) | **Fail** | D-006 |

Note: `API-DD-08` and `API-DD-09` set `completed_at` directly in the test database, because the API always uses the current time when a task is marked done.

---

## 4. Results Summary

| Endpoint | Cases | Passed | Failed |
| :--- | :---: | :---: | :---: |
| `DELETE /api/tasks/<id>` | 3 | 1 | 2 |
| `GET /api/dashboard` | 7 | 5 | 2 |
| **Total** | **10** | **6** | **4** |

## 5. Findings

1. **Cross-user delete causes real data loss (D-025, Critical).** `API-DD-01` proves User A's task is gone after User B's request. This confirms the IDOR risk raised in `API-TSK-DEL-05` and `TC-API-UI-24`.
2. **Delete never reports "not found" (D-024).** Even a second delete of the same task returns `{"result": "ok"}`.
3. **The dashboard's access control is correct.** `API-DD-04` shows each user only sees their own counts, because the dashboard query filters by `user_id`.
4. **Due Soon and Overdue boundaries are correct** except for "today" (D-001, already logged from `API-DASH-01`).
5. **The 7-day counter misses the boundary day (D-005).** The Week 1 dashboard defect also affects the API.
6. **One bad date breaks the whole dashboard (D-006).** Before, D-006 was known to break the task list. It also breaks `GET /api/dashboard`, so the user loses both views.
