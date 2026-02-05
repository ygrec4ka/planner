from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class CommentableType(str, Enum):
    TASK = "task"
    NOTE = "note"


class CommentBase(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=3000,
    )


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=1,
        max_length=3000,
    )


class CommentRead(BaseModel):
    id: int
    commentable_type: str
    commentable_id: int


class CommentResponse(CommentRead):
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
