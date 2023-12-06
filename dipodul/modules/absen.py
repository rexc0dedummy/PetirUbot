from config import app, owner, owners
from pyrogram import Client, filters
from pyrogram.types import Message

@app.on_message(filters.command("absen", prefixes=""))
async def absen(client, message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:    
        chat_id = message.chat.id
        text = f"**__Hadirr tuhan dipoo__**"
        
        await message.reply_text(text)