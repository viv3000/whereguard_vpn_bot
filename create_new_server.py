import sys

from sqlalchemy import create_engine


from db.models import Base

from services.data import Data

from vpn.create_new_server import create_new_server


def main():
    engine = create_engine("sqlite:///db.sqlite", echo=True)
    Base.metadata.create_all(engine)
    Data.engine = engine

    config_vpn = {
        "ipwg": "10.11.84.101/24",
        "ip": sys.argv[1],
        "port": sys.argv[2],
        "wg_interface": sys.argv[3],
        "interface": sys.argv[4],
        "ip_local": sys.argv[5]

    }
    create_new_server(config_vpn, int(sys.argv[6]))

if __name__ == "__main__":
    main()
