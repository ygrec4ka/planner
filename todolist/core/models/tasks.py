# from datetime import datetime
# from enum import Enum
# from typing import TYPE_CHECKING
#
# from core.models.base import Base
# from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Enum as SAEnum
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func
#
# if TYPE_CHECKING:
#     from core.models import User
#     from core.models import Comment
#
#
# class TaskPriority(Enum):
#     UNSPECIFIED = "unspecified"
#     IMPORTANT_URGENT = "important_urgent"
#     IMPORTANT_NOT_URGENT = "important_not_urgent"
#     NOT_IMPORTANT_URGENT = "not_important_urgent"
#     NOT_IMPORTANT_NOT_URGENT = "not_important_not_urgent"
#
#
# class Task(Base):
#     __tablename__ = "tasks"
#
#     title: Mapped[str] = mapped_column(String(255), nullable=False)
#     description: Mapped[str | None] = mapped_column(Text, nullable=True)
#     is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
#     # Приоритеты
#     priority: Mapped[TaskPriority] = mapped_column(
#         SAEnum(TaskPriority),
#         default=TaskPriority.UNSPECIFIED,
#         nullable=False,
#     )
#
#     # Таймстемпы
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
#     )
#     # Связи
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     # Отношения
#     user: Mapped["User"] = relationship(back_populates="tasks")
#     comments: Mapped[list["Comment"]] = relationship(
#         back_populates="task", cascade="all, delete-orphan"
#     )
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from core.models.base import Base

from sqlalchemy import String, Text, func, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import User


class EisenhowerPriority(str, PyEnum):
    DO_FIRST = "do_first"  # 1. Срочные и важные
    SCHEDULE = "schedule"  # 2. Не срочные, но важные
    DELEGATE = "delegate"  # 3. Срочные, но не важные
    DONT_DO = "dont_do"  # 4. Не срочные и не важные


class Task(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)

    priority: Mapped[EisenhowerPriority] = mapped_column(
        SAEnum(EisenhowerPriority),
        default=EisenhowerPriority.SCHEDULE,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

