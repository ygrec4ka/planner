from typing import List
from fastapi import APIRouter, Depends

from api.dependencies.comment.comment import comment_getter
from api.dependencies.note.note import note_getter
from api.dependencies.services.service import get_note_service, get_comment_service
from core.authentication.fastapi_users import current_user
from core.config import settings

from core.models import User, Note, Comment

from core.schemas.comment import CommentResponse, CommentCreate, CommentUpdate
from core.schemas.note import NoteCreate, NoteResponse, NoteUpdate

from services.comments import CommentService
from services.notes import NoteService


router = APIRouter(
    prefix=settings.api.v1.notes,
    tags=["Notes"],
)


@router.post("/", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    return await service.create_note(
        note_data=note_data,
        user=user,
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    return await service.get_note_by_id(
        note_id=note_id,
        user=user,
    )


@router.get("/", response_model=List[NoteResponse])
async def get_all_notes(
    service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    return await service.get_notes(
        user=user,
    )


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_data: NoteUpdate,
    note: Note = Depends(note_getter),
    service: NoteService = Depends(get_note_service),
):
    return await service.update_note(
        note=note,
        note_data=note_data,
    )


@router.delete("/{note_id}")
async def delete_note(
    note: Note = Depends(note_getter),
    service: NoteService = Depends(get_note_service),
):
    return await service.delete_note(
        note=note,
    )


@router.post("/{note_id}/comments", response_model=CommentResponse)
async def create_comment_for_note(
    note_id: int,
    comment_data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
    user: User = Depends(current_user),
):
    return await service.create_note_comment(
        comment_data=comment_data,
        user=user,
        note_id=note_id,
    )


@router.get("/{note_id}/comments", response_model=List[CommentResponse])
async def get_comments_for_note(
    note_id: int,
    service: CommentService = Depends(get_comment_service),
    user: User = Depends(current_user),
):
    return await service.get_note_comments(
        user_id=user.id,
        note_id=note_id,
    )


@router.patch("/comment/{comment_id}", response_model=CommentResponse)
async def update_comment_for_note(
    comment_data: CommentUpdate,
    comment: Comment = Depends(comment_getter),
    service: CommentService = Depends(get_comment_service),
):
    return await service.update_comment(
        comment_data=comment_data,
        comment=comment,
    )


@router.delete("/comment/{comment_id}")
async def delete_comment_for_note(
    comment: Comment = Depends(comment_getter),
    service: CommentService = Depends(get_comment_service),
):
    return await service.delete_comment(
        comment=comment,
    )
