from datetime import datetime, UTC, timezone
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Notes
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user

router = APIRouter(
    prefix= '/notes',
    tags= ['notes']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class NoteRequest(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=3, max_length=100)

@router.get("/notes/", status_code=status.HTTP_200_OK)
async def get_user_notes(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    notes = db.query(Notes).filter(Notes.user_id == user.get("user_id")).all()
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found for this user")
    return notes

# POST endpoint
@router.post("/notes/", status_code=status.HTTP_201_CREATED)
async def create_note(user: user_dependency, db: db_dependency, note_request: NoteRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    note_model = Notes(
        title=note_request.title,
        content=note_request.content,
        user_id=user.get("user_id"),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    db.add(note_model)
    db.commit()
    return {"message": "Note created successfully", "note_id": note_model.note_id}

# PUT endpoint to update a note
@router.put("/notes/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(user: user_dependency, db: db_dependency,
                      note_request: NoteRequest, note_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    note_model = db.query(Notes).filter(Notes.note_id == note_id).filter(Notes.user_id == user.get('user_id')).first()

    if note_model is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note_model.title = note_request.title
    note_model.content = note_request.content
    note_model.updated_at = datetime.now(timezone.utc) # Updated time when altered

    db.add(note_model)
    db.commit()
    return {"message": "Note updated successfully", "note_id": note_id}

#DELETE endpoint 
@router.delete("/notes/{note_id}/", status_code=status.HTTP_200_OK)
async def delete_note(user: user_dependency, db: db_dependency, note_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    note_model = db.query(Notes).filter(
        Notes.note_id == note_id, Notes.user_id == user.get("user_id")).first()

    if note_model is None:
        raise HTTPException(status_code=404, detail="Note not found or unauthorized to delete")

    db.delete(note_model)
    db.commit()
    return {"message": "Note deleted successfully", "note_id": note_id}