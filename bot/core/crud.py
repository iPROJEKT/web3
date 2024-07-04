from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.db import AsyncSessionLocal
from bot.models.wallet import User


async def create_user(
    user_id: int,
    seed_phrase: str,
    private_key: hex,
    public_key: hex,
    six_code: int,
    address

):
    result = User(
        user_id=user_id,
        seed_phrase=seed_phrase,
        private_key=private_key,
        public_key=public_key,
        six_code=six_code,
        address=address

    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)


async def get_six_code(
    six_codes: int,
):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.six_code).where(
                User.six_code == six_codes
            )
        )
    print(result.scalars().all())
    return result.scalars().all()


async def get_user(
    user_id: int,
):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.six_code).where(
                User.user_id == user_id
            )
        )
    return result.scalars().first()
