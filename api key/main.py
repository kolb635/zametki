from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pyodbc

app = FastAPI()

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=NotesCloudDB.mssql.somee.com;"
    "DATABASE=NotesCloudDB;"
    "UID=asd635536_SQLLogin_1;"
    "PWD=5vz9igna6us;"
)

class UserSchema(BaseModel):
    username: str
    password: str

class NoteSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    content: str

def get_db():
    return pyodbc.connect(CONN_STR)

@app.post("/register")
def register(user: UserSchema):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (user.username, user.password))
            conn.commit()
            return {"status": "ok"}
        except:
            raise HTTPException(status_code=400, detail="User exists")

@app.post("/login")
def login(user: UserSchema):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE username=? AND password=?", (user.username, user.password))
        res = cursor.fetchone()
        if res: return {"user_id": res[0]}
        raise HTTPException(status_code=401, detail="Wrong login/pass")

@app.get("/notes/{u_id}")
def get_notes(u_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content FROM Notes WHERE user_id=?", (u_id))
        return [{"id": r[0], "title": r[1], "content": r[2]} for r in cursor.fetchall()]

@app.post("/notes/save")
def save_note(n: NoteSchema):
    with get_db() as conn:
        cursor = conn.cursor()
        if n.id:
            cursor.execute("UPDATE Notes SET title=?, content=? WHERE id=?", (n.title, n.content, n.id))
        else:
            cursor.execute("INSERT INTO Notes (user_id, title, content) VALUES (?, ?, ?)", (n.user_id, n.title, n.content))
        conn.commit()
        return {"status": "saved"}