print("Install sepam.py")
from pyrogram import Client, filters
from pyrogram.raw.functions import users
from config import app, owner, owners

import asyncio
import time
import os

spamming = False  # Variabel untuk menandai apakah sedang dalam proses spam

async def send_messages(chat_id, message, count, delay, initiator_chat_id):
    global spamming
    spamming = True
    for _ in range(count):
        await app.send_message(chat_id, message)
        await asyncio.sleep(delay)
    spamming = False
    await app.send_message(initiator_chat_id, "🎉 Spam selesai!")

@app.on_message(filters.me & filters.command("spamdelay", prefixes="."))
async def sepam_messages(client, message):
    global spamming
    command = message.text.split()
    if len(command) >= 5:
        chat_id = int(command[1])
        count = int(command[2])
        delay = int(command[3])
        text = ' '.join(command[4:])
        await app.send_message(message.chat.id, "🚀 Mulai spam!")
        await send_messages(chat_id, text, count, delay, message.chat.id)
        
@app.on_message(filters.me & filters.command("stopspam", prefixes="."))
async def stop_spam(client, message):
    global spamming
    spamming = False
    await app.send_message(message.chat.id, f"😓 `Proses spam dihentikan secara paksa.`")        