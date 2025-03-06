import datetime
from aiogram import Bot
from aiogram.types import User as TGUser
from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound

from db.models import ConfigFile, Server, User

from services.data import Data


class VPNUser:
    def __init__(self, user_data: TGUser):
        self.user_data: TGUser = user_data
        try:
            self.user = self.__get_user()
        except NoResultFound:
            self.user = self.__create_user()

    def __get_user(self):
        return Data.get_user_on_tg(self.user_data)

    def __create_user(self):
        return Data.create_user(
            self.user_data, 
            Data.add_months(datetime.datetime.today(), -1), 
        )


    def is_payed(self):
        return self.__get_expiration_date()>datetime.datetime.today().date()

    def __get_expiration_date(self) -> datetime.datetime:
        return Data.get_expiration_date(self.user_data)


    def pay(self):
        return Data.pay(self.user_data)

"""
    async def pay_processing(self, bot: Bot):
        if self.is_payed():
            await bot.send_message(chat_id=self.user_data.id, text=f"не оплачено")
        else:
            self.pay()
            await bot.send_message(chat_id=self.user_data.id, text=f"оплачено")
"""

class UserBuilder:
    def __init__(self, user_data: TGUser):
        self.user_data: TGUser = user_data

    def build(self):
        return VPNUser(self.user_data)
