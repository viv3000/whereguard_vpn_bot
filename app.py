from typing import Any, Optional
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode
from dotenv import dotenv_values


class App:
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self.bot = bot 
        self.dispatcher = dispatcher

    async def start(self) -> None:
        await self.dispatcher.start_polling(self.bot)
