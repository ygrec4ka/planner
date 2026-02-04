from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user.id,
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

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
        update_data = task_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(
        self,
        task: Task,
    ) -> None:

        await self.session.delete(task)
        await self.session.commit()
