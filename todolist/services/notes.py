# from typing import Sequence
#
# from core.exceptions import ValidationException
# from core.exceptions.notes import (
#     NoteNotFoundException,
#     NoteAccessDeniedException,
# )
# from core.models import User
# from core.models.notes import Note
# from core.schemas.note import NoteCreate, NoteUpdate, NoteFilter, SortOrder
# from sqlalchemy import select, Result, asc, desc
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
#
#
# class NoteServices:
#     @staticmethod
#     async def create_note(
#         note_create: NoteCreate,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Note:
#         try:
#             # Создаем новую заметку с данными из запроса и ID текущего пользователя
#             note = Note(
#                 **note_create.model_dump(),
#                 user_id=current_user.id,
#             )
#
#             # Сохраняем заметку в базе данных
#             session.add(note)
#             await session.commit()
#             await session.refresh(note)
#             return note
#
#         except Exception:
#             # В случае ошибки откатываем транзакцию и возвращаем сообщение
#             await session.rollback()
#             raise ValidationException("Note creation failed. Please try again")
#
#     @staticmethod
#     async def get_note(
#         note_id: int,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Note:
#         try:
#             # Получаем заметку по ID вместе с комментариями
#             stmt = (
#                 select(Note)
#                 .options(selectinload(Note.comments))
#                 .where(Note.id == note_id)
#             )
#             result: Result = await session.execute(stmt)
#             note = result.scalar_one_or_none()
#
#             # Проверяем существование заметки
#             if not note:
#                 raise NoteNotFoundException()
#
#             # Проверяем права доступа к заметке
#             if note.user_id != current_user.id:
#                 raise NoteAccessDeniedException()
#
#             return note
#
#         except (NoteNotFoundException, NoteAccessDeniedException):
#             raise
#         except Exception:
#             # Ловим все остальные ошибки и возвращаем общее сообщение
#             raise ValidationException("Failed to retrieve note")
#
#     @staticmethod
#     async def get_all_notes(
#         session: AsyncSession,
#         current_user: User,
#         filters: NoteFilter,
#     ) -> Sequence[Note]:
#         try:
#             # Получаем все заметки текущего пользователя
#             stmt = select(Note).where(Note.user_id == current_user.id)
#
#             # Фильтр по важности
#             if filters.is_important is not None:
#                 stmt = stmt.where(Note.is_important == filters.is_important)
#
#             # Сортировка
#             sort_column = filters.sort_column
#
#             if filters.sort_order == SortOrder.ASC:
#                 stmt = stmt.order_by(asc(sort_column))
#             else:
#                 stmt = stmt.order_by(desc(sort_column))
#
#             result: Result = await session.execute(stmt)
#             return result.scalars().all()
#
#         except Exception:
#             # Ловим все ошибки и возвращаем общее сообщение
#             raise ValidationException("Failed to retrieve notes")
#
#     @staticmethod
#     async def update_note(
#         note_id: int,
#         data: NoteUpdate,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Note:
#         try:
#             # Получаем заметку и проверяем права доступа
#             note = await NoteServices.get_note(note_id, session, current_user)
#
#             # Обновляем только переданные поля
#             for key, value in data.model_dump(exclude_unset=True).items():
#                 setattr(note, key, value)
#
#             # Сохраняем изменения в базе данных
#             await session.commit()
#             await session.refresh(note)
#             return note
#
#         except (NoteNotFoundException, NoteAccessDeniedException):
#             # Откатываем транзакцию и пробрасываем исключение
#             await session.rollback()
#             raise
#         except Exception:
#             # Откатываем транзакцию и возвращаем общее сообщение об ошибке
#             await session.rollback()
#             raise ValidationException("Failed to update note")
#
#     @staticmethod
#     async def delete_note(
#         note_id: int,
#         session: AsyncSession,
#         current_user: User,
#     ) -> None:
#         try:
#             # Получаем заметку и проверяем права доступа
#             note = await NoteServices.get_note(note_id, session, current_user)
#
#             # Удаляем заметку из базы данных
#             await session.delete(note)
#             await session.commit()
#
#         except (NoteNotFoundException, NoteAccessDeniedException):
#             # Откатываем транзакцию и пробрасываем исключение
#             await session.rollback()
#             raise
#         except Exception:
#             # Откатываем транзакцию и возвращаем общее сообщение об ошибке
#             await session.rollback()
#             raise ValidationException("Failed to delete note")
#
#
# note_services = NoteServices()
