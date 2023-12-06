print("install blacklist.py")
import json
import asyncio
from config import app, owner, owners
from pyrogram import Client, filters
from pyrogram.types import Message

# ...
# Fungsi untuk menambahkan grup ke daftar blacklist
def addbl(chat_id):
    if chat_id not in blacklist_group:
        blacklist_group.append(chat_id)
        save_blacklist_to_json(blacklist_group)
        return True
    return False

# Fungsi untuk menghapus grup dari daftar blacklist
def delbl(chat_id):
    if chat_id in blacklist_group:
        blacklist_group.remove(chat_id)
        save_blacklist_to_json(blacklist_group)
        return True
    return False

# Fungsi untuk menyimpan daftar blacklist ke dalam file JSON
def save_blacklist_to_json(blacklist):
    with open("blacklist.json", "w") as file:
        json.dump(blacklist, file)

# Fungsi untuk memuat daftar blacklist dari file JSON
def load_blacklist_from_json():
    try:
        with open("blacklist.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Fungsi untuk menyinkronkan daftar blacklist
def sync_blacklist():
    global blacklist_group
    blacklist_group = load_blacklist_from_json()

# Fungsi untuk menampilkan daftar grup di blacklist
async def listbl():
    blacklist_groups = load_blacklist_from_json()
    if blacklist_groups:
        result = "**⚙️ Daftar Grup dalam Blacklist:**\n\n"
        for chat_id in blacklist_groups:
            chat_info = await app.get_chat(chat_id)  # Menggunakan await untuk coroutine
            if chat_info:
                chat_name = chat_info.title
                result += f"🔰 {chat_name}\n🆔 `{chat_id}`\n\n"
            else:
                result += f"🆔 ID Grup : `{chat_id}`, Nama Grup: Tidak Dapat Ditemukan\n"
        return result
    else:
        return "Daftar blacklist kosong."

# Fungsi handler untuk pesan yang mengandung ".listbl"
@app.on_message(filters.me & filters.command("listbl", prefixes="."))
async def handle_list_blacklist(client, message: Message):
    result = await listbl()  # Menggunakan await untuk coroutine
    await message.reply_text(result)
    await message.delete()  
# Fungsi handler untuk pesan yang mengandung ".addbl"
@app.on_message(filters.me & filters.command("addbl", prefixes="."))
async def handle_add_blacklist(client, message):
    chat_id = message.chat.id
    if chat_id < 0 and str(chat_id).startswith("-100"):
        if addbl(chat_id):
            await message.reply_text("✅ Grup telah ditambahkan ke daftar blacklist.")
            sync_blacklist()  # Memanggil fungsi untuk menyinkronkan daftar blacklist
        else:
            await message.reply_text("🚨 Grup sudah ada dalam daftar blacklist.")
    else:
        await message.reply_text("🤬 ini fitur buat group goblok")
    await message.delete()  
# Fungsi handler untuk pesan yang mengandung ".delbl"
@app.on_message(filters.me & filters.command("delbl", prefixes="."))
async def handle_del_blacklist(client, message):
    chat_id = message.chat.id
    if chat_id < 0 and str(chat_id).startswith("-100"):
        if delbl(chat_id):
            await message.reply_text("✅ Grup telah dihapus dari daftar blacklist.")
            sync_blacklist()  # Memanggil fungsi untuk menyinkronkan daftar blacklist
        else:
            await message.reply_text("🚨 Grup tidak ada dalam daftar blacklist atau sudah dihapus sebelumnya.")
    else:
        await message.reply_text("🤬 ini fitur buat group goblok")
    await message.delete()              
# Memuat daftar blacklist saat memulai aplikasi
blacklist_group = load_blacklist_from_json()