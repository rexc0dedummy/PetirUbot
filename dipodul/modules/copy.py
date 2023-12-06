print("install copy.py")

from config import app, owner, owners

from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Tuple, Union

def get_arg(message):
    msg = message.text
    msg = msg.lstrip()  # Remove leading spaces
    split = msg.split(None, 1)  # Split at the first space
    if len(split) == 1:
        return ""
    return split[1]

def get_msg_id(link):
    # Menggunakan ekspresi reguler untuk mengekstrak nomor pesan
    msg_id_match = re.search(r'/(\d+)\?', link)
    if msg_id_match:
        return int(msg_id_match.group(1))
    return None

@app.on_message(filters.command("kopi", prefixes="$"))
async def owner_kopi_command(client, message):
    if message.from_user and message.from_user.id in (owner, owners):  # Check if the user is the owner or one of the owners
        msg = message.reply_to_message or message
        Tm = await message.reply("Tunggu sebentar")
        await Tm.delete()
        link = get_arg(message)
        if not link:
            return await message.reply(f"<b><code>{message.text}</code> [link_konten_telegram]</b>")
        if link.startswith(("https", "t.me")):
            msg_id = int(link.split("/")[-1])
            if "t.me/c/" in link:
                chat = int("-100" + str(link.split("/")[-2]))
            else:
                chat = str(link.split("/")[-2])
            try:
                get = await client.get_messages(chat, msg_id)
                await get.copy(message.chat.id, reply_to_message_id=msg.id)
            except Exception as error:
                await message.reply(str(error))  # Convert the error to a string for reply
        else:
            await message.reply("Masukkan link yang valid")
    await message.delete()  
    
@app.on_message(filters.me & filters.command("kopi", prefixes="."))
async def kopi_command(client, message):
    msg = message.reply_to_message or message
    Tm = await message.reply("Tunggu sebentar")
    await Tm.delete()
    link = get_arg(message)
    if not link:
        return await message.reply(f"<b><code>{message.text}</code> [link_konten_telegram]</b>")
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
        else:
            chat = str(link.split("/")[-2])
        try:
            get = await client.get_messages(chat, msg_id)
            await get.copy(message.chat.id, reply_to_message_id=msg.id)
        except Exception as error:
            await message.reply(str(error))  # Convert the error to a string for reply
    else:
        await message.reply("Masukkan link yang valid")
    await message.delete()  

@app.on_message(filters.command("tol", prefixes="$"))
async def start_command(client, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:   
        chat_id = message.chat.id
    
        # Pesan yang akan muncul ketika pengguna mengirim ".tol"
        start_message = "DANA `081394369076` A/N MUC* AG AL*\nBCA `0882410445` A/N MUC* AG AL*"
    
        try:
            await client.send_message(chat_id, text=start_message)
        except Exception as e:
            print(f"Error saat mengirim pesan: {str(e)}")