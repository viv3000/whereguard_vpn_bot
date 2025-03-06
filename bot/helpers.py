from typing import Optional
from aiogram import Bot
from aiogram.types import User


async def send_message_to_support(text: str, user: User, bot: Bot):
    await bot.send_message(chat_id=-4711555769, text=f"@{user.username} вопрошает:\n{text}")


async def send_message_to_log(user: User, bot: Bot):
    await bot.send_message(chat_id=-4711555769, text=f"Новый гой нагрет!\n@{user.username}")
