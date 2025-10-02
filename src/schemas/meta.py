from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    status: str


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of items to return")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    offset: int
    limit: int
    has_next: bool


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str
    error_code: str | None = None
    timestamp: str | None = None
