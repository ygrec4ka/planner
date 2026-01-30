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

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="tasks")
