from uuid import UUID
from typing import Annotated, AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.repository import comments as comments_repo
from src.schemas import (
    CommentCreateDto, 
    CommentDto, 
    CommentUpdateDto,
    PaginationParams,
    PaginatedResponse
)

router = APIRouter(prefix="/comments", tags=["comments"])

async def get_current_user_id() -> int:
    """Temporary function to get current user ID. Replace with actual auth."""
    return 1  


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async for session in db_helper.session_getter():
        yield session


@router.post("/photo/{photo_uuid}", response_model=CommentDto, status_code=status.HTTP_201_CREATED)
async def create_comment(
    photo_uuid: UUID,
    body: CommentCreateDto,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CommentDto:
    """Create a comment under a photo."""
    if body.photo_uuid != photo_uuid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Photo UUID in body must match the path parameter"
        )
    
    comment = await comments_repo.create_comment(session, body, current_user_id)
    return CommentDto.model_validate(comment)


@router.get("/photo/{photo_uuid}", response_model=PaginatedResponse[CommentDto])
async def get_comments_by_photo(
    photo_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
) -> PaginatedResponse[CommentDto]:
    """Get comments for a photo with pagination. Sorted by created_at ASC."""
    comments = await comments_repo.get_comments_by_photo(
        session, photo_uuid, offset, limit
    )
    
    total = await comments_repo.count_comments_by_photo(session, photo_uuid)
    
    comment_dtos = [CommentDto.model_validate(comment) for comment in comments]
    
    return PaginatedResponse[CommentDto](
        items=comment_dtos,
        total=total,
        offset=offset,
        limit=limit,
        has_next=offset + limit < total
    )


@router.get("/comment/{comment_uuid}", response_model=CommentDto)
async def get_comment_by_uuid(
    comment_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CommentDto:
    """Get a comment by its UUID."""
    comment = await comments_repo.get_comment_by_uuid(session, comment_uuid)
    
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    return CommentDto.model_validate(comment)


@router.put("/comment/{comment_uuid}", response_model=CommentDto)
async def update_comment(
    comment_uuid: UUID,
    body: CommentUpdateDto,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CommentDto:
    """Update a comment's text."""
    existing_comment = await comments_repo.get_comment_by_uuid(session, comment_uuid)
    
    if existing_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if existing_comment.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments"
        )
    
    updated_comment = await comments_repo.update_comment(session, comment_uuid, body)
    
    if updated_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    return CommentDto.model_validate(updated_comment)


@router.delete("/comment/{comment_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    """Delete a comment by its UUID."""
    existing_comment = await comments_repo.get_comment_by_uuid(session, comment_uuid)
    
    if existing_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if existing_comment.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )
    
    deleted = await comments_repo.delete_comment(session, comment_uuid)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )