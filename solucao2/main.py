from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData, select
from fastapi import Depends
from databases import Database
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import database
from models import users, notes

app = FastAPI()

SECRET_KEY = "vitorzeferino25"

def create_jwt_token(username: str):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
    payload = {"sub": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

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

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
)

class LoginData(BaseModel):
    username: str
    password: str

class NoteIn(BaseModel):
    note: str

@app.on_event("startup")
async def startup():
    await database.connect()
    
    query = select([users]).where(users.c.username == "teste")
    result = await database.fetch_all(query)
    
    if not result:
        hashed_password = get_password_hash("teste123")
        query = users.insert().values(
            username="teste", hashed_password=hashed_password
        )
        await database.execute(query)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    return {"message": f"Bem-vindo, {payload['sub']}!"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = users.select().where(users.c.username == form_data.username)
    user = await database.fetch_one(query)
    if user and verify_password(form_data.password, user["hashed_password"]):
        token = create_jwt_token(user["username"])
        return {"token": token}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.get("/notes")
async def notes_page():
    return FileResponse("templates/notes.html")

@app.post("/notes/{user}")
async def add_note(user: str, note: NoteIn):
    query = users.select().where(users.c.username == user)
    db_user = await database.fetch_one(query)
    if db_user:
        values = {"user": user, "note": note.note}
        query = notes.insert().values(**values)
        await database.execute(query)
        return {"message": "Nota adicionada com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/notes/{user}")
async def get_notes(user: str):
    query = notes.select().where(notes.c.user == user)
    user_notes = await database.fetch_all(query)
    if user_notes:
        return {"notes": user_notes}
    raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para o usuário")

@app.put("/notes/{user}/{note_id}")
async def update_note(user: str, note_id: int, updated_note: NoteIn):
    query = users.select().where(users.c.username == user)
    db_user = await database.fetch_one(query)
    if db_user:
        values = {"note": updated_note.note}
        query = notes.update().where(notes.c.id == note_id).values(**values)
        await database.execute(query)
        return {"message": "Nota atualizada com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.delete("/notes/{user}/{note_id}")
async def delete_note(user: str, note_id: int):
    query = users.select().where(users.c.username == user)
    db_user = await database.fetch_one(query)
    if db_user:
        query = notes.delete().where(notes.c.id == note_id)
        await database.execute(query)
        return {"message": "Nota excluída com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

app.mount("/static", StaticFiles(directory="static"), name="static")
