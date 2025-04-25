import os, math, logging, logging.config

from aiohttp import web
from pyrogram import Client, types
from typing import Union, Optional, AsyncGenerator
from info import API_ID, API_HASH, BOT_TOKEN, SUDO, LOG_MSG
from plugins import web_server

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger(__name__).setLevel(logging.INFO)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Professor-Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        
        await super().start()
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name
        self.mention = me.mention
        self.username = me.username
        self.log_channel = LOG_CHANNEL
        logging.info(LOG_MSG.format(me.first_name))
        
        try: await self.send_message(SUDO, text=LOG_MSG.format(me.first_name), disable_web_page_preview=True)   
        except Exception as e: logging.warning(f"Bot Isn't Able To Send Message To LOG_CHANNEL \n{e}")
        
        if bool(WEB_SUPPORT) is True:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()
            logging.info("Web Response Is Running......🕸️")
            
    async def stop(self, *args):
        await super().stop()
        logging.info(f"Bot Is Restarting ⟳...")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1


        
Bot().run()





