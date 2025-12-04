import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from typing import AsyncGenerator

# from core import broker
from core.fs_broker import broker
from core.models import db_helper

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    # if not broker.is_worker_process:
    #     await broker.startup()
    # FastStream broker
    await broker.start()
    yield
    # shutdown
    await db_helper.dispose()

    # if not broker.is_worker_process:
    #     await broker.shutdown()
    # FastStream broker
    await broker.stop()


def create_app(
    create_custom_static_urls: bool = False,
) -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        # webhooks=webhooks_router,
    )
    if create_custom_static_urls:
        pass

    return app
