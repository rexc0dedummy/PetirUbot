print("install asupan.py")
from config import app, owner, owners
import asyncio
from random import choice

from pyrogram import enums, filters
from pyrogram.types import Message

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id

@app.on_message(filters.command("asupan", prefixes=".") & filters.me)
async def asupan_cmd(client, message):
    await message.delete()
    await asyncio.gather(
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        "IndomieGantengV3", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=message.id,
        ),
    )
    await message.delete()  

@app.on_message(filters.command("ayang", prefixes=".") & filters.me)
async def asupan_cmd(client, message):
    await message.delete()    
    await asyncio.gather(
        client.send_photo(
            message.chat.id,
            choice(
                [
                    asupan.photo.file_id
                    async for asupan in client.search_messages(
                        "IndomieGantengV2", filter=enums.MessagesFilter.PHOTO
                    )
                ]
            ),
            reply_to_message_id=message.id,
        ),
    )


@app.on_message(filters.command("ayang2", prefixes=".") & filters.me)
async def asupan_cmd(client, message):
    message.reply_to_message or message
    await message.delete()  
    await asyncio.gather(
        client.send_photo(
            message.chat.id,
            choice(
                [
                    asupan.photo.file_id
                    async for asupan in client.search_messages(
                        "galeriCogann", filter=enums.MessagesFilter.PHOTO
                    )
                ]
            ),
            reply_to_message_id=message.id,
        ),
    )
