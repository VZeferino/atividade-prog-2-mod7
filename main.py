from fastapi import FastAPI, HTTPException, Cookie, Response, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData, select
from databases import Database
from datetime import timedelta
from jose import JWTError, jwt
from auth import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, get_password_hash

app = FastAPI()

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

def get_current_user(token: str = Cookie(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.on_event("startup")
async def startup():
    await database.connect()
    
    query = select([users]).limit(1)
    result = await database.fetch_all(query)
    if not result:
        query = users.insert().values(
            username="teste", hashed_password=get_password_hash("teste123")
        )
        await database.execute(query)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

@app.post("/login")
async def login(data: LoginData, response: Response):
    query = users.select().where(users.c.username == data.username)
    user = await database.fetch_one(query)
    if user and verify_password(data.password, user["hashed_password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": data.username}, expires_delta=access_token_expires)
        response.set_cookie(key="access_token", value=access_token)
        return RedirectResponse(url="/notes", status_code=302, headers={"Location": "/notes"})
    raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

@app.get("/notes")
async def notes_page(user: str = Depends(get_current_user)):
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

@app.put("/notes/{user}/{note_id}")
async def update_note(user: str, note_id: int, updated_note: NoteIn):
    if user in users:
        values = {"note": updated_note.note}
        query = notes.update().where(notes.c.id == note_id).values(**values)
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

app.mount("/static", StaticFiles(directory="static"), name="static")
