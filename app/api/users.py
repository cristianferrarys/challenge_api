from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import get_user_service
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,

)
from app.services.user_service import UserService
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

ServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
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
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(get_current_user)],
)
async def list_users(service: ServiceDep):
    return await service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user)],
)
async def get_user(
    user_id: UUID,
    service: ServiceDep,
):
    return await service.get_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user)],
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: ServiceDep,
):
    return await service.update(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: UUID,
    service: ServiceDep,
):
    await service.delete(user_id)