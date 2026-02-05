from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Comment


async def comment_getter(
    comment_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Comment:
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return comment
