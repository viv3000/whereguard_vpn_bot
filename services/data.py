import datetime
import calendar
import os 
import math
import random

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.models import Base, Peer, Server, User

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
                peer_id = cls.get_peer(tg_user)
                user.peer_id = peer_id 
                user.expiration_date = cls.add_months(datetime.datetime.today(), 1)

                peer = session.scalars(
                    select(Peer).where(Peer.id.in_([peer_id]))
                ).one()
                peer.is_use = True
                session.commit()
        except NoResultFound as err:
            raise err


    @classmethod
    def extend(cls, tg_user):
        try:
            with Session(cls.engine) as session:
                user = session.scalars(
                    select(User).where(User.tg_id.in_([tg_user.id]))
                ).one()
                peer_id = cls.get_peer(tg_user)
                user.peer_id = peer_id 
                user.expiration_date = cls.add_months(user.expiration_date, 1)

                peer = session.scalars(
                    select(Peer).where(Peer.id.in_([peer_id]))
                ).one()
                peer.is_use = True
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
                public_key = public_key,
                s1 = math.floor(random.random()*1279)+1,
                s2 = math.floor(random.random()*1279)+1,
                h1 = math.floor(random.random()*1279)+1,
                h2 = math.floor(random.random()*1279)+1,
                h3 = math.floor(random.random()*1279)+1,
                h4 = math.floor(random.random()*1279)+1
            )
            session.add_all([server])
            session.flush()
            id = server.id
            session.commit()
        return id

    @classmethod
    def get_server(cls, server_id):
        with Session(cls.engine) as session:
            server = session.scalars(
                select(Server).where(Server.id == server_id)
            ).one()
            return server.__dict__



    @classmethod
    def create_peer(cls, config_id, ip, server_id, private_key, is_use):
        id = -1
        with Session(cls.engine) as session:
            peer = Peer(
                config_id = config_id,
                ip = ip, 
                server_id = server_id,
                private_key = private_key,
                is_use = is_use
            )
            session.add_all([peer])
            session.flush()
            id = peer.id
            session.commit()
        return id

    @classmethod
    def get_peer(cls, tg_user) -> int: #rewrite, later
        try: 
            with Session(cls.engine) as session:
                user = session.scalars(
                    select(User)
                    .where(User.tg_id.in_([tg_user.id]))
                ).one()
                try: 
                    peer = session.scalars(
                        select(Peer)
                        .where(Peer.id.in_([user.peer_id]))
                    ).one()
                except NoResultFound as err:
                    try:
                        peer = session.scalars(
                            select(Peer)
                            .where(Peer.is_use.in_([False]))
                        ).all()[0]
                    except NoResultFound as err:
                        raise err
            return peer.id
        except NoResultFound as err:
            raise err


    @classmethod
    def compile_peer(cls, peer_id):
        with Session(cls.engine) as session:
            peer = session.scalars(
                select(Peer).where(Peer.id == peer_id)
            ).one()
            server = session.scalars(
                select(Server).where(Server.id == peer.server_id)
            ).one()
            Jmax = math.floor(random.random()*1278)+2
            file = ("[Interface]\n" + 
                "PrivateKey = " + peer.private_key + "\n" +
                "Address = " + Data.gen_wg_ip(peer.id) + "\n" +
                "DNS = 8.8.8.8\n" +
                f"Jc = {math.floor(random.random()*127)+1}\n" +
                f"Jmin = {math.floor(random.random()*(Jmax-1))+1}\n" +
                f"Jmax = {Jmax}\n" +
                f"S1 = {server.s1}\n" +
                f"S2 = {server.s2}\n" +
                f"H1 = {server.h1}\n" +
                f"H2 = {server.h2}\n" +
                f"H3 = {server.h3}\n" +
                f"H4 = {server.h4}\n\n" +
                "[Peer]\n" +
                "PublicKey = " + Data.gen_public_key(server.private_key) + "\n" +
                "Endpoint = " + server.ip + ":" + server.port + "\n" +
                "AllowedIPs = 0.0.0.0/0")
        return file

    @staticmethod
    def gen_public_key(private_key):
        return os.popen("echo " + private_key + " | awg pubkey").read()[0:-1]


    @staticmethod
    def gen_wg_ip(i):
        return "10.11.84." + str(i) + "/32"

    @staticmethod
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.date(year, month, day)

