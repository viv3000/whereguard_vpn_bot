import os
import sys

from services.data import Data

def gen_private_key():
    return os.popen("wg genkey").read()[0:-1]


def gen_public_key(private_key):
    return os.popen("echo " + private_key + " | wg pubkey").read()[0:-1]


def create_keys():
    private_key = gen_private_key()
    public_key = gen_public_key(private_key)
    return [private_key, public_key]


def gen_wg_ip(i):
    return "10.11.84." + str(i+1) + "/32"


def create_peer(i, key):
    return (
        "[Peer]\n" +
        "#" + str(i) + "\n" +
        "PublicKey = " + key + "\n" +
        "AllowedIPs = " + gen_wg_ip(i) + "\n\n"
    )


def create_new_server(config, number_of_slots=100):
    keys = create_keys()
    server_id = Data.create_server(config["ip"], config["ipwg"], config["port"], config["interface"], config["wg_interface"], keys[0], keys[1])
    file = (
        "[Interface]\n" +
        "PrivateKey = " + keys[0] + "\n" +
        "Address = " + config["ip"] + "\n" +
        "ListenPort = " + config["port"] + "\n" +
        "PostUp = iptables -A FORWARD -i " + config["wg_interface"] + " -j ACCEPT; iptables -t nat -A POSTROUTING -o " + config["interface"] + " -j MASQUERADE\n" +
        "PostDown = iptables -D FORWARD -i " + config["wg_interface"] + " -j ACCEPT; iptables -t nat -D POSTROUTING -o " + config["interface"] + " -j MASQUERADE\n\n"
    )

    for i in range(number_of_slots):
        private_key = gen_private_key()
        Data.create_config_file(i, gen_wg_ip(i), server_id, private_key, False)
        file += create_peer(i, gen_public_key(private_key))
    os.system("echo '" + file + "' > " + config["wg_interface"] + ".conf")
