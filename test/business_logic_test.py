import unittest

from aiogram import Bot
from aiogram.types import User
from sqlalchemy import Date, create_engine
from sqlalchemy.exc import NoResultFound

from db.models import Base

from services.data import Data
from services.entities import UserBuilder, VPNUser
from vpn.create_new_server import create_new_server


engine = create_engine("sqlite:///db.test.sqlite", echo=True)
Base.metadata.create_all(engine)
Data.engine = engine


argv = ["main.py", "147.45.240.229", "25569", "wg0", "eth0", "10.10.10.", "200"]

config_vpn = {
        "ipwg": "10.11.84.101/24",
        "ip": argv[1],
        "port": argv[2],
        "wg_interface": argv[3],
        "interface": argv[4]
}
create_new_server(config_vpn, int(argv[5]))

class TestLogic(unittest.TestCase):
    def test_create_user(self):
        test_user = User(id=1, is_bot=False, first_name="test", username="test1")
        builder = UserBuilder(test_user)
        user = builder.build()
        self.assertEqual(user.user_data.__dict__, VPNUser(test_user).user_data.__dict__)


    def test_get_user_false(self):
        test_user = User(id=2, is_bot=False, first_name="test", username="test2")
        try:
            Data.get_user_on_tg(test_user)
            self.assertEqual(1, 2)
        except NoResultFound as err:
            self.assertEqual(1, 1)


    def test_get_user_true(self):
        test_user = User(id=1, is_bot=False, first_name="test", username="test1")
        try:
            Data.get_user_on_tg(test_user)
            self.assertEqual(1, 1)
        except NoResultFound as err:
            self.assertEqual(1, 2)


    def test_is_payed_false(self):
        test_user = User(id=1, is_bot=False, first_name="test", username="test1")
        builder = UserBuilder(test_user)
        user = builder.build()
        self.assertEqual(user.is_payed(), False)


    def test_payed_true(self):
        test_user = User(id=3, is_bot=False, first_name="test", username="test3")
        builder = UserBuilder(test_user)
        user = builder.build()
        user.pay()
        self.assertEqual(user.is_payed(), True)

if __name__ == "__main__":
    unittest.main()

