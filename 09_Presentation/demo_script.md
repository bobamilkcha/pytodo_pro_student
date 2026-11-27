# Week 9: Live Automation & Coverage Demo Script

**Presenter:** Automation/Tool Coordinator (Nisrina)  
**Target Duration:** 3–4 minutes  
**Pre-Demo Setup (Run 5 minutes before presenting):**
1. Open VS Code in `C:\Users\nisrina\Desktop\pytodo_pro_student` with two split PowerShell terminals.
2. Activate the virtual environment in both terminals: `.\venv\Scripts\Activate.ps1`
3. Start the Flask server in **Terminal 1** (needed only if running Selenium UI tests): `python app.py`
4. Keep **Terminal 2** clear for live `pytest` commands, and have `06_Automation_Regression/logs/full_suite.log` open in an editor tab as offline backup.

---

## Step 1: Run the Focused Regression Suite (`~15 seconds`)

**Command (Terminal 2):**
```powershell
pytest 06_Automation_Regression/tests/ -m regression -v
```

**Expected Output:**
* `51 passed/failed selected, 52 deselected` → **`22 passed, 29 failed in ~14.6s`** (`0 errors`).

**Talking Points:**
* *"We tagged 51 high-risk unit, API, and markup tests with `@pytest.mark.regression` in `pytest.ini` so developers can run a fast smoke/regression check after any code change."*
* *"Notice there are 0 script errors. The 22 passing tests verify our core baseline—registration, login, task CRUD, toggling `Open` to `Done`, filtering, and web ownership protection."*
* *"The 29 failures are intentional: we wrote standard assertions for expected behavior rather than `xfail`, so all 16 unpatched defect types stay visibly red until fixed."*

---

## Step 2: Show a Known Defect Failing Live (`~5 seconds`)

**Command (Terminal 2):**
```powershell
pytest 06_Automation_Regression/tests/unit/test_bva_unit.py 06_Automation_Regression/tests/api/test_ep_and_core_api.py -k "eight_char_password or cross_user_delete" -v
```

**Expected Output:**
* `test_tc_bb_bva_f01_02_eight_char_password` → **FAILED** (`AssertionError: assert False is True` on `is_valid_password('Pass1234')` — **Defect D-004**).
* `test_tc_sec_21_cross_user_delete_blocked` → **FAILED** (`AssertionError: assert 200 in (403, 404)` on `DELETE /api/tasks/<id>` — **Defect D-025**).

**Talking Points:**
* *"Here are two real defects caught automatically: first, `is_valid_password('Pass1234')` fails our Week 1 BVA exact-boundary test (`D-004`) because `helpers.py` checks `len(pw) > 8` instead of `>= 8`."*
* *"Second, `DELETE /api/tasks/<id>` returns `200 OK` when User B deletes User A's task (`D-025`) because the API query omits `AND user_id = ?`, unlike the web route."*

---

## Step 3: Show the Live Statement & Branch Coverage Report (`~5 seconds`)

**Command (Terminal 2):**
```powershell
pytest 06_Automation_Regression/tests/unit 06_Automation_Regression/tests/api --cov=app --cov=helpers --cov-branch --cov-report=term-missing
```

**Expected Output:**
* Displays statement and branch coverage percentages for `app.py` and `helpers.py` along with exact `Missing` line/branch numbers.

**Talking Points:**
* *"Using `pytest-cov` with `--cov-branch`, our combined automated tests reach ~95% statement and ~89% branch coverage across `app.py` and `helpers.py`."*
* *"This also illustrates an important QA lesson: `compute_urgency()` in `helpers.py` reached 100% branch coverage in Week 2, yet still missed Defect `D-001` (tasks due today labeled Overdue) because a missing `due == today` condition creates no branch for a coverage tool to flag."*

---

## Step 4 (Optional / If Time Permits): End-to-End Selenium Browser Test (`~10 seconds`)

*(Ensure `python app.py` is running in Terminal 1 before running this command.)*

**Command (Terminal 2):**
```powershell
pytest 06_Automation_Regression/tests/ui/test_ui_auth.py -v
```

**Expected Output:**
* `test_wts_01_02_08_auth_lifecycle PASSED` (`1 passed in ~5s`).

**Talking Points:**
* *"We excluded Selenium scripts from `@pytest.mark.regression` to keep per-commit runs fast, running them instead before demos or releases to verify end-to-end browser sessions."*