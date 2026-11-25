# Week 5: Performance Test Results

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Test Script:** `05_Security_Performance/locustfile.py`  
**Target Host:** `http://127.0.0.1:5000`

---

## 1. Aggregated Summary Across Load Stages

| Load Stage | Concurrent Users | Total Requests | Failed Requests | Error Rate (%) | Avg Response Time (ms) | Median / P50 (ms) | P90 (ms) | P95 (ms) | Max (ms) | Throughput (req/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1 (Baseline)** | 10 | 221 | 0 | 0.00% | 24 | 10 | 45 | 140 | 204 | 7.55 |
| **Stage 2 (Moderate)** | 50 | 1,073 | 0 | 0.00% | 47 | 13 | 84 | 310 | 770 | 36.92 |
| **Stage 3 (High Load)** | 100 | 2,122 | 0 | 0.00% | 95 | 19 | 360 | 520 | 1,478 | 72.19 |

---

## 2. Detailed Endpoint Metrics by Stage

### Stage 1: 10 Concurrent Users (`-u 10 -r 2 -t 30s`)

| Method | Endpoint | Requests | Failures | Error Rate | Avg (ms) | Min (ms) | Median (ms) | P95 (ms) | Max (ms) | Throughput (req/s) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/api/categories` | 36 | 0 | 0.00% | 10 | 5 | 10 | 22 | 45 | 1.23 |
| `GET` | `/api/dashboard` | 63 | 0 | 0.00% | 9 | 4 | 8 | 21 | 45 | 2.15 |
| `POST` | `/api/login` | 10 | 0 | 0.00% | 148 | 127 | 140 | 200 | 204 | 0.34 |
| `POST` | `/api/register` | 10 | 0 | 0.00% | 147 | 116 | 150 | 180 | 182 | 0.34 |
| `GET` | `/api/tasks` | 64 | 0 | 0.00% | 10 | 4 | 8 | 23 | 75 | 2.19 |
| `POST` | `/api/tasks` | 19 | 0 | 0.00% | 19 | 11 | 16 | 44 | 43 | 0.65 |
| `DELETE` | `/api/tasks/<id>` | 19 | 0 | 0.00% | 16 | 11 | 16 | 32 | 32 | 0.65 |
| **Total** | **Aggregated** | **221** | **0** | **0.00%** | **24** | **4** | **10** | **140** | **204** | **7.55** |

---

### Stage 2: 50 Concurrent Users (`-u 50 -r 10 -t 30s`)

| Method | Endpoint | Requests | Failures | Error Rate | Avg (ms) | Min (ms) | Median (ms) | P95 (ms) | Max (ms) | Throughput (req/s) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/api/categories` | 181 | 0 | 0.00% | 13 | 5 | 10 | 30 | 84 | 6.23 |
| `GET` | `/api/dashboard` | 268 | 0 | 0.00% | 15 | 5 | 10 | 47 | 220 | 9.22 |
| `POST` | `/api/login` | 50 | 0 | 0.00% | 289 | 219 | 280 | 380 | 522 | 1.72 |
| `POST` | `/api/register` | 50 | 0 | 0.00% | 412 | 265 | 390 | 710 | 770 | 1.72 |
| `GET` | `/api/tasks` | 350 | 0 | 0.00% | 15 | 5 | 11 | 42 | 136 | 12.04 |
| `POST` | `/api/tasks` | 87 | 0 | 0.00% | 22 | 10 | 19 | 44 | 84 | 2.99 |
| `DELETE` | `/api/tasks/<id>` | 87 | 0 | 0.00% | 22 | 11 | 20 | 40 | 56 | 2.99 |
| **Total** | **Aggregated** | **1,073** | **0** | **0.00%** | **47** | **5** | **13** | **310** | **770** | **36.92** |

---

### Stage 3: 100 Concurrent Users (`-u 100 -r 20 -t 30s`)

| Method | Endpoint | Requests | Failures | Error Rate | Avg (ms) | Min (ms) | Median (ms) | P95 (ms) | Max (ms) | Throughput (req/s) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/api/categories` | 327 | 0 | 0.00% | 40 | 5 | 14 | 190 | 582 | 11.13 |
| `GET` | `/api/dashboard` | 531 | 0 | 0.00% | 42 | 4 | 15 | 210 | 544 | 18.07 |
| `POST` | `/api/login` | 100 | 0 | 0.00% | 427 | 230 | 400 | 630 | 716 | 3.40 |
| `POST` | `/api/register` | 100 | 0 | 0.00% | 662 | 177 | 640 | 1,200 | 1,478 | 3.40 |
| `GET` | `/api/tasks` | 694 | 0 | 0.00% | 46 | 5 | 16 | 230 | 606 | 23.61 |
| `POST` | `/api/tasks` | 185 | 0 | 0.00% | 78 | 12 | 25 | 400 | 1,276 | 6.29 |
| `DELETE` | `/api/tasks/<id>` | 185 | 0 | 0.00% | 58 | 12 | 26 | 230 | 949 | 6.29 |
| **Total** | **Aggregated** | **2,122** | **0** | **0.00%** | **95** | **4** | **19** | **520** | **1,478** | **72.19** |

---

## 3. Key Observations (Data Summary for Interpretation)

* **Zero Failures:** Across all 3 stages (3,416 total requests), the error rate remained **0.00%** with zero timeouts or HTTP `500` responses.
* **Throughput Scaling:** Throughput scaled nearly linearly with concurrent users—from **7.55 req/s** (10 users) to **36.92 req/s** (50 users) and **72.19 req/s** (100 users).
* **Authentication Bottleneck:** `POST /api/register` (147 ms → 412 ms → 662 ms avg) and `POST /api/login` (148 ms → 289 ms → 427 ms avg) exhibited significantly higher latency than task/category endpoints due to CPU-intensive password hashing (`werkzeug.security`) during simultaneous user ramp-up.
* **Read/Write Task Stability:** Core task and dashboard endpoints stayed fast even at 100 concurrent users (median response times between **14 ms and 26 ms**), with P95 crossing the 500 ms threshold overall (520 ms) primarily due to the authentication burst during initial spawn.