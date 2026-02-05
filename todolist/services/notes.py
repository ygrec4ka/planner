from fastapi import HTTPException, status
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from core.models import User, Note
from core.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_note(
        self,
        note_data: NoteCreate,
        user: User,
    ) -> Note:
        new_note = Note(
            **note_data.model_dump(),
            user_id=user.id,
        )

        self.session.add(new_note)
        await self.session.commit()
        await self.session.refresh(new_note)

        return new_note

    async def get_note_by_id(
        self,
        note_id: int,
        user: User,
    ) -> Note:
        note = await self.session.get(Note, note_id)
        if not note or note.user_id != user.id:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Note not found",
            )
        return note

    async def get_notes(
        self,
        user: User,
    ) -> Sequence[Note]:
        stmt = select(Note).where(Note.user_id == user.id)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def update_note(
        self,
        note: Note,
        note_data: NoteUpdate,
    ) -> Note:
        for key, value in note_data.model_dump(exclude_unset=True).items():
            setattr(note_data, key, value)

        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def delete_note(
        self,
        note: Note,
    ) -> None:
        await self.session.delete(note)
        await self.session.commit()
