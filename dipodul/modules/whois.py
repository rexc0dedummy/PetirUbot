print("install whois.py")

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardButton, Message, User

from config import app, owner, owners

def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


def userdata():
    button = [
        [
            InlineKeyboardButton(text="UserLink", callback_data="userlink"),
            InlineKeyboardButton(text="Description", callback_data="description"),
        ],
    ]
    return button


infotext = (
    "<b><a href=tg://user?id={user_id}>{full_name}</a></b>\n"
    " <b>• ID Pengguna:</b> <code>{user_id}</code>\n"
    " <b>• Nama Depan:</b> <code>{first_name}</code>\n"
    " <b>• Nama Belakang:</b> <code>{last_name}</code>\n"
    " <b>• Username:</b> {username}\n"
    " <b>• DC:</b> {dc_id}\n"
    " <b>• Status:</b> {status}\n"
    " <b>• Apakah Penipu:</b> {scam}\n"
    " <b>• Apakah Bot:</b> {bot}\n"
    " <b>• Apakah Premium:</b> {premium}\n"
    " <b>• Diverifikasi:</b> {verifies}\n"
    " <b>• Apakah Kontak:</b> {contact}\n"
    " <b>• Total Grup yang Sama:</b> {common}"
)


@app.on_message(filters.command(["whoiss", "infos"], prefixes=".") & filters.me)
async def who_is(client, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except RPCError:
            pass
    try:
        user = await client.get_users(get_user)
        msg = await message.reply(
            f"<b>🔄 Sedang Mengumpulkan Data Dari {user.mention}</b>"
        )
        await msg.delete()
    except RPCError:
        await message.reply("Saya tidak tahu Pengguna itu.")
        return
    common = await client.get_common_chats(user.id)
    # countpf = await client.get_chat_photos_count(user.id)
    async for pfp in client.get_chat_photos(user.id, 1):
        if pfp:
            await client.send_photo(
                message.chat.id,
                pfp.file_id,
                caption=infotext.format(
                    full_name=FullName(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                    dc_id=user.dc_id or "1",
                    status=user.status or "None",
                    premium=user.is_premium,
                    scam=user.is_scam,
                    bot=user.is_bot,
                    verifies=user.is_verified,
                    contact=user.is_contact,
                    common=len(common),
                ),
                reply_to_message_id=message.reply_to_message.id
                if message.reply_to_message
                else None,
            )
        else:
            await message.reply(
                infotext.format(
                    full_name=FullName(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                    dc_id=user.dc_id or "1",
                    status=user.status or "None",
                    premium=user.is_premium,
                    scam=user.is_scam,
                    bot=user.is_bot,
                    verifies=user.is_verified,
                    contact=user.is_contact,
                    common=len(common),
                ),
                disable_web_page_preview=True,
            )
    await message.delete()  

@app.on_callback_query(filters.regex("userlink"))
async def userlink(client, callback_query, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except RPCError:
            pass
    try:
        user = await client.get_users(get_user)
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        await callback_query.answer(
            f"User permanent link: <a href='tg://user?id={user.id}'>{fullname}</a>",
            show_alert=True,
        )
    except:
        return


@app.on_callback_query(filters.regex("description"))
async def userlink(client, callback_query):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except RPCError:
            pass
    try:
        user = await client.get_users(get_user)
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        await callback_query.answer(
            f"User Bio: {bio}",
            show_alert=True,
        )
    except:
        return


@app.on_message(filters.command(["whois", "info"], prefixes=".") & filters.me)
async def who_is(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
        Man = await message.reply("<code>Processing</code>")
        await Man.delete()
        username = f"@{user.username}" if user.username else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        out_str = f"""<b>UserInfo:</b>
    <b>name: {fullname}</b>
    <b>user_id:</b> <code>{user.id}</code>
    <b>username:</b> <code>{username}</code>
    <b>dc_id:</b> <code>{dc_id}</code>
"""
        await message.reply(
            out_str,
            disable_web_page_preview=True,
        )
    except Exception:
        return await message.reply("<code>cannot find the user.</code>")
    await message.delete()  

@app.on_message(filters.command(["chatinfo", "cinfo", "ginfo"], prefixes=".") & filters.me)
async def chatinfo_handler(client, message):
    Man = await message.reply("<code>Processing</code>")
    await Man.delete()
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.reply(
                    f"Gunakan perintah ini di dalam grup atau gunakan <code>{PREFIXES}chatinfo [group username atau id]</code>"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>CHAT INFORMATION:</b>
    <b>Chat ID:</b> <code>{chat.id}</code>
    <b>Title:</b> {chat.title}
    <b>Username:</b> {username}
    <b>Type:</b> <code>{type}</code>
    <b>DC ID:</b> <code>{dc_id}</code>
    <b>Total members:</b> <code>{chat.members_count}</code>
    <b>online_members:</b> <code>{chat.online_count}</code>
    <b>Description:</b>
    <code>{description}</code>
"""
        await message.reply(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await message.reply(f"<b>INFO:</b> <code>{e}</code>")
    await message.delete()  