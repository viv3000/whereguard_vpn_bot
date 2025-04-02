from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command

from bot.VPNBot import VPNBot
from bot.routers.FSMSupport import support_router
from bot.routers.pay import pay_router
from bot.handlers import get_config, get_date, get_instruction, start


menu_router = Router()


@menu_router.message(F.text == VPNBot.messages["buttons"]["get_config"])
async def message_get_config(message: Message, bot: VPNBot):
    await get_config(message, message.from_user, bot.messages)


@menu_router.message(F.text == VPNBot.messages["buttons"]["get_date"])
async def message_get_date(message: Message, bot: VPNBot):
    await get_date(message, message.from_user, bot.messages)


@menu_router.message(F.text == VPNBot.messages["buttons"]["get_instruction"])
async def message_get_instruction(message: Message, bot: VPNBot):
    await get_instruction(message, bot.messages)
