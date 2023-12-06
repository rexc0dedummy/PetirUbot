print("install id.py")
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import Message

from config import app, owner, owners

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(filters.command("id", prefixes=".") & filters.me)
async def showid(_, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = ""
    text += f"<b><a href={message.link}>Message ID:</a></b> <code>{message_id}</code>\n"
    text += (
        f"<b><a href=tg://user?id={your_id}>Your ID:</a></b> <code>{your_id}</code>\n"
    )

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await _.get_users(split)).id
            text += f"<b><a href=tg://user?id={user_id}>User ID:</a></b> <code>{user_id}</code>\n"
        except Exception:
            return await message.reply("This user doesn't exist.")

    text += f"<b><a href=https://t.me/{chat.username}>Chat ID:</a></b> <code>{chat.id}</code>\n\n"

    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += (
            f"<b><a href=tg://user?id={id_}>Replied User ID:</a></b> <code>{id_}</code>"
        )

    await message.reply(text, disable_web_page_preview=True)
    await message.delete()  