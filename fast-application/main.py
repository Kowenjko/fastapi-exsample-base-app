from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from api import router as api_router
from core.config import settings

from contextlib import asynccontextmanager

from core.models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # # startup
    # if not broker.is_worker_process:
    #     await broker.startup()

    # FastStream broker
    # await broker.start()

    yield
    # shutdown
    print("dispose engine")

    await db_helper.dispose()

    # FastStream broker
    # await broker.stop()

    # if not broker.is_worker_process:
    #     await broker.shutdown()


main_app = FastAPI(lifespan=lifespan)


main_app.include_router(api_router, prefix=settings.api.prefix)


@main_app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":

    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
