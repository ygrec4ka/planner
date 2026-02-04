from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import User


class Comment(Base, IdIntPkMixin):
    content: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    commentable_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    commentable_id: Mapped[int] = mapped_column(
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
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="comments")
