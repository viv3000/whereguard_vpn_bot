from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(16))
    ipwg: Mapped[str] = mapped_column(String(19))
    ip_local: Mapped[str] = mapped_column(String(19))
    port: Mapped[str] = mapped_column(String(5))
    interface: Mapped[str] = mapped_column(String(256))
    wg_interface: Mapped[str] = mapped_column(String(256))
    public_key: Mapped[str] =  mapped_column(String(45))
    private_key: Mapped[str] =  mapped_column(String(45))

    s1: Mapped[str] = mapped_column(Integer(), default=111)
    s2: Mapped[str] = mapped_column(Integer(), default=112)
    h1: Mapped[str] = mapped_column(Integer(), default=113)
    h2: Mapped[str] = mapped_column(Integer(), default=114)
    h3: Mapped[str] = mapped_column(Integer(), default=115)
    h4: Mapped[str] = mapped_column(Integer(), default=116)


class Peer(Base):
    __tablename__ = "peer"

    id: Mapped[int] = mapped_column(primary_key=True)
    config_id: Mapped[int] = mapped_column(Integer())
    ip: Mapped[str] = mapped_column(String(19))
    private_key: Mapped[str] =  mapped_column(String(45))
    is_use: Mapped[bool] = mapped_column(Boolean(), default=False)

    server_id: Mapped[int] = mapped_column(ForeignKey("server.id"))


class User(Base):
    __tablename__ = "vpn_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(256))
    tg_name: Mapped[str] = mapped_column(String(256), nullable=True)
    expiration_date = mapped_column(Date())
    is_not_use_it: Mapped[bool] = mapped_column(Boolean(), default=False)

    peer_id: Mapped[int] = mapped_column(ForeignKey("peer.id"), nullable=True)
