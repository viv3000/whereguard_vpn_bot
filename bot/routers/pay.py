import logging

from aiogram import F, Bot, Router, types
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery, User
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bot.keyboards import start_keyboard
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
        logging.info(f"start_pay: {call.from_user.username}")
    except Exception as exception:
        logging.error(f"error in start_pay: {call.from_user.username}", exc_info=True)


@pay_router.callback_query(F.text == VPNBot.messages["buttons"]["pay"])
async def message_start_pay(message: Message, bot: VPNBot):
    try:
        await await_with_markup(
            message, 
            bot.messages["greetings"], bot.messages["greetings_first"], 
            message.from_user, 
            bot.messages
        )

        logging.info(f"start_pay: {message.from_user.username}")
    except Exception as exception:
        logging.error(f"error in start_pay: {message.from_user.username}", exc_info=True)


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
        logging.info(f"create pay invoice: {message.from_user.username}")
    except Exception as exception:
        logging.error(f"error in create pay invoice: {message.from_user.username}", exc_info=True)


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
        logging.info(f"create pay invoice: {message.from_user.username}")
    except Exception as exception:
        logging.error(f"error in create pay invoice: {message.from_user.username}", exc_info=True)


@pay_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    builder = UserBuilder(pre_checkout_query.from_user)
    user = builder.build()
    if user.is_payed():
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@pay_router.message(F.successful_payment)
async def successful_payment(message: Message, bot: VPNBot):
    try:
        builder = UserBuilder(message.from_user)
        user = builder.build()
        user.pay()
        await get_config(message, message.from_user, bot.messages)
        await start(message, message.from_user, bot.messages)
        if (message.successful_payment.invoice_payload == "pay"):
            logging.info(f"successful_payment: {message.from_user.username}")
            await send_message_to_log("Новый гой нагрет!", message.from_user, bot)
        elif (message.successful_payment.invoice_payload == "extend"):
            logging.info(f"successful_extend: {message.from_user.username}")
            await send_message_to_log("Старый гой оплатил ещё месяц!", message.from_user, bot)
    except Exception as exception:
        logging.error(f"error in pay: {message.from_user.username}", exc_info=True)


