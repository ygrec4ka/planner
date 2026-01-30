from datetime import datetime
from typing import TYPE_CHECKING

from core.models.base import Base

from sqlalchemy import Text, func, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import User


class Note(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)

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
    user: Mapped["User"] = relationship(back_populates="notes")
