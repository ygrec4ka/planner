from fastapi import HTTPException, status
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from core.models import User, Task
from core.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(
        self,
        task_data: TaskCreate,
        user: User,
    ) -> Task:
        new_task = Task(
            **task_data.model_dump(),
            user_id=user.id,
        )

        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)

        return new_task

    async def get_task_by_id(
        self,
        task_id: int,
        user: User,
    ) -> Task | None:
        task = await self.session.get(Task, task_id)
        if not task or task.user_id != user.id:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Note not found",
            )
        return task

    async def get_tasks(
        self,
        user: User,
    ) -> Sequence[Task]:
        stmt = select(Task).where(Task.user_id == user.id)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def update_task(
        self,
        task: Task,
        task_data: TaskUpdate,
    ) -> Task:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task_data, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(
        self,
        task: Task,
    ) -> None:

        await self.session.delete(task)
        await self.session.commit()
