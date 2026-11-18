# Week 3: GUI Checklist & Visual Evaluation (`gui_checklist.md`)

**Owner:** Test Design Coordinator (Aida)  
**Target Application:** PyTodo Pro (`http://127.0.0.1:5000/`)  
**Primary Test Environment:** Windows 11, Microsoft Edge (Desktop, Maximized, plus `375px` DevTools mobile emulation for `GUI-16`)  
**Evidence Directory:** `03_Special_Testing/evidence/GUI_testing/`

---

## 1. Evaluation Scope & Categories

This checklist evaluates all 8 pages and shared layout components defined in `03_Special_Testing/README.md` across seven GUI quality dimensions:
1. **Forms** (field alignment, input types, pre-population, HTML5 validation)
2. **Buttons** (sizing, spacing, hover/click affordance, confirmation prompts)
3. **Links** (navigation targets, styling consistency, unauthenticated vs. authenticated states)
4. **Labels** (clarity, `for`/`id` association, instructional hints)
5. **Navigation** (top bar consistency, active page orientation, post-action redirects)
6. **Messages** (error banners, empty-state messaging, destructive action confirmations)
7. **Visual Consistency** (CSS box-sizing, typography, badge color semantics, card grids)

---

## 2. GUI Execution Checklist

| Check ID | Page / Component | Feature ID | Category | Check Description | Expected Result | Actual Result | Status | Browser & Window Size | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| **GUI-01** | Log in (`/login`) | F-03 | Visual Consistency | Verify `.auth-card` container centering, padding, and input box alignment | Card is centered (`360px` max-width) and text inputs align flush with label edges | Card is centered, but inputs slightly overflow the right inner alignment due to invalid `- { box-sizing: border-box; }` selector on line 1 of `style.css` | **Fail** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-01.png` |
| **GUI-02** | Log in (`/login`) | F-03 | Labels | Click the **"Username"** label text to verify input focus behavior | Clicking a label focuses its paired input field | Clicking the label does nothing because `<label>` tags omit `for` attributes and inputs lack `id` attributes | **Fail** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-02.png` |
| **GUI-03** | Log in (`/login`) | F-03 | Messages | Submit invalid credentials and inspect error banner styling | Red `.error` banner (`#fdecea` background, `#b3261e` text) appears cleanly above form | Red error banner renders clearly with readable message `"Invalid username or password."` | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-03.png` |
| **GUI-04** | Log in (`/login`) | F-03 | Links | Verify **"Register"** link below login button navigates to registration page | Clicking `"Register"` loads `/register` with registration form | Navigates cleanly to `/register` | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-04.png` |
| **GUI-05** | Register (`/register`) | F-01 | Labels & Forms | Inspect label hints and submit an 8-character password matching the displayed hint | Hint accurately reflects rules and accepts an 8-character password | Label displays `(min 8 characters)`, but submitting 8 characters fails with `"Password must be at least 8 characters."` (linked to `D-004`) | **Fail** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-05.png` |
| **GUI-06** | Register (`/register`) | F-01 | Links | Verify **"Log in"** link below registration form returns to login page | Clicking `"Log in"` loads `/login` | Navigates cleanly to `/login` | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-06.png` |
| **GUI-07** | Navigation Bar (All Pages) | F-05, F-06 | Navigation | Verify top navbar layout, contrast, and user context when logged in | Dark navy bar (`#1B3A5C`) displays brand on left; `Tasks`, `Dashboard`, current username, and `Log out` on right | All 5 elements render with proper horizontal spacing and hover highlight on links | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-07.png` |
| **GUI-08** | Task List (`/`) | F-09 | Messages | Inspect empty-state table message when a user has 0 tasks and no filters selected | Message states that no tasks exist yet (e.g., `"No tasks yet"`) | Displays misleading `"No tasks match your filters."` even when all filter dropdowns are empty | **Fail** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-08.png` |
| **GUI-09** | Task List (`/`) | F-11 | Forms | Verify filter bar controls (category dropdown, status dropdown, search input, Filter button) | All 4 filter controls align horizontally and display selected values cleanly | Controls align horizontally with `0.6rem` gap and retain selected filter state | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-09.png` |
| **GUI-10** | Task List (`/`) | F-09, F-12, F-14 | Visual Consistency | Verify task table rows, done toggle (`○`/`✓`), urgency badges, and title text rendering | Done tasks show `✓` and strikethrough; badges are color-coded; task titles render as plain text | Toggle, strikethrough, and badge colors work, but `{{ t.title\|safe }}` renders HTML tags (`<b>`) as rich formatting instead of literal text | **Fail** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-10.png` |
| **GUI-11** | Task List (`/`) | F-13 | Buttons & Messages | Click **Delete** on a task row to verify destructive action confirmation | Browser confirmation dialog (`"Delete this task?"`) prompts user before deletion | Native confirmation dialog appears and cancels deletion cleanly when dismissed | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-11.png` |
| **GUI-12** | New Task (`/tasks/new`) | F-08 | Buttons & Forms | Verify form layout and visual alignment between **Create Task** button and **Cancel** link | Primary button and secondary Cancel button share consistent height and vertical alignment | Functional, though `<button>` (`0.6rem` padding, `0.95rem` font) is slightly taller than `<a class="btn-secondary">` (`0.55rem` padding, `0.9rem` font) | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-12.png` |
| **GUI-13** | New Task (`/tasks/new`) | F-08 | Forms & Messages | Submit New Task form with an empty **Title** field | Client-side validation prevents empty submission and highlights Title input | Native HTML5 `required` tooltip blocks submission and focuses Title input | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-13.png` |
| **GUI-14** | Edit Task (`/tasks/<id>/edit`) | F-10 | Forms & Links | Open Edit Task and verify pre-filled values, **Save Changes** button, and **Cancel** link | Existing title, description, category, and due date populate accurately; Cancel returns to `/` | All existing task fields pre-populate accurately and Cancel returns to `/` without saving | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-14.png` |
| **GUI-15** | Dashboard (`/dashboard`) | F-15 | Visual Consistency | Verify 5 summary stat cards layout, typography, and semantic color coding | Cards display in an even grid with distinct colors for Overdue (red), Due Soon (amber), and Completed (green) | All 5 stat cards render in a balanced grid with accurate semantic color coding | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-15.png` |
| **GUI-16** | Dashboard (`/dashboard`) | F-15 | Visual Consistency | Inspect responsive card grid behavior at narrow width (`375px` via Edge DevTools) | Stat cards stack cleanly into a single column without horizontal page overflow | `auto-fit` grid stacks all 5 cards cleanly into 1 column with no horizontal scrollbar | **Pass** | Microsoft Edge DevTools (`375px` mobile emulation) | `evidence/GUI_testing/GUI-16.png` |
| **GUI-17** | Log out (`/logout`) | F-05 | Navigation | Click **Log out** in navbar and verify session termination and UI state | Redirects to `/login` and removes `Tasks`, `Dashboard`, username, and `Log out` links from navbar | Redirects immediately to `/login` and hides authenticated navigation items | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-17.png` |
| **GUI-18** | Navigation Bar (Logged Out) | F-06 | Links | Click **PyTodo Pro** brand link while logged out | Keeps user on `/login` rather than rendering an empty or broken dashboard | Brand link routes cleanly to `/login` | **Pass** | Microsoft Edge (Desktop, Maximized) | `evidence/GUI_testing/GUI-18.png` |

---

## 3. Summary Metrics

| Metric | Count / Percentage |
|---|---|
| Total GUI Checks Executed | 18 |
| Passed | 13 (72.2%) |
| Failed | 5 (27.8%) |
| Not Tested | 0 (0%) |

---

## 4. GUI Improvement Recommendations

1. **Fix CSS Universal Selector Typo (`static/style.css` line 1):** Replace `- { box-sizing: border-box; }` with `* { box-sizing: border-box; }` so `width: 100%` form inputs include their padding and border inside the container width.
2. **Pair All Form Labels with Inputs (`login.html`, `register.html`, `task_form.html`):** Add matching `for` and `id` attributes (e.g., `<label for="title">Title</label>` + `<input id="title" ...>`) so clicking labels focuses inputs and screen readers announce field names.
3. **Remove `|safe` Filter from Task Titles (`templates/index.html` line 39):** Change `{{ t.title|safe }}` to `{{ t.title }}` so Jinja2 auto-escapes special characters (`<`, `>`, `&`), preventing broken markup and XSS rendering issues.
4. **Differentiate Empty Task List vs. Empty Filter Results (`templates/index.html` line 50):** Check whether `category_filter`, `status_filter`, or `q` is active; if none are active, display *"No tasks yet. Click '+ New Task' to add your first task."*
5. **Unify Button & Secondary Link Styling (`static/style.css`):** Apply identical padding (`0.6rem 1.2rem`), font size (`0.95rem`), and `:hover` state transitions across `.btn`, `.btn-secondary`, and form `<button>` elements so side-by-side buttons align symmetrically.
6. **Align Registration Password Hint with Validation (`templates/register.html`):** Either update the hint text to `(min 9 characters)` or fix `is_valid_password()` in `helpers.py` (`>= 8`) so the UI label matches system behavior.

---

## 5. Draft Defect Reports (For Handoff to Defect & Metrics Coordinator)

*(Note: `D-001` through `D-005` are logged in `01_Black_Box/defect_log.md` and `D-006` was drafted in Week 2; the new GUI defects below are numbered starting at `D-007` for logging in `defect_log.md`.)*

### Defect ID: D-007
* **Title:** Invalid CSS selector `-` on line 1 of `style.css` disables `box-sizing: border-box` and causes form inputs to overflow container alignment
* **Affected Feature:** F-01 Register, F-03 Login, F-08 Create Task, F-10 Edit Task (`static/style.css`)
* **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized), Localhost (`http://127.0.0.1:5000/`)
* **Preconditions:** User opens `/login`, `/register`, or `/tasks/new`.
* **Steps to Reproduce:**
  1. Navigate to `http://127.0.0.1:5000/login` or `/tasks/new`.
  2. Inspect the right-hand edge of the text input fields relative to the form labels and card padding.
* **Expected Result:** All text inputs, textareas, and select boxes align flush on both left and right edges within their parent container.
* **Actual Result:** Because line 1 of `static/style.css` contains `- { box-sizing: border-box; }` instead of `* { box-sizing: border-box; }`, inputs with `width: 100%` add horizontal padding and border on top of 100% width and protrude past the right alignment edge.
* **Severity:** Minor
* **Priority:** Low
* **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-01.png`
* **Status:** Open

### Defect ID: D-008
* **Title:** Task list displays misleading `"No tasks match your filters."` message when user has zero tasks and no filters applied
* **Affected Feature:** F-09 Task list (`templates/index.html`)
* **Environment:** Windows 11, Microsoft Edge (Desktop, Maximized), Localhost (`http://127.0.0.1:5000/`)
* **Preconditions:** Logged-in user has 0 tasks in the database and all filter controls (`category`, `status`, `q`) are empty.
* **Steps to Reproduce:**
  1. Log in with an account that has no tasks.
  2. View the home page (`/`) without selecting any category, status, or search term.
* **Expected Result:** The table displays an accurate empty-list prompt (e.g., `"No tasks yet. Click + New Task to create one."`).
* **Actual Result:** The table displays `"No tasks match your filters."`, falsely implying that active filters are hiding existing tasks.
* **Severity:** Minor
* **Priority:** Low
* **Evidence:** `03_Special_Testing/evidence/GUI_testing/GUI-08.png`
* **Status:** Open