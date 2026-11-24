# Week 4 Testing Metrics Summary - PyTodo Pro

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Scope:** Web workflow scenarios, JSON API testing of all 9 endpoints, and UI vs API comparison

**Contributors:**
- Nisrina (Automation/Tool Coordinator) - tool setup, `api_endpoints.md`, auth and categories API tests
- Aida (Test Design Coordinator) - `web_test_scenarios.md`, `api_test_data.md`, task, delete and dashboard API tests
- QA/Test Lead - `ui_vs_api_comparison.md`, `test_ui_vs_api.py`
- Nafiesa (Defect & Metrics Coordinator) - extra delete and dashboard tests, `defect_log.md`, this summary

**How we measured:** all four test files were run together on 24 Nov 2026 with `pytest 04_Web_API/tests -v` on a fresh clone (Python 3, Flask test client).

---

## 1. Week 4 Traceability Matrix

| Activity | Owner | File(s) | Cases | Passed | Failed | Pass Rate | Defects linked |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| Auth and categories API (`/api/register`, `/api/login`, `/api/categories`) | Nisrina | `api_test_cases.md` §1–3, `tests/test_api_auth.py` | 19 | 16 | 3 | 84.21% | D-013, D-019 |
| Task API (`GET`, `POST`, `PUT`, `DELETE /api/tasks`) and dashboard | Aida | `api_test_cases.md` §4–9, `tests/test_api_tasks.py` | 36 | 27 | 9 | 75.00% | D-001, D-006, D-019, D-020, D-021, D-022, D-023, D-024, D-025 |
| Extra delete and dashboard checks | Nafiesa | `api_test_cases_delete_dashboard.md`, `tests/test_api_delete_dashboard.py` | 10 | 6 | 4 | 60.00% | D-005, D-006, D-024, D-025 |
| UI vs API comparison | QA/Test Lead | `ui_vs_api_comparison.md`, `tests/test_ui_vs_api.py` | 30 | 16 | 14 | 53.33% | D-001, D-004, D-006, D-012, D-013, D-014, D-019 to D-025 |
| Web workflow scenarios | Aida | `web_test_scenarios.md` | 8 workflows + 6 validation checks | - | - | - | D-011 |

Note: the web scenarios describe expected behaviour and validation gaps but do not record a Pass/Fail per scenario, so they are not counted in the totals below. `test_api_smoke.py` (2 setup checks, both pass) is also not counted.

---

## 2. Test Execution Metrics (Week 4)

| Metric Category | Count | Percentage |
| :--- | :---: | :---: |
| **Automated Test Cases Planned** | 95 | 100% |
| **Executed** | 95 | 100.00% |
| **Passed** | 65 | 68.42% |
| **Failed** | 30 | 31.58% |
| **Blocked / Not Run** | 0 | 0.00% |

- **Execution Rate:** **100%** (95 / 95)
- **Overall Pass Rate:** **68.42%** (65 / 95)
- **Overall Failure Rate:** **31.58%** (30 / 95)

### Results by endpoint (API test cases only, 65 cases)

| Endpoint | Cases | Passed | Failed |
| :--- | :---: | :---: | :---: |
| `POST /api/register` | 9 | 7 | 2 |
| `POST /api/login` | 7 | 6 | 1 |
| `GET /api/categories` | 3 | 3 | 0 |
| `GET /api/tasks` | 7 | 6 | 1 |
| `GET /api/tasks/<id>` | 5 | 5 | 0 |
| `POST /api/tasks` | 8 | 5 | 3 |
| `PUT /api/tasks/<id>` | 7 | 5 | 2 |
| `DELETE /api/tasks/<id>` | 8 (5 + 3) | 4 | 4 |
| `GET /api/dashboard` | 11 (4 + 7) | 8 | 3 |
| **Total** | **65** | **49** | **16** |

`DELETE /api/tasks/<id>` has the lowest pass rate (50%). It also holds one of the two Critical defects.

---

## 3. Defect Metrics

### 3.1 New defects found in Week 4

| Defect ID | Title (short) | Severity | Priority | Found by |
| :--- | :--- | :---: | :---: | :--- |
| **D-019** | Wrong data types crash the API with HTTP 500 | Moderate | Medium | API-REG-08, API-LOG-06, API-TSK-POST-07, TC-API-UI-06 |
| **D-020** | SQL injection in `GET /api/tasks?q=` | **Critical** | High | API-TSK-GETALL-04, TC-API-UI-27 |
| **D-021** | Non-existent `category_id` accepted | Moderate | Low | API-TSK-POST-08, TC-API-UI-16 |
| **D-022** | `PUT` accepts an empty title | Major | Medium | API-TSK-PUT-03, TC-API-UI-18 |
| **D-023** | `"done": "false"` completes the task | Moderate | Medium | API-TSK-PUT-06, TC-API-UI-22 |
| **D-024** | Delete returns 200 for a missing task | Minor | Low | API-TSK-DEL-02, API-DD-02, TC-API-UI-23 |
| **D-025** | Any user can delete another user's task (IDOR) | **Critical** | High | API-TSK-DEL-05, API-DD-01, TC-API-UI-24 |

### 3.2 Earlier defects confirmed again through the API

| Defect ID | Week 4 test case(s) | What Week 4 adds |
| :--- | :--- | :--- |
| D-001 | API-DASH-01, TC-API-UI-14 | The API urgency and the dashboard count also treat "today" as Overdue |
| D-004 | TC-API-UI-02 | The API rejects an 8-character password too (shared helper) |
| D-005 | API-DD-08 | `GET /api/dashboard` also misses the 7th day |
| D-006 | API-TSK-POST-04, TC-API-UI-15, API-DD-10 | **New effect:** one bad date also crashes the dashboard (500) |
| D-011 | WTS-VAL-03 | The web **edit** route has the same blank-title gap as create |
| D-012 | TC-API-UI-12 | The API also has no title length limit |
| D-013 | API-REG-09, TC-API-UI-04 | The API also accepts duplicate usernames |
| D-014 | TC-API-UI-25, TC-API-UI-26 | The API search also treats `_` and `%` as wildcards |

All 30 failed cases are linked to a logged defect. No failure was left unexplained.

### 3.3 Week 4 Defect Distribution

| Metric | Count |
| :--- | :---: |
| **New defects found in Week 4** | 7 (D-019 to D-025) |
| **Critical** | 2 (D-020, D-025) |
| **Major** | 1 (D-022) |
| **Moderate** | 3 (D-019, D-021, D-023) |
| **Minor** | 1 (D-024) |
| **Earlier defects confirmed through the API** | 8 |
| **Draft IDs merged** | 4 (DEF-API-01, DEF-API-02, DEF-API-03, draft "D-009") |

- **API-only defects:** all 7 new defects (D-019 to D-025) can only be reached by calling the API directly. The web forms either cannot send such input or the web routes already check it.
- **Security defects:** 2 Critical (D-020, D-025). Both are API-only: the web routes use a parameterised query and check the task owner, but the API does not.

### 3.4 Cumulative Defect Status (Week 1 to Week 4)

| Metric | Count |
| :--- | :---: |
| **Total defect IDs logged** | 25 (D-001 to D-025) |
| **Unique defects** | 23 |
| **Closed as duplicate** | 2 (D-002, D-003) |
| **Open (incl. Confirmed)** | 23 |
| **Resolved** | 0 |

| Week | Technique | New defects |
| :--- | :--- | :---: |
| Week 1 | Black-box | 3 |
| Week 2 | White-box | 1 |
| Week 3 | Special testing | 12 |
| Week 4 | Web and API | 7 |
| **Total** | | **23** |

| Severity | Count | Percentage |
| :--- | :---: | :---: |
| Critical | 2 | 8.70% |
| Major | 6 | 26.09% |
| Moderate | 10 | 43.48% |
| Minor | 5 | 21.74% |

---

## 4. Test Suite Notes

1. **`conftest.py` uses the real `pytodo_pro.db`.** On a fresh clone the file has no tables, so 13 of the 19 tests in `test_api_auth.py` fail with `no such table` before any app logic runs. After running `init_db()` once, the results match the team's report (16 passed, 3 failed). `test_ui_vs_api.py` and `test_api_delete_dashboard.py` avoid this by creating a temporary database in each test. **Suggestion (Nisrina):** use the same temporary-database fixture in `conftest.py`, so every test file works on any machine.
2. **README endpoint split is out of date.** The README assigns `GET /api/tasks` to the QA/Test Lead and `DELETE`/dashboard to the Defect & Metrics Coordinator, but `api_test_cases.md` sections 4–9 were all prepared and run by Aida. The extra delete and dashboard checks are in `test_api_delete_dashboard.py`. **Suggestion (QA/Test Lead):** update the table when writing the final README.
3. **Missing evidence.** `web_test_scenarios.md` refers to `WTS-VAL-03.png`, which is not in the repo. `ui_vs_api_comparison.md` lists 10 UI checks done by hand with no screenshot yet.
4. **Two defect logs.** `04_Web_API/defect_log.md` holds draft IDs (DEF-API-01 to 03). The official IDs are in `01_Black_Box/defect_log.md`, with a mapping table at the top.

---

## 5. Outstanding Actions

| Owner | Action |
| :--- | :--- |
| Nisrina | Change `conftest.py` to use a temporary database (note 1). Add "Logged as D-019 / D-013" next to DEF-API-01 to 03 in `04_Web_API/defect_log.md`. |
| Aida | Upload `WTS-VAL-03.png`. Change the draft "D-009" in `web_test_scenarios.md` to D-011. |
| QA/Test Lead | Add screenshots for the 10 hand-checked UI cases. Update the README endpoint table. Write the Week 4 README summary. |
| All (Week 5) | Add D-020 (SQL injection) and D-025 (IDOR delete) to the STRIDE table as confirmed threats TH-07 and TH-21. |

---

## 6. Week 4 Summary & Conclusion

- **Progress:** All 9 API endpoints were tested, with 95 automated cases and a 100% execution rate. 8 web workflows and 6 validation checks were also documented.
- **Quality status:** 65 of 95 cases passed (68.42%). Every failure is linked to a logged defect.
- **Key findings:**
  1. **The API is less safe than the web UI.** The two Critical defects found so far (D-020 SQL injection, D-025 cross-user delete) exist only in the API. The web routes for the same features are protected. This shows why the server must check every rule, and why API testing is needed even when the UI looks correct.
  2. **The API trusts input too much.** Wrong data types, unknown categories, empty titles and the text `"false"` are all accepted or crash the server (D-019, D-021, D-022, D-023).
  3. **Old defects reach further than we knew.** API testing confirmed 8 earlier defects, and showed that D-006 also breaks the dashboard.
- **Risk for next week:** 2 Critical and 6 Major defects are open, and none are fixed. Week 5 (security and performance) should start from D-020 and D-025, because both are confirmed and easy to exploit.
