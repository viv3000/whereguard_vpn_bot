from asyncio.streams import StreamReader, StreamWriter
import socket
import asyncio

from bot.VPNBot import VPNBot
from services.data import Data


class CmdServer:
    bot = None

    @staticmethod
    async def start_cmd_server(bot):
        print('start cmd server')
        CmdServer.bot = bot
        server = await asyncio.start_server(CmdServer.handle_connetcion, 'localhost', 9090)
        async with server:
            await server.serve_forever()

    @staticmethod
    async def handle_connetcion(reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
        print("Connected by", addr)
        while True:
            await CmdServer.read(reader, writer, addr)


    @staticmethod
    async def read(reader, writer, addr):
        try:
            raw_data = await reader.read(1024)
            data = raw_data.decode().split('/')
        except ConnectionError:
            print(f"Client suddenly closed while receiving from {addr}")
            writer.close()
            reader.close()
            return
        try:
            writer.write(await CmdServer.create_exist(data, CmdServer.bot))
            writer.close()
            reader.close()
        except ConnectionError:
            print(f"Client suddenly closed, cannot send")
            writer.close()
            reader.close()
            return


    @staticmethod
    async def create_exist(data, bot) -> bytes:
        if (data[0] == "send_message"):
            await bot.send_message(chat_id=data[1], text=data[2])
            return b'Ok'
        elif (data[0] == "newsletter_message"):
            users = Data.get_all_users()
            ret = ''
            for user in users:
                await bot.send_message(chat_id=user.tg_id, text=data[1])
            return b'Ok'
        elif (data[0] == "get_all_users"):
            users = Data.get_all_users()
            ret = ''
            for user in users:
                ret += str([user.id, user.tg_name, user.tg_id, user.expiration_date, user.peer_id])
            return ret.encode()
        else:
            return b'404'

