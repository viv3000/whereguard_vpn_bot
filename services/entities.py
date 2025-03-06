from aiogram import Bot
from aiogram.types import User


class VPNUser:
    def __init__(self, user_data: User):
        self.user_data: User = user_data

    def is_payed(self):
        return False

    async def pay_processing(self, bot: Bot):
        await bot.send_message(chat_id=self.user_data.id, text=f"оплачено")


class UserBuilder:
    def __init__(self, user_data: User):
        self.user_data: User = user_data

    def build(self):
        return VPNUser(self.user_data)
