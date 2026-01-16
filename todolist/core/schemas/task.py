# from datetime import datetime
# from enum import Enum
# from typing import Optional
#
# from core.models import Task
# from core.models.tasks import TaskPriority
# from pydantic import BaseModel, Field, ConfigDict
#
#
# class TaskSortField(str, Enum):
#     CREATED_AT = "created_at"
#     UPDATED_AT = "updated_at"
#     TITLE = "title"
#     PRIORITY = "priority"
#
#
# class SortOrder(str, Enum):
#     ASC = "asc"
#     DESC = "desc"
#
#
# class TaskCreate(BaseModel):
#     title: str = Field(..., min_length=1, max_length=255)
#     description: Optional[str] = Field(None, max_length=1000)
#     priority: TaskPriority = TaskPriority.UNSPECIFIED
#
#
# class TaskUpdate(BaseModel):
#     title: Optional[str] = Field(None, min_length=1, max_length=255)
#     description: Optional[str] = Field(None, max_length=1000)
#     is_completed: Optional[bool] = None
#     priority: Optional[TaskPriority] = None
#
#
# class TaskResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: int
#     title: str
#     description: Optional[str] = None
#     is_completed: bool = False
#     priority: TaskPriority
#     created_at: datetime
#     updated_at: datetime
#
#
# class TaskFilter(BaseModel):
#     priority: Optional[TaskPriority] = None
#     is_completed: Optional[bool] = None
#     sort_by: TaskSortField = TaskSortField.CREATED_AT
#     sort_order: SortOrder = SortOrder.DESC
#
#     @property
#     def sort_column(self):  # Окно - сортировка: sorty_by:
#         """Возвращает колонку для сортировки"""
#         sort_columns = {
#             TaskSortField.CREATED_AT: Task.created_at,
#             TaskSortField.UPDATED_AT: Task.updated_at,
#             TaskSortField.TITLE: Task.title,
#             TaskSortField.PRIORITY: self.priority_weight,
#         }
#
#         return sort_columns.get(self.sort_by, Task.created_at)
#
#     @property
#     def priority_weight(self):
#         """Возвращает case выражение для сортировки по приоритету"""
#         from sqlalchemy import case
#
#         return case(
#             {
#                 TaskPriority.IMPORTANT_URGENT: 4,
#                 TaskPriority.IMPORTANT_NOT_URGENT: 3,
#                 TaskPriority.NOT_IMPORTANT_URGENT: 2,
#                 TaskPriority.NOT_IMPORTANT_NOT_URGENT: 1,
#                 TaskPriority.UNSPECIFIED: 0,
#             },
#             value=Task.priority,
#         )
