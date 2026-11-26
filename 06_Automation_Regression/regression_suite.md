# Week 6: Focused Regression Suite

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**PyTest Marker:** `@pytest.mark.regression` (registered in `pytest.ini`)

---

## 1. Selection Criteria

The focused regression suite runs after every code change to verify core user workflows and track active high-impact defects without waiting for slower end-to-end browser scripts.

* **Fast execution:** Includes only direct `PyTest` unit and Flask test-client (`PyTest API`) checks (completes in ~1–2 seconds).
* **Core flow protection:** Covers registration, login, session redirects, task creation, status toggling, and task deletion.
* **Known defect tracking:** Covers active defects (`D-001`, `D-004`, `D-005`, `D-006`, `D-010`, `D-011`, `D-013`, `D-020`, `D-022`, `D-025`) using standard assertions so unfixed bugs remain visible as caught failures until patched.
* **Excluded from per-commit regression:** Selenium UI scripts (`tests/ui/`) are excluded from `@pytest.mark.regression` due to browser startup overhead and are executed separately prior to demos or releases.

---

## 2. Execution Command

Run only the marked regression subset from the project root:

```powershell
pytest 06_Automation_Regression/tests/ -m regression -v