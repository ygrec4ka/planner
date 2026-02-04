from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> Note | None:
        stmt = select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id,
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

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
        update_data = note_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(note, key, value)

        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def delete_note(
        self,
        note: Note,
    ) -> None:
        await self.session.delete(note)
        await self.session.commit()
