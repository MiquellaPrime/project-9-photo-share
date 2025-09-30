from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper
from src.core.models import UserOrm
from src.services import TokenService, user_is_active

offset_param = Annotated[int, Query(ge=0)]
limit_param = Annotated[int, Query(gt=0, le=20)]

db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]

token_service_dependency = Annotated[TokenService, Depends(TokenService)]

user_dependency = Annotated[UserOrm, Depends(user_is_active)]
