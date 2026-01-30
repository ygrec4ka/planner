from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class PriorityEnum(str, Enum):
    DO_FIRST = "do_first"  # Срочные важные
    SCHEDULE = "schedule"  # Не срочные важные
    DELEGATE = "delegate"  # Срочные не важные
    DONT_DO = "dont_do"  # Не срочные не важные


class TaskRead(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=255)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=255)
    priority: PriorityEnum = PriorityEnum.SCHEDULE


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    priority: Optional[PriorityEnum] = None


class TaskResponse(TaskRead):
    priority: PriorityEnum
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
