"""
Week 6 - Automated accessibility checks (from Week 3) on the page HTML and CSS.

Owner: Nafiesa (Defect & Metrics Coordinator)
Source: 03_Special_Testing/accessibility_findings.md (Week 3, WCAG 2.2 checks)

These checks read the HTML that each page sends and the colours in style.css.
They need no browser, so they are fast and stable. They do NOT replace the
Selenium UI tests or a Lighthouse audit: checks that need a real screen
(keyboard focus, target size, reflow width) still need a browser.

Automated here:
    ACC-01  Form fields have a programmatic label            (D-009)
    ACC-02  Done toggle button has an accessible name        (D-016)
    ACC-03  Grey text meets 4.5:1 contrast                   (D-015)
    ACC-05  Each page has a title and one <h1>               (passed in Week 3)
    ACC-07  Page language is set                             (passed in Week 3)
    ACC-08  Filter controls have an accessible name          (D-009)
    ACC-09  Viewport meta tag present (needed for reflow)    (D-017)
    ACC-12  Urgency badges carry text, not colour only       (passed in Week 3)
    GUI-08  Empty task list shows a correct message          (D-008)

Not automated here (need a browser): ACC-04, ACC-06, ACC-10, ACC-11 (D-018),
ACC-13, ACC-16.

Tests that guard a known open defect are EXPECTED TO FAIL until it is fixed.

Run from the repository root:
    pytest 06_Automation_Regression/tests/ui/test_reg_accessibility_markup.py -v
"""

import os
import re
import sys
from html.parser import HTMLParser

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT)

import app as app_module

PASSWORD = "Password123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class PageParser(HTMLParser):
    """Collects the tags and text we need for the checks."""

    def __init__(self):
        super().__init__()
        self.tags = []            # (tag, attrs dict)
        self.label_for = set()    # ids named by <label for="...">
        self.titles = []
        self.h1 = 0
        self._in = None
        self._buf = ""
        self.buttons = []         # (attrs, text)
        self.badges = []          # text of each .badge span

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == "label" and a.get("for"):
            self.label_for.add(a["for"])
        if tag == "h1":
            self.h1 += 1
        if tag in ("title", "button") or (tag == "span" and "badge" in a.get("class", "")):
            self._in, self._attrs, self._buf = tag, a, ""

    def handle_data(self, data):
        if self._in:
            self._buf += data

    def handle_endtag(self, tag):
        if tag == self._in:
            text = self._buf.strip()
            if tag == "title":
                self.titles.append(text)
            elif tag == "button":
                self.buttons.append((self._attrs, text))
            else:
                self.badges.append(text)
            self._in = None


def parse(html_bytes):
    p = PageParser()
    p.feed(html_bytes.decode("utf-8"))
    return p


def has_name(attrs, page):
    """True if a form control has a programmatic label."""
    return bool(attrs.get("aria-label") or attrs.get("aria-labelledby")
                or (attrs.get("id") and attrs["id"] in page.label_for))


def contrast(hex1, hex2="#ffffff"):
    """WCAG contrast ratio between two hex colours."""
    def lum(h):
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    l1, l2 = sorted((lum(hex1), lum(hex2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def css_colour(selector):
    """Return the text colour set for a CSS selector in static/style.css."""
    css = open(os.path.join(ROOT, "static", "style.css"), encoding="utf-8").read()
    rule = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
    assert rule, f"selector {selector} not found in style.css"
    colour = re.search(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})", rule.group(1))
    assert colour, f"no colour set for {selector}"
    return colour.group(1)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "test_acc.db"))
    app_module.app.config["TESTING"] = True
    app_module.app.config["PROPAGATE_EXCEPTIONS"] = False
    app_module.init_db()
    return app_module.app.test_client()


@pytest.fixture
def user(client):
    client.post("/api/register", json={"username": "acc_tester", "password": PASSWORD})
    return client


@pytest.fixture
def user_with_tasks(user):
    tid = user.post("/api/tasks", json={"title": "Pay bills", "due_date": "2030-01-01"}).get_json()["id"]
    done = user.post("/api/tasks", json={"title": "Old task"}).get_json()["id"]
    user.put(f"/api/tasks/{done}", json={"done": True})
    user.task_id = tid
    return user


FORM_PAGES_LOGGED_OUT = ["/login", "/register"]


# ---------------------------------------------------------------------------
# ACC-01 / ACC-08 - labels (D-009)
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.parametrize("path", FORM_PAGES_LOGGED_OUT)
def test_acc_01_login_register_fields_have_labels(client, path):
    """ACC-01: every input on /login and /register has a linked label. EXPECTED TO FAIL: D-009."""
    page = parse(client.get(path).data)
    fields = [a for t, a in page.tags if t == "input" and a.get("type") not in ("hidden", "submit")]
    unnamed = [a.get("name") for a in fields if not has_name(a, page)]
    assert not unnamed, f"{path}: fields with no label: {unnamed}"


@pytest.mark.regression
@pytest.mark.parametrize("path", ["/tasks/new", "EDIT"])
def test_acc_01_task_form_fields_have_labels(user_with_tasks, path):
    """ACC-01: every field on the new and edit task forms has a linked label. EXPECTED TO FAIL: D-009."""
    if path == "EDIT":
        path = f"/tasks/{user_with_tasks.task_id}/edit"
    page = parse(user_with_tasks.get(path).data)
    fields = [a for t, a in page.tags
              if t in ("input", "select", "textarea") and a.get("type") not in ("hidden", "submit")]
    unnamed = [a.get("name") for a in fields if not has_name(a, page)]
    assert not unnamed, f"{path}: fields with no label: {unnamed}"


@pytest.mark.regression
def test_acc_08_filter_controls_have_names(user_with_tasks):
    """ACC-08: category, status and search controls on / have a name. EXPECTED TO FAIL: D-009."""
    page = parse(user_with_tasks.get("/").data)
    filters = [a for t, a in page.tags if t in ("select", "input") and a.get("name") in ("category", "status", "q")]
    assert len(filters) == 3
    unnamed = [a["name"] for a in filters if not has_name(a, page)]
    assert not unnamed, f"filter controls with no name: {unnamed}"


# ---------------------------------------------------------------------------
# ACC-02 - toggle button name (D-016)
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_acc_02_done_toggle_has_accessible_name(user_with_tasks):
    """ACC-02: the done toggle has a name in words, not only a symbol. EXPECTED TO FAIL: D-016."""
    page = parse(user_with_tasks.get("/").data)
    toggles = [(a, txt) for a, txt in page.buttons if "check-btn" in a.get("class", "")]
    assert toggles, "no done toggle found"
    for attrs, text in toggles:
        name = attrs.get("aria-label") or attrs.get("title") or text
        assert re.search(r"[A-Za-z]", name), f"toggle name is only {name!r}"


# ---------------------------------------------------------------------------
# ACC-03 - contrast (D-015)
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.parametrize("selector", [".task-table tr.done .title-cell", ".empty"])
def test_acc_03_grey_text_contrast(selector):
    """ACC-03: done titles and the empty message reach 4.5:1 on white. EXPECTED TO FAIL: D-015."""
    colour = css_colour(selector)
    ratio = contrast(colour)
    assert ratio >= 4.5, f"{selector} uses {colour}: contrast {ratio:.2f}:1"


# ---------------------------------------------------------------------------
# ACC-05 / ACC-07 / ACC-12 - checks that passed in Week 3
# ---------------------------------------------------------------------------

def test_acc_05_each_page_has_unique_title_and_one_h1(user_with_tasks):
    """ACC-05: each logged-in page has its own <title> and exactly one <h1>."""
    titles = []
    for path in ["/", "/tasks/new", "/dashboard"]:
        page = parse(user_with_tasks.get(path).data)
        assert page.h1 == 1, f"{path} has {page.h1} <h1> elements"
        titles.append(page.titles[0])
    assert len(set(titles)) == len(titles), f"titles repeat: {titles}"


@pytest.mark.regression
@pytest.mark.parametrize("path", ["/login", "/register"])
def test_acc_07_page_language_set(client, path):
    """ACC-07: <html lang="en"> is set."""
    page = parse(client.get(path).data)
    html = next(a for t, a in page.tags if t == "html")
    assert html.get("lang") == "en"


def test_acc_12_badges_have_text(user_with_tasks):
    """ACC-12: every urgency badge shows a word, so colour is not the only cue."""
    page = parse(user_with_tasks.get("/").data)
    assert page.badges, "no badges found"
    assert all(re.search(r"[A-Za-z]", b) for b in page.badges), page.badges


# ---------------------------------------------------------------------------
# ACC-09 - reflow needs a viewport tag (D-017)
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_acc_09_viewport_meta_present(client):
    """ACC-09: pages include <meta name="viewport">, needed for reflow at 320 px. EXPECTED TO FAIL: D-017."""
    page = parse(client.get("/login").data)
    assert any(t == "meta" and a.get("name") == "viewport" for t, a in page.tags)


# ---------------------------------------------------------------------------
# GUI-08 - empty list message (D-008)
# ---------------------------------------------------------------------------

@pytest.mark.regression
def test_gui_08_empty_list_message_without_filters(user):
    """GUI-08: a new user with no tasks and no filters does not see "No tasks match your filters."
    EXPECTED TO FAIL: D-008."""
    page = user.get("/").data
    assert b"No tasks match your filters." not in page
