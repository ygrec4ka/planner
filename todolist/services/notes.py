import logging
from fastapi import HTTPException, status
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Note
from core.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def create_note(
        self,
        note_data: NoteCreate,
        user: User,
    ) -> Note:
        self.logger.debug("Starting note creation for user: %s", user.id)

        new_note = Note(
            **note_data.model_dump(),
            user_id=user.id,
        )
        self.logger.debug("Note object created for user: %s", user.id)

        self.session.add(new_note)
        await self.session.commit()
        await self.session.refresh(new_note)
        self.logger.info(
            "Note created successfully! note %s for user %s",
            new_note.id,
            user.id,
        )

        return new_note

    async def get_note_by_id(
        self,
        note_id: int,
        user: User,
    ) -> Note:
        self.logger.debug(
            "Starting note getting by id: %s for user: %s",
            note_id,
            user.id,
        )
        note = await self.session.get(Note, note_id)
        if not note or note.user_id != user.id:
            self.logger.info(
                "No access or note: %s not found for user: %s",
                note_id,
                user.id,
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        self.logger.info(
            "Note: %s retrieved for user: %s",
            note.id,
            user.id,
        )
        return note

    async def get_notes(
        self,
        user: User,
    ) -> Sequence[Note]:
        self.logger.debug(
            "Starting notes list getting for user: %s",
            user.id,
        )

        stmt = select(Note).where(Note.user_id == user.id)
        result = await self.session.execute(stmt)
        self.logger.info(
            "Notes list retrieved for user: %s",
            user.id,
        )

        return result.scalars().all()

    async def update_note(
        self,
        note: Note,
        note_data: NoteUpdate,
    ) -> Note:
        self.logger.debug(
            "Starting note update for note: %s",
            note.id,
        )

        for key, value in note_data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)

        await self.session.commit()
        await self.session.refresh(note)
        self.logger.info(
            "Note: %s updated successfully!",
            note.id,
        )

        return note

    async def delete_note(
        self,
        note: Note,
    ) -> None:
        self.logger.debug(
            "Starting note deletion for note: %s",
            note.id,
        )

        await self.session.delete(note)
        await self.session.commit()
        self.logger.info(
            "Note: %s deleted successfully!",
            note.id,
        )
