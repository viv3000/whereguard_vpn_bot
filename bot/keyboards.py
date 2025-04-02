from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_keyboard(messages):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=messages["buttons"]["start"])],
        [KeyboardButton(text=messages["buttons"]["pay"])],
        [KeyboardButton(text=messages["buttons"]["support"])]
    ])

def main_menu_keyboard(messages):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=messages["buttons"]["get_config"]), KeyboardButton(text=messages["buttons"]["get_date"])],
        [KeyboardButton(text=messages["buttons"]["support"]), KeyboardButton(text=messages["buttons"]["get_instruction"])],
        [KeyboardButton(text=messages["buttons"]["extend"]), KeyboardButton(text=messages["buttons"]["start"])]
        
    ])

def cancel_keyboard(messages) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=messages["buttons"]["cancel"])]
    ])
