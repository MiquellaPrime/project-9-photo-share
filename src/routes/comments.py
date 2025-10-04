from uuid import UUID
from typing import Annotated, AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.database import db_helper
from src.repository import comments as comments_repo
from src.repository import photos as photos_repo
from src.schemas import (
    CommentCreateDto, 
    CommentDto, 
    CommentUpdateDto,
    PaginationParams,
    PaginatedResponse
)

router = APIRouter(prefix="/comments", tags=["comments"])

async def get_current_user_id() -> UUID:
    """Temporary function to get current user ID. Replace with actual auth."""
    from uuid import uuid4
    return uuid4()  # Mock UUID for now  


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async for session in db_helper.session_getter():
        yield session


@router.post(
    "/photo/{photo_uuid}", 
    response_model=CommentDto, 
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Comment created successfully"},
        400: {"description": "Bad request - Invalid data or mismatched photo UUID"},
        401: {"description": "Unauthorized - Invalid or missing user authentication"},
        404: {"description": "Photo not found"},
        500: {"description": "Internal server error"}
    }
)
async def create_comment(
    photo_uuid: UUID,
    body: CommentCreateDto,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> CommentDto:
    """Create a comment under a photo."""
    if body.photo_uuid != photo_uuid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Photo UUID in body must match the path parameter"
        )
    
    try:
        # Check if photo exists before creating comment
        photo = await photos_repo.get_photo_by_uuid(session, photo_uuid)
        if photo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )
        
        comment = await comments_repo.create_comment(session, body, current_user_id)
        return CommentDto.model_validate(comment)
        
    except IntegrityError as e:
        await session.rollback()
        if "foreign key constraint" in str(e).lower():
            if "photo_uuid" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Photo not found"
                )
            elif "user_id" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or unauthorized"
                )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data provided"
        )
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@router.get(
    "/photo/{photo_uuid}", 
    response_model=PaginatedResponse[CommentDto],
    responses={
        200: {"description": "Comments retrieved successfully"},
        404: {"description": "Photo not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_comments_by_photo(
    photo_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
) -> PaginatedResponse[CommentDto]:
    """Get comments for a photo with pagination. Sorted by created_at ASC."""
    try:
        photo = await photos_repo.get_photo_by_uuid(session, photo_uuid)
        if photo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )
        
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
        
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@router.get(
    "/comment/{comment_uuid}", 
    response_model=CommentDto,
    responses={
        200: {"description": "Comment retrieved successfully"},
        404: {"description": "Comment not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_comment_by_uuid(
    comment_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CommentDto:
    """Get a comment by its UUID."""
    try:
        comment = await comments_repo.get_comment_by_uuid(session, comment_uuid)
        
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        return CommentDto.model_validate(comment)
        
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@router.put(
    "/comment/{comment_uuid}", 
    response_model=CommentDto,
    responses={
        200: {"description": "Comment updated successfully"},
        400: {"description": "Bad request - Invalid comment data"},
        403: {"description": "Forbidden - Can only edit own comments"},
        404: {"description": "Comment not found"},
        500: {"description": "Internal server error"}
    }
)
async def update_comment(
    comment_uuid: UUID,
    body: CommentUpdateDto,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> CommentDto:
    """Update a comment's text."""
    try:
        # Check if comment exists and user owns it
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
        
        # Update the comment using ORM style (reuse existing comment object)
        updated_comment = await comments_repo.update_comment(session, existing_comment, body)
        
        return CommentDto.model_validate(updated_comment)
        
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid comment data"
        )
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@router.delete(
    "/comment/{comment_uuid}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Comment deleted successfully"},
        403: {"description": "Forbidden - Can only delete own comments"},
        404: {"description": "Comment not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_comment(
    comment_uuid: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> None:
    """Delete a comment by its UUID."""
    try:
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
        
        # Delete using ORM style (reuse existing comment object)
        await comments_repo.delete_comment(session, existing_comment)
            
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )