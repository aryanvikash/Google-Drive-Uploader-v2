from pyrogram import Client, Message, StopPropagation
from bot.drivefunc.Tokenverify import token_make


@Client.on_message(group=-1)
async def checkauthfunc(c: Client, m: Message):
    is_created = token_make(c, m)
    if is_created:
        pass
    else:
        await m.reply_text("You havn't authenticated me. Use /login to authorize me.")
        raise StopPropagation
