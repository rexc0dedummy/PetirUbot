print("install sg.py")
from config import app, owner, owners
from dipodul.helpers import usage_command

from pyrogram import Client, filters
from pyrogram.types import Message, Chat, User
from typing import Tuple, Union

import asyncio
async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None


async def extract_users(message):
    result = await extract_user_and_reason(message)
    if result:
        return result[0]


def extract_user(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    """extracts the user from a message"""
    user_id = None
    user_first_name = None
    aviyal = None

    if len(message.command) > 1:
        if (
            len(message.entities) > 1
            and message.entities[1].type == MessageEntityType.TEXT_MENTION
        ):
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
            aviyal = required_entity.user
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
            aviyal = True

        try:
            user_id = int(user_id)
        except ValueError:
            print("പൊട്ടൻ ")

    elif message.reply_to_message:
        user_id, user_first_name, aviyal = _eufm(message.reply_to_message)

    elif message:
        user_id, user_first_name, aviyal = _eufm(message)

    return (user_id, user_first_name, aviyal)


def _eufm(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    user_id = None
    user_first_name = None
    ithuenthoothengaa = None

    if message.from_user:
        ithuenthoothengaa = message.from_user
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.first_name

    elif message.sender_chat:
        ithuenthoothengaa = message.sender_chat
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.title

    return (user_id, user_first_name, ithuenthoothengaa)

@app.on_message(filters.me & filters.command(["sg", "sa"], prefixes="."))
async def sg_command(_, message: Message):
    usage_command.user_command = ".sg"
    usage_command.update_command_usage(".sg")
    
    usage_command.usage_count = usage_command.get_command_usage (".sg")
    await message.delete()        
    args = await extract_users(message)
    lol = await message.reply(
        f"`#{usage_command.usage_count}`\n<code>LU SIAPA SI KENTOT, GUA KEPO, GA SENENG PC!!</code>"
    )
    if not args:
        return await lol.edit(f"`#{usage_command.usage_count}`\n<code>Error, reply pesan usernya</code>")
    try:
        user = await _.get_users(args)
    except Exception:
        return await lol.edit(
            f"`#{usage_count}`\n<code>Reply Ke Pesan User Yang Kau Pengen KEPOIN ngentot.</code>"
        )
    bot = "SangMata_BOT"
    try:
        txt = await _.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await _.unblock_user(bot)
    await asyncio.sleep(1)
    await txt.delete()
    await lol.delete()
    for getName in ["Name", "Username"]:
        async for getText in _.search_messages(bot, query=getName, limit=1):
            if getName not in getText.text:
                await message.reply(
                    f"`#{usage_command.usage_count}`\n<code>Masa Gua Gak Nemu Riwayat {getName} si ngentot, Wah si anjing belom pernah ganti apa apa su!!</code>"
                )
            else:
                await message.reply(getText.text)
                  
                  
@app.on_message(filters.command(["sg", "sa"], prefixes="$"))
async def owner_sg_command(_, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:
        usage_command.user_command = "$sg"
        usage_command.update_command_usage("$sg")
        
        usage_command.usage_count = usage_command.get_command_usage ("$sg")
        await message.delete()        
        args = await extract_users(message)
        lol = await message.reply(
            f"`#{usage_command.usage_count}`\n<code>LU SIAPA SI KENTOT, GUA KEPO, GA SENENG PC!!</code>"
        )
        if not args:
            return await lol.edit(f"`#{usage_command.usage_count}`\n<code>Error, reply pesan usernya</code>")
        try:
            user = await _.get_users(args)
        except Exception:
            return await lol.edit(
                f"`#{usage_count}`\n<code>Reply Ke Pesan User Yang Kau Pengen KEPOIN ngentot.</code>"
            )
        bot = "SangMata_BOT"
        try:
            txt = await _.send_message(bot, f"{user.id}")
        except YouBlockedUser:
            await _.unblock_user(bot)
        await asyncio.sleep(1)
        await txt.delete()
        await lol.delete()
        for getName in ["Name", "Username"]:
            async for getText in _.search_messages(bot, query=getName, limit=1):
                if getName not in getText.text:
                    await message.reply(
                        f"`#{usage_command.usage_count}`\n<code>Masa Gua Gak Nemu Riwayat {getName} si ngentot, Wah si anjing belom pernah ganti apa apa su!!</code>"
                    )
                else:
                    await message.reply(getText.text)                  