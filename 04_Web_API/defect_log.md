## API Defects Found — Auth & Categories (`test_api_auth.py`)

**Reported by:** Automation/Tool Coordinator (Nisrina)  
**Test Suite:** `04_Web_API/tests/test_api_auth.py`  
**Evidence:** `04_Web_API/evidence_api_auth.txt`

| Defect ID | Related Test Case | Endpoint | Severity | Summary | Steps to Reproduce | Expected Result | Actual Result |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **DEF-API-01** | `API-REG-08` | `POST /api/register` | Medium | Unhandled `AttributeError` when `username` is a non-string (e.g., integer) | Send `POST /api/register` with JSON body `{"username": 12345, "password": "Password123"}`. | Return `400 Bad Request` with `{"error": "invalid username"}`. | Crashes with `AttributeError: 'int' object has no attribute 'strip'` at `app.py:318`. |
| **DEF-API-02** | `API-REG-09` | `POST /api/register` | High | Allows registration of duplicate usernames | 1. Send `POST /api/register` with a new username.<br>2. Send `POST /api/register` again with the exact same username. | Reject duplicate registration with `400 Bad Request` or `409 Conflict`. | Returns `201 Created` and inserts a duplicate user record into the database. |
| **DEF-API-03** | `API-LOG-06` | `POST /api/login` | Medium | Unhandled `AttributeError` when `username` is a non-string (e.g., integer) | Send `POST /api/login` with JSON body `{"username": 12345, "password": "Password123"}`. | Return `400 Bad Request` or `401 Unauthorized`. | Crashes with `AttributeError: 'int' object has no attribute 'strip'` at `app.py:336`. |