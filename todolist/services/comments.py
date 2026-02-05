from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, Note, Comment, User
from core.schemas.comment import CommentableType, CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def create_note_comment(
        self,
        comment_data: CommentCreate,
        user: User,
        note_id: int,
    ) -> Comment:
        note = await self.session.get(Note, note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        if note.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this note",
            )

        new_comment_for_note = Comment(
            **comment_data.model_dump(),
            user_id=user.id,
            commentable_type=CommentableType.NOTE,
            commentable_id=note_id,
        )

        self.session.add(new_comment_for_note)
        await self.session.commit()
        await self.session.refresh(new_comment_for_note)

        return new_comment_for_note

    async def get_task_comments(
        self,
        task_id: int,
        user_id: int,
    ) -> List[Comment]:
        task = await self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return []

        stmt = (
            select(Comment)
            .where(
                Comment.user_id == user_id,
                Comment.commentable_type == CommentableType.TASK,
            )
            .order_by(Comment.created_at.asc())
        )

        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())

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
