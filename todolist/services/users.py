# from core.exceptions import ValidationException
# from core.models import User
# from core.schemas.user import UserUpdate
# from sqlalchemy import select, Result
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# class UserService:
#     @staticmethod
#     async def get_user(
#         user_id: int,
#         session: AsyncSession,
#     ) -> User | None:
#         try:
#             # Получаем пользователя по ID из базы данных
#             stmt = select(User).where(User.id == user_id)
#             result: Result = await session.execute(stmt)
#             user = result.scalar_one_or_none()
#
#             # Возвращаем пользователя или None если не найден
#             return user
#
#         except Exception:
#             raise ValidationException("Failed to retrieve user")
#
#     @staticmethod
#     async def update_user_profile(
#         current_user: User,
#         data: UserUpdate,
#         session: AsyncSession,
#     ) -> User:
#         try:
#             # Обновляем только переданные поля профиля пользователя
#             for key, value in data.model_dump(exclude_unset=True).items():
#                 setattr(current_user, key, value)
#
#             # Сохраняем изменения в базе данных
#             await session.commit()
#             await session.refresh(current_user)
#             return current_user
#
#         except Exception:
#             # В случае ошибки откатываем транзакцию и возвращаем сообщение
#             await session.rollback()
#             raise ValidationException("Failed to update user profile")
#
#     @staticmethod
#     async def delete_user_account(
#         current_user: User,
#         session: AsyncSession,
#     ) -> None:
#         try:
#             # Удаляем пользователя из базы данных
#             await session.delete(current_user)
#             await session.commit()
#
#         except Exception:
#             # В случае ошибки откатываем транзакцию и возвращаем сообщение
#             await session.rollback()
#             raise ValidationException("Failed to delete user account")
#
#
# user_services = UserService()
