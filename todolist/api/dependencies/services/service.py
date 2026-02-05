from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.comments import CommentService
from services.notes import NoteService
from services.tasks import TaskService


async def get_note_service(
    session: AsyncSession = Depends(
        db_helper.session_getter,
    ),
) -> NoteService:
    return NoteService(session)


async def get_task_service(
    session: AsyncSession = Depends(
        db_helper.session_getter,
    ),
) -> TaskService:
    return TaskService(session)


async def get_comment_service(
    session: AsyncSession = Depends(
        db_helper.session_getter,
    ),
) -> CommentService:
    return CommentService(session)
