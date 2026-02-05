from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, Note, Comment, User
from core.schemas.comment import CommentableType, CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_commentable_object(
    async def create_task_comment(
        self,
        comment_data: CommentCreate,
        user: User,
        task_id: int,
    ) -> Comment:
        task = await self.session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this task",
            )

        new_comment_for_task = Comment(
            **comment_data.model_dump(),
            user_id=user.id,
            commentable_type=CommentableType.TASK,
            commentable_id=task_id,
        )

        self.session.add(new_comment_for_task)
        await self.session.commit()
        await self.session.refresh(new_comment_for_task)

        return new_comment_for_task

        self,
        commentable_id: int,
        commentable_type: CommentableType,
    ) -> Optional[Task | Note]:
        if commentable_type == CommentableType.TASK:
            stmt = select(Task).where(Task.id == commentable_id)
        elif commentable_type == CommentableType.NOTE:
            stmt = select(Note).where(Note.id == commentable_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неизвестный тип объекта: {commentable_type}",
            )

        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_comment(self, comment_data: CommentCreate, user: User) -> Comment:
        await self._get_commentable_object(
            commentable_id=comment_data.commentable_id,
            commentable_type=comment_data.commentable_type,
        )

        new_comment = Comment(
            **comment_data.model_dump(),
            user_id=user.id,
        )

        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)

        return new_comment

    async def update_comment(
        self,
        comment_data: CommentUpdate,
        comment: Comment,
    ) -> Comment:
        update_data = comment_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(comment, key, value)

        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def delete_comment(
        self,
        comment: Comment,
    ) -> None:

        await self.session.delete(comment)
        await self.session.commit()
