import re
from http import HTTPStatus
from sqlalchemy import select

from bot.core.db import AsyncSessionLocal
from bot.models.wallet import User
from bot.core.crud import get_six_code, get_user


async def check_id_duplicate(
    user_id: int,
) -> bool:
    charity_project_id = await (
        get_user(
            user_id=user_id,
        )
    )
    if charity_project_id is not None:
        return False


async def check_code_duplicate(
    six_code: int,
) -> bool:
    charity_project_id = await (
        get_six_code(
            six_codes=six_code,
        )
    )
    if charity_project_id is None:
        return False
