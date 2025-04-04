from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL
import logging
import re
import asyncio
from utils import temp
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()
INDEX_CHANNEL = -1002498086501

@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL))
async def join_reqs(client, message: ChatJoinRequest):
  if not await db.find_join_req(message.from_user.id):
    await db.add_join_req(message.from_user.id)

@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")



@Client.on_message(filters.document | filters.audio | filters.video)
async def auto(bot, message):
    # Check if the message is from the specified channel
    if message.chat.id == INDEX_CHANNEL:
        # Log the received media for tracking purposes
        logger.info(f"Received {message.media.value} from {message.chat.title or message.chat.id}")

        # Check if the media attribute exists
        if message.media:
            # Extract the media type
            media_type = message.media.value
            media = getattr(message, media_type, None)

            if media:
                media.file_type = media_type
                media.caption = message.caption
                
                # Save the media file
                try:
                    aynav, vnay = await save_file(media)
                    if aynav:
                        logger.info("File successfully indexed and saved.")
                    elif vnay == 0:
                        logger.info("Duplicate file was skipped.")
                    elif vnay == 2:
                        logger.error("Error(index) occurred")
                    
                except Exception as e:
                    logger.exception("Failed to save file: %s", e)
                    await message.reply("An error occurred while processing the file.")
            else:
                logger.warning("No media found in the message.")
        else:
            logger.warning("Message does not contain media.")
