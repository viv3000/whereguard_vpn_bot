from aiogram import F, Bot, Router, types
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery, User
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.exc import NoResultFound

from bot.keyboards import start_keyboard
from log import logInfo
from log import logError
from services.data import Data
from services.entities import UserBuilder

from bot.VPNBot import VPNBot
from bot.handlers import get_config, start
from bot.helpers import await_with_markup, send_message_to_log, send_message_to_support


pay_router = Router()

PRICE = LabeledPrice(label=VPNBot.messages["pay_title"], amount=100*100)  # в копейках (руб)


@pay_router.callback_query(F.data == "start_pay")
async def call_start_pay(call: CallbackQuery, bot: VPNBot):
    try:
        await await_with_markup(
            call.message, 
            bot.messages["greetings"], bot.messages["greetings_first"], 
            call.from_user, 
            bot.messages
        )
        logInfo("start pay", call.from_user)
    except Exception as exception:
        logError("error in start_pay:", call.from_user)


@pay_router.callback_query(F.text == VPNBot.messages["buttons"]["pay"])
async def message_start_pay(message: Message, bot: VPNBot):
    try:
        await await_with_markup(
            message, 
            bot.messages["greetings"], bot.messages["greetings_first"], 
            message.from_user, 
            bot.messages
        )

        logInfo("start pay", message.from_user)
    except Exception as exception:
        logError("error in start_pay:", message.from_user)


@pay_router.message(F.text == VPNBot.messages["buttons"]["pay"])
async def call_pay(message: Message, state: FSMContext, bot: VPNBot):
    try:
        await state.clear()
        builder = UserBuilder(message.from_user)
        user = builder.build()

        await bot.send_invoice(message.chat.id,
                        title=bot.messages["pay_title"],
                        description=bot.messages["pay"],
                        provider_token=bot.pay_token,
                        currency="rub",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="pay")
        logInfo("create pay invoice", message.from_user)
    except Exception as exception:
        logError(f"error in create pay invoice", message.from_user)


@pay_router.message(F.text == VPNBot.messages["buttons"]["extend"])
async def call_pay(message: Message, state: FSMContext, bot: VPNBot):
    try:
        await state.clear()
        builder = UserBuilder(message.from_user)
        user = builder.build()

        await bot.send_invoice(message.chat.id,
                        title=bot.messages["extend_title"],
                        description=bot.messages["extend"],
                        provider_token=bot.pay_token,
                        currency="rub",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="extend")
        logInfo("create pay invoice", message.from_user)
    except Exception as exception:
        logError(f"error in create pay invoice", message.from_user)


@pay_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: VPNBot):
    try:
        Data.get_peer(pre_checkout_query.from_user)
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except:
        await bot.send_message(chat_id=pre_checkout_query.from_user.id, text=bot.messages["end_of_limit"])
        await send_message_to_log("Капитан, закончились сервера!", pre_checkout_query.from_user, bot)
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)



@pay_router.message(F.successful_payment)
async def successful_payment(message: Message, bot: VPNBot):
    try:
        builder = UserBuilder(message.from_user)
        user = builder.build()
        user.pay()
        await get_config(message, message.from_user, bot.messages)
        await start(message, message.from_user, bot.messages)
        if (message.successful_payment.invoice_payload == "pay"):
            logInfo(f"successful_payment", message.from_user)
            await send_message_to_log("Новый гой нагрет!", message.from_user, bot)
        elif (message.successful_payment.invoice_payload == "extend"):
            logInfo(f"successful_extend", message.from_user)
            await send_message_to_log("Старый гой оплатил ещё месяц!", message.from_user, bot)
    except Exception as exception:
        logError(f"error in pay", message.from_user)


