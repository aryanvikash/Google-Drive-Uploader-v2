from bot.helper.progress_pyro import get_progress
import time

from bot import LOGGER , TgFileDownloadlist
from pyrogram import Client, Filters,StopPropagation , InlineKeyboardButton, InlineKeyboardMarkup
from bot.drivefunc.Tokenverify import token_make
from bot.helper.check_channel import inChannel
from bot.helper.send_join import sendJoinmsg
from bot.uploadHandler.upload import upload_handler


@Client.on_message(Filters.media)
async def Document_Downloader(client, message):

    await extrastuffs(client,message)
    user_id = str(message.from_user.id)
    if user_id in TgFileDownloadlist:
        await message.reply_text(
            "`Multiple Telegram File Download is Not allowed at a same time !!"
            "\nPlease Wait For Complete Your Download `")
        return
    sentm = await message.reply_text("Processing Your File....")
    s_time = time.time()
    try:
        TgFileDownloadlist.append(user_id)
        filename = await message.download(progress=get_progress, progress_args=(
                        "Download Started ...", sentm, s_time))
        if filename is not None:
            await upload_handler(filename, sentm)
    except Exception as e:
        LOGGER.error(e)
        await sentm.edit(e)
    finally:
        TgFileDownloadlist.remove(user_id)


            



async def extrastuffs(client,message):
    # channel check
    if not await inChannel(client ,message):
        await sendJoinmsg(message)
        raise StopPropagation

    # Auth check
    if not token_make(client, message):
        await message.reply_text("You havn't authenticated me. Use /login to authorize me.")
        raise StopPropagation