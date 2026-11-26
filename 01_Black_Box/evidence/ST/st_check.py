import sys, re, tempfile, os, datetime
sys.path.insert(0, r"c:\Users\syasy\OneDrive\Documents\2026\STQA\pytodo_pro_student")
import app as A
tmp = os.path.join(tempfile.mkdtemp(), "t.db")
A.DATABASE = tmp
A.init_db()
app = A.app; app.config["TESTING"] = True
def cl(): return app.test_client()
def body(r): return r.get_data(as_text=True)
def dash(c):
    h = body(c.get("/dashboard"))
    v = re.findall(r'stat-value">(\d+)<', h)
    return dict(zip(["Total","Open","Overdue","DueSoon","Completed"], map(int, v)))
def tasks(c, q=""):
    h = body(c.get("/"+q))
    rows = re.findall(r'<tr class="(done)?">.*?check-btn">(.)</button>.*?title-cell">(.*?)</td>.*?badge[^>]*>(.*?)</span>', h, re.S)
    return [(t, m, b) for _, m, t, b in rows]
def post(c, path, data): return c.post(path, data=data)
def reg(c,u): return post(c,"/register",{"username":u,"password":"testpass123"})
def login(c,u,p="testpass123"): return post(c,"/login",{"username":u,"password":p})
def loc(r): return r.headers.get("Location")
def newtask(c,title,cat="",due=""):
    return post(c,"/tasks/new",{"title":title,"description":"","category":cat,"due_date":due})
def tid(title):
    d=A.get_db if False else None
    import sqlite3
    con=sqlite3.connect(tmp); r=con.execute("select id from tasks where title=?",(title,)).fetchone(); con.close(); return r[0] if r else None
P=lambda *a: print(*a)
# setup
for u in ["qa_user1","qa_user2"]:
    c=cl(); reg(c,u)
c2=cl(); login(c2,"qa_user2"); newtask(c2,"user2 task"); 
today=datetime.date.today()
c=cl()
r=login(c,"qa_user1"); h=body(c.get("/"))
P("060", r.status_code, loc(r), "qa_user1" in h, "Log out" in h, "Dashboard" in h)
c3=cl(); r=reg(c3,"qa_user3"); h=body(c3.get("/")); P("061", r.status_code, loc(r), "qa_user3" in h)
r=c.get("/logout"); P("062", r.status_code, loc(r)); h=body(cl().get("/login")); P("062 login page has no Log out/Dashboard", "Log out" not in h, "Dashboard" not in h)
# 063
c=cl(); login(c,"qa_user1"); newtask(c,"user1 task"); r=login(c,"qa_user2"); h=body(c.get("/"))
P("063", r.status_code, loc(r), "qa_user2" in h, tasks(c))
# 064
c=cl(); r=login(c,"qa_user1","wrongpass999"); P("064", r.status_code, "Invalid username or password." in body(r)); r=c.get("/"); P("064 step4", r.status_code, loc(r))
# 065
c=cl(); login(c,"qa_user1"); c.get("/logout")
for p in ["/dashboard","/tasks/new","/"]:
    r=c.get(p); P("065",p,r.status_code,loc(r))
# 066
r=cl().get("/logout"); P("066", r.status_code, loc(r))
# 067 headers
c=cl(); login(c,"qa_user1"); r=c.get("/"); P("067 headers", r.headers.get("Cache-Control"), r.headers.get("Expires"), r.headers.get("Pragma"))
# 068
c=cl(); login(c,"qa_user1"); newtask(c,"stale68"); i=tid("stale68")
c.get("/logout"); r=post(c,f"/tasks/{i}/toggle",{}); P("068 step3", r.status_code, loc(r))
c=cl(); login(c,"qa_user1"); P("068 step4", [t for t in tasks(c) if "stale68" in t[0]])
# lifecycle
c=cl(); login(c,"qa_user1")
d0=dash(c); P("069 before",d0)
newtask(c,"ST open task","Study",(today+datetime.timedelta(days=5)).isoformat())
P("069", tasks(c)[0], dash(c))
i=tid("ST open task"); d=dash(c)
post(c,f"/tasks/{i}/toggle",{}); P("070 row", [t for t in tasks(c) if "ST open" in t[0]], "done filter", [t for t in tasks(c,"?status=done") if "ST open" in t[0]], "before",d,"after",dash(c))
d=dash(c); post(c,f"/tasks/{i}/toggle",{}); P("071", [t for t in tasks(c) if "ST open" in t[0]], "before",d,"after",dash(c))
d=dash(c)
r=post(c,f"/tasks/{i}/edit",{"title":"ST open task edited","description":"","category":"Work","due_date":(today+datetime.timedelta(days=5)).isoformat()})
h=body(c.get("/")); P("072", r.status_code, [t for t in tasks(c) if "edited" in t[0]], "Work" in h, "before",d,"after",dash(c))
newtask(c,"ST done task"); j=tid("ST done task"); post(c,f"/tasks/{j}/toggle",{}); d=dash(c)
post(c,f"/tasks/{j}/edit",{"title":"ST done task edited","description":"","category":"","due_date":""})
P("073", [t for t in tasks(c) if "ST done" in t[0]], "before",d,"after",dash(c))
newtask(c,"ST delete open"); k=tid("ST delete open"); d=dash(c); post(c,f"/tasks/{k}/delete",{}); P("074", [t for t in tasks(c) if "delete open" in t[0]], "before",d,"after",dash(c))
newtask(c,"ST delete done"); k=tid("ST delete done"); post(c,f"/tasks/{k}/toggle",{}); d=dash(c); post(c,f"/tasks/{k}/delete",{}); P("075", [t for t in tasks(c) if "delete done" in t[0]], "before",d,"after",dash(c))
P("076 template has confirm:", "confirm('Delete this task?')" in open(r"c:\Users\syasy\OneDrive\Documents\2026\STQA\pytodo_pro_student\templates\index.html").read())
# 077
newtask(c,"ST stale"); s=tid("ST stale"); n=len(tasks(c)); post(c,f"/tasks/{s}/delete",{}); r=post(c,f"/tasks/{s}/toggle",{}); P("077", r.status_code, loc(r), n, len(tasks(c)), [t for t in tasks(c) if "stale" in t[0] and "68" not in t[0]])
# 078
newtask(c,"ST gone"); g=tid("ST gone"); post(c,f"/tasks/{g}/delete",{}); r=c.get(f"/tasks/{g}/edit"); P("078", r.status_code, loc(r), "<form" in body(r) and "Save" in body(r))
# 079
newtask(c,"ST own"); o=tid("ST own"); c2=cl(); login(c2,"qa_user2"); r=c2.get(f"/tasks/{o}/edit"); P("079", r.status_code, loc(r), "ST own" in body(r))
c1=cl(); login(c1,"qa_user1"); P("079 step3", [t for t in tasks(c1) if "ST own" in t[0]])
