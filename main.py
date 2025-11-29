from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import random, string, sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")
conn = sqlite3.connect("db.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS p(id TEXT PRIMARY KEY,name TEXT,s TEXT)")

def id(): return "sp"+''.join(random.choices(string.ascii_lowercase+string.digits, k=10))

@app.get("/", response_class=HTMLResponse)
async def home(r:Request): return templates.TemplateResponse("a.html", {"request": r})

@app.post("/c")
async def c(r:Request, n:str=Form(), s:str=Form()):
    i = id()
    conn.execute("INSERT INTO p VALUES(?,?,?)", (i,n,s)); conn.commit()
    return templates.TemplateResponse("b.html", {"request":r, "id":i, "n":n})

@app.get("/api/{i}", response_class=JSONResponse)
async def api(i:str):
    cur = conn.execute("SELECT name,s FROM p WHERE id=?", (i,))
    row = cur.fetchone()
    if row: return {"name":row[0], "sentences":[x for x in row[1].split("\n") if x.strip()]}
    return {"error":"no"}


from netlify_py import handler

netlify_handler = handler(app) 
