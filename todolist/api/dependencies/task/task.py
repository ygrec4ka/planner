from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, db_helper


async def task_getter(
    task_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Task:
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task
