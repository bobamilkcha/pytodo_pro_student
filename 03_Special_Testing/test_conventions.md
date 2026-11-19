# Test Conventions - PyTodo Pro

**Maintained by:** Defect & Metrics Coordinator (Nafiesa)
**Applies to:** All weeks (`01_Black_Box` onward)

This file sets the shared rules for IDs, results, evidence and defect reports, so every folder uses the same format. It follows the templates in the group project brief.

---

## 1. ID formats

| Item | Format | Example |
| :--- | :--- | :--- |
| Black-box test case | `TC-BB-<feature>-<nn>` | `TC-BB-F14-02` |
| White-box test case | `TC-WB-<feature>-<nn>` | `TC-WB-F14-04` |
| GUI check | `GUI-<nn>` | `GUI-08` |
| Compatibility check | `COMP-<nn>` | `COMP-03` |
| Accessibility check | `ACC-<nn>` | `ACC-02` |
| Usability observation | `US-<nn>` | `US-11` |
| Defect | `D-<nnn>`, numbered in order, never reused | `D-012` |
| Recommendation | `R-<nn>` inside each file | `R-03` |

- Defect IDs are given out **only** by the Defect & Metrics Coordinator, so two people never use the same number. Use `DEF-TBC` in your own file until you get an ID.
- If a new issue is the same bug as an old defect, do not give it a new ID. Link it to the old one (e.g. "same as D-001").

## 2. Results and status

**Test result** (every test case or check): `Pass` / `Fail` / `Blocked` / `Not Run` (Week 3 files may use `Not tested`).

**Defect status:** `Open` → `Confirmed` → `Retest` → `Closed`. A duplicate is closed as `Closed (Duplicate of D-xxx)`.

## 3. Severity and priority

**Severity** (how bad the impact is):

| Severity | Meaning | Example |
| :--- | :--- | :--- |
| Critical | App crashes, data is lost, or a security hole lets users reach other users' data | Server error stops every user from logging in |
| Major | A main feature gives a wrong result or accepts invalid data, with no workaround | Duplicate usernames can be registered |
| Moderate | A feature is wrong but a workaround exists, or a group of users is blocked from part of the app | Due-today task shown as Overdue |
| Minor | Cosmetic or wording problem, no effect on results | Inputs overflow the card by a few pixels |

**Priority** (how soon to fix): `High` / `Medium` / `Low`.

Do not use "High" as a severity. Severity and priority are separate. A minor bug can still be high priority if many users see it.

## 4. Evidence

- Save screenshots in your week's `evidence/` folder.
- Name each file by its check or test ID: `GUI-01.png`, `ACC-03a.png`, `TC-BB-F14-02_Actual.png`. Add a letter if one check needs more than one image.
- Every result must state the **browser, version and window size**.

## 5. Defect report template

Send each new defect to the Defect & Metrics Coordinator in this format. It is logged in `01_Black_Box/defect_log.md`.

```markdown
### Defect ID: DEF-TBC
- **Title:** Short, specific summary of the problem
- **Affected Feature:** F-xx Feature name (file or route)
- **Environment:** OS, browser and version, window size, http://127.0.0.1:5000
- **Preconditions:** State needed before the steps
- **Steps to Reproduce:**
  1. ...
  2. ...
- **Expected Result:** What should happen
- **Actual Result:** What actually happened
- **Severity:** Critical / Major / Moderate / Minor
- **Priority:** High / Medium / Low
- **Status:** Open
- **Evidence:** path to screenshot or log
- **Related Test Case:** test case or check ID
- **Suggested Fix (optional):** idea only, we do not change the app code
```
