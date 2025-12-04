import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# from tasks import send_welcome_email
from core.fs_broker import user_registered, broker

from faststream.nats import NatsMessage

from crud import users as users_crud
from core.models import db_helper, User

from core.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserStatsRequest,
    UserStatsResponse,
)

log = logging.getLogger(__name__)
router = APIRouter(tags=["Users"])

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(
    # session: AsyncSession = Depends(db_helper.session_getter)
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await users_crud.get_all_users(session=session)

    return users


@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: int,
) -> UserStatsResponse:
    msg = UserStatsRequest(
        user_id=user_id,
        stat_type="addresses",
    )
    subject = f"users.{user_id}.stats"
    try:
        response: NatsMessage = await broker.request(
            message=msg.model_dump(mode="json"),
            subject=subject,
            timeout=1,
        )
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Request timed out",
        )

    user_stats = UserStatsResponse.model_validate_json(
        response.body,
    )
    return user_stats


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_create: UserCreate,
) -> User:
    user = await users_crud.create_user(session=session, user_create=user_create)
    log.info("Created user %s", user.id)
    await user_registered.publish(
        subject=f"users.{user.id}.created",
        message=None,
    )
    # await send_welcome_email.kiq(user_id=user.id)
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    user = await users_crud.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> None:
    user = await users_crud.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await users_crud.delete_user(session=session, user=user)
