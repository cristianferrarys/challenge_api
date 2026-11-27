from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_user_service,
    get_current_user,
)

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

from app.services.user_service import UserService




router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

ServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

UserDep = Annotated[
    User,
    Depends(get_current_user),
]

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    service: ServiceDep,
):
    return await service.create(data)

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_user(auth_user: UserDep):
    return auth_user


@router.patch(
    "/me",
    response_model=UserResponse,
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: ServiceDep,
):
    return await service.update(user_id, data)

