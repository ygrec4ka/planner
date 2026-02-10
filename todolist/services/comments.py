import logging

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, Note, Comment, User
from core.schemas.comment import CommentableType, CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def create_task_comment(
        self,
        comment_data: CommentCreate,
        user: User,
        task_id: int,
    ) -> Comment:
        self.logger.debug(
            "Starting task comment creation for user: %s, task: %s",
            user.id,
            task_id,
        )

        task = await self.session.get(Task, task_id)
        if not task:
            self.logger.warning(
                "Task not found for comment creation: task_id: %s, user_id: %s",
                task_id,
                user.id,
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.user_id != user.id:
            self.logger.warning(
                "Access denied for comment creation: task_id: %s, user_id: %s",
                task_id,
                user.id,
            )

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
        self.logger.debug("Task comment object created")

        self.session.add(new_comment_for_task)
        await self.session.commit()
        await self.session.refresh(new_comment_for_task)
        self.logger.info(
            "Task comment created successfully! comment_id: %s, task_id: %s, user_id: %s",
            new_comment_for_task.id,
            task_id,
            user.id,
        )

        return new_comment_for_task

    async def create_note_comment(
        self,
        comment_data: CommentCreate,
        user: User,
        note_id: int,
    ) -> Comment:
        self.logger.debug(
            "Starting note comment creation for user: %s, note: %s",
            user.id,
            note_id,
        )

        note = await self.session.get(Note, note_id)
        if not note:
            self.logger.warning(
                "Note not found for comment creation: note_id: %s, user_id: %s",
                note_id,
                user.id,
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        if note.user_id != user.id:
            self.logger.warning(
                "Access denied for comment creation: note_id: %s, user_id: %s",
                note_id,
                user.id,
            )

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
        self.logger.debug("Note comment object created")

        self.session.add(new_comment_for_note)
        await self.session.commit()
        await self.session.refresh(new_comment_for_note)
        self.logger.info(
            "Note comment created successfully! comment_id: %s, note_id: %s, user_id: %s",
            new_comment_for_note.id,
            note_id,
            user.id,
        )

        return new_comment_for_note

    async def get_task_comments(
        self,
        task_id: int,
        user_id: int,
    ) -> List[Comment]:
        self.logger.debug(
            "Starting task comments retrieval for task: %s, user: %s",
            task_id,
            user_id,
        )

        task = await self.session.get(Task, task_id)
        if not task or task.user_id != user_id:
            self.logger.info(
                "No access or task not found for comments: task_id: %s, user_id: %s",
                task_id,
                user_id,
            )
            return []

        stmt = (
            select(Comment)
            .where(
                Comment.user_id == user_id,
                Comment.commentable_type == CommentableType.TASK,
                Comment.commentable_id == task_id,
            )
            .order_by(Comment.created_at.asc())
        )

        result: Result = await self.session.execute(stmt)
        comments = list(result.scalars().all())
        self.logger.info(
            "Task comments retrieved successfully! task_id: %s, user_id: %s, count: %s",
            task_id,
            user_id,
            len(comments),
        )

        return comments

    async def get_note_comments(
        self,
        note_id: int,
        user_id: int,
    ) -> List[Comment]:
        self.logger.debug(
            "Starting note comments retrieval for note: %s, user: %s",
            note_id,
            user_id,
        )

        note = await self.session.get(Note, note_id)
        if not note or note.user_id != user_id:
            self.logger.info(
                "No access or note not found for comments: note_id: %s, user_id: %s",
                note_id,
                user_id,
            )
            return []

        stmt = (
            select(Comment)
            .where(
                Comment.user_id == user_id,
                Comment.commentable_type == CommentableType.NOTE,
                Comment.commentable_id == note_id,
            )
            .order_by(Comment.created_at.asc())
        )

        result: Result = await self.session.execute(stmt)
        comments = list(result.scalars().all())
        self.logger.info(
            "Note comments retrieved successfully! note_id: %s, user_id: %s, count: s",
            note_id,
            user_id,
            len(comments),
        )

        return comments

    async def update_comment(
        self,
        comment_data: CommentUpdate,
        comment: Comment,
    ) -> Comment:
        self.logger.debug(
            "Starting comment update for comment: %s",
            comment.id,
        )

        for key, value in comment_data.model_dump(exclude_unset=True).items():
            setattr(comment, key, value)

        await self.session.commit()
        await self.session.refresh(comment)
        self.logger.info(
            "Comment updated successfully! comment_id: %s",
            comment.id,
        )

        return comment

    async def delete_comment(
        self,
        comment: Comment,
    ) -> None:
        self.logger.debug(
            "Starting comment deletion for comment: %s",
            comment.id,
        )

        await self.session.delete(comment)
        await self.session.commit()
        self.logger.info(
            "Comment deleted successfully! comment_id: %s",
            comment.id,
        )
