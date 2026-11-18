# Usability Observations

**Owner:** QA/Test Lead
**Pages covered:** `/register`, `/login`, `/`, `/tasks/new`, `/tasks/<id>/edit`, `/dashboard`

## 1. Introduction

Usability testing checks how easy the app is to use for a normal person. We look at whether people can find things, whether the app tells them what happened, and whether the wording makes sense. We did this with one tester (the QA/Test Lead). The tester walks through the main tasks in section 2 by hand, like a new user, and writes down what happened. This is one person's view, so some ratings are opinion and not fact.

The "Code-based note" column comes from reading `templates/`, `app.py` and `static/style.css` before using the app. Each note is only a guess until we see it in the browser. The Observation, Rating, Evidence and Recommendation columns are filled in after the walkthrough.

## 2. Tasks we walk through

| Task | Steps | Feature ID |
|---|---|---|
| T1 Register | Open `/register`, fill the form, submit | F-01 |
| T2 Log in | Open `/login`, fill the form, submit | F-03 |
| T3 Create a task | Click "+ New Task", fill the form, submit | F-08 |
| T4 Edit a task | Click "Edit" on a task, change something, save | F-10 |
| T5 Mark a task done | Click the circle button on a task, then click it again to reopen | F-12 |
| T6 Delete a task | Click "Delete" on a task, answer the popup | F-13 |
| T7 Find a task | Use the category dropdown, status dropdown and search box | F-11 |
| T8 Read the dashboard | Open "Dashboard" from the nav bar | F-15 |
| T9 Log out | Click "Log out" | F-05 |

The API is not part of this sheet because it has no pages.

## 3. Rating scale and criteria

- **Good:** no problem.
- **Minor issue:** we can still finish the task, but it is confusing or annoying.
- **Major issue:** we get stuck, make a mistake, or cannot tell what happened.

Criteria: **Navigation** (ease of navigation), **Feedback**, **Consistency**, **Error prevention**, **Understandability**.

Evidence screenshots go in `evidence/` and are named by ID, for example `US-01.png`.

## 4. Observation table

| ID | Task | Criterion | What we checked | Code-based note | Observation | Rating | Evidence | Recommendation |
|---|---|---|---|---|---|---|---|---|
| US-01 | T1 Register | Navigation | Can we find the register page from the first page we see? | The nav bar is empty when logged out, so the only way to Register is the small link under the login form. Opening `/` redirects to `/login`. (to verify in UI) | | | | |
| US-02 | T1 Register | Understandability | Do the hints under "Username" and "Password" explain the rules? | The hint says "min 8 characters", but the code needs more than 8. A password of exactly 8 is rejected. (to verify in UI) | | | | |
| US-03 | T1 Register | Feedback | What do we see after a bad username, a short password and a good registration? | Error text appears in a red box above the form. On success there is no message, we are just sent to the task list. (to verify in UI) | | | | |
| US-04 | T1 Register | Error prevention | What happens if we use a username that already exists? | The code does not check for duplicates, so we might get a second account with no warning. (to verify in UI) | | | | |
| US-05 | T1 Register | Understandability | Is the error message clear when the password is exactly 8 characters? | The message says "at least 8 characters", but 8 fails. This could confuse the user. (to verify in UI) | | | | |
| US-06 | T2 Log in | Feedback | What do we see for a wrong username and for a wrong password? | Both cases show "Invalid username or password." Good for security, but we do not know if it helps the user. (to verify in UI) | | | | |
| US-07 | T2 Log in | Consistency | Do the login and register pages look and behave the same way? | Both use the same card, same fields and the same error box. Button text is "Log in" on one page and "Register" on the other. The page title is "Log in" but the heading is "Create an account" for register. (to verify in UI) | | | | |
| US-08 | T2 Log in | Error prevention | Are the password characters hidden? Does the form stop us sending empty fields? | The password input has `type="password"` and both inputs are `required`. The browser shows its own message for empty fields. (to verify in UI) | | | | |
| US-09 | T3 Create a task | Navigation | Is "+ New Task" easy to find? Can we get back without saving? | The button is at the top right of the task list. The form has a "Cancel" link. (to verify in UI) | | | | |
| US-10 | T3 Create a task | Feedback | What tells us the task was saved? | No success message in the code. We go back to the list and the new task is at the top. (to verify in UI) | | | | |
| US-11 | T3 Create a task | Error prevention | What happens with an empty title, a title with only spaces, a very long title, or an odd date? | Only the browser `required` check is used. The server does not check the title. A title with only spaces may be saved. (to verify in UI) | | | | |
| US-12 | T3 Create a task | Understandability | Are the form labels clear? Is it clear what is optional? | Labels are Title, Description, Category, Due Date. Nothing says which fields are optional. (to verify in UI) | | | | |
| US-13 | T4 Edit a task | Consistency | Does the edit form look like the new task form? Do the button names make sense? | Same template for both. Buttons are "Create Task" and "Save Changes". The edit page does not have a done checkbox. (to verify in UI) | | | | |
| US-14 | T4 Edit a task | Feedback | What do we see after saving? What if we open an edit link for a task that does not exist? | After saving we go back to the list with no message. A wrong or missing task id silently goes back to `/` with no error. (to verify in UI) | | | | |
| US-15 | T4 Edit a task | Navigation | Is the "Edit" link easy to spot on each row? | "Edit" is a small blue text link in the last column. (to verify in UI) | | | | |
| US-16 | T5 Mark done | Understandability | Is it clear what the circle button does? | The button only shows ○ or ✓ and has no text or tooltip. (to verify in UI) | | | | |
| US-17 | T5 Mark done | Feedback | What changes on the row when a task is done? Can we tell how to undo it? | The code adds a line-through on the title and a grey colour. The button changes to ✓ and the badge says "Done". The page reloads after each click. (to verify in UI) | | | | |
| US-18 | T5 Mark done | Consistency | Do the urgency badge names match what we expect? Does "Due Today" ever show? | Per the feature inventory, tasks due today show "Overdue" and "Due Today" never appears. This could be confusing. (to verify in UI) | | | | |
| US-19 | T6 Delete | Error prevention | Do we get a warning before a task is deleted? Can we cancel? | A browser popup asks "Delete this task?". The popup does not show the task name. No undo after deleting. (to verify in UI) | | | | |
| US-20 | T6 Delete | Consistency | Does "Delete" look like "Edit"? Could we click it by mistake? | Both are small blue text, side by side. "Delete" is not red. (to verify in UI) | | | | |
| US-21 | T6 Delete | Feedback | What do we see after a delete? | No message. The row just disappears after the page reloads. (to verify in UI) | | | | |
| US-22 | T7 Find a task | Feedback | What happens when we change a dropdown? When nothing matches? | The dropdowns reload the page on change by JavaScript. The search box needs the "Filter" button. The empty message is "No tasks match your filters." (to verify in UI) | | | | |
| US-23 | T7 Find a task | Consistency | Do the dropdowns and the search box behave in the same way? | The dropdowns submit by themselves but the search box does not. There is no "clear filters" button. (to verify in UI) | | | | |
| US-24 | T7 Find a task | Understandability | Does the search placeholder tell us what is searched? Does `%` or `_` in the search behave oddly? | The placeholder is "Search title...". Search is title only. `%` and `_` act as wildcards. (to verify in UI) | | | | |
| US-25 | T8 Dashboard | Understandability | Can we understand each counter without help? | Labels are Total Tasks, Open, Overdue, Due Soon, Completed (last 7 days). Nothing explains how they are counted. Tasks due today count as Overdue. (to verify in UI) | | | | |
| US-26 | T8 Dashboard | Navigation | Can we jump from a counter to the matching tasks? | The stat cards are not links. (to verify in UI) | | | | |
| US-27 | T9 Log out | Navigation | Is "Log out" easy to find on every page? | It is in the nav bar on all logged-in pages, next to the username. (to verify in UI) | | | | |
| US-28 | T9 Log out | Feedback | What do we see after logging out? | We land on the login page with no "logged out" message. (to verify in UI) | | | | |
| US-29 | T9 Log out | Error prevention | Is logging out by clicking a link risky? What if we press the browser Back button afterwards? | Logout is a plain GET link, so a mistaken click logs us out without asking. Pages should redirect to login after logout. (to verify in UI) | | | | |
| US-30 | All pages | Consistency | Do the pages look like one app (colours, fonts, spacing, button style)? | All pages share `base.html` and `style.css`. Buttons are blue, but "Filter" uses a different blue. (to verify in UI) | | | | |
| US-31 | All pages | Navigation | Does the "PyTodo Pro" brand link take us home? Do the nav links show where we are? | The brand goes to `/` when logged in and to `/login` when not. The nav links have no "current page" style. (to verify in UI) | | | | |

## Week 3 notes for this file

Anything that looks like a real defect (not only a usability opinion) goes to the Defect & Metrics Coordinator using the template in `test_conventions.md`.
