# Week 9 Standards Integration: Defect & Metrics Coordinator (Nafiesa)

**Date:** 27 Nov 2026
**Task:** Week 9, QA and process improvements for an Agile/DevOps workflow (brief: "Identify QA/process improvements that could be incorporated into an Agile/DevOps workflow")
**For:** Integration into `08_Final_QA_Report/final_qa_report.md` (QA/Test Lead)
**Based on:** `07_Test_Management/defect_log.md`, `08_Final_QA_Report/metrics.md`, `06_Automation_Regression/week6_defect_check.md`

---

## QA and process improvements for an Agile/DevOps workflow

In Agile and DevOps, a team delivers small changes often, so quality checks have to run continuously, not once at the end (Forsgren et al., 2018). Our project tested a finished app in weekly phases, which is closer to a traditional test stage. Below are five improvements that would move this QA work into an Agile/DevOps workflow. Each one is based on something we observed.

| # | Improvement | Where it fits | Evidence from our project | Defects it would have prevented or caught earlier |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Definition of Done includes tests and a security check.** A user story is "done" only when it has automated tests for its normal path, invalid input and another user's data. | Sprint planning and review | Both Critical API defects come from a missing check that the web version of the same feature has | D-020, D-025, D-022 |
| 2 | **Shift-left review of risky code.** A short peer review checklist for every pull request: parameterised SQL, owner check on every query by id, no secrets in code, no `debug=True`. | Pull request, before merge | D-020, D-027 and D-031 are each one visible line in `app.py` that a checklist would catch | D-020, D-025, D-027, D-031 |
| 3 | **Static analysis in the pipeline.** Run a Python security linter (for example Bandit) and an accessibility check (for example axe or Lighthouse CI) on every push. | CI pipeline (with the regression suite) | Week 3 accessibility defects were found with axe and Lighthouse but are checked only once; secrets and debug mode are findings a linter reports automatically | D-009, D-015, D-016, D-017, D-027, D-031 |
| 4 | **Defect-to-test rule** (section B). Every defect gets a failing regression test, and it is closed only when that test passes in the pipeline. | Defect workflow, linked to CI | Same defects rediscovered across 3–4 weeks; 2 duplicate IDs in Week 1 | Duplicates and re-opened defects in general |
| 5 | **Shared definition of the rules between web and API.** Validation (title, password, due date, category) lives in one function, used by both web and API routes, and is tested once. | Design and code review | The same rule is applied differently by web and API in D-006, D-011/D-022, D-019, D-020 and D-025 | D-006, D-011, D-019, D-021, D-022 |

Improvement 3 matters because accessibility is easy to break again with any template change. WCAG 2.2 (World Wide Web Consortium, 2023) gives testable success criteria, such as labels and contrast, so most of the checks we did by hand in Week 3 can run automatically on each push.

**Metrics to track each sprint.** These continue the metrics we already calculate, so the team can see whether quality is improving:
- defects found per sprint by severity, and how many were found **before** merge rather than after;
- the pass rate of the regression suite (it should rise as fixes arrive; today it is 43.1%: 22 of the 51 regression tests pass);
- automated defect coverage (96.9% today; the target is 100%);
- the time from a defect being logged to it being `Closed`.

These metrics only help if the team reads them as signals, not targets. For example, a falling defect count could mean that testing has stopped, not that the app got better.

**Link to the other sections.** These improvements are process rules: what must be tested before code is merged, and how defects move through their lifecycle. They assume a CI step that runs `pytest 06_Automation_Regression/tests -m regression` on every push or pull request, as recommended in `section_3_5_automation_performance.md`. We did not build that pipeline in this project, so it is a recommendation, not something we tested.

### Summary for the final report

Our testing found that most defects come from missing checks that a continuous process would catch early: the same rule applied differently in the web pages and the API, secrets and debug settings left in the code and defects that were found again in later weeks because they had no automated test. The five improvements above move these checks earlier (shift-left), make them automatic on every change and tie every defect to a regression test. It complements the Week 9 CI/CD section (Automation/Tool Coordinator), which covers where the regression suite would run.

### References

Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean software and DevOps: Building and scaling high performing technology organizations*. IT Revolution Press.

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. W3C. https://www.w3.org/TR/WCAG22/
