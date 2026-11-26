## 3. Coverage, Automation, and Performance Evaluation

### 3.1 Code Coverage and Automation Results Interpretation (Order 3a)

#### White-Box Code Coverage (`pytest-cov`, Week 2)
* **Coverage Achieved:** Three of the four selected units—`compute_urgency()`, `completed_in_last_n_days()`, and the `index()` route—achieved **100% statement and branch coverage** across 28 white-box tests (`24` Passed, `4` Failed). The fourth planned unit, `toggle_task()`, had **0% unit-level coverage** in Week 2 because its tests were not written, though its state transitions (`Open` ↔ `Done` and `completed_at` updates) were later verified via functional state-transition tests (`TC-BB-070`, `TC-BB-071`) and `tests/api/test_state_transition.py`.
* **Key Coverage Insight:** Achieving **100% branch coverage does not guarantee defect-free logic**. In `compute_urgency()`, every branch executed cleanly, yet **D-001** (tasks due today classified as `"Overdue"` instead of `"Due Today"`) remained hidden from coverage tools because the missing `due == today` condition was absorbed into the `due <= today` branch. Conversely, branch and boundary inspection directly exposed **D-005** (strict `< n` instead of `<= n` excluding day 7 in `completed_in_last_n_days()`) and **D-006** (unhandled `ValueError` exceptions on malformed `due_date` strings).

#### Automated Suite & Regression Execution (Week 6)
* **Full Automated Suite (`103` tests across `10` scripts):** Executed via `pytest 06_Automation_Regression/tests/ -v` in `~26s` with **69 Passed (67.0%)**, **34 Failed (33.0%)**, and **0 Collection/Setup Errors**:
  * **Unit Layer (`14` tests):** `6` Passed, `8` Failed — isolates password boundary (`D-004`) and due-today urgency (`D-001`) in milliseconds without HTTP overhead.
  * **API & Route Layer (`77` tests):** `61` Passed, `16` Failed — validates core CRUD, auth, filtering, and state transitions while confirming `D-005`, `D-006`, `D-009`, `D-010`, `D-013`, `D-016`, `D-017`, `D-019`, `D-020`, `D-022`, `D-024`, and `D-025`.
  * **Browser UI Layer (`12` tests):** `2` Passed, `10` Failed — both end-to-end Selenium flows (`test_ui_auth.py`, `test_ui_tasks.py`) pass, confirming registration, login, task creation, toggle completion, and JavaScript `confirm()` dialog behavior work end-to-end, while 10 automated markup/accessibility checks fail on `D-008`, `D-009`, `D-015` (`ACC-03`), `D-016`, and `D-017`.
* **Focused Regression Suite (`-m regression`):** Executed via `pytest 06_Automation_Regression/tests/ -m regression -v` in `14.61s`, selecting **51 high-risk tests** (`52` deselected): **22 Passed (43.1%)** and **29 Failed (56.9%)** with **0 Errors**.
* **Signal Quality:** Every single failure (`34` in the full suite; `29` in the regression suite) maps to a documented open defect across **16 distinct defect IDs**, demonstrating zero false positives from test flakiness. Because tests assert expected behavior rather than `xfail`, unpatched defects stay visibly red until fixed and will automatically turn green upon retest.

---

### 3.2 Performance Evidence Consolidation (Order 3b — Locust Load Testing)

Load testing was conducted in Week 5 using Locust (`05_Security_Performance/locustfile.py`) across seven core API endpoints (`POST /api/register`, `POST /api/login`, `GET /api/categories`, `POST /api/tasks`, `GET /api/tasks`, `PUT /api/tasks/<id>`, and `GET /api/dashboard`) against the local Flask development server (`127.0.0.1:5000`).

| Test ID | Load Stage | Virtual Users & Spawn Rate | Duration | Total Requests | Error Rate | Avg Latency | P95 Latency | Throughput | Evaluation Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `PERF-01` | Stage 1 (Baseline) | 10 users (`2/s`) | 30s | 221 | 0.00% | 24 ms | 140 ms | 7.55 req/s | **Pass** (`Avg < 200 ms`, `P95 < 500 ms`) |
| `PERF-02` | Stage 2 (Moderate) | 50 users (`10/s`) | 30s | 1,073 | 0.00% | 47 ms | 310 ms | 36.92 req/s | **Pass** (`Avg < 200 ms`, `P95 < 500 ms`) |
| `PERF-03` | Stage 3 (High Load) | 100 users (`20/s`) | 30s | 2,122 | 0.00% | 95 ms | 520 ms | 72.19 req/s | **Observation** (`P95 > 500 ms`; `PERF-OBS-01/02`) |
| **Total** | **All Stages** | **10 → 100 users** | **90s** | **3,416** | **0.00%** | — | — | **Up to 72.19 req/s** | **Zero HTTP 5xx/4xx errors under load** |

#### Performance Findings & Bottleneck Analysis
* **Reliability & Scaling:** Across all **3,416 requests**, PyTodo Pro recorded **0.00% HTTP errors** and scaled throughput linearly from `7.55 req/s` (10 users) to `72.19 req/s` (100 users), meeting the `< 200 ms` average latency target at every stage.
* **Authentication CPU Bottleneck (`PERF-OBS-01` / `PERF-OBS-02`):** At 100 concurrent users (`PERF-03`), overall P95 response time reached **520 ms**, exceeding the `500 ms` target by `20 ms`. Endpoint-level metrics showed that task CRUD and dashboard routes stayed fast, whereas `POST /api/register` and `POST /api/login` dominated tail latency due to synchronous Werkzeug PBKDF2 password hashing on the single-threaded Flask development server.
* **Environment Caveat:** A cross-machine re-run on a 2-core Linux environment (`evidence_performance_rerun.txt`) reproduced the same relative authentication slowdown (`1,521 ms` login average) but confirmed that absolute latency values depend heavily on host CPU capacity and development-server threading limits.

---

## 5. Process Improvements to Prevent Recurring Defects (Automation & Tooling)

* **Standardize Reproducible Test Environments and Pre-Merge Regression Gates:**  
  During Weeks 2–6, test dependencies (`pytest`, `pytest-cov`, `selenium`, `locust`) were omitted from `requirements.txt` (requiring manual per-machine setup across different Python versions), and early API suites wrote directly to the shared `pytodo_pro.db` SQLite database (`S-02`). Pinning all test and linting tools in a dedicated `requirements-dev.txt`, enforcing isolated `tmp_path` database fixtures across every test suite (as implemented in `06_Automation_Regression/tests/conftest.py`), and running `pytest 06_Automation_Regression/tests/ -m regression` automatically on every pull request would eliminate environment drift, prevent database state pollution, and catch boundary or parity regressions (`D-001`, `D-004`, `D-013`, `D-022`) before changes are merged.