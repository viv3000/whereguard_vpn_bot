import asyncio
import datetime
import logging
import sys
import json

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


def main():
    logging.basicConfig(
            filename=f"logs/{datetime.datetime.today()}log.log", filemode="w", level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config = dotenv_values(".env") 

    TOKEN = str(config["TG_TOKEN"])
    PAY_TOKEN = str(config["TG_PAY_TOKEN"])

    with open('messages.json', 'r') as file:
        messages = json.load(file)

    engine = create_engine("sqlite:///db.sqlite", echo=True)
    Base.metadata.create_all(engine)
    Data.engine = engine


    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    bot = VPNBot(token=TOKEN, pay_token=PAY_TOKEN, messages=messages, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = App(bot, dispatcher)


    asyncio.run(app.start())


if __name__ == "__main__":
    main()

