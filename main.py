import asyncio
import logging
import sys

from aiogram import Dispatcher

from app import App
from bot.router import router


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    app = App(dispatcher)


    asyncio.run(app.start())
