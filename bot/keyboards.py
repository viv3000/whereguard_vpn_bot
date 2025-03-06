from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать", callback_data='start_pay')],
    [InlineKeyboardButton(text="Тех поддержка", callback_data='support')]
])


pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Согласен", callback_data="pay")],
        [InlineKeyboardButton(text="Позже", callback_data="start")],
    ])

main_menu_keyboard  = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить конфиг", callback_data="get_config")],
        [InlineKeyboardButton(text="Срок подписки", callback_data="get_date")],
        [InlineKeyboardButton(text="Тех поддержка", callback_data='support')]
    ])
