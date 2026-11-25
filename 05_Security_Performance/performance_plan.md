# Week 5: Performance Test Plan

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Output Folder:** `/05_Security_Performance`  
**Test Script:** `05_Security_Performance/locustfile.py`

---

## 1. Performance Objectives & Target Thresholds

The objective of performance testing is to evaluate how the PyTodo Pro REST API handles increasing concurrent user traffic, identify latency bottlenecks, and verify stability without HTTP or server errors.

| Metric | Target Threshold (Normal Load) | Purpose |
| :--- | :--- | :--- |
| **Average Response Time** | `< 200 ms` | Ensure responsive API interactions under normal usage. |
| **95th Percentile (P95) Latency** | `< 500 ms` | Confirm that at least 95% of requests complete within half a second. |
| **Error Rate** | `< 1.00%` (`0%` target) | Ensure no unhandled `500` errors, database locks, or dropped connections. |
| **Throughput** | Scales linearly with user count | Verify the server processes higher request volumes without stalling. |

---

## 2. Test Environment & Tool Setup

* **Load Testing Tool:** Locust (`v2.46.0`) running in headless CLI mode
* **Application Under Test:** PyTodo Pro Flask REST API (`http://127.0.0.1:5000`)
* **Database:** Local SQLite database (`pytodo.db`)
* **Runtime & OS:** Python `3.10.11` on Windows (local loopback testing)

### Setup & Execution Commands
1. Activate the virtual environment and start the Flask server:
   ```powershell
   .\venv\Scripts\Activate.ps1
   python app.py