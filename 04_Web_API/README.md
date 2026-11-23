# Week 4: Web API Testing Setup

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Output Folder:** `/04_Web_API`

---

## 1. Selected API Testing Tool
**Tool:** **PyTest** with the **Flask Test Client** (`app.test_client()`)

### Why This Tool?
- **No live server required:** Requests are sent directly to the Flask application in-memory, making test execution fast and reliable.
- **Built-in session handling:** `app.test_client()` automatically manages Flask session cookies (`session["user_id"]`) across `POST /api/login` and protected `/api/tasks` requests.
- **Consistent stack:** Uses the existing Python `venv` and `pytest` environment already configured from Weeks 1–2 without needing external tools.

---

## 2. Environment Setup

1. **Pull the latest changes** and activate the virtual environment (from the project root in PowerShell):
   ```powershell
   git pull origin main
   .\venv\Scripts\Activate.ps1
   ```
2. **Run the API tests:**
   ```powershell
   pytest 04_Web_API/tests/ -v
   ```

## Endpoint Division (Task 3b & Task 4)

| Role | Assigned Endpoints | Count | Test File | Scope Focus |
| :--- | :--- | :---: | :--- | :--- |
| **Automation/Tool Coordinator** | `POST /api/register`<br>`POST /api/login`<br>`GET /api/categories` | 3 | `tests/test_api_auth.py` | Registration/login validation, session cookie setup, and public category listing. |
| **QA/Test Lead** | `GET /api/tasks`<br>`GET /api/tasks/<id>` | 2 | `tests/test_api_tasks_read.py` | Pagination (`page`, `per_page`), filtering (`category`, `status`), search (`q` / SQLi edge cases), and single-task `404` handling. |
| **Test Design Coordinator** | `POST /api/tasks`<br>`PUT /api/tasks/<id>` | 2 | `tests/test_api_tasks_write.py` | JSON payload validation, missing/invalid fields, partial updates, and `done`/`completed_at` transitions. |
| **Defect & Metrics Coordinator** | `DELETE /api/tasks/<id>`<br>`GET /api/dashboard` | 2 | `tests/test_api_delete_dashboard.py` | Task deletion, cross-user access control (IDOR) check, and verifying all 5 dashboard stat counts. |

---