# White-Box Testing: `index`

Owner: Test Design Coordinator (Aida)  
Unit: `index()` in `app.py`, lines 189–222  
Feature: F-09 Task list & F-11 Filter and search  
Test file: `02_White_Box_Coverage/index/tests/test_index.py`

---

## 1. Control-Flow Analysis

### Nodes

| Node | Line(s) | Code |
|---|---|---|
| N0 | 189–190 | `@app.route("/")` and `@login_required_web` (decorator check: `session.get("user_id")`) |
| N1 | 191–198 | Extract `category_filter`, `status_filter`, `q`; initialize `query` and `params` |
| N2 | 200 | `cat_id = get_category_id_by_name(db, category_filter) if category_filter else None` (Decision B1 — ternary) |
| N3 | 201 | `if cat_id:` (Decision B2) |
| N4 | 202–203 | `query += " AND category_id = ?"`; `params.append(cat_id)` |
| N5 | 205 | `if status_filter == "done":` (Decision B3) |
| N6 | 206 | `query += " AND done = 1"` |
| N7 | 207 | `elif status_filter == "open":` (Decision B4) |
| N8 | 208 | `query += " AND done = 0"` |
| N9 | 210 | `if q:` (Decision B5) |
| N10 | 211–212 | `query += " AND title LIKE ?"`; `params.append(f"%{q}%")` |
| N11 | 214–215 | `query += " ORDER BY id DESC"`; `rows = db.execute(query, params).fetchall()` |
| N12 | 216 | `for r in rows` in list comprehension `[row_to_task(...) for r in rows]` (Decision B6 — loop) |
| N13 | 216 | `row_to_task(r, get_category_name(db, r["category_id"]))` |
| N14 | 217–222 | Fetch `categories` and `return render_template("index.html", ...)` |

### Control-Flow Graph

```mermaid
flowchart TD
    N0{"N0: session user_id?"} -- False --> REDIR(["Redirect /login (302)"])
    N0 -- True --> N1["N1: Read args & init query/params (lines 192-198)"]
    N1 --> N2{"N2 (B1): category_filter?"}
    N2 -- True --> N2T["cat_id = get_category_id_by_name(...)"]
    N2 -- False --> N2F["cat_id = None"]
    N2T --> N3{"N3 (B2): cat_id?"}
    N2F --> N3
    N3 -- True --> N4["N4: Append AND category_id = ?"]
    N3 -- False --> N5{"N5 (B3): status_filter == 'done'?"}
    N4 --> N5
    N5 -- True --> N6["N6: Append AND done = 1"]
    N5 -- False --> N7{"N7 (B4): status_filter == 'open'?"}
    N6 --> N9{"N9 (B5): q?"}
    N7 -- True --> N8["N8: Append AND done = 0"]
    N7 -- False --> N9
    N8 --> N9
    N9 -- True --> N10["N10: Append AND title LIKE ?"]
    N9 -- False --> N11["N11: Execute SQL query (lines 214-215)"]
    N10 --> N11
    N11 --> N12{"N12 (B6): next r in rows?"}
    N12 -- True --> N13["N13: row_to_task(r, category_name)"]
    N13 --> N12
    N12 -- False --> N14(["N14: Fetch categories & render index.html"])