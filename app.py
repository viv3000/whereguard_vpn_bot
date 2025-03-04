from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import dotenv_values


class App:
    config = dotenv_values(".env") 

    TOKEN = str(config["TG_TOKEN"])
    PAY_TOKEN = str(config["TG_PAY_TOKEN"])

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.bot = Bot(token=self.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dispatcher = dispatcher

    async def start(self) -> None:
        await self.dispatcher.start_polling(self.bot)
