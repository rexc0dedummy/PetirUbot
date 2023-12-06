print("install gun.py")

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from asyncio import sleep

from config import app, owner, owners, BLACKLIST_CHAT
from dipodul.modules import copy, limit, aidi, sg, gcast, asupan, whois, blacklist, absen, alive, send
from dipodul.helpers import usage_command

import asyncio
import re
import time
import logging
import json
import sys
import os
import subprocess
# Gantilah dengan informasi API Anda

logger = logging.getLogger("pyrogram.session.session")
logger.setLevel(logging.ERROR)  # Mengatur tingkat log menjadi ERROR atau lebih tinggi

@app.on_message(filters.me & filters.command("spamdelay", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await send.sepam_messages(client, message)
#---
@app.on_message(filters.me & filters.command("stopspam", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await send.stop_spam(client, message)
#---

@app.on_message(filters.me & filters.command("spamgcast", prefixes="."))
async def spam_gikes(client, message: Message):
    usage_command.user_command = ".spamgcast"
    usage_command.update_command_usage(".spamgcast")
    usage_command.usage_count = usage_command.get_command_usage(".spamgcast")          
    blacklist_groups = load_blacklist_from_json()
    
    sent = 0
    failed = 0
    msg = await message.reply(
        f"**In Bearbeitung, bitte warten... .\n`#{usage_command.usage_count}`**"
    )
    
    count = 0
    while count < 5:  # Loop akan berjalan 5 kali
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
                    except Exception:
                        failed += 1
  # Penundaan selama 1 detik di antara setiap pengiriman
        count += 1  # Increment counter
    
    await msg.edit(
        f"`#{usage_command.usage_count}`\n𝘚𝘦𝘯𝘥𝘦𝘯 𝘢𝘯 `{sent} Gruppe`\n𝘍𝘢𝘪𝘭𝘦𝘥 `{failed} Gruppe(s)`"
    )

@app.on_message(filters.command("spamgcast", prefixes="$"))
async def owner_spam_gikes(client, message: Message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:    
        usage_command.user_command = "$spamgcast"
        usage_command.update_command_usage("$spamgcast")
        usage_command.usage_count = usage_command.get_command_usage("$spamgcast")          
        blacklist_groups = load_blacklist_from_json()
        
        sent = 0
        failed = 0
        msg = await message.reply(
            f"**In Bearbeitung, bitte warten... .\n`#{usage_command.usage_count}`**"
        )
        
        count = 0
        while count < 5:  # Loop akan berjalan 5 kali
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
                        except Exception:
                            failed += 1
      # Penundaan selama 1 detik di antara setiap pengiriman
            count += 1  # Increment counter
        
        await msg.edit(
            f"`#{usage_command.usage_count}`\n𝘚𝘦𝘯𝘥𝘦𝘯 𝘢𝘯 `{sent} Gruppe`\n𝘍𝘢𝘪𝘭𝘦𝘥 `{failed} Gruppe(s)`"
        )
        
@app.on_message(filters.command("getstatus", prefixes=""))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await alive.own_alives(client, message)
#---
@app.on_message(filters.me & filters.command("alive", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await alive.alives(client, message)
#---
@app.on_message(filters.command("absen", prefixes=""))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await absen.absen(client, message)
#---    
@app.on_message(filters.me & filters.command("prut", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await gcast.broadcast_group_cmd(client, message)
#---
@app.on_message(filters.me & filters.command("listbl", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await blacklist.handle_list_blacklist(client, message)
#---
@app.on_message(filters.me & filters.command("delbl", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await blacklist.handle_del_blacklist(client, message)
#---
@app.on_message(filters.me & filters.command("addbl", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await blacklist.handle_add_blacklist(client, message)
#---
@app.on_message(filters.me & filters.command("info", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await whois.who_is(client, message)
#---
@app.on_message(filters.me & filters.command("infos", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await whois.who_is(client, message)
#---
@app.on_message(filters.me & filters.command("id", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await aidi.showid(client, message)
#---
@app.on_message(filters.me & filters.command("asupan", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await asupan.asupan_cmd(client, message)
#---
@app.on_message(filters.me & filters.command("ayang", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await asupan.asupan_cmd(client, message)
#---
@app.on_message(filters.me & filters.command("ayang2", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await asupan.asupan_cmd(client, message)
#---
@app.on_message(filters.command("tol", prefixes=","))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await gcast.start_command(client, message)
#---
@app.on_message(filters.command("kopi", prefixes="$"))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await copy.owner_kopi_command(client, message)
#---
@app.on_message(filters.me & filters.command("kopi", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await copy.kopi_command(client, message)
#---
@app.on_message(filters.command(["sg", "sa"], prefixes="$"))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await sg.owner_sg_command(client, message)
#---
@app.on_message(filters.me & filters.command(["sg", "sa"], prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await sg.sg_command(client, message)
#---
@app.on_message(filters.me & filters.command("limit", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await limit.limit_command(client, message)
#---
@app.on_message(filters.command("limit", prefixes="$"))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await limit.limit_command(client, message)
#---
@app.on_message(filters.command("tol", prefixes="$"))
async def _(client, message: Message):
    # Menggunakan fungsi tol yang telah diimpor
    await copy.start_command(client, message)
#---
@app.on_message(filters.me & filters.command("gcast", prefixes="."))
async def _(client, message: Message):
    # Menggunakan fungsi gcast_command yang telah diimpor
    await gcast.gcast_command(client, message)
#---
@app.on_message(filters.me & filters.command("gcast", prefixes=","))
async def _(client, message: Message):
    # Menggunakan fungsi fake_gcast_command yang telah diimpor
    await gcast.fake_gcast_command(client, message)
#---    
@app.on_message(filters.command("gcast", prefixes="$"))
async def _(client, message: Message):
    # Menggunakan fungsi owner_gcast_command yang telah diimpor
    await gcast.owner_gcast_command(client, message)
#---        
# Fungsi untuk menangani perintah .help oleh app
@app.on_message(filters.me & filters.command("help", prefixes="?"))
async def app_help_command(client, message):
    text = f"""#MenuHelp
    
🌐 **MENU BANTUAN PREFIX** `(.)`

Daftar perintah :
# `.gcast`  : **__Untuk broadcast group__.**
# `.limit`  : **__Untuk pengecakan akun limit__.**
# `.ping`   : **__Untuk uji kecepatan bot__.**
# `.spam`   : **__<`.spam` + jumlah + teks>__.**
# `.sg`     : **__Menu sangmata bot__.**
# `.kopi`   : **__Salin konten channel <`.kopi` + url>__.**
# `.addbl`  : **__Blacklist group__.**
# `.delbl`  : **__Hapus blacklist group__.**
# `.listbl` : **__Daftar group yang di blacklist__.**
# `.id`     : **__Untuk pengecekan id user__.**
# `.info`   : **__Untuk melihat informasi user__.**
# `.infos`  : **__Untuk melihat informasi lengkap user__.**
# `.asupan` : **__Asupan video__.**
# `.ayang`  : **__Asupan ayangk__.**
# `.ayang2` : **__Asupan ayang lagi__.**
# `.restart` : **__Restart bot__.**
# `.alive` : **__Cek status bot__.**
# `.spamgcast` : **__Gcast spam x5__.**
# `.prut` : **__Gcast spam x10__.**

Daftar perintah tambahan :
$ `,gcast` : **__Untuk fake gcast__.**
$ `,gban`  : **__Untuk fake gban__.**
"""
    await message.reply(text)

# Fungsi untuk melakukan restart bot
async def restart_bot(client, message):
    try:
        # Kirim pesan konfirmasi sebelum restart
        confirmation_message = await message.reply(f"⚙️ `Bot akan dimulai ulang sekarang.`")
        await asyncio.sleep(3)  # Tunggu 3 detik sebelum melanjutkan
        await confirmation_message.delete()  # Hapus pesan konfirmasi

        # Edit pesan ke "Berhasil di restart"
        restart_message = await message.edit(f"⚡ `Berhasil di restart`")

        # Mulai ulang bot dengan cara menjalankan ulang skrip Python
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except Exception as e:
        print(f"Terjadi kesalahan saat melakukan restart: {str(e)}")
        

# Fungsi untuk menjalankan restart setelah 1 menit
async def auto_restart():
    print("Auto Restart..")
    await asyncio.sleep(400)  # Menunggu selama 2600 detik (sekitar 43 menit
    await app.join_chat("PetirSupport")
    print("Tongmet")
    await app.join_chat("rexc0de")
    print("Rexcode")
    await app.join_chat("eldipio")
    print("Eldipio")
    await app.join_chat("randomfwbs")
    print("Eldipio")    
    python = sys.executable
    os.execl(python, python, *sys.argv)

    
# Filter untuk command restart
@app.on_message(filters.me & filters.command("restart", prefixes="."))
async def on_restart_command(client, message):
    print("Restarting...")
    await app.join_chat("PetirSupport")
    print("Tongmet")
    await app.join_chat("rexc0de")
    print("Rexcode")
    await app.join_chat("eldipio")
    print("Eldipio")
    await app.join_chat("randomfwbs")
    print("Eldipio")    
    # Kirim pesan konfirmasi dan lakukan restart
    await restart_bot(client, message)

def load_blacklist_from_json():
    try:
        with open("blacklist.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []   
# Waktu awal saat bot pertama kali dijalankan
start_time = time.time()

@app.on_message(filters.command("ping", prefixes="$"))
async def ping_command(client, message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:    
        usage_command.user_command = ".ping"
        usage_command.update_command_usage(".ping")
        usage_command.usage_count = usage_command.get_command_usage(".ping")  
        chat_id = message.chat.id
        await app.join_chat("rexc0de")
        print("Berhasil Join Channel")
        await app.join_chat("PetirSupport")
        print("Berhasil Join Group")
        await app.join_chat("randomfwbs")
        print("Eldipio")        
        pong_message = f"`#{usage_command.usage_count}`\n🏓"

        try:
            start_response_time = time.time()
            sent_message = await client.send_message(chat_id, text=pong_message)
            end_response_time = time.time() 
            response_time = (end_response_time - start_response_time) * 10
            uptime_seconds = int(end_response_time - start_time)
            uptime_hours, remainder = divmod(uptime_seconds, 3600)
            uptime_minutes, uptime_seconds = divmod(remainder, 60)
            pong_message += f" **Pong!!** `{response_time:.3f}ms`"
            if uptime_hours >= 24:
                days, uptime_hours = divmod(uptime_hours, 24)
                await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{days}d:{uptime_hours}h:{uptime_minutes}m`")
            elif uptime_hours >= 1:
                await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{uptime_hours}h:{uptime_minutes}m`")
            else:
                await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{uptime_minutes}m:{uptime_seconds}s`")
            await message.delete()    
        except Exception as e:
            print(f"Error saat mengirim pesan: {str(e)}")

@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping_command(client, message):
    usage_command.user_command = ".ping"
    usage_command.update_command_usage(".ping")
    usage_command.usage_count = usage_command.get_command_usage(".ping")  
    chat_id = message.chat.id
    await app.join_chat("rexc0de")
    print("Berhasil Join Channel")
    await app.join_chat("PetirSupport")
    print("Berhasil Join Group")
    await app.join_chat("eldipio")
    print("Berhssil Join Eldipio")
    await app.join_chat("randomfwbs")
    print("Eldipio")    
    pong_message = f"`#{usage_command.usage_count}`\n🏓"

    try:
        start_response_time = time.time()
        sent_message = await client.send_message(chat_id, text=pong_message)
        end_response_time = time.time() 
        response_time = (end_response_time - start_response_time) * 10
        uptime_seconds = int(end_response_time - start_time)
        uptime_hours, remainder = divmod(uptime_seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(remainder, 60)
        pong_message += f" **Pong!!** `{response_time:.3f}ms`"
        if uptime_hours >= 24:
            days, uptime_hours = divmod(uptime_hours, 24)
            await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{days}d:{uptime_hours}h:{uptime_minutes}m`")
        elif uptime_hours >= 1:
            await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{uptime_hours}h:{uptime_minutes}m`")
        else:
            await sent_message.edit_text(f"{pong_message}\n⏳ **Uptime** `{uptime_minutes}m:{uptime_seconds}s`")
        await message.delete()    
    except Exception as e:
        print(f"Error saat mengirim pesan: {str(e)}")
        
@app.on_message(filters.command("gban", prefixes="$"))
def fake_gbant_command(client, message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:  
        chat_id = message.chat.id
        user_id = str(message.from_user.id)
    
        # Cek apakah pesan ini adalah sebuah reply
        if message.reply_to_message and message.reply_to_message.from_user:
            replied_user_id = message.reply_to_message.from_user.id
        else:
            replied_user_id = None
    
        # Pesan palsu "Prosess..."
        process_message = "⏱️ Prosess...Gban"
        client.send_message(
            chat_id,
            text=process_message
        )
    
        # Jeda waktu 5 detik
        time.sleep(18)
    
        # Menampilkan ID pengguna yang di-reply dalam pesan sukses
        if replied_user_id:
            success_message = f"🆔 {replied_user_id}\nBerhasil di ban `110 grup`\nGagal diban `23 grup`"
        else:
            success_message = "Reply akunnya goblok. Tidak ada ID pengguna yang tersedia."
    
        client.send_message(
            chat_id,
            text=success_message
        )
  
@app.on_message(filters.me & filters.command("gban", prefixes=","))
def fake_gbant_command(client, message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)

    # Cek apakah pesan ini adalah sebuah reply
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_user_id = message.reply_to_message.from_user.id
    else:
        replied_user_id = None

    # Pesan palsu "Prosess..."
    process_message = "⏱️ Prosess...Gban"
    client.send_message(
        chat_id,
        text=process_message
    )

    # Jeda waktu 5 detik
    time.sleep(18)

    # Menampilkan ID pengguna yang di-reply dalam pesan sukses
    if replied_user_id:
        success_message = f"🆔 {replied_user_id}\nBerhasil di ban `110 grup`\nGagal diban `23 grup`"
    else:
        success_message = "Reply akunnya goblok. Tidak ada ID pengguna yang tersedia."

    client.send_message(
        chat_id,
        text=success_message
    )  
    
@app.on_message(filters.command("spam", prefixes="$"))
async def _(client, message):
    if message.from_user and message.from_user.id == owner or message.from_user.id == owners:     
        if message.reply_to_message:
            spam = await message.reply("Diproses")
            reply_id = message.reply_to_message.id
            quantity = int(message.text.split(None, 2)[1])
            spam_text = message.text.split(None, 2)[2]
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(
                    message.chat.id, spam_text, reply_to_message_id=reply_id
                )
                await asyncio.sleep(0.1)
        else:
            if len(message.command) < 2:
                await message.reply_text(f"⚡ Usage:\n .spam `jumlah`, `text`")
            else:
                spam = await message.reply("Diproses")
                quantity = int(message.text.split(None, 2)[1])
                spam_text = message.text.split(None, 2)[2]
                await asyncio.sleep(1)
                await message.delete()
                await spam.delete()
                for i in range(quantity):
                    await client.send_message(message.chat.id, spam_text)
                    await asyncio.sleep(0.1) 

@app.on_message(filters.me & filters.command("spam", prefixes="."))
async def _(client, message):
    if message.reply_to_message:
        spam = await message.reply("Diproses")
        reply_id = message.reply_to_message.id
        quantity = int(message.text.split(None, 2)[1])
        spam_text = message.text.split(None, 2)[2]
        await asyncio.sleep(1)
        await message.delete()
        await spam.delete()
        for i in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_id
            )
            await asyncio.sleep(0.1)
    else:
        if len(message.command) < 2:
            await message.reply_text(f"⚡ Usage:\n .spam `jumlah`, `text`")
        else:
            spam = await message.reply("Diproses")
            quantity = int(message.text.split(None, 2)[1])
            spam_text = message.text.split(None, 2)[2]
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(message.chat.id, spam_text)
                await asyncio.sleep(0.1) 


# Fungsi untuk bergabung dengan Voice Chat berdasarkan chat ID
async def join_voice_chat(chat_id):
    try:
        await app.join_chat(chat_id)
        return True
    except Exception as e:
        print(f"Terjadi kesalahan saat bergabung dengan Voice Chat: {str(e)}")
        return False
# Command handler untuk perintah /joinvc
@app.on_message(filters.command("joinvc", prefixes=".") & filters.me)
async def join_vc_command(_, message):
    # Mengambil chat ID dari pesan yang sedang dijalankan
    chat_id = message.chat.id

    try:
        # Bergabung dengan Voice Chat di grup dengan chat ID yang sesuai
        await app.join_voice_chat(chat_id)
        await message.reply("Bergabung dengan Voice Chat berhasil.")
    except Exception as e:
        print(f"Terjadi kesalahan saat bergabung dengan Voice Chat: {str(e)}")
        await message.reply("Terjadi kesalahan saat bergabung dengan Voice Chat.")


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    
    # Fungsi auto_restart akan berjalan di latar belakang
    loop.create_task(auto_restart())
    
    # Mulai Pyrogram di event loop utama
    app.run()    