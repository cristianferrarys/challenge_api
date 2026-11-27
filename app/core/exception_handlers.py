
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InvalidAccessTokenError,
    InvalidUserDataError,
    NotificationNotFoundError,
    InvalidRecipientError,
    InvalidNotificationContentError,
    UnsupportedChannelError,
)


async def not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def conflict_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


async def unauthorized_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:

    # 404 - Not Found
    app.add_exception_handler(
        UserNotFoundError,
        not_found_handler,
    )

    app.add_exception_handler(
        NotificationNotFoundError,
        not_found_handler,
    )

    # 409 - Conflict
    app.add_exception_handler(
        UserAlreadyExistsError,
        conflict_handler,
    )

    # 401 - Unauthorized
    app.add_exception_handler(
        InvalidCredentialsError,
        unauthorized_handler,
    )

    app.add_exception_handler(
        InvalidAccessTokenError,
        unauthorized_handler,
    )

    # 422 - Unprocessable Entity
    app.add_exception_handler(
        InvalidUserDataError,
        validation_error_handler,
    )

    app.add_exception_handler(
        InvalidRecipientError,
        validation_error_handler,
    )

    app.add_exception_handler(
        InvalidNotificationContentError,
        validation_error_handler,
    )

    app.add_exception_handler(
        UnsupportedChannelError,
        validation_error_handler,
    )
