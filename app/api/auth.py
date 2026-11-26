from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import (get_auth_service)
from app.services.auth_service import AuthService

from app.schemas.user import Token



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


CurrentUserDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


@router.post(
    "/token",
    response_model=Token,
)
async def login(
    form: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    service: CurrentUserDep,
):
    return await service.login(
        email=form.username,
        password=form.password,
    )

