from bot.util.progress_pyro import get_progress
import time
import asyncio
from bot import LOGGER , TgFileDownloadlist


from pyrogram import Client, filters,StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

from bot.drivefunc.Tokenverify import token_make
from bot.util.check_channel import inChannel
from bot.util.send_join import sendJoinmsg
from bot.uploadHandler.upload import upload_handler


@Client.on_message(filters.media)
async def Document_Downloader(client, message):

    await extrastuffs(client,message)
    user_id = str(message.from_user.id)

    try:
        if TgFileDownloadlist[user_id]:
            await message.reply_text(
                "`Multiple Telegram File Download is Not allowed at a same time !!"
                "\nPlease Wait For Complete Your Download `")
            return
    except :
        pass
        
    sentm = await message.reply_text("Hold on !! Preparing For Download...")
    s_time = time.time()
    try:
        TgFileDownloadlist[user_id]={}
        TgFileDownloadlist[user_id] = True
        # print(sentm)
        # return
        filename = await message.download(progress=get_progress, progress_args=(
                        "Downloading", sentm, s_time,client,user_id))
        if filename is not None:
            await upload_handler(filename, sentm)
        else:
            if TgFileDownloadlist[user_id] == False:
                await sentm.edit(f"`Download Cancelled`")
            else:
                await sentm.edit(f"`Download Stopped Due To Some Unknow reason`")
        
    except FloodWait as fw:
        LOGGER.error(fw)
        await message.reply_text(f"FloodWait Sleeping For {fw.x}")

        await asyncio.sleep(fw.x)




        
    finally:
        TgFileDownloadlist[user_id] = False


            



async def extrastuffs(client,message):
    # channel check
    if not await inChannel(client ,message):
        await sendJoinmsg(message)
        raise StopPropagation

    # Auth check
    if not token_make(client, message):
        await message.reply_text("You havn't authenticated me. Use /login to authorize me.")
        raise StopPropagation