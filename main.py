from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random, string, sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("db.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS p(id TEXT PRIMARY KEY, name TEXT, s TEXT)")
conn.commit()

def gen_id():
    return "sp-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=10))

@app.post("/c")
async def create_pack(request: Request):
    form = await request.form()
    name = form.get("n", "Unnamed Pack")
    sentences = form.get("s", "")
    if not sentences.strip():
        return JSONResponse({"error": "empty"}, status_code=400)
    plugin_id = gen_id()
    conn.execute("INSERT INTO p VALUES(?, ?, ?)", (plugin_id, name, sentences))
    conn.commit()
    return {"id": plugin_id, "name": name}

@app.get("/api/{plugin_id}")
async def get_pack(plugin_id: str):
    cur = conn.execute("SELECT name, s FROM p WHERE id=?", (plugin_id,))
    row = cur.fetchone()
    if not row:
        return {"error": "not found"}
    name, sentences = row
    return {
        "name": name,
        "sentences": [line.strip() for line in sentences.split("\n") if line.strip()]
    }

from netlify_py import handler
netlify_handler = handler(app)
