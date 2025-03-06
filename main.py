import asyncio
import logging
import sys
from typing import Any, Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode
from dotenv import dotenv_values

from app import App
from bot.VPNBot import VPNBot
from bot.router import router


if __name__ == "__main__":
    config = dotenv_values(".env") 
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    TOKEN = str(config["TG_TOKEN"])
    PAY_TOKEN = str(config["TG_PAY_TOKEN"])

    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    bot = VPNBot(token=TOKEN, pay_token=PAY_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = App(bot, dispatcher)


    asyncio.run(app.start())
