# from datetime import datetime
# from enum import Enum
# from typing import Optional
#
# from core.models import Note
# from pydantic import BaseModel, Field, ConfigDict
#
#
# class NoteSortField(str, Enum):
#     CREATED_AT = "created_at"
#     UPDATED_AT = "updated_at"
#     IS_IMPORTANT = "is_important"
#
#
# class SortOrder(str, Enum):
#     ASC = "asc"
#     DESC = "desc"
#
#
# class NoteCreate(BaseModel):
#     content: str = Field(..., min_length=1)
#     is_important: bool = False
#
#
# class NoteUpdate(BaseModel):
#     content: Optional[str] = Field(None, min_length=1)
#     is_important: Optional[bool] = None
#
#
# class NoteResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: int
#     content: str
#     is_important: bool = False
#     created_at: datetime
#     updated_at: datetime
#
#
# class NoteFilter(BaseModel):
#     is_important: Optional[bool] = None
#     sort_by: NoteSortField = NoteSortField.CREATED_AT
#     sort_order: SortOrder = SortOrder.DESC
#
#     @property
#     def sort_column(self):
#         """Возвращает колонку для сортировки"""
#         sort_columns = {
#             NoteSortField.CREATED_AT: Note.created_at,
#             NoteSortField.UPDATED_AT: Note.updated_at,
#             NoteSortField.IS_IMPORTANT: Note.is_important,
#         }
#         return sort_columns.get(self.sort_by, Note.created_at)
