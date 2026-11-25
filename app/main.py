from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.users import router as users_router
from app.core.database import Base, engine
from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)

# Importar los modelos para registrar sus tablas.
from app.models.user import User  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Solo para aprendizaje/desarrollo.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Users API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(UserNotFoundError)
async def not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(UserAlreadyExistsError)
async def conflict_handler(
    request: Request,
    exc: UserAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    exc: ValueError,
):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )


app.include_router(users_router)