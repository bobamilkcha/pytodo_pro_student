# Week 3 Testing Metrics Summary - PyTodo Pro

**Prepared by:** Nafiesa (Defect & Metrics Coordinator)
**Date:** 20 Nov 2026
**Scope:** Special testing of the web pages in `README.md` section 2 (GUI, compatibility, usability and accessibility)

**Contributors:**
- Aida (Test Design Coordinator) - `gui_checklist.md`
- Nisrina (Automation/Tool Coordinator) - `compatibility_matrix.md`
- Nafiesa (Defect & Metrics Coordinator) - `accessibility_findings.md`, `defect_log.md`
- QA/Test Lead - `usability_observations.md`

---

## 1. Week 3 Traceability Matrix

This matrix links each Week 3 activity to its owner, file, results and defects.

| Activity | Owner | File | Checks | Passed | Failed | Not Tested | Pass Rate | Defects Raised | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| GUI testing | Aida | `gui_checklist.md` | 18 | 13 | 5 | 0 | 72.22% | D-007, D-008, D-009, D-010 (+ GUI-05 linked to D-004) | Done |
| Compatibility testing | Nisrina | `compatibility_matrix.md` | 9 (45 results) | 9 (45) | 0 | 0 | 100.00% | None | Done |
| Accessibility testing | Nafiesa | `accessibility_findings.md` | 16 | 8 | 8 | 0 | 50.00% | D-015, D-016, D-017, D-018 (+ ACC-01/08 linked to D-009) | Done |
| Usability testing | QA/Test Lead | `usability_observations.md` | 31 | 6 Good | 25 issues | 0 | 19.35% Good | D-011, D-012, D-013, D-014 (+ US-05 to D-004, US-18 to D-001) | Done |

Note: compatibility has 9 checks run on 5 configurations (Chrome, Edge, Firefox, mobile view, tablet view), which gives 45 results. Usability uses ratings (Good / Minor issue / Major issue), not Pass / Fail, so it is counted separately below.

---

## 2. Test Execution Metrics (Week 3)

### 2.1 Pass / Fail checks (GUI, compatibility, accessibility)

| Metric Category | Count | Percentage |
| :--- | :---: | :---: |
| **Checks Planned** | 43 | 100% |
| **Checks Executed** | 43 | 100.00% |
| **Passed Checks** | 30 | 69.77% |
| **Failed Checks** | 13 | 30.23% |
| **Not Tested** | 0 | 0.00% |

- **Execution Rate:** **100%** (43 / 43)
- **Overall Pass Rate:** **69.77%** (30 / 43)
- **Overall Failure Rate:** **30.23%** (13 / 43)

### 2.2 Usability observations

| Rating | Count | Percentage |
| :--- | :---: | :---: |
| Good | 6 | 19.35% |
| Minor issue | 21 | 67.74% |
| Major issue | 4 | 12.90% |
| **Total** | **31** | 100% |

### 2.3 Breakdown by Activity
- **GUI (Aida):** 18 Executed | 13 Passed | 5 Failed (GUI-01, GUI-02, GUI-05, GUI-08, GUI-10)
- **Compatibility (Nisrina):** 9 Executed on 5 configurations | 45 / 45 results Passed | 0 Failed
- **Accessibility (Nafiesa):** 16 Executed | 8 Passed | 8 Failed (ACC-01, 02, 03, 08, 09, 10, 11, 15)
- **Usability (QA/Test Lead):** 31 Observed | 6 Good | 21 Minor | 4 Major

---

## 3. Quality Scores

### 3.1 Lighthouse accessibility scores

| Page | Score (out of 100) | Main failed audits |
| :--- | :---: | :--- |
| Log in | 85 | Form labels |
| Register | 85 | Form labels |
| Task list | 72 | Labels, select names, contrast, target size, table headers |
| New task | 74 | Form labels, select name |
| Dashboard | 95 | No `<main>` landmark |
| **Average** | **82.2** | |

### 3.2 Accessibility results by WCAG principle

| Principle | Checks | Passed | Failed |
| :--- | :---: | :---: | :---: |
| Perceivable | 7 | 2 | 5 |
| Operable | 5 | 4 | 1 |
| Understandable | 2 | 2 | 0 |
| Robust | 1 | 0 | 1 |
| Automated audit | 1 | 0 | 1 |

### 3.3 Compatibility results by configuration

| Configuration | Version | Results | Passed |
| :--- | :--- | :---: | :---: |
| Google Chrome (Desktop) | 157.0.8103.79 | 9 | 9 |
| Microsoft Edge (Desktop) | 157.0.4341.60 | 9 | 9 |
| Mozilla Firefox (Desktop) | 127.0 | 9 | 9 |
| Mobile view (Galaxy A55, DevTools) | 157.0.8103.79 | 9 | 9 |
| Tablet view (iPad Pro 13, DevTools) | 157.0.8103.79 | 9 | 9 |

---

## 4. Defect Metrics

### 4.1 Defects raised in Week 3

| Defect ID | Title (short) | Found by | Severity | Priority | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **D-007** | Invalid CSS selector makes inputs overflow | GUI-01 | Minor | Low | Open |
| **D-008** | Wrong empty-list message for new users | GUI-08, US-22 | Minor | Low | Open |
| **D-009** | Form fields and filters have no label | GUI-02, ACC-01, ACC-08 | Moderate | Medium | Open |
| **D-010** | Task title rendered as HTML (`\|safe`) | GUI-10 | Major | High | Open |
| **D-011** | Title with only spaces accepted | US-11 | Major | Medium | Open |
| **D-012** | No title length limit | US-11 | Moderate | Low | Open |
| **D-013** | Duplicate usernames can be registered | US-04 (retested) | Major | High | Confirmed |
| **D-014** | `_` acts as a wildcard in search | US-24 | Minor | Low | Open |
| **D-015** | Grey text fails 4.5:1 contrast | ACC-03 | Moderate | Medium | Open |
| **D-016** | Done toggle has no meaningful name | ACC-02, US-16 | Moderate | Medium | Open |
| **D-017** | Pages do not reflow at 320 px | ACC-09 | Moderate | Medium | Open |
| **D-018** | Edit / Delete targets smaller than 24 px | ACC-11 | Minor | Low | Open |

**Issues linked to earlier defects (not given new IDs):** GUI-05 and US-05 → **D-004** (8-character password rejected). US-18 and US-25 → **D-001** (due today shown as Overdue).

### 4.2 Week 3 Defect Distribution

| Metric | Count |
| :--- | :---: |
| **New defects found in Week 3** | 12 (D-007 to D-018) |
| **Major** | 3 (D-010, D-011, D-013) |
| **Moderate** | 5 (D-009, D-012, D-015, D-016, D-017) |
| **Minor** | 4 (D-007, D-008, D-014, D-018) |
| **Critical** | 0 |
| **Issues matched to existing defects** | 3 (GUI-05, US-05, US-18) |

- **By activity (first found):** GUI: 4 | Usability: 4 | Accessibility: 4 | Compatibility: 0
- **Defects found by more than one activity:** D-008 (GUI + Usability), D-009 (GUI + Accessibility), D-016 (Accessibility + Usability). Different techniques confirmed the same problems, which makes these findings stronger.

### 4.3 Cumulative Defect Status (Week 1 to Week 3)

| Metric | Count |
| :--- | :---: |
| **Total defect IDs logged** | 18 (D-001 to D-018) |
| **Unique defects** | 16 |
| **Closed as duplicate** | 2 (D-002, D-003) |
| **Open (incl. Confirmed)** | 16 |
| **Resolved** | 0 |

| Week | Technique | New defects |
| :--- | :--- | :---: |
| Week 1 | Black-box | 3 |
| Week 2 | White-box | 1 |
| Week 3 | Special testing | 12 |
| **Total** | | **16** |

| Severity | Count | Percentage |
| :--- | :---: | :---: |
| Critical | 0 | 0.00% |
| Major | 5 | 31.25% |
| Moderate | 7 | 43.75% |
| Minor | 4 | 25.00% |

---

## 5. Cross-File Consistency Notes

1. **Mobile view: compatibility Pass vs accessibility Fail (D-017).** These two results test different things, so both are kept:
   - `compatibility_matrix.md` used Chrome DevTools device presets (Galaxy A55, iPad Pro 13). Because the pages have **no `<meta name="viewport">` tag**, the browser shrinks the whole desktop layout to fit the phone screen. Nothing overflows, so the check passed, but the text becomes very small (see `COMP-09_mobile.png`).
   - `accessibility_findings.md` (ACC-09) set the page width itself to 320 px, as WCAG 1.4.10 Reflow requires. There the page is 510 px wide and scrolls sideways.
   - Both point to the same root cause: no viewport tag and no `@media` rules. Fixing D-017 should fix both.
2. **Week 1 result to correct.** `TC-BB-002` ("Registration fails when username already exists") is marked Pass, but D-013 shows duplicate usernames are accepted. Owner: Aida, to re-run and update.
3. **Defect IDs in `usability_observations.md`.** Section 4 still shows `DEF-TBC` for US-04, US-05, US-11, US-18 and US-24. The IDs are now D-013, D-004, D-011 and D-012, D-001 and D-014.
4. **Test environments differ by file.** GUI used Edge on Windows 11. Usability used Chrome on Windows. Compatibility used Chrome, Edge and Firefox on Windows 11. Accessibility used Chrome 153 (headless, Linux). Each file states its own environment, as required by `test_conventions.md`.

---

## 6. Outstanding Actions

| Owner | Action |
| :--- | :--- |
| Aida | Re-run `TC-BB-002` and change it to Fail (see D-013). |
| QA/Test Lead | Replace `DEF-TBC` in `usability_observations.md` with the defect IDs in section 5. |
| QA/Test Lead | Run the 20 State Transition cases (TC-BB-060 to TC-BB-079) and push `toggle_task` white-box tests (carried over from Weeks 1 and 2). |
| QA/Test Lead | Write the Week 3 README summary. |
| All | Week 4: retest D-004, D-011 and D-013 through the API, as planned in `usability_observations.md` section 6. |

---

## 7. Week 3 Summary & Conclusion

- **Progress:** All four Week 3 activities are complete. 43 pass/fail checks and 31 usability observations were executed, with no checks left untested.
- **Quality status:**
  1. **Compatibility is strong.** All 45 results passed across three desktop browsers and two simulated devices.
  2. **Accessibility is the weakest area.** Only 8 of 16 checks passed, and the average Lighthouse score is 82.2. The app works well with a keyboard, but screen reader users cannot identify form fields or the done button.
  3. **Usability is mostly fine but rough.** Only 4 of 31 observations are major. Most issues are missing success messages and inconsistent wording.
- **Key findings:**
  1. **Week 3 found the most defects so far (12 of 16).** Special testing found problems in areas that functional testing does not look at: layout, labels, contrast and wording.
  2. **Server-side checks are weak.** D-011, D-012 and D-013 show that the server trusts input that only the browser checks. This is a clear focus for Week 4 (client-server validation).
  3. **One defect affects security.** D-010 (`|safe`) is a display defect now but a stored XSS risk for Week 5.
- **Risk for next week:** 5 Major defects are open and none are fixed. Week 4 API testing is likely to find more server-side validation defects in the same areas (register, task title, due date).
