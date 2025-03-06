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
    def create_user(cls, tg_user, expiration_date) -> User:
        user = None
        try:
            return cls.get_user_on_tg(tg_user)
        except NoResultFound as err:
            with Session(cls.engine) as session:
                user = User(
                    tg_id = tg_user.id, 
                    tg_name = tg_user.username, 
                    expiration_date = expiration_date,
                )
                session.add_all([user])
                session.flush()
                session.commit()
            return user


    @classmethod
    def get_expiration_date(cls, tg_user) -> datetime.datetime:
        try:
            return cls.get_user_on_tg(tg_user).expiration_date
        except NoResultFound as err:
            raise err


    @classmethod
    def pay(cls, tg_user):
        try:
            with Session(cls.engine) as session:
                user = session.scalars(
                    select(User).where(User.tg_id.in_([tg_user.id]))
                ).one()
                user.expiration_date = cls.add_months(datetime.datetime.today(), 1)
                session.commit()
        except NoResultFound as err:
            raise err

        
    @classmethod
    def create_server(cls, ip, ipwg, port, interface, wg_interface, private_key, public_key):
        id = -1
        with Session(cls.engine) as session:
            server = Server(
                ip = ip, 
                ipwg = ipwg, 
                port = port, 
                interface = interface, 
                wg_interface = wg_interface, 
                private_key = private_key, 
                public_key = public_key
            )
            session.add_all([server])
            session.flush()
            id = server.id
            session.commit()
        return id



    @classmethod
    def create_config_file(cls, config_id, ip, server_id, private_key, is_use):
        id = -1
        with Session(cls.engine) as session:
            config_file = ConfigFile(
                config_id = config_id,
                ip = ip, 
                server_id = server_id,
                private_key = private_key,
                is_use = is_use
            )
            session.add_all([config_file])
            session.flush()
            id = config_file.id
            session.commit()
        return id


    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.date(year, month, day)

