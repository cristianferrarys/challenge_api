
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.notifications import router as noti_router
from app.core.exception_handlers import (
    register_exception_handlers,
)
from app.core.database import Base, engine
from app.models.user import User  # noqa: F401
from app.models.notification import Notification  # noqa: F401

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

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

# Register exception handlers
register_exception_handlers(app)

# Register routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(noti_router)
