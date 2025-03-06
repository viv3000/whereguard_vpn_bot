import asyncio
import logging
import sys

from dotenv import dotenv_values

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from sqlalchemy import create_engine

from bot.VPNBot import VPNBot
from bot.router import router

from db.models import Base

from services.data import Data

from app import App


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    config = dotenv_values(".env") 

    TOKEN = str(config["TG_TOKEN"])
    PAY_TOKEN = str(config["TG_PAY_TOKEN"])


    engine = create_engine("sqlite:///db.sqlite", echo=True)
    Base.metadata.create_all(engine)
    Data.engine = engine


    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    bot = VPNBot(token=TOKEN, pay_token=PAY_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = App(bot, dispatcher)


    asyncio.run(app.start())
