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
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/notifications",
    tags=["Notification"],
)

ServiceDep = Annotated[
    NotificationService,
    Depends(get_noti_service),
]

UserDep = Annotated[
    AuthService,
    Depends(get_current_user),
]

@router.post(
    "",
    response_model=NotiResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
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
async def list_noti(service: ServiceDep):
    return await service.get_all()

@router.get(
    "/me",
    response_model=list[NotiResponse],
    dependencies=[Depends(get_current_user)],
)
async def get_my_notifications(
    service: ServiceDep,
    auth_user: UserDep,
):
    print(f'servicoio  {auth_user}')
    return await service.get_my_notifications(auth_user.id)

@router.get(
    "/{noti_id}",
    response_model=NotiResponse,
)
async def get_noti(
    noti_id: UUID,
    service: ServiceDep,
):
    return await service.get_by_id(noti_id)

@router.get(
    "/me",
    response_model=list[NotiResponse],
    dependencies=[Depends(get_current_user)],
)
async def get_my_notifications(
    service: ServiceDep,
    auth_user: UserDep,
):
    print(f'servicoio  {auth_user}')
    return await service.get_my_notifications(auth_user.id)


@router.put(
    "/{noti_id}",
    response_model=NotiResponse,
)
async def update_noti(
    noti_id: UUID,
    data: NotiUpdate,
    service: ServiceDep,
):
    return await service.update(noti_id, data)


@router.delete(
    "/{noti_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_noti(
    noti_id: UUID,
    service: ServiceDep,
):
    await service.delete(noti_id)