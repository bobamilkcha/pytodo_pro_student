# Week 3: GUI, Compatibility, Usability and Accessibility Testing

**Prepared by:** QA Test Lead

## 1. Introduction

In Week 3 we stop looking at logic and look at how the app appears and feels in a browser. We check the layout and controls (GUI), how the pages behave in different browsers and screen sizes (compatibility), how easy the app is to use (usability), and whether people using a keyboard or a screen reader can use it (accessibility). We still do not change any app code. We only report what we find.

## 2. Pages in scope

All pages use `templates/base.html` (top navigation bar) and `static/style.css`. Feature IDs come from `01_Black_Box/feature_inventory.md`.

| Page | Route | Template file | Main UI elements | Related Feature ID |
|---|---|---|---|---|
| Register | `/register` | `register.html` | Form with username and password fields, "Register" button, "Log in" link, error message, hints under the labels | F-01 |
| Log in | `/login` | `login.html` | Form with username and password fields, "Log in" button, "Register" link, error message | F-03 |
| Log out | `/logout` | none (redirect to `/login`) | "Log out" link in the nav bar | F-05 |
| Task list | `/` | `index.html` | "+ New Task" button, category dropdown, status dropdown, search box, "Filter" button, task table, done toggle button, urgency badge, "Edit" link, "Delete" button with confirm popup, "No tasks match your filters." message | F-09, F-11, F-12, F-13, F-14 |
| New task | `/tasks/new` | `task_form.html` | Title box, description box, category dropdown, date picker, "Create Task" button, "Cancel" link | F-08 |
| Edit task | `/tasks/<id>/edit` | `task_form.html` | Same form, pre-filled, "Save Changes" button, "Cancel" link | F-10 |
| Dashboard | `/dashboard` | `dashboard.html` | Five stat cards: Total Tasks, Open, Overdue, Due Soon, Completed (last 7 days) | F-15 |
| Navigation bar (all logged-in pages) | all | `base.html` | Brand link, "Tasks" link, "Dashboard" link, username text, "Log out" link | F-05, F-06 |

Not in scope: the JSON API routes (`/api/...`). They have no pages. `static/style.css` is checked only through how the pages look.

Things we noticed while reading the files (to verify in the browser, not confirmed yet):
- `style.css` has no `@media` rules, so the mobile-width view may look bad.
- The form labels in the templates have no `for` attribute, so they may not be linked to their inputs.
- The done toggle button only shows a symbol (○ or ✓) and has no text label.
- `index.html` prints the task title with the `safe` filter (this is the XSS risk from the feature inventory). We only look at it as a display problem here. The security side was Week 2.

## 3. Browsers and configurations

Same test accounts and same sample data in every browser, so the results can be compared. Please write the exact browser version in `compatibility_matrix.md`.

| Configuration | How we test it | Tester |
|---|---|---|
| Google Chrome (desktop) | Normal window, full size | |
| Microsoft Edge (desktop) | Normal window, full size | |
| Mozilla Firefox (desktop) | Normal window, full size | |
| Mobile-width view | Chrome DevTools device mode (F12, then the device toggle). We start at 375 px wide and also try 768 px. This is only a simulation, not a real phone. | |

Tester options: QA/Test Lead, Test Design Coordinator, Automation/Tool Coordinator, Defect & Metrics Coordinator. We fill this column in at our first meeting.

## 4. Who does what this week

| File | Owner | What goes in it |
|---|---|---|
| `gui_checklist.md` | Test Design Coordinator | Checks for layout, labels, buttons, links, messages and form behaviour on each page in section 2. Each check has an ID like GUI-01. |
| `compatibility_matrix.md` | Automation/Tool Coordinator | Pages against browsers from section 3, with pass or fail and notes on differences. |
| `accessibility_findings.md` | Defect & Metrics Coordinator | Keyboard use, labels, colour contrast, headings, and anything a screen reader would miss. Each finding has an ID like ACC-01. |
| `usability_observations.md` | QA/Test Lead | Notes from using the app like a new user: confusing wording, extra steps, missing feedback. |

Each person also writes up their own defects (see section 5).

## 5. Shared format rules

- Evidence screenshots go in an `evidence/` folder inside `03_Special_Testing/`.
- Name each screenshot by its check ID, for example `GUI-01.png`, `COMP-03.png`, `ACC-02.png`, `USA-01.png`. If one check needs more than one image, add a letter: `GUI-01a.png`, `GUI-01b.png`.
- Every check in every file has an ID, a page, a result (Pass / Fail / Not tested) and the screenshot name.
- Defects are sent to the Defect & Metrics Coordinator using the template in `test_conventions.md`. Use the same defect wording and severity scale as Weeks 1 and 2.
- Note the browser and window size for every result.
- Do not edit the app code. If a fix seems obvious, write it in the defect report as a suggestion.

Note: we could not find `test_conventions.md` in the repository when we wrote this. We need to add it or confirm where it is before anyone files a defect.

## Week 3 summary
