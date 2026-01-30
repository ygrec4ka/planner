from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NoteRead(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=255)


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=255)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None


class NoteResponse(NoteRead):
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
