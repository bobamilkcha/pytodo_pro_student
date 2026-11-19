Week 3: Accessibility Findings (accessibility_findings.md)

Owner: Defect & Metrics Coordinator (Nafiesa)
Target Application: PyTodo Pro (http://127.0.0.1:5000/)
Date tested: 19 Nov 2026
Test Environment: Google Chrome 153 (headless, Linux), window 1366 x 768. ACC-09 uses a 320 px wide window.
Tools: Keyboard-only checks scripted with Playwright, axe-core (automated WCAG rules), Lighthouse (accessibility audit)
Evidence Directory: 03_Special_Testing/evidence/accessibility_testing/

1. Approach

We checked PyTodo Pro against the WCAG 2.1 / 2.2 Level AA ideas from the lecture. Level AA is the recommended target for most websites. We grouped the checks by the four POUR principles:

Perceivable: can users see or hear the content? (labels, contrast, colour)
Operable: can users work the app with a keyboard? (tab order, focus, target size)
Understandable: are pages and errors clear? (titles, language, error messages)
Robust: can screen readers read the controls? (names of buttons and fields)

We used two kinds of checks:

Manual checks. We used the keyboard only (Tab, Shift+Tab, Enter) and checked labels, focus and error messages on every page.
Automated checks. We ran Lighthouse and axe-core on each page. Automated tools only find part of the problems, so we used them as supporting evidence, not as the only test.

Test data: two accounts. acc_tester has four tasks (one overdue, one upcoming, one with no due date, one done). empty_user has no tasks, so we could check the empty list.

2. Accessibility Checklist
Check ID	Page(s)	WCAG criterion (principle)	Check	Expected Result	Actual Result	Result	Evidence	Defect
ACC-01	Log in, Register, New task, Edit task	1.3.1 Info and Relationships, 3.3.2 Labels or Instructions (Perceivable / Understandable)	Click each form label. Check whether the label is linked to its input.	Clicking "Username" moves focus into the username box. Screen readers read the label with the field.	Clicking the label does nothing. Focus stays on the page body. No <label> has a for attribute and no input has an id. axe reports "Form elements must have labels" (critical) on all 4 form pages.	Fail	ACC-01.png	D-009
ACC-02	Task list	4.1.2 Name, Role, Value (Robust)	Read the accessible name of the done toggle button.	The button has a clear name such as "Mark as done" or "Mark as open".	The button's only name is the symbol ○ or ✓. It has no aria-label and no title. A screen reader user hears "white circle, button" and cannot tell what it does.	Fail	ACC-02.png	D-016
ACC-03	Task list	1.4.3 Contrast (Minimum) (Perceivable)	Measure the text contrast of done task titles and the empty-list message.	Normal text has a contrast ratio of at least 4.5:1.	Both use grey 
#999999 on white, which gives 2.84:1. Done task titles (ACC-03a) and the "No tasks match your filters." message (ACC-03b) are hard to read. Other text passed.	Fail	ACC-03a.png, ACC-03b.png	D-015
ACC-04	All pages	2.1.1 Keyboard, 2.4.3 Focus Order, 2.4.7 Focus Visible (Operable)	Use only the Tab key on each page. Check order and whether focus is visible.	Every control can be reached in a logical order. The focused control has a visible outline.	All links, dropdowns, buttons and inputs can be reached. The order follows the page: nav bar, "+ New Task", filters, then each row (toggle, Edit, Delete). The browser's default focus outline is visible on every control.	Pass	ACC-04a.png, ACC-04b.png	-
ACC-05	All pages	2.4.2 Page Titled, 1.3.1 headings (Operable)	Read each page's browser tab title and heading structure.	Each page has its own title and one main heading.	Each page has a unique title, e.g. "Tasks — PyTodo Pro" and "Dashboard — PyTodo Pro", and one <h1>.	Pass	ACC-05.png, ACC_scan_log.txt	-
ACC-06	Register	3.3.1 Error Identification (Understandable)	Submit an invalid username (ab) and read the error.	The error is shown in text and says what is wrong.	The text error "Username must be 3-20 characters (letters, numbers, underscore)." is clear and shows at the top of the form. Two weaker points: the error is not linked to the field (aria-invalid is not set), and the username box is cleared, so the user must retype it (see US-03).	Pass	ACC-06.png	-
ACC-07	All pages	3.1.1 Language of Page (Understandable)	Check the page language.	<html lang="en"> is set so screen readers use the right voice.	lang="en" is set in base.html for every page.	Pass	ACC_scan_log.txt	-
ACC-08	Task list	1.3.1, 4.1.2 (Perceivable / Robust)	Check the names of the category dropdown, status dropdown and search box.	Each filter control has a label or aria-label.	None of the three has a label. The dropdowns rely on their first option ("All categories") and the search box relies on its placeholder ("Search title..."). axe reports "Select element must have an accessible name" (critical).	Fail	ACC-08.png	D-009
ACC-09	Task list (all pages share the layout)	1.4.10 Reflow (Perceivable)	Set the window to 320 px wide and check whether content fits without sideways scrolling.	Content reflows into one column with no horizontal scrolling.	The page is 510 px wide in a 320 px window, so users must scroll sideways. The "Log out" link falls off the dark nav bar and becomes almost invisible. The pages have no <meta name="viewport"> tag and style.css has no @media rules.	Fail	ACC-09.png	D-017
ACC-10	Log in, Register, Task list, New task, Dashboard	Automated audit (all principles)	Run a Lighthouse accessibility audit on each page.	Score of 90 or more, with no failed audits.	Scores: Log in 85, Register 85, Task list 72, New task 74, Dashboard 95. Failed audits match ACC-01, ACC-03, ACC-08, ACC-11 and ACC-15.	Fail	ACC-10a.png to ACC-10e.png, lighthouse_*.report.html	See linked checks
ACC-11	Task list	2.5.8 Target Size (Minimum), WCAG 2.2 (Operable)	Measure the size of the Edit and Delete links.	Click targets are at least 24 x 24 px, or have enough space around them.	Edit is 24 x 16 px and Delete is 39 x 15 px, stacked close together. They are hard to hit on touch screens or with shaky hands. Lighthouse also flags this.	Fail	ACC-11.png	D-018
ACC-12	Task list	1.4.1 Use of Colour (Perceivable)	Check whether urgency badges rely on colour alone.	Meaning is also given in text.	Every badge has a text label (Overdue, Upcoming, No due date, Done) as well as a colour, so colour is not the only cue.	Pass	ACC-12.png	-
ACC-13	Task list	2.1.1 Keyboard (Operable)	Use the done toggle and the Delete confirm popup with the keyboard only.	Enter activates the button. The confirm popup can be answered by keyboard.	Enter works on the toggle and on Delete. The browser's "Delete this task?" popup opens and can be answered with the keyboard.	Pass	ACC_scan_log.txt	-
ACC-14	All pages	1.1.1 Non-text Content (Perceivable)	Check images for alt text.	Every meaningful image has alt text.	The app has no images. The brand "PyTodo Pro" is text, so nothing needs alt text.	Pass	ACC_scan_log.txt	-
ACC-15	All pages	1.3.1 Info and Relationships (Perceivable)	Check page landmarks and table headers.	Pages have a <main> region. Every table column has a header.	No page has a <main> landmark, so screen reader users cannot jump to the main content. The task table's first column (toggle) and last column (actions) have empty headers.	Fail	ACC-10c.png, ACC_scan_log.txt	Recommendation R-04 (best practice, not logged as a defect)
ACC-16	All pages	2.3.1 Three Flashes (Operable)	Look for flashing or moving content.	Nothing flashes more than 3 times per second.	No animation or flashing content on any page.	Pass	-	-
3. Summary
Metric	Count	Percentage
Total checks	16	100%
Passed	8	50.00%
Failed	8	50.00%
Not tested	0	0.00%
New defects raised	5 (D-009, D-015, D-016, D-017, D-018)	-
Results by WCAG principle
Principle	Checks	Passed	Failed
Perceivable	7 (ACC-01, 03, 08, 09, 12, 14, 15)	2	5
Operable	5 (ACC-04, 05, 11, 13, 16)	4	1
Understandable	2 (ACC-06, 07)	2	0
Robust	1 (ACC-02)	0	1
Automated audit	1 (ACC-10)	0	1

Main finding: PyTodo Pro works well for keyboard users. Every control can be reached, focus is visible and the pages have clear titles. But it is weak for screen reader users: no form field or filter is linked to a label, and the done button has no meaningful name. It also does not reflow on narrow screens. Most of these problems are small template changes. The app does not yet meet WCAG Level AA.

4. Improvement Recommendations
ID	Recommendation	Fixes
R-01	Add id to every input and for="..." to its label. Add aria-label (or a visually hidden label) to the two filter dropdowns and the search box.	ACC-01, ACC-08
R-02	Give the done toggle an aria-label such as "Mark 'Pay bills' as done" / "Mark as open".	ACC-02
R-03	Change the grey #999 text to at least 
#767676 (4.5:1 on white).	ACC-03
R-04	Wrap the page content in <main> and give the empty table headers screen-reader text (e.g. "Done", "Actions").	ACC-15
R-05	Add <meta name="viewport" content="width=device-width, initial-scale=1"> and @media rules so the table and nav stack on small screens.	ACC-09
R-06	Make Edit and Delete at least 24 x 24 px (more padding or button styling) with space between them.	ACC-11
R-07	On a form error, keep the typed username, set aria-invalid="true" on the wrong field and link the message with aria-describedby.	ACC-06
5. Limitations
Testing used Chrome on Linux through a script, not a physical screen reader. We checked what a screen reader would read (accessible names) but did not listen with NVDA or VoiceOver.
Automated tools find only part of accessibility problems. Lighthouse itself lists 10 more items to check by hand.
Mobile width was checked by resizing the window, not on a real phone. Real-device checks are covered in compatibility_matrix.md.
