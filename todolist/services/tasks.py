import logging
from fastapi import HTTPException, status
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Task
from core.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def create_task(
        self,
        task_data: TaskCreate,
        user: User,
    ) -> Task:
        self.logger.debug(
            "Starting task creation for user: %s",
            user.id,
        )

        new_task = Task(
            **task_data.model_dump(),
            user_id=user.id,
        )
        self.logger.debug(
            "Task created %s",
            new_task.id,
        )

        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        self.logger.info(
            "Task created successfully! task %s for user: %s",
            new_task.id,
            user.id,
        )

        return new_task

    async def get_task_by_id(
        self,
        task_id: int,
        user: User,
    ) -> Task:
        self.logger.debug(
            "Starting task getting by id: %s for user: %s",
            task_id,
            user.id,
        )

        task = await self.session.get(Task, task_id)

        if not task or task.user_id != user.id:
            self.logger.info(
                "No access or task: %s not found for user: %s",
                task_id,
                user.id,
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        self.logger.info(
            "Task: %s retrieved for user: %s",
            task.id,
            user.id,
        )
        return task

    async def get_tasks(
        self,
        user: User,
    ) -> Sequence[Task]:
        self.logger.debug(
            "Starting tasks list getting for user: %s",
            user.id,
        )

        stmt = select(Task).where(Task.user_id == user.id)
        result = await self.session.execute(stmt)
        tasks = result.scalars().all()

        self.logger.info(
            "Tasks list retrieved: user_id: %s, count: %s",
            user.id,
            len(tasks),
        )
        return tasks

    async def update_task(
        self,
        task: Task,
        task_data: TaskUpdate,
    ) -> Task:
        self.logger.debug(
            "Starting task update for task: %s",
            task.id,
        )

        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        self.logger.info(
            "Task: %s updated successfully!",
            task.id,
        )

        return task

    async def delete_task(
        self,
        task: Task,
    ) -> None:
        self.logger.debug(
            "Starting task deletion for task: %s",
            task.id,
        )

        await self.session.delete(task)
        await self.session.commit()
        self.logger.info(
            "Task: %s deleted successfully!",
            task.id,
        )
