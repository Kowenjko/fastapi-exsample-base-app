import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from tasks import send_welcome_email
from core.fs_broker import user_registered

from crud import users as users_crud
from core.models import db_helper, User
from fastapi import HTTPException
from core.schemas.user import UserCreate, UserRead, UserUpdate

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
