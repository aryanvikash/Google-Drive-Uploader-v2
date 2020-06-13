from pyrogram import Client, Message, StopPropagation
from bot.drivefunc.Tokenverify import is_token , token_make
from bot.helper.check_channel import inChannel
from bot.helper.send_join import sendJoinmsg

@Client.on_message(group=-1)
async def checkauthfunc(c: Client, m: Message):
    
    #channel User checker
    if not await inChannel(c ,m):
        await sendJoinmsg(m)
        raise StopPropagation
    
    if is_token(m):
        return
    is_created = token_make(c, m)
    if is_created:
        pass
    else:
        await m.reply_text("You havn't authenticated me. Use /login to authorize me.")
        raise StopPropagation
