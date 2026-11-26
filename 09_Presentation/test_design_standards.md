# Week 9 Standards Integration: Test Design Coordinator (Aida)

**Date:** 26 Nov 2026
**Task:** Week 9, Order 2c — Link to ISO 9001 and CMMI where relevant (brief)
**For:** Integration into `08_Final_QA_Report/final_qa_report.md` (QA/Test Lead)

---

## Link to ISO 9001 and CMMI

Although our team evaluated PyTodo Pro as an independent QA team rather than managing its development organization, our testing workflow and artefacts align directly with core quality management practices in **ISO 9001:2015** and **CMMI**:

### 1. Alignment with ISO 9001 (Quality Management Principles)

| ISO 9001 Concept | How It Applies to Our PyTodo Pro QA Work | Supporting Artefacts |
| :--- | :--- | :--- |
| **Process Approach & Planned Control** | Rather than ad-hoc exploratory clicking, we structured testing across progressive weekly stages (black-box, white-box, special testing, web/API, security/performance, automation, and test management) governed by explicit entry and exit criteria (`EX-1` to `EX-11`). | `07_Test_Management/test_plan.md` |
| **Documented Information & Traceability** | Every requirement (`F-01` to `F-22`, `NFR-01` to `NFR-03`) is mapped forward to test cases and backward from defects (`D-001` to `D-036`) using standardized templates, ensuring auditable records across all 286 unique checks. | `07_Test_Management/rtm.md`, `master_test_repository.md` |
| **Nonconformity & Corrective Tracking** | Confirmed failures were logged with reproducible steps, severity, and priority, cross-checked across artefacts (`cross_check_defects.md`), and linked to automated regression guards so fixes can be verified objectively before closure. | `07_Test_Management/defect_log.md`, `06_Automation_Regression/` |
| **Evidence-Based Decision Making & Continual Improvement** | Our release readiness verdict ("not ready for production") is grounded in quantitative pass rates, severity distributions (`3` Critical, `9` Major), code coverage (`94.8%` statements, `89.0%` branches), and unmet exit criteria, paired with actionable process improvements to prevent defect recurrence. | `08_Final_QA_Report/metrics.md`, `lead_sections.md`, `test_design_sections.md` |

### 2. Alignment with CMMI (Process Maturity & Verification/Validation)

In **CMMI** terms, our QA team operated primarily at **Maturity Level 2 (Managed)** with selected **Maturity Level 3 (Defined)** verification practices:
- **Managed Practices (Level 2 — PP, REQM, MA, PPQA):** We established explicit test planning (`test_plan.md`), bidirectional **Requirements Management (REQM)** traceability (`rtm.md` at `100%` requirement coverage), quantitative **Measurement and Analysis (MA)** (`metrics.md`), and objective **Process and Product Quality Assurance (PPQA)** audits (`cross_check_defects.md`) to reconcile inconsistencies across Weeks 1–7.
- **Defined Verification & Validation (Level 3 — VER, VAL):** Applying standardized test-design techniques (EP, BVA, decision tables, state transitions, branch coverage, STRIDE, and Locust load stages) alongside a repeatable `51`-test automated regression suite reflects structured **Verification (VER)** and **Validation (VAL)** processes.
- **Maturity Gap Highlighted by Our Findings:** Because PyTodo Pro was tested after implementation without upfront shared web/API acceptance contracts, defects such as `D-001` (due-today urgency), `D-004` (8-character password mismatch), `D-020` (API SQL injection), and `D-025` (API IDOR delete) were detected late during testing rather than prevented early in requirements and design—reinforcing why higher CMMI maturity integrates QA into early requirements development and peer review.

### References

International Organization for Standardization. (2015). *Quality management systems — Requirements* (ISO Standard No. 9001:2015). https://www.iso.org/standard/62085.html

ISACA. (2018). *CMMI Model V2.0*. CMMI Institute.