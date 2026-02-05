from typing import List
from fastapi import APIRouter, Depends

from api.dependencies.note.note import note_getter
from core.authentication.fastapi_users import current_user
from core.config import settings

from core.models import User, Note

from core.schemas.comment import CommentResponse, CommentCreate
from core.schemas.note import NoteCreate, NoteResponse, NoteUpdate

from services.comments import CommentService
from services.notes import NoteService


router = APIRouter(
    prefix=settings.api.v1.notes,
    tags=["Notes"],
)


@router.get("/", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    service: NoteService = Depends(NoteService),
    user: User = Depends(current_user),
):
    return await service.create_note(
        note_data=note_data,
        user=user,
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    service: NoteService = Depends(NoteService),
    user: User = Depends(current_user),
):
    return await service.get_note_by_id(
        note_id=note_id,
        user=user,
    )


@router.get("/", response_model=List[NoteResponse])
async def get_all_notes(
    service: NoteService = Depends(NoteService),
    user: User = Depends(current_user),
):
    return await service.get_notes(
        user=user,
    )


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_data: NoteUpdate,
    note: Note = Depends(note_getter),
    service: NoteService = Depends(NoteService),
):
    return await service.update_note(
        note=note,
        note_data=note_data,
    )


@router.delete("/{note_id}")
