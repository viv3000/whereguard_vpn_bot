import datetime
import calendar 

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models import Base, ConfigFile, Server, User

class Data:
    engine = None
    
    @classmethod
    def get_user_on_tg(cls, tg_user) -> User:
        try: 
            with Session(cls.engine) as session:
                user = session.scalars(
                    select(User)
                    .where(User.tg_id.in_([tg_user.id]))
                ).one()
            return user
        except NoResultFound as err:
            raise err


    @classmethod
    def create_user(cls, tg_user, subscription_end_date) -> User:
        user = None
        try:
            return cls.get_user_on_tg(tg_user)
        except NoResultFound as err:
            with Session(cls.engine) as session:
                user = User(
                    tg_id = tg_user.id, 
                    tg_name = tg_user.username, 
                    subscription_end_date = subscription_end_date,
                )
                session.add_all([user])
                session.flush()
                session.commit()
            return user


    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.date(year, month, day)
