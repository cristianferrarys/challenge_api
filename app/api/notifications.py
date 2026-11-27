from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import (get_noti_service,get_current_user,)
from app.schemas.notification import (
    NotiCreate,
    NotiUpdate,
    NotiResponse,
)
from app.services.notification_service import NotificationService
from app.models.user import User

router = APIRouter(
    prefix="/notifications",
    tags=["Notification"],
)

ServiceDep = Annotated[
    NotificationService,
    Depends(get_noti_service),
]

UserDep = Annotated[
    User,
    Depends(get_current_user),
]

@router.post(
    "",
    response_model=NotiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_noti(
    data: NotiCreate,
    service: ServiceDep,
    auth_user: UserDep,
):
    return await service.create(data, auth_user.id)

@router.get(
    "",
    response_model=list[NotiResponse],
)
async def list_noti(service: ServiceDep,auth_user: UserDep,):
    return await service.get_my_notifications(auth_user.id)

@router.get(
    "/{noti_id}",
    response_model=NotiResponse,
)
async def get_noti(
    noti_id: UUID,
    service: ServiceDep,
    auth_user: UserDep,
):
    return await service.get_by_id(noti_id=noti_id, user_id=auth_user.id)


@router.put(
    "/{noti_id}",
    response_model=NotiResponse,
)
async def update_noti(
    noti_id: UUID,
    data: NotiUpdate,
    service: ServiceDep,
    auth_user: UserDep,
):
    return await service.update(noti_id=noti_id, data=data,user_id=auth_user.id)


@router.delete(
    "/{noti_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_noti(
    noti_id: UUID,
    service: ServiceDep,
    auth_user: UserDep,
):
    await service.delete(noti_id=noti_id, user_id=auth_user.id)