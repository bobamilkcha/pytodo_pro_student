    # Usability Observations

**Owner:** QA/Test Lead
**Pages covered:** `/register`, `/login`, `/`, `/tasks/new`, `/tasks/<id>/edit`, `/dashboard`
**Test accounts:** `syasya_test1`, `syasya_test2`
**Browser:** Chrome on Windows

## 1. Introduction

Usability testing checks how easy the app is to use for a normal person. We look at whether people can find things, whether the app tells them what happened, and whether the wording makes sense. We did this with one tester (the QA/Test Lead). The tester walked through the main tasks in section 2 by hand, like a new user, and wrote down what happened. This is one person's view, so some ratings are opinion and not fact.

Before the walkthrough, we read `templates/`, `app.py` and `static/style.css` and wrote down what we expected to see. During the walkthrough we checked each of these notes in the browser. The table below only shows what we actually observed.

## 2. Tasks we walked through

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

Evidence screenshots are in `evidence/` and are named by ID, for example `US-01.png`.

## 4. Observation table

| ID | Task | Criterion | What we checked | Observation | Rating | Evidence | Recommendation | Linked Defect |
|---|---|---|---|---|---|---|---|---|
| US-01 | T1 Register | Navigation | Can we find the register page from the first page we see? | Opening the app goes straight to the login page. The nav bar only shows "PyTodo Pro" with no Register or Log in links. The only way to register is the small "Register" link under the form ("No account? Register"). It is easy to find once you look at the form, but a new user has to read the whole card to see it. | Minor issue | US-01.png | Add "Log in" and "Register" links to the nav bar when logged out, or make the Register link a second button so it stands out. | - |
| US-02 | T1 Register | Understandability | Do the hints under "Username" and "Password" explain the rules? | Both fields have grey hints next to the label. Username says "3-20 chars, letters/numbers/underscore" and Password says "min 8 characters". The username hint is clear and specific. The password hint is misleading because a password of exactly 8 characters is rejected (see US-05). The hints are also light grey and small, so they are easy to miss. | Minor issue | US-02.png | Make the hints a little darker, and fix the password rule so it matches the hint. | See US-05 |
| US-03 | T1 Register | Feedback | What do we see after a bad username, a short password and a good registration? | Errors show in a pink box above the form with clear text, for example "Username must be 3-20 characters (letters, numbers, underscore)." The messages match the hints. However, both fields are cleared after an error, so the user has to retype the username even when only the password was wrong. A valid registration goes straight to the task list with no success message. | Minor issue | US-03a.png, US-03b.png | Keep the username filled in after an error, and show a short "Account created" message after registering. | - |
| US-04 | T1 Register | Error prevention | What happens if we use a username that already exists? | Registering again with the same username and password works with no warning. A second account with the same name seems to be created. | Major issue | No screenshot | Check whether the username is already taken and show "This username is already in use." | D-013 |
| US-05 | T1 Register | Understandability | Is the error message clear when the password is exactly 8 characters? | We entered an 8-character password (`abcd1234`). The app rejected it with "Password must be at least 8 characters." Both the hint and the error message say 8 is allowed, so the message tells the user something that is not true. A user following the instructions would not know what to change. | Major issue | US-05.png | Make the check accept 8 characters so it matches the hint and the message. | D-004 (Week 1 BVA defect) |
| US-06 | T2 Log in | Feedback | What do we see for a wrong username and for a wrong password? | We tried a wrong username and, separately, a wrong password. Both show the same message, "Invalid username or password.", in the same pink box as the register errors. This is good for security because it does not reveal which usernames exist. However, both fields are cleared after the error, so the user has to retype their username even if only the password was wrong. | Minor issue | US-06a.png | Keep the username filled in after a failed login. Keep the general message as it is. | - |
| US-07 | T2 Log in | Consistency | Do the login and register pages look and behave the same way? | Both pages use the same white card, field layout, dark blue button and link at the bottom. The bottom links match each other ("No account? Register" / "Already have an account? Log in"). The wording is a little inconsistent: the login heading and button both say "Log in", but the register heading says "Create an account" while the button says "Register". | Good | US-07a.png, US-07b.png | Use the same word in the heading and the button on the register page. | - |
| US-08 | T2 Log in | Error prevention | Are the password characters hidden? Does the form stop us sending empty fields? | Submitting with an empty password shows the browser's own "Please fill out this field." popup, and the form is not sent. The username stays filled in here because the page does not reload. Typed password characters are hidden as dots. | Good | US-08.png | None needed. The popup comes from the browser, so it looks different in Chrome, Edge and Firefox (see compatibility matrix). | - |
| US-09 | T3 Create a task | Navigation | Is "+ New Task" easy to find? Can we get back without saving? | The "+ New Task" button is dark blue and clearly visible at the top right of My Tasks. The form has a grey "Cancel" button next to "Create Task", so it is easy to leave without saving. | Good | US-09.png, US-13.png | None needed. | - |
| US-10 | T3 Create a task | Feedback | What tells us the task was saved? | After clicking "Create Task", we go back to My Tasks and the new task appears in the list. There is no success message, but seeing the task in the list is enough to tell it worked. | Minor issue | US-10.png | Show a short "Task created" message. | - |
| US-11 | T3 Create a task | Error prevention | What happens with an empty title, a title with only spaces, a very long title, or a past date? | Empty title: blocked by the browser's "Please fill out this field." popup. Good.<br>Title with only spaces: accepted. The task appears in the list as a row with no visible title, so the user cannot tell what it is.<br>Very long title: accepted with no limit. The text wraps across many lines and squashes the Category, Due Date and Urgency columns.<br>Past due date (2026-10-14): accepted with no warning. It shows "Overdue" straight away. | Major issue | US-11b.png, US-11c.png, US-11d.png | Check on the server that the title is not blank after removing spaces. Set a maximum title length and tell the user. Show a warning when the due date is in the past. | D-011 (whitespace title), D-012 (no length limit) |
| US-12 | T3 Create a task | Understandability | Are the form labels clear? Is it clear what is optional? | The labels (Title, Description, Category, Due Date) are clear. Nothing shows which fields are required or optional. The date is entered as `20/11/2026` (day/month/year) but shown in the list as `2026-11-20`, so the format changes between the form and the list. The Description box also uses a different font (monospace) from the other fields. | Minor issue | US-12.png | Mark required fields (for example with *), and show the date in the same format everywhere. | - |
| US-13 | T4 Edit a task | Consistency | Does the edit form look like the new task form? Do the button names make sense? | The Edit Task page uses the same layout as New Task, with the fields already filled in. The heading changes to "Edit Task" and the button to "Save Changes", which makes it clear we are editing. The Cancel button is in the same place. There is no way to mark the task as done from this form, only from the circle button on the list. | Good | US-13.png | None needed. Optionally add a "Done" checkbox so all task details can be changed in one place. | - |
| US-14 | T4 Edit a task | Feedback | What do we see after saving? What if we open an edit link for a task that does not exist? | Opening `/tasks/9999/edit` for a task that does not exist sends us straight back to My Tasks with no error message. The user is not told the task was not found, so it looks like the link just did not work. Feedback after saving was not checked separately, but like the other forms there is no success message. | Minor issue | No screenshot | Show a "Task not found" message, or a proper 404 page. | - |
| US-15 | T4 Edit a task | Navigation | Is the "Edit" link easy to spot on each row? | "Edit" and "Delete" are small blue text links stacked in the last column with no column heading. They are easy to miss, and the two look the same, so it is easy to click the wrong one. | Minor issue | US-15.png | Use small buttons or icons, and make Delete red (see US-20). | - |
| US-16 | T5 Mark done | Understandability | Is it clear what the circle button does? | Each row has a small circle on the left with no label, tooltip or column heading. Nothing tells the user that clicking it marks the task as done. We only found out by trying it. | Minor issue | US-16.png | Add a tooltip ("Mark as done") or a short label, or give the column a heading like "Done". | D-016 |
| US-17 | T5 Mark done | Feedback | What changes on the row when a task is done? Can we tell how to undo it? | After clicking the circle, the page reloads and the row changes clearly: the circle becomes a tick, the title is crossed out and greyed, and the badge changes to a grey "Done". Clicking the tick again reopens the task straight away and the badge goes back to its urgency label. Marking and undoing are both easy, though nothing tells the user that clicking the tick will undo it. | Good | US-17a.png, US-17b.png | None needed. The tooltip in US-16 could say "Mark as not done" when the task is finished. | - |
| US-18 | T5 Mark done | Consistency | Do the urgency badge names match what we expect? Does "Due Today" ever show? | A task due today (2026-11-19) shows "Overdue", the same red badge as a task due a month ago (2026-10-14). A task cannot be overdue on the day it is due. After marking it done and reopening it, it goes back to "Overdue", so this is not a one-time display issue. We never saw a "Due Today" badge. | Major issue | US-18.png, US-17b.png | Treat a task as Overdue only after its due date has passed, and show "Due Today" for tasks due today. | D-001 (due-date boundary) |
| US-19 | T6 Delete | Error prevention | Do we get a warning before a task is deleted? Can we cancel? | Clicking "Delete" opens the browser's own popup, "Delete this task?", with OK and Cancel. This stops accidental deletes. However, the popup does not say which task is being deleted, which matters when several rows look similar (for example our blank-title tasks). There is no undo after clicking OK. | Minor issue | US-19.png | Show the task title in the confirmation, for example "Delete 'Test Task 1'?". | - |
| US-20 | T6 Delete | Consistency | Does "Delete" look like "Edit"? Could we click it by mistake? | "Edit" and "Delete" are the same small blue text, stacked right next to each other. Delete does not look any more dangerous than Edit, so it is easy to click the wrong one. The popup reduces the damage, but the user still has to stop and cancel. | Minor issue | US-20.png | Make Delete red, or use a separate button or bin icon, and add some space between the two. | - |
| US-21 | T6 Delete | Feedback | What do we see after a delete? | After clicking OK, the page reloads and the task disappears from the list. No message confirms the delete, so the user has to scan the list to check it worked. In a long list this is harder. | Minor issue | US-21.png | Show a short "Task deleted" message. | - |
| US-22 | T7 Find a task | Feedback | What happens when we change a dropdown? When nothing matches? | Searching "due today" shows only the matching task. Adding the category "Personal" shows "No tasks match your filters.", which is correct because that task has no category. The filters are kept in the URL, so the page remembers them after reloading. The empty message makes sense when filters are on, but the same message also appears for a new user with no tasks and no filters, which suggests something is wrong. | Minor issue | US-22a.png, US-22b.png | Use a different message when the user has no tasks at all, for example "You have no tasks yet. Click + New Task to add one." | D-008 |
| US-23 | T7 Find a task | Consistency | Do the dropdowns and the search box behave in the same way? | Changing the category or status dropdown updates the list straight away. The search box only updates after clicking "Filter" or pressing Enter. The three controls sit side by side and look like one group, but they behave differently, so a user may type in the search box and wait for nothing to happen. There is also no "Clear filters" button. | Minor issue | US-23.png | Make all three behave the same way, and add a "Clear filters" button. | - |
| US-24 | T7 Find a task | Understandability | Does the search placeholder tell us what is searched? Do special characters behave oddly? | The placeholder "Search title..." tells us only titles are searched. However, searching `due_today` (with an underscore) matches a task called "due today" (with a space). The underscore acts as a wildcard that matches any single character, so results can include tasks the user did not search for. | Minor issue | US-24.png | Treat `_` and `%` as normal characters in search. | D-014 |
| US-25 | T8 Dashboard | Understandability | Can we understand each counter without help? | The dashboard shows five cards: Total Tasks, Open, Overdue, Due Soon and Completed (last 7 days). The labels are short and the colours help (red for Overdue, orange for Due Soon, green for Completed). The counts matched the task list. After marking a task with no due date as done, Open went from 4 to 3 and Completed from 0 to 1, so the counters react to changes. However, one of the 2 overdue tasks is the one due today, so the dashboard repeats the wrong label from US-18. Nothing explains how each number is worked out, for example how many days "Due Soon" means. | Minor issue | US-25a.png, US-25b.png | Add a short hint under each card (for example "Due in the next 3 days"), and fix the due-today rule so the Overdue count is correct. | D-001 (see US-18) |
| US-26 | T8 Dashboard | Navigation | Can we jump from a counter to the matching tasks? | The cards are not clickable. To see which tasks are behind a number (for example the 2 overdue tasks), the user has to go back to Tasks and look through the list. | Minor issue | US-26.png | Make each card a link to the task list with the matching filter applied. | - |
| US-27 | T9 Log out | Navigation | Is "Log out" easy to find on every page? | "Log out" is in the top right of the nav bar on every logged-in page, next to the username. It is always in the same place and easy to find. | Good | US-27.png | None needed. | - |
| US-28 | T9 Log out | Feedback | What do we see after logging out? | Clicking "Log out" goes straight to the login page with no message such as "You have been logged out." The nav bar also becomes empty. The user can guess it worked because the login form appears, but it is not confirmed. | Minor issue | US-28.png | Show a short "You have been logged out" message on the login page. | - |
| US-29 | T9 Log out | Error prevention | Is logging out by clicking a link risky? What if we press the browser Back button afterwards? | Clicking "Log out" logs out straight away with no confirmation, since it is a plain link. After logging out, pressing the browser Back button shows the old Dashboard page again, with the username and task counts still visible. As soon as we click anything on it, we are sent to the login page, so the account itself is protected. However, the cached page can still be seen, which could expose information if someone else uses the same computer. | Minor issue | No screenshot | Tell the browser not to cache logged-in pages, so Back after logout goes to the login page. Making logout a button with a POST request would also stop it being triggered by accident. | D-032 |
| US-30 | All pages | Consistency | Do the pages look like one app (colours, fonts, spacing, button style)? | All pages share the same dark blue nav bar, white cards, fonts and dark blue main buttons, so the app looks like one product. A few small things are inconsistent:<br>- The "Filter" button is a lighter blue than the other buttons.<br>- The Description box uses a monospace font, unlike the other fields.<br>- Dates are entered as `dd/mm/yyyy` but shown as `yyyy-mm-dd`.<br>- The register and login forms clear all fields after a server error.<br>- No page shows a success message after an action.<br>- One long title stretches the whole task table and squashes the other columns. | Minor issue | US-11c.png, US-12.png, US-03b.png | Use one button colour, one font for all inputs and one date format. Add short success messages. Limit title width in the table, for example cut it off with "..." and show the full title on hover. | - |
| US-31 | All pages | Navigation | Does the "PyTodo Pro" brand link take us home? Do the nav links show where we are? | Clicking "PyTodo Pro" while logged out keeps us on the login page. While logged in, it takes us to My Tasks. This works as expected. However, "Tasks" and "Dashboard" in the nav bar look the same on every page, so nothing shows which page we are on. | Minor issue | US-31a.png, US-31b.png | Highlight the current page's link, for example bold, underlined or a different colour. | - |

## 5. Summary

| Rating | Count |
|---|---|
| Good | 6 |
| Minor issue | 21 |
| Major issue | 4 |
| **Total** | **31** |

The app is easy to get around. The nav bar is the same on every page, the main buttons are easy to find, and marking a task as done or undoing it is quick and clear. Most problems are small and are about feedback and consistency, not about users getting stuck.

The main problems we found:

1. **Rules that do not match the messages.** The password hint and error both say 8 characters is allowed, but 8 is rejected (US-05). A task due today is shown as Overdue (US-18), and this also makes the dashboard count wrong (US-25).
2. **Weak input checking.** Duplicate usernames (US-04), titles with only spaces and very long titles (US-11) are all accepted. The empty title check only works because of the browser, not the server.
3. **No success messages anywhere.** Register, create, edit, delete and log out all finish with no message. Users have to look at the page to work out whether their action worked.

Smaller patterns that came up more than once:

- Forms clear the username after a server error (US-03, US-06).
- Controls with no label or a confusing label: the circle button (US-16), Edit and Delete looking the same (US-15, US-20), the empty-list message for new users (US-22).
- No way to tell which page you are on (US-31).

## 6. Follow-up

**Sent to the Defect & Metrics Coordinator and now logged:**

| From | Issue | Severity | Defect ID |
|---|---|---|---|
| US-04 | Duplicate usernames can be registered | Major | D-013 |
| US-05 | 8-character password rejected (boundary defect from Week 1) | Major | D-004 (already logged) |
| US-11 | Title with only spaces is accepted | Major | D-011 |
| US-11 | No title length limit, long titles break the table layout | Moderate | D-012 |
| US-18 | Task due today shown as Overdue (boundary defect from Week 1) | Moderate (Major usability rating) | D-001 (already logged) |
| US-24 | `_` in search acts as a wildcard | Minor | D-014 |
| US-16 | Done toggle has no label or tooltip (logged as an accessibility defect) | Moderate | D-016 |
| US-22 | Wrong empty-list message for a user with no tasks | Minor | D-008 |
| US-29 | Back button after logout shows a cached page (found again in Week 5 and Week 7, same bug) | Moderate | D-032 |

**For later weeks:**

- **Week 4 (Web/API):** retest US-04, US-05 and US-11 through the API to check whether the server applies the same rules.
- **Week 5 (Security):** US-29 (cached pages after logout, logout as a GET link) and US-24 (search input not escaped) go into the STRIDE table. We should also check whether one user can open another user's task by changing the ID in the edit URL.

**Note on ratings (26 Nov):** the ratings in the table are usability ratings (Good, Minor issue, Major issue). They are not the same as the defect severity in the defect log. For example, US-18 is a Major usability issue, but D-001 is a Moderate defect. The master test repository turns the ratings into Pass, Fail and Observation, and we have not agreed on the rule yet.

## 7. Limitations

- One tester only, so the ratings are one person's opinion.
- Tested on Chrome on Windows only. Other browsers are covered in `compatibility_matrix.md`.
- The tester already knew the app from Week 1 and 2 testing, so they were not a true first-time user. A real new user might struggle more with things like the circle button.
