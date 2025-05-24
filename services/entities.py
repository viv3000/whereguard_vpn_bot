import datetime
from aiogram import Bot
from aiogram.types import User as TGUser
from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound

from db.models import Peer, Server, User

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
        return self.get_expiration_date()>datetime.datetime.today().date()

    def is_not_use_it(self) -> bool:
        return self.get_is_not_use_it()

    def get_expiration_date(self) -> datetime.datetime:
        return Data.get_expiration_date(self.user_data)

    def get_is_not_use_it(self) -> bool:
        return Data.get_is_not_use_it(self.user_data)


    def pay(self):
        if self.is_payed():
            return Data.extend(self.user_data)
        else:
            if self.is_not_use_it():
                Data.pay(self.user_data)
                return Data.extend(self.user_data)
            else:
                return Data.pay(self.user_data)


    def get_config(self):
        if self.is_payed():
            return Data.get_peer(self.user_data)
        else:
            raise NoResultFound()



class UserBuilder:
    def __init__(self, user_data: TGUser):
        self.user_data: TGUser = user_data

    def build(self):
        return VPNUser(self.user_data)
