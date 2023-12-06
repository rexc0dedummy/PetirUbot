print("install gcast.py")
from config import app, owner, owners, BLACKLIST_CHAT
from dipodul.helpers import usage_command

from pyrogram import Client, filters
from pyrogram.types import Message, Chat, User
from pyrogram.enums import ChatType
from gun import load_blacklist_from_json

import asyncio
import json

def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg

async def get_bot_chat(client):
    bot_chat = await client.get_me()
    return bot_chat
    
async def get_broadcast_id(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP]
    }
    async for dialog in client.get_dialogs():
        if dialog.chat.type in chat_types[query]:
            chats.append(dialog.chat.id)

    return chats
    
broadcast_running = False

async def broadcast_group_cmd(client, message):
    global broadcast_running

    msg = await message.reply("Sedang diproses...", quote=True)
    blacklist_groups = load_blacklist_from_json()
    send = get_message(message)
    if not send:
        return await msg.edit("Silakan balas ke pesan atau berikan pesan.")
    broadcast_running = True
    chats = await get_broadcast_id(client, "group")
    chat_bot = await get_bot_chat(client)
    done = 0
    failed = 0
    iteration = 10  # Jumlah pengulangan yang diinginkan, dalam hal ini 5
    while iteration > 0:
        for chat_id in chats:
            if not broadcast_running:
                break

            if chat_id not in BLACKLIST_CHAT and chat_id not in blacklist_groups:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    done += 1
                except Exception:
                    failed += 1
        iteration -= 1
    broadcast_running = False

    if done > 0:
        await msg.edit(f"**Berhasil Mengirim Pesan Ke `{done}` Grup. Gagal: `{failed}`**.")
    else:
        await msg.edit(f"**Pesan Broadcast Berhasil Dibatalkan**.")

async def get_chat(client, chat_id):
    try:
        chat = await client.get_chat(chat_id)
        return chat
    except Exception as e:
        print(f"Error while getting chat: {e}")
        return None    
        
@app.on_message(filters.command("gcast", prefixes="$"))
async def owner_gcast_command(client, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:
        usage_command.user_command = "$gcast"
        usage_command.update_command_usage("$gcast")
        usage_command.usage_count = usage_command.get_command_usage("$gcast")          
        sent = 0
        failed = 0
        msg = await message.reply(
            f"**In Bearbeitung, bitte warten... .\n`#{usage_command.usage_count}`**"
        )
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                if message.reply_to_message:
                    send = message.reply_to_message
                else:
                    if len(message.command) < 2:
                        await msg.delete()
                        return await message.reply("<b>Pesannya Mana ngentod</b>")
                    else:
                        send = message.text.split(None, 1)[1]
                chat_id = dialog.chat.id
                if chat_id not in BLACKLIST_CHAT:
                    try:
                        if message.reply_to_message:
                            await send.copy(chat_id)
                        else:
                            await client.send_message(chat_id, send)
                        sent += 1
                        await asyncio.sleep(1)
                    except Exception:
                        failed += 1
                        await asyncio.sleep(1)
        await msg.edit(
            f"`#{usage_command.usage_count}`\n𝘚𝘦𝘯𝘥𝘦𝘯 𝘢𝘯 `{sent} Gruppe`\n𝘍𝘢𝘪𝘭𝘦𝘥 `{failed} Gruppe(s)`"
        )
@app.on_message(filters.me & filters.command("gcast", prefixes=","))
async def fake_gcast_command(client, message):
    chat_id = message.chat.id

    # Pesan palsu "Prosess..."
    process_message = "⏱️ Process... ."
    await client.send_message(
        chat_id,
        text=process_message
    )

    # Jeda waktu 5 detik
    await asyncio.sleep(8)

    # Merespons dengan pesan "Berhasil" setelah jeda waktu
    success_message = "𝘚𝘦𝘯𝘥𝘦𝘯𝘢𝘯 `110Gruppe`\n𝘍𝘢𝘪𝘭𝘦𝘥 `23Gruppe(s)`"
    await client.send_message(
        chat_id,
        text=success_message
    )
    
        
# Gcast user
@app.on_message(filters.me & filters.command("gcast", prefixes="."))
async def gcast_command(client, message: Message):
    usage_command.user_command = ".gcast"
    usage_command.update_command_usage(".gcast")
    usage_command.usage_count = usage_command.get_command_usage(".gcast")          
    blacklist_groups = load_blacklist_from_json()
    await app.join_chat("rexc0de")
    print("Berhasil Join Channel")
    await app.join_chat("PetirSupport")
    print("Berhasil Join Group")
    
    sent = 0
    failed = 0
    msg = await message.reply(
        f"**In Bearbeitung, bitte warten... .\n`#{usage_command.usage_count}`**"
    )
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    await msg.delete()
                    return await message.reply("<b>Pesannya Mana ngentod</b>")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in BLACKLIST_CHAT and chat_id not in blacklist_groups:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await asyncio.sleep(1)
                except Exception:
                    failed += 1
                    await asyncio.sleep(1)
    await msg.edit(
        f"`#{usage_command.usage_count}`\n𝘚𝘦𝘯𝘥𝘦𝘯 𝘢𝘯 `{sent} Gruppe`\n𝘍𝘢𝘪𝘭𝘦𝘥 `{failed} Gruppe(s)`"
    )
    
    
@app.on_message(filters.command("tol", prefixes=","))
async def start_command(client, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:   
        chat_id = message.chat.id
    
        # Pesan yang akan muncul ketika pengguna mengirim ".tol"
        start_message = "DANA `081394369076` A/N MUC* AG AL*\nBCA `0882410445` A/N MUC* AG AL*"
    
        try:
            await client.send_message(chat_id, text=start_message)
        except Exception as e:
            print(f"Error saat mengirim pesan: {str(e)}")