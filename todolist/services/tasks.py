# from typing import Sequence
#
# from core.exceptions import ValidationException
# from core.exceptions.tasks import (
#     TaskNotFoundException,
#     TaskAccessDeniedException,
# )
# from core.models import User
# from core.models.tasks import Task
# from core.schemas.task import (
#     TaskCreate,
#     TaskUpdate,
#     TaskFilter,
#     SortOrder,
# )
# from sqlalchemy import select, Result, asc, desc
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
#
#
# class TaskServices:
#     @staticmethod
#     async def create_task(
#         task_create: TaskCreate,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Task:
#         try:
#             # Создаем новую задачу с данными из запроса и ID текущего пользователя
#             task = Task(
#                 **task_create.model_dump(),
#                 user_id=current_user.id,
#             )
#
#             # Сохраняем задачу в базе данных
#             session.add(task)
#             await session.commit()
#             await session.refresh(task)
#             return task
#
#         except Exception:
#             # В случае ошибки откатываем транзакцию и возвращаем сообщение
#             await session.rollback()
#             raise ValidationException("Task creation failed. Please try again")
#
#     @staticmethod
#     async def get_task(
#         task_id: int,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Task:
#         try:
#             # Получаем задачу по ID вместе с комментариями
#             stmt = (
#                 select(Task)
#                 .options(selectinload(Task.comments))
#                 .where(Task.id == task_id)
#             )
#             result: Result = await session.execute(stmt)
#             task = result.scalar_one_or_none()
#
#             # Проверяем существование задачи
#             if not task:
#                 raise TaskNotFoundException()
#
#             # Проверяем права доступа к задаче
#             if task.user_id != current_user.id:
#                 raise TaskAccessDeniedException()
#
#             return task
#
#         except (TaskNotFoundException, TaskAccessDeniedException):
#             raise
#         except Exception:
#             # Ловим все остальные ошибки и возвращаем общее сообщение
#             raise ValidationException("Failed to retrieve task")
#
#     @staticmethod
#     async def get_all_tasks(
#         session: AsyncSession,
#         current_user: User,
#         filters: TaskFilter,
#     ) -> Sequence[Task]:
#         try:
#             # Получаем все tasks текущего пользователя
#             stmt = select(Task).where(Task.user_id == current_user.id)
#
#             # Фильтрация по приоритету
#             if filters.priority:
#                 stmt = stmt.where(Task.priority == filters.priority)
#
#             # Фильтрация по статусу выполнения
#             if filters.is_completed is not None:
#                 stmt = stmt.where(Task.is_completed == filters.is_completed)
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
#             raise ValidationException("Failed to retrieve tasks")
#
#     @staticmethod
#     async def update_task(
#         task_id: int,
#         data: TaskUpdate,
#         session: AsyncSession,
#         current_user: User,
#     ) -> Task:
#         try:
#             # Получаем задачу и проверяем права доступа
#             task = await TaskServices.get_task(task_id, session, current_user)
#
#             # Обновляем только переданные поля
#             for key, value in data.model_dump(exclude_unset=True).items():
#                 setattr(task, key, value)
#
#             # Сохраняем изменения в базе данных
#             await session.commit()
#             await session.refresh(task)
#             return task
#
#         except (TaskNotFoundException, TaskAccessDeniedException):
#             # Откатываем транзакцию и пробрасываем исключение
#             await session.rollback()
#             raise
#         except Exception:
#             # Откатываем транзакцию и возвращаем общее сообщение об ошибке
#             await session.rollback()
#             raise ValidationException("Failed to update task")
#
#     @staticmethod
#     async def delete_task(
#         task_id: int,
#         session: AsyncSession,
#         current_user: User,
#     ) -> None:
#         try:
#             # Получаем задачу и проверяем права доступа
#             task = await TaskServices.get_task(task_id, session, current_user)
#
#             # Удаляем задачу из базы данных
#             await session.delete(task)
#             await session.commit()
#
#         except (TaskNotFoundException, TaskAccessDeniedException):
#             # Откатываем транзакцию и пробрасываем исключение
#             await session.rollback()
#             raise
#         except Exception:
#             # Откатываем транзакцию и возвращаем общее сообщение об ошибке
#             await session.rollback()
#             raise ValidationException("Failed to delete task")
#
#
# task_services = TaskServices()
