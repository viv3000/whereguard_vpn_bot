import asyncio
import datetime
import logging
import json

from dotenv import dotenv_values

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from sqlalchemy import create_engine

from admin_bot.router import admin_router
from admin_bot.AdminBot import AdminBot

from bot.VPNBot import VPNBot
from bot.router import router
from bot.server.server import CmdServer

from db.models import Base

from services.data import Data

from app import App


async def main():
    logging.basicConfig(
            filename=f"logs/{datetime.datetime.today()}log.log", filemode="w", level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config = dotenv_values(".env") 

    TOKEN = str(config["TG_TOKEN"])
    PAY_TOKEN = str(config["TG_PAY_TOKEN"])
    ADMIN_TOKEN = str(config["TG_ADMIN_TOKEN"])

    with open('messages.json', 'r') as file:
        messages = json.load(file)

    engine = create_engine("sqlite:///db.sqlite", echo=True)
    Base.metadata.create_all(engine)
    Data.engine = engine


    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    bot = VPNBot(token=TOKEN, pay_token=PAY_TOKEN, messages=messages, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = App(bot, dispatcher)


    admin_dispatcher = Dispatcher()
    admin_dispatcher.include_routers(admin_router)
    admin_bot = AdminBot(token=ADMIN_TOKEN, vpnBot=bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


    await asyncio.gather(
            admin_dispatcher.start_polling(admin_bot),
            app.start(),
            CmdServer.start_cmd_server(bot),
        )



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

