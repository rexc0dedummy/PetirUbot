print("install limit.py")
from config import app, owner, owners
from dipodul.helpers import usage_command

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.enums import MessageEntityType
from pyrogram.types import Chat, Message, User

import asyncio

@app.on_message(filters.command("limit", prefixes="$"))
async def limit_command(client, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:  
        usage_command.user_command = "$limit"
        usage_command.update_command_usage("$limit")
        usage_command.usage_count = usage_command.get_command_usage ("$limit")
        await message.delete()          
        await client.unblock_user("SpamBot")
        bot_info = await client.resolve_peer("SpamBot")
        msg = await message.reply(f"`#{usage_command.usage_count}\n🔍Proses... . .")
        response = await client.invoke(
            StartBot(
                bot=bot_info,
                peer=bot_info,
                random_id=client.rnd_id(),
                start_param="start",
            )
        )
        await asyncio.sleep(1)
        status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
        await msg.edit(status.text)
        await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    await message.delete()       
     
     
@app.on_message(filters.me & filters.command("limit", prefixes="."))
async def limit_command(client, message: Message):
    usage_command.user_command = ".limit"
    usage_command.update_command_usage(".limit")
    usage_command.usage_count = usage_command.get_command_usage (".limit")
    
    await message.delete()      
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    msg = await message.reply(f"`#{usage_command.usage_count}\n🔍Proses... . .")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await asyncio.sleep(1)
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    await msg.edit(status.text)
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))        
    
     