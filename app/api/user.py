from typing import Sequence, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.config import get_session
from app.db.models import Users
from app.logging.cache_hit import log_cache_hit
from app.schemas.user import UserResponseModel, UserCreateModel

router = APIRouter()


@log_cache_hit(cache_key="users", expire=60)
async def fetch_users() -> Sequence[Users]:
    async for session in get_session():
        result = await session.execute(select(Users))
        return list(result.scalars().all())


@router.get("/users", response_model=Sequence[UserResponseModel], status_code=status.HTTP_200_OK)
async def get_users() -> Sequence[Users]:
    users = await fetch_users()
    return users


@router.get("/users/{user_id}", response_model=Optional[UserResponseModel])
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> Optional[Users]:
    user = await session.execute(select(Users).where(Users.id == user_id))
    return user.scalars().first()


@router.post("/users", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateModel, session: AsyncSession = Depends(get_session)) -> Users:
    db_user = Users(**user.dict())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=UserResponseModel)
async def update_user(
        user_id: int,
        user: UserCreateModel,
        session: AsyncSession = Depends(get_session)
) -> Optional[Users]:
    db_user = await session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.dish_of_the_day = user.dish_of_the_day
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(Users, user_id)
    await session.delete(user)
    await session.commit()
