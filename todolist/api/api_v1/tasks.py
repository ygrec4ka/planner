# from core.config import settings
# from api.dependencies.users import get_current_user
# from core.models import User
# from core.models.db_helper import db_helper
# from core.schemas.task import (
#     TaskResponse,
#     TaskCreate,
#     TaskUpdate,
#     TaskFilter,
# )
# from services.tasks import task_services
# from fastapi import APIRouter
# from fastapi.params import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# router = APIRouter(prefix=settings.api.v1.tasks, tags=["Tasks"])
#
#
# @router.post("/", response_model=TaskResponse)
# async def create_task(
#     task_create: TaskCreate,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(get_current_user),
# ):
#     # Создаем task
#     task = await task_services.create_task(
#         task_create=task_create,
#         session=session,
#         current_user=current_user,
#     )
#
#     return task
#
#
# @router.get("/{task_id}", response_model=TaskResponse)
# async def get_task(
#     task_id: int,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(get_current_user),
# ):
#     # Получаем конкретную task
#     task = await task_services.get_task(
#         task_id=task_id,
#         session=session,
#         current_user=current_user,
#     )
#
#     return task
#
#
# @router.get("/", response_model=list[TaskResponse])
# async def get_all_tasks(
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(get_current_user),
#     filters: TaskFilter = Depends(),
# ):
#     # Получаем все user_tasks
#     tasks = await task_services.get_all_tasks(
#         session=session,
#         current_user=current_user,
#         filters=filters,
#     )
#
#     return tasks
#
#
# @router.put("/{task_id}", response_model=TaskResponse)
# async def update_task(
#     task_id: int,
#     task_update: TaskUpdate,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(get_current_user),
# ):
#     # Обновляем task
#     task = await task_services.update_task(
#         task_id=task_id,
#         data=task_update,
#         session=session,
#         current_user=current_user,
#     )
#
#     return task
#
#
# @router.delete("/{task_id}")
# async def delete_task(
#     task_id: int,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     current_user: User = Depends(get_current_user),
# ):
#     # Удаляем task
#     await task_services.delete_task(
#         task_id=task_id,
#         session=session,
#         current_user=current_user,
#     )
#
#     return {"message": "Task deleted successfully"}

from api.dependencies.task.task import task_getter
from core.authentication.fastapi_users import current_user
from core.config import settings

from core.models import User, Task

from core.schemas.comment import CommentResponse, CommentCreate
from core.schemas.task import TaskResponse, TaskCreate, TaskUpdate

from services.comments import CommentService
from services.tasks import TaskService

router = APIRouter(
    prefix=settings.api.v1.tasks,
    tags=["Tasks"],
)


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(TaskService),
    user: User = Depends(current_user),
):
    return await service.create_task(
        task_data=task_data,
        user=user,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(TaskService),
    user: User = Depends(current_user),
):
    return await service.get_task_by_id(
        task_id=task_id,
        user=user,
    )


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(
    service: TaskService = Depends(TaskService),
    user: User = Depends(current_user),
):
    return await service.get_tasks(
        user=user,
    )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_data: TaskUpdate,
    task: Task = Depends(task_getter),
    service: TaskService = Depends(TaskService),
):
    return await service.update_task(
        task=task,
        task_data=task_data,
    )


@router.delete("/{task_id}")
async def delete_task(
    task: Task = Depends(task_getter),
    service: TaskService = Depends(TaskService),
):
    return await service.delete_task(
        task=task,
    )


@router.post("/{task_id}/comments", response_model=CommentResponse)
async def create_comment_for_task(
    task_id: int,
    comment_data: CommentCreate,
    service: CommentService = Depends(CommentService),
    user: User = Depends(current_user),
):
    return await service.create_task_comment(
        comment_data=comment_data,
        user=user,
        task_id=task_id,
    )


@router.get("/{task_id}/comments", response_model=List[CommentResponse])
async def get_comments_for_task(
    task_id: int,
    service: CommentService = Depends(CommentService),
    user: User = Depends(current_user),
):
    return await service.get_task_comments(
        user_id=user.id,
        task_id=task_id,
    )
