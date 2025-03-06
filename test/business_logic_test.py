from aiogram import Bot
from aiogram.types import User
from sqlalchemy import Date, create_engine
from sqlalchemy.exc import NoResultFound

from db.models import Base

from services.data import Data
from services.entities import UserBuilder, VPNUser


engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(engine)
Data.engine = engine


def test_create_user():
    test_user = User(id=1, is_bot=False, first_name="test", username="test1")
    builder = UserBuilder(test_user)
    user = builder.build()
    assert user.user_data.__dict__ == VPNUser(test_user).user_data.__dict__


def test_get_user_false():
    test_user = User(id=2, is_bot=False, first_name="test", username="test2")
    try:
        Data.get_user_on_tg(test_user)
        assert 1==2
    except NoResultFound as err:
        assert 1==1


def test_get_user_true():
    test_user = User(id=1, is_bot=False, first_name="test", username="test1")
    try:
        Data.get_user_on_tg(test_user)
        assert 1==1
    except NoResultFound as err:
        assert 1==2


def test_is_payed_false():
    test_user = User(id=1, is_bot=False, first_name="test", username="test1")
    builder = UserBuilder(test_user)
    user = builder.build()
    assert not user.is_payed()


def test_payed_true():
    test_user = User(id=3, is_bot=False, first_name="test", username="test3")
    builder = UserBuilder(test_user)
    user = builder.build()
    user.pay()
    assert user.is_payed()


