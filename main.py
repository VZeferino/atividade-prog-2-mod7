from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Table, Column, Integer, String, MetaData
from databases import Database
from fastapi.responses import RedirectResponse

app = FastAPI()

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String, index=True),
    Column("note", String),
)

@app.on_event("startup")
async def startup():
    await database.connect()
    # Cria a tabela se ela não existir
    await database.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user TEXT, note TEXT)")

# Modelo Pydantic para os dados de login
class LoginData(BaseModel):
    username: str
    password: str

class NoteIn(BaseModel):
    note: str

# Simulando um banco de dados em memória
users = {"teste": "teste123"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

@app.post("/login")
def login(data: LoginData):
    if data.username in users and users[data.username] == data.password:
        return RedirectResponse(url="/notes", status_code=302, headers={"Location": "/notes"})
    raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

@app.get("/notes")
def notes_page():
    return FileResponse("templates/notes.html")

@app.post("/notes/{user}")
async def add_note(user: str, note: NoteIn):
    if user in users:
        query = notes.insert().values(user=user, note=note.note)
        await database.execute(query)
        return {"message": "Nota adicionada com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/notes/{user}")
async def get_notes(user: str):
    if user in users:
        query = notes.select().where(notes.c.user == user)
        notes_data = await database.fetch_all(query)
        return {"notes": notes_data}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.put("/notes/{user}/{note_id}")
async def update_note(user: str, note_id: int, updated_note: NoteIn):
    if user in users:
        query = notes.update().where(notes.c.id == note_id).values(note=updated_note.note)
        await database.execute(query)
        return {"message": "Nota atualizada com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.delete("/notes/{user}/{note_id}")
async def delete_note(user: str, note_id: int):
    if user in users:
        query = notes.delete().where(notes.c.id == note_id)
        await database.execute(query)
        return {"message": "Nota excluída com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# Configuração para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
