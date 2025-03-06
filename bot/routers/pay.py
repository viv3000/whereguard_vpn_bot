import logging

from aiogram import F, Bot, Router, types
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery, User
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from services.entities import UserBuilder

from bot.VPNBot import VPNBot
from bot.handlers import get_config, start
from bot.helpers import send_message_to_log, send_message_to_support
from bot.keyboards import pay_keyboard


pay_router = Router()

PRICE = LabeledPrice(label="Подписка на 1 месяц", amount=200*100)  # в копейках (руб)


@pay_router.callback_query(F.data == "start_pay")
async def call_start_pay(call: CallbackQuery):
    try:
        await call.message.answer(
            text="Вот наши условия всего за 200 зублей в месяц:\n1. Быстрый vpn\n2. Защита туннеля протоколом wireguard\n", 
            reply_markup=pay_keyboard
        )
        logging.info(f"start_pay: {call.from_user.username}")
    except Exception as exception:
        logging.error(f"error in start_pay: {call.from_user.username}", exc_info=True)



@pay_router.callback_query(F.data == "pay")
async def call_pay(call: CallbackQuery, state: FSMContext, bot: VPNBot):
    try:
        await state.clear()
        builder = UserBuilder(call.from_user)
        user = builder.build()

        if user.is_payed():
            await start(call.message.answer)
            logging.info(f"create pay invoice aborted (payed): {call.from_user.username}")
        else:
            await bot.send_invoice(call.message.chat.id,
                        title="Подписка на VPN",
                        description="Активация подписки на VPN на 1 месяц",
                        provider_token=bot.pay_token,
                        currency="rub",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload")
            logging.info(f"create pay invoice: {call.from_user.username}")
    except Exception as exception:
        logging.error(f"error in create pay invoice: {call.from_user.username}", exc_info=True)


@pay_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@pay_router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    try:
        builder = UserBuilder(message.from_user)
        user = builder.build()
        if user.is_payed():
            await start(message.answer)
        else:
            user.pay()
            await get_config(message.answer)
            await start(message.answer)
        logging.info(f"successful_payment: {message.from_user.username}")
        await send_message_to_log(message.from_user, bot)
    except Exception as exception:
        logging.error(f"error in pay: {message.from_user.username}", exc_info=True)


