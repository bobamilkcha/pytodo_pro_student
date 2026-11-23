# Week 4: Web API Testing Setup

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Output Folder:** `/04_Web_API`

---

## 1. Selected API Testing Tool
**Tool:** **PyTest** with the **Flask Test Client** (`app.test_client()`)

### Why This Tool?
* **No live server required:** Requests are sent directly to the Flask application in-memory, making test execution fast and reliable.
* **Built-in session handling:** `app.test_client()` automatically manages Flask session cookies (`session["user_id"]`) across `POST /api/login` and protected `/api/tasks` requests.
* **Consistent stack:** Uses the existing Python `venv` and `pytest` environment already configured from Weeks 1–2 without needing external tools.

---

## 2. Environment Setup

1. **Activate the virtual environment** (from the project root in PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
