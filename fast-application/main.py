from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api import router as api_router
from views import router as views_router

from core.config import settings

from contextlib import asynccontextmanager

from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # # startup

    yield
    # shutdown

    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)


main_app.include_router(api_router)

main_app.include_router(
    views_router,
)


if __name__ == "__main__":

    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
