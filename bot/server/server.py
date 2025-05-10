from asyncio.streams import StreamReader, StreamWriter
import datetime
import socket
import asyncio

from bot.VPNBot import VPNBot
from services.data import Data


class CmdServer:
    bot = None

    @staticmethod
    async def start_cmd_server(bot):
        CmdServer.bot = bot
        server = await asyncio.start_server(CmdServer.handle_connetcion, 'localhost', 9090)
        async with server:
            await server.serve_forever()

    @staticmethod
    async def handle_connetcion(reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
        while True:
            await CmdServer.read(reader, writer, addr)


    @staticmethod
    async def read(reader, writer, addr):
        try:
            raw_data = await reader.read(1024)
            data = raw_data.decode().split('/')
        except ConnectionError:
            writer.close()
            reader.close()
            return
        try:
            writer.write(await CmdServer.create_exist(data, CmdServer.bot))
            writer.close()
            reader.close()
        except ConnectionError:
            writer.close()
            reader.close()
            return


    @staticmethod
    async def create_exist(data, bot: VPNBot) -> bytes:
        if (data[0] == "send_message"):
            await bot.send_message(chat_id=data[1], text=data[2])
            return b'Ok'
        elif (data[0] == "newsletter_message"):
            for user in Data.get_all_users():
                await bot.send_message(chat_id=user.tg_id, text=data[1])
            return b'Ok'
        elif (data[0] == "get_all_users"):
            ret = ''
            for user in Data.get_all_users():
                ret += str([user.id, user.tg_name, user.tg_id, user.expiration_date, user.peer_id])
            return ret.encode()
        elif (data[0] == "send_alerts"):
            for user in Data.get_all_users():
                different = user.expiration_date - datetime.date.today()
                if ((different.days<=3) and (different.days>=0)):
                    if (different.days == 0):
                        await bot.send_message(
                                chat_id=bot.non_payers_chat_id,
                                text=f'{user.tg_name}: {user.tg_id} Отключай!!!!!\n#неПлатит')
                    elif (different.days == 1):
                        await bot.send_message(
                                chat_id=user.tg_id,
                                text=bot.messages['shutdown_warning'])
                    else:
                        await bot.send_message(
                                chat_id=user.tg_id,
                                text=bot.messages['alert'].replace(
                                    '<day>',
                                    str(different.days)))
            return b'Ok'
        else:
            return b'404'

