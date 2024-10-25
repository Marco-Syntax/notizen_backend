from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.sql import func
from models import notes, metadata
from database import database, engine
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaube alle Quellen
    allow_credentials=True,
    allow_methods=["*"],  # Erlaube alle HTTP-Methoden (einschließlich OPTIONS)
    allow_headers=["*"],  # Erlaube alle Header
)

# Tabellen erstellen, falls nicht vorhanden
metadata.create_all(engine)

# Verbindung zur Datenbank herstellen
@app.on_event("startup")
async def startup():
    await database.connect()

# Verbindung zur Datenbank trennen
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Pydantic-Modelle zur Validierung
class NoteIn(BaseModel):
    title: str
    content: str

class NoteOut(NoteIn):
    id: int
    created_at: str

# GET: Alle Notizen abrufen
@app.get("/notes", response_model=List[NoteOut])
async def get_notes():
    query = notes.select()
    return await database.fetch_all(query)

# POST: Neue Notiz hinzufügen
@app.post("/notes", response_model=NoteOut)
async def create_note(note: NoteIn):
    query = notes.insert().values(title=note.title, content=note.content)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id, "created_at": str(func.now())}

# PUT: Eine Notiz bearbeiten
@app.put("/notes/{note_id}", response_model=NoteOut)
async def update_note(note_id: int, updated_note: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(title=updated_note.title, content=updated_note.content)
    await database.execute(query)
    return {**updated_note.dict(), "id": note_id, "created_at": str(func.now())}

# DELETE: Eine Notiz löschen
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": f"Notiz mit ID {note_id} wurde gelöscht."}
