from pyrogram import Client, filters
from pyrogram.raw.functions import users
from pyrogram.raw.types import UserStatusOnline
from config import app, owner, owners

import asyncio
import time
import os
import json

start_time = time.time()
# Nama file untuk menyimpan data uptime
uptime_file = "uptime.json"

# Membaca data uptime sebelum restart jika ada
if os.path.exists(uptime_file):
    with open(uptime_file, "r") as f:
        data = json.load(f)
        start_time = data.get("start_time", time.time())

# File untuk menyimpan waktu uptime
uptime_file = "uptime.json"

# Membaca data uptime sebelum restart jika ada
if os.path.exists(uptime_file):
    with open(uptime_file, "r") as f:
        data = json.load(f)
        start_time = data.get("start_time", start_time)

@app.on_message(filters.me & filters.command("alive", prefixes="."))
async def alives(client, message):
    chat_id = message.chat.id
    pong_message = f"`Tunggu...`"
    try:
        start_response_time = time.time()
        sent_message = await client.send_message(chat_id, text=pong_message)
        end_response_time = time.time()
        response_time = (end_response_time - start_response_time) * 100

        # Info pengguna
        user = await app.get_me()
        user_name = user.first_name
        user_id = user.id
        user_id = int(str(user_id)[:2])
        total_groups = 1

        # Mendapatkan status pengguna
        user_status = user.status

        # Hitung waktu aktif (uptime)
        current_time = time.time()

        uptime_seconds = int(current_time - start_time)
        uptime_hours, remainder = divmod(uptime_seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(remainder, 60)

        if uptime_hours >= 24:
            days, uptime_hours = divmod(uptime_hours, 24)
            uptime_message = f"**uptime** : `{days}d:{uptime_hours}h:{uptime_minutes}m`"
        elif uptime_hours >= 1:
            uptime_message = f"**uptime** : `{uptime_hours}h:{uptime_minutes}m`"
        else:
            uptime_message = f"**uptime** : `{uptime_minutes}m:{uptime_seconds}s`"

        total_uptime_seconds = int(data.get("total_uptime", 0))
        total_uptime_hours, remainder = divmod(total_uptime_seconds, 3600)
        total_uptime_minutes, total_uptime_seconds = divmod(remainder, 60)

        total_uptime_message = f"**last_uptime** : `{total_uptime_hours}h:{total_uptime_minutes}m:{total_uptime_seconds}s`"

        if user_status == "online":
            status_message = "Status: Aktif"
        else:
            status_message = "**status: PETIR** [__BUYYER ACTIVE__]"

        # Hapus pesan "Tunggu..."
        await message.delete()
        await sent_message.delete()
        await message.reply_text(f"""**PETIRUBOT**\n   {status_message}\n     **name : {user_name}**\n     **dc_id :** `{user_id}`\n     **ping_dc** : `{response_time:.3f}ms`\n     **peer_gc :** `{total_groups}`\n     {uptime_message}\n     {total_uptime_message}\n\n**Framework : Pyrogram 2.0.106\nDeveloper :** @eldipion""")
    except Exception as e:
        print(f"Error saat mengirim pesan: {str(e)}")

# Simpan waktu mulai untuk menghitung uptime
data = {"start_time": start_time}
with open(uptime_file, "w") as f:
    json.dump(data, f)

# Tambahkan waktu setelah restart ke data dan simpan ke file
current_time = time.time()
data["last_time"] = current_time
data["total_uptime"] = data.get("total_uptime", 0) + (current_time - start_time)
with open(uptime_file, "w") as f:
    json.dump(data, f)
    
# FUNGSI ALIVE / CEK STATUS SEMUA CUSTOMER

@app.on_message(filters.command("getstatus", prefixes=""))
async def own_alives(client, message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:
        chat_id = message.chat.id
        pong_message = f"`Tunggu...`"
        try:
            start_response_time = time.time()
            sent_message = await client.send_message(chat_id, text=pong_message)
            end_response_time = time.time()
            response_time = (end_response_time - start_response_time) * 100

            # Info pengguna
            user = await app.get_me()
            user_name = user.first_name
            user_id = user.id
            user_id = int(str(user_id)[:2])
            total_groups = 1

            # Mendapatkan status pengguna
            user_status = user.status

            # Hitung waktu aktif (uptime)
            current_time = time.time()

            uptime_seconds = int(current_time - start_time)
            uptime_hours, remainder = divmod(uptime_seconds, 3600)
            uptime_minutes, uptime_seconds = divmod(remainder, 60)

            if uptime_hours >= 24:
                days, uptime_hours = divmod(uptime_hours, 24)
                uptime_message = f"**uptime** : `{days}d:{uptime_hours}h:{uptime_minutes}m`"
            elif uptime_hours >= 1:
                uptime_message = f"**uptime** : `{uptime_hours}h:{uptime_minutes}m`"
            else:
                uptime_message = f"**uptime** : `{uptime_minutes}m:{uptime_seconds}s`"

            total_uptime_seconds = int(data.get("total_uptime", 0))
            total_uptime_hours, remainder = divmod(total_uptime_seconds, 3600)
            total_uptime_minutes, total_uptime_seconds = divmod(remainder, 60)

            total_uptime_message = f"**last_uptime** : `{total_uptime_hours}h:{total_uptime_minutes}m:{total_uptime_seconds}s`"

            if user_status == "online":
                status_message = "Status: Aktif"
            else:
                status_message = "**status: PETIR** [__BUYYER ACTIVE__]"

            # Hapus pesan "Tunggu..."
            await message.delete()
            await sent_message.delete()
            await message.reply_text(f"""**PETIRUBOT**\n   {status_message}\n     **name : {user_name}**\n     **dc_id :** `{user_id}`\n     **ping_dc** : `{response_time:.3f}ms`\n     **peer_gc :** `{total_groups}`\n     {uptime_message}\n     {total_uptime_message}\n\n**Framework : Pyrogram 2.0.106\nDeveloper :** @eldipion""")
        except Exception as e:
            print(f"Error saat mengirim pesan: {str(e)}")
            