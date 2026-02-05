from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Note, db_helper


async def note_getter(
    note_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Note:
    note = await session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note
