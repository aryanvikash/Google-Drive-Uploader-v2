from pyrogram import Client, Message, StopPropagation
from bot.drivefunc.Tokenverify import is_token, token_make
from bot.util.check_channel import inChannel
from bot.util.send_join import sendJoinmsg
import re


@Client.on_message(group=-1)
async def checkauthfunc(c: Client, m: Message):
    # channel User checker
    if not await inChannel(c, m):
        await sendJoinmsg(m)
        raise StopPropagation

    if re.match(r"\w/(.{55})", m.text):
        return
    is_created = token_make(c, m)
    if is_created:
        pass
    else:
        await m.reply_text("You haven't authenticated me. Use /login to authorize me.")
        raise StopPropagation
