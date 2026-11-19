# Week 3: Browser & Responsive Compatibility Matrix

**Prepared by:** Automation/Tool Coordinator (Nisrina)  
**Test Account Used:** `compat_user`  
**Sample Data:** 8 tasks across Personal (3), Study (2), Work (1), Urgent (1), and Uncategorized (1) — comprising 4 Overdue, 2 Upcoming, and 2 Done tasks.

---

## 1. Test Environments & Browser Versions

| Configuration | Browser / Tool | Exact Version | OS | Window / Viewport Size |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop 1** | Google Chrome | `157.0.8103.79` | Windows 11 | Full screen (`1920x1080`) |
| **Desktop 2** | Microsoft Edge | `157.0.4341.60` | Windows 11 | Full screen (`1920x1080`) |
| **Desktop 3** | Mozilla Firefox | `127.0` | Windows 11 | Full screen (`1920x1080`) |
| **Mobile** | Chrome DevTools (Device Mode) | `157.0.8103.79` | Windows 11 | Samsung Galaxy A55 (Simulated) |
| **Tablet** | Chrome DevTools (Device Mode) | `157.0.8103.79` | Windows 11 | iPad Pro 13 (Simulated) |

---

## 2. Compatibility Test Matrix

*Legend: **Pass** = Renders and functions as expected | **Fail** = Visual breakage, overflow, or broken control | **Not tested** = Not executed*

| Check ID | Page / Component | Route | Chrome (Desktop) | Edge (Desktop) | Firefox (Desktop) | Mobile (Galaxy A55) | Tablet (iPad Pro 13) | Evidence Screenshot(s) | Notes on Differences / Issues |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **COMP-01** | Register | `/register` | Pass | Pass | Pass | Pass | Pass | `COMP-01_register.png`, `COMP-01_register_red_error_box_username.png`, `COMP-01_register_red_error_box_password.png` | Form inputs, helper hints, and error boxes render cleanly across all browsers and viewports. |
| **COMP-02** | Log in | `/login` | Pass | Pass | Pass | Pass | Pass | `COMP-02_login.png`, `COMP-02_login_invalid_red_error_box_.png` | Input alignment, button width, and error banner are consistent across all setups. |
| **COMP-03** | Log out | `/logout` | Pass | Pass | Pass | Pass | Pass | `COMP-03_logout.png`, `COMP-03_after_logout.png` | Cleanly clears session and redirects to `/login` in all browsers. |
| **COMP-04** | Navigation Bar | All logged-in | Pass | Pass | Pass | Pass | Pass | `COMP-04_navigation_bar.png`, `COMP-04_mobile_web_navigation_bar.png` | Brand, navigation links, username, and Log out link remain visible and accessible. |
| **COMP-05** | Task List (Layout & Filters) | `/` | Pass | Pass | Pass | Pass | Pass | `COMP-05.png` | Filter dropdowns, search bar, task table, and empty-filter state display properly across all tested viewports. |
| **COMP-06** | Task List (Controls & Popup) | `/` | Pass | Pass | Pass | Pass | Pass | `COMP-06.png` | Done toggle (`○`/`✓`) and urgency badges render cleanly; native `confirm()` popup styling varies slightly by browser (expected) and functions properly. |
| **COMP-07** | New Task (Form & Date Picker) | `/tasks/new` | Pass | Pass | Pass | Pass | Pass | `COMP-07_chrome_edge_calendar.png`, `COMP-07_firefox_calendar.png` | Native `<input type="date">` calendar UI differs between Chromium (Chrome/Edge) and Firefox (expected); date selection works in all browsers. |
| **COMP-08** | Edit Task | `/tasks/<id>/edit` | Pass | Pass | Pass | Pass | Pass | `COMP-08_edit_task.png` | Title, description, category, and due date pre-fill accurately across all browsers and viewports. |
| **COMP-09** | Dashboard (Stat Cards) | `/dashboard` | Pass | Pass | Pass | Pass | Pass | `COMP-09_web.png`, `COMP-09_mobile.png` | All 5 stat cards display identical counts and remain readable across desktop, tablet, and mobile views. |

---

## 3. Summary of Cross-Browser & Responsive Findings

* **Desktop Browsers (Chrome `157.0.8103.79` vs. Edge `157.0.4341.60` vs. Firefox `127.0`):**
  * All 7 pages and the shared navigation bar rendered and functioned consistently across all three desktop browsers.
  * Expected native browser UI differences were observed in the `<input type="date">` picker (`COMP-07`) and the JavaScript `confirm()` delete dialog (`COMP-06`) between Chromium-based browsers (Chrome/Edge) and Firefox, with no functional issues.
* **Mobile & Tablet View (Chrome DevTools Device Mode):**
  * Despite `static/style.css` having no `@media` queries, all pages remained usable and passed functional and visual checks on the simulated mobile and tablet device presets.

---

## 4. Compatibility Defects Identified (For Defect Coordinator)

*No compatibility defects were identified during Week 3 testing across the tested desktop browsers and simulated mobile/tablet viewports.*