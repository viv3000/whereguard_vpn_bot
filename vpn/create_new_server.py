import os
import sys
import math
import random

from services.data import Data

def gen_private_key():
    return os.popen("awg genkey").read()[0:-1]


def gen_public_key(private_key):
    return os.popen("echo " + private_key + " | awg pubkey").read()[0:-1]


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
    server = Data.get_server(server_id)
    Jmax = math.floor(random.random()*1278)+2
    file = (
        "[Interface]\n" +
        "PrivateKey = " + keys[0] + "\n" +
        "Address = " + config["ip"] + "\n" +
        "ListenPort = " + config["port"] + "\n\n" +
        f'PostUp = iptables -A INPUT -p udp --dport {config["port"]} -m conntrack --ctstate NEW -j ACCEPT --wait 10 --wait-interval 50; iptables -A FORWARD -i {config["interface"]} -o {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; iptables -A FORWARD -i {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; iptables -t nat -A POSTROUTING -o {config["interface"]} -j MASQUERADE --wait 10 --wait-interval 50; ip6tables -A FORWARD -i {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; ip6tables -t nat -A POSTROUTING -o {config["interface"]} -j MASQUERADE --wait 10 --wait-interval 50\n\n' +
        f'PostDown = iptables -D INPUT -p udp --dport {config["port"]} -m conntrack --ctstate NEW -j ACCEPT --wait 10 --wait-interval 50; iptables -D FORWARD -i {config["interface"]} -o {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; iptables -D FORWARD -i {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; iptables -t nat -D POSTROUTING -o {config["interface"]} -j MASQUERADE --wait 10 --wait-interval 50; ip6tables -D FORWARD -i {config["wg_interface"]} -j ACCEPT --wait 10 --wait-interval 50; ip6tables -t nat -D POSTROUTING -o {config["interface"]} -j MASQUERADE --wait 10 --wait-interval 50\n\n' +
        
        f'Jc = {math.floor(random.random()*127)+1}\n' +
        f'Jmin = {math.floor(random.random()*(Jmax-1))+1}\n' +
        f'Jmax = {Jmax}\n' +
        f'S1 = {server['s1']}\n' +
        f'S2 = {server['s2']}\n' +
        f'H1 = {server['h1']}\n' +
        f'H2 = {server['h2']}\n' +
        f'H3 = {server['h3']}\n' +
        f'H4 = {server['h4']}\n\n' 
    )

    for i in range(number_of_slots):
        private_key = gen_private_key()
        Data.create_peer(i, gen_wg_ip(i), server_id, private_key, False)
        file += create_peer(i, gen_public_key(private_key))
    os.system("echo '" + file + "' > " + config["wg_interface"] + ".conf")
