from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(16))
    ipwg: Mapped[str] = mapped_column(String(19))
    port: Mapped[str] = mapped_column(String(5))
    interface: Mapped[str] = mapped_column(String(256))
    wg_interface: Mapped[str] = mapped_column(String(256))
    public_key: Mapped[str] =  mapped_column(String(45))
    private_key: Mapped[str] =  mapped_column(String(45))


class ConfigFile(Base):
    __tablename__ = "config_file"

    id: Mapped[int] = mapped_column(primary_key=True)
    config_id: Mapped[int] = mapped_column(Integer())
    ip: Mapped[str] = mapped_column(String(19))
    private_key: Mapped[str] =  mapped_column(String(45))
    is_use: Mapped[bool] = mapped_column(Boolean(), default=False)

    server_id: Mapped[int] = mapped_column(ForeignKey("server.id"))


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(256))
    tg_name: Mapped[str] = mapped_column(String(256))
    expiration_date = mapped_column(Date())

    config_file_id: Mapped[int] = mapped_column(ForeignKey("config_file.id"), nullable=True)
