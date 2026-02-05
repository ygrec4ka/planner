from typing import List
from fastapi import APIRouter, Depends

from api.dependencies.comment.comment import comment_getter
from api.dependencies.services.service import get_task_service, get_comment_service
from api.dependencies.task.task import task_getter
from core.authentication.fastapi_users import current_user
from core.config import settings

from core.models import User, Task, Comment

from core.schemas.comment import CommentResponse, CommentCreate, CommentUpdate
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
    service: TaskService = Depends(get_task_service),
    user: User = Depends(current_user),
):
    return await service.create_task(
        task_data=task_data,
        user=user,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    user: User = Depends(current_user),
):
    return await service.get_task_by_id(
        task_id=task_id,
        user=user,
    )


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(
    service: TaskService = Depends(get_task_service),
    user: User = Depends(current_user),
):
    return await service.get_tasks(
        user=user,
    )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_data: TaskUpdate,
    task: Task = Depends(task_getter),
    service: TaskService = Depends(get_task_service),
):
    return await service.update_task(
        task=task,
        task_data=task_data,
    )


@router.delete("/{task_id}")
async def delete_task(
    task: Task = Depends(task_getter),
    service: TaskService = Depends(get_task_service),
):
    return await service.delete_task(
        task=task,
    )


@router.post("/{task_id}/comments", response_model=CommentResponse)
async def create_comment_for_task(
    task_id: int,
    comment_data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
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
    service: CommentService = Depends(get_comment_service),
    user: User = Depends(current_user),
):
    return await service.get_task_comments(
        user_id=user.id,
        task_id=task_id,
    )


@router.patch("/comment/{comment_id}", response_model=CommentResponse)
async def update_comment_for_task(
    comment_data: CommentUpdate,
    comment: Comment = Depends(comment_getter),
    service: CommentService = Depends(get_comment_service),
):
    return await service.update_comment(
        comment_data=comment_data,
        comment=comment,
    )


@router.delete("/comment/{comment_id}")
async def delete_comment_for_task(
    comment: Comment = Depends(comment_getter),
    service: CommentService = Depends(get_comment_service),
):
    return await service.delete_comment(
        comment=comment,
    )
