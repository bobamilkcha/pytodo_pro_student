# Week 3: Browser & Responsive Compatibility Matrix

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Test Account Used:** `<your_test_username>`  
**Sample Data:** `<e.g., 5 tasks across Work/Personal, 1 overdue, 1 due soon, 1 completed>`

---

## 1. Test Environments & Browser Versions

| Configuration | Browser / Tool | Exact Version | OS | Window / Viewport Size |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop 1** | Google Chrome | `157.0.8103.79` | Windows 11 | Full screen (`1920x1080`) |
| **Desktop 2** | Microsoft Edge | `157.0.4341.60` | Windows 11 | Full screen (`1920x1080`) |
| **Desktop 3** | Mozilla Firefox | `127.0` | Windows 11 | Full screen (`1920x1080`) |
| **Mobile (Small)** | Chrome DevTools (Device Mode) | `157.0.8103.79` | Windows 11 | `375x667` (Simulated) |
| **Mobile (Tablet)** | Chrome DevTools (Device Mode) | `157.0.8103.79` | Windows 11 | `768x1024` (Simulated) |

---

## 2. Compatibility Test Matrix

*Legend: **Pass** = Renders and functions as expected | **Fail** = Visual breakage, overflow, or broken control | **Not tested** = Not executed*

| Check ID | Page / Component | Route | Chrome (Desktop) | Edge (Desktop) | Firefox (Desktop) | Mobile (`375px`) | Tablet (`768px`) | Evidence Screenshot(s) | Notes on Differences / Issues |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **COMP-01** | Register | `/register` | | | | | | `COMP-01.png` | Check form alignment, hints, and error box |
| **COMP-02** | Log in | `/login` | | | | | | `COMP-02.png` | Check input alignment and button width |
| **COMP-03** | Log out | `/logout` | | | | | | `COMP-03.png` | Verify redirect to `/login` works identically |
| **COMP-04** | Navigation Bar | All logged-in | | | | | | `COMP-04.png` | Watch for link wrapping or overflow at `375px` |
| **COMP-05** | Task List (Layout & Filters) | `/` | | | | | | `COMP-05.png` | Check filter dropdowns, search bar, and table horizontal scroll |
| **COMP-06** | Task List (Controls & Popup) | `/` | | | | | | `COMP-06.png` | Check done toggle (`○`/`✓`), urgency badges, and native Delete confirm popup across browsers |
| **COMP-07** | New Task (Form & Date Picker) | `/tasks/new` | | | | | | `COMP-07a.png`, `COMP-07b.png` | Compare `<input type="date">` rendering in Chrome/Edge vs. Firefox |
| **COMP-08** | Edit Task | `/tasks/<id>/edit` | | | | | | `COMP-08.png` | Verify pre-filled values and date picker formatting |
| **COMP-09** | Dashboard (Stat Cards) | `/dashboard` | | | | | | `COMP-09.png` | Check how the 5 stat cards wrap/stack at `768px` and `375px` |

---

## 3. Summary of Cross-Browser & Responsive Findings

* **Desktop Browsers (Chrome vs. Edge vs. Firefox):**
  * *(Note any differences in date picker UI, font rendering, or the native `confirm()` delete dialog.)*
* **Mobile / Responsive View (`375px` and `768px`):**
  * *(Note horizontal scrolling, squished tables, nav bar overflow, or unstyled stacking due to missing `@media` rules in `static/style.css`.)*

---

## 4. Compatibility Defects Identified (For Defect Coordinator)

| Defect Ref | Check ID | Browser / Viewport | Severity | Summary & Suggested Fix |
| :--- | :--- | :--- | :---: | :--- |
| *Pending ID* | `COMP-05` | Chrome DevTools (`375px`) | Medium | *(Example: Task table overflows horizontally; suggest adding `@media` queries and `overflow-x: auto` wrapper.)* |