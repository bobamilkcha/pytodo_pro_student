# Week 5: Performance Results - Interpretation, Limitations and Recommendations

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Based on:** `performance_plan.md`, `performance_results.md` and `locustfile.py` (Nisrina, Automation/Tool Coordinator)
**Confirmation run:** `evidence_performance_rerun.txt` (same script, second machine)

This file covers the brief's Week 5 deliverables "performance results and interpretation" and "security/performance limitations and recommendations". The raw numbers stay in Nisrina's `performance_results.md`. This file explains what they mean.

---

## 1. Checking the results

| Check | Result |
| :--- | :--- |
| Endpoint requests add up to each stage total (221, 1,073, 2,122) | Pass |
| Stage totals add up to 3,416 requests | Pass |
| Throughput is close to requests ÷ 30 s in each stage | Pass (small differences come from ramp-up time) |
| The same pattern repeats on a second machine (`evidence_performance_rerun.txt`) | Pass: 0 errors, near-linear throughput, login and register slowest |

The numbers in `performance_results.md` are consistent, and the pattern can be repeated.

## 2. Results against the targets in the plan

Targets from `performance_plan.md`: average below 200 ms, P95 below 500 ms, error rate below 1%, and throughput that grows with the number of users.

| Stage | Users | Avg (ms) | P95 (ms) | Error rate | Throughput (req/s) | Avg target | P95 target | Error target | Throughput |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 Baseline | 10 | 24 | 140 | 0.00% | 7.55 | Met | Met | Met | Base |
| 2 Moderate | 50 | 47 | 310 | 0.00% | 36.92 | Met | Met | Met | ×4.9 for ×5 users |
| 3 High | 100 | 95 | **520** | 0.00% | 72.19 | Met | **Not met** (+20 ms) | Met | ×9.6 for ×10 users |

**Overall:** the API met every target at 10 and 50 users. At 100 users it met three of the four targets. Only the overall P95 was slightly above 500 ms.

## 3. What the results mean

1. **The API stayed stable up to 100 users.** No request failed in 3,416 requests: no HTTP 500, no timeout and no "database is locked" error. Within this workload, the app does not break under load.

2. **The server kept up with the load.** Ten times more users gave 9.6 times more throughput. If the server were saturated, throughput would level off while users kept rising. That did not happen here.

3. **Response time grew faster than it should, mainly at the slow end.** From 10 to 100 users, the average grew about 4 times (24 → 95 ms) and P95 about 3.7 times (140 → 520 ms). The median only went from 10 to 19 ms. So most requests stayed fast, but a growing group of requests waited much longer. This is typical of requests queuing for one busy server process.

4. **Login and register are the bottleneck.**

   | Endpoint | Avg at 10 users | Avg at 50 users | Avg at 100 users | P95 at 100 users |
   | :--- | :---: | :---: | :---: | :---: |
   | `POST /api/register` | 147 ms | 412 ms | 662 ms | 1,200 ms |
   | `POST /api/login` | 148 ms | 289 ms | 427 ms | 630 ms |
   | Task, dashboard and category endpoints (range) | 9–19 ms | 13–22 ms | 40–78 ms | 190–400 ms |

   Both endpoints compute a password hash, which is slow **on purpose**: it makes stolen password hashes hard to crack. Our Week 5 security test TC-SEC-13 confirmed this hashing works. The slowness is the cost of a security control, not a coding mistake.

5. **The P95 breach comes from login and register, not the task features.** Every task, dashboard and category endpoint stayed below 500 ms P95 in all three stages (the highest was `POST /api/tasks` at 400 ms). Only 200 of the 2,122 requests in Stage 3 were logins and registrations, but most of them took over 400 ms, so they fill the slowest 5% of requests and push the overall P95 to 520 ms.

6. **The script made the login burst worse than real use.** Each simulated user registers and logs in once, at the start. With a spawn rate of 20 users per second, all 100 users hash their passwords within about 5 seconds. Real users log in at different times. The Stage 3 result is therefore a **worst case** for login bursts, not typical daily use.

7. **The results depend on the machine.** On a 2-core machine (`evidence_performance_rerun.txt`), Stage 3 was much slower: login averaged 1,521 ms and the overall P95 was 1,600 ms, with still no errors. Password hashing needs CPU time, so fewer cores means longer queues. This means our numbers describe *this* setup, not the app in general.

## 4. Link to security findings

The performance and security results connect in one important way:

- Login and register are the most expensive requests on the server (finding 4).
- The app has **no rate limit** on login (D-026, Major).

Together, these mean an attacker could send many login requests and keep the CPU busy hashing passwords, which would slow the app down for everyone. Our load test did not try this, because the brief asks for controlled testing. It is still a reason to treat D-026 as a priority. The test also ran with `debug=True` (D-031) on Flask's development server, which is not meant for real users.

## 5. Defect decision

**No new defect was logged.** *(Update 27 Nov: D-036 has since been used for a state transition defect, so the next free ID is **D-037**.)*

| Reason | Detail |
| :--- | :--- |
| No failure | 0 errors in all stages |
| Targets met under normal load | The plan sets the targets for normal load. Stages 1 and 2 met all of them |
| The one miss has a known, intended cause | The Stage 3 P95 (520 ms) is caused by deliberate password hashing during a burst of logins that real use would not produce |
| No performance requirement in the app's specification | The 200 ms / 500 ms targets are our own test targets, not a requirement the developers were given |

Instead, it is recorded as a **performance observation** for the risk section of the final report:

| ID | Observation | Risk | Suggested owner of decision |
| :--- | :--- | :--- | :--- |
| PERF-OBS-01 | Login and register response time grows quickly with concurrent users (avg 662 ms, P95 1,200 ms at 100 users) | Slow sign-in at peak times; possible slowdown attack combined with D-026 | Developers |
| PERF-OBS-02 | Overall P95 is 520 ms at 100 users, just above our 500 ms target | Users at peak load may notice delays | Team, when setting a final target |

If the team decides that the 500 ms target should also apply at 100 users, PERF-OBS-02 can be logged as **D-037** (Minor, Low priority). I will add it to the log if we agree.

## 6. Limitations of the experiment

| # | Limitation | Effect on the results |
| :--- | :--- | :--- |
| 1 | Load generator and server ran on the same laptop | They compete for CPU, so response times are partly caused by Locust itself |
| 2 | Flask development server with `debug=True`, not a production server (e.g. Gunicorn or Waitress) | A production setup could behave better or differently |
| 3 | Each stage ran for only 30 seconds, once | No warm-up, no repeat runs, so we cannot say how much results vary. No long (soak) test for memory or database growth |
| 4 | Small data: each user creates a task and deletes it straight away | `GET /api/tasks` returns very short lists. Users with hundreds of tasks were not tested, and neither was a large `per_page` (D-034) |
| 5 | Light write load (1 in 10 tasks writes) on SQLite | SQLite allows one writer at a time. Heavier writing could cause "database is locked" errors that this test could not show |
| 6 | API only | Web pages (HTML rendering) were not load tested |
| 7 | Maximum 100 users | We did not find the point where the app starts to fail |
| 8 | Local loopback network | No real network delay, so real users would see slower times |

## 7. Recommendations

**For the developers (proposed; they decide):**
1. Add rate limiting on `/login` and `/api/login` (fixes D-026, and protects the expensive hashing step).
2. Run the app on a production server with several workers, with `debug` off (fixes D-031, and lets requests run in parallel).
3. Keep the current password hashing strength. Do not weaken it to gain speed.
4. If many users are expected, move from SQLite to a database built for concurrent writes.

**For future testing:**
1. Run the load generator on a different machine from the server.
2. Repeat each stage 3 times, and report the average and the spread.
3. Separate the login burst from steady use: log users in first, then measure the task endpoints on their own.
4. Add a stress test that increases users until errors appear, a 30-minute soak test, and a test with users who own many tasks.
5. Load test one or two web pages (`/`, `/dashboard`), not only the API.

## 8. Small fixes needed in the Week 5 performance files (for Nisrina)

| # | File | Issue | Fix |
| :--- | :--- | :--- | :--- |
| 1 | `performance_plan.md` | The file stops after `python app.py`: the code block is not closed, and the Locust commands, workload (users, spawn rate, duration, task mix 4:3:2:1, 1–2 s wait) and load stages are missing. The brief says the workload must be defined **before** execution | Complete sections 2 and 3, and close the code block |
| 2 | `performance_plan.md` | Database is named `pytodo.db` | The app uses `pytodo_pro.db` |
| 3 | `requirements.txt` / README | Locust is not listed, so the test cannot be set up from the README | Add `locust` and the run command |
| 4 | `performance_results.md` | Machine details (CPU cores, RAM) are not stated | Add them, since the re-run shows the results depend on hardware |
