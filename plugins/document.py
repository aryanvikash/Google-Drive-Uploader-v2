from bot.helper.progress_pyro import get_progress
import time
import os
from bot.drivefunc.gdriveUpload import gupload
from bot.helper.utils import Human_size
import asyncio
from bot import LOGGER
from bot.customFilters.authchecker import is_auth_user
from pyrogram import Client ,Filters
from bot.customFilters.authchecker import is_auth

@Client.on_message(Filters.media & is_auth())
async def Document_Downloader(client, messsage):
    ID = str(messsage.from_user.id)
    if not is_auth_user(ID):
        await messsage.reply_text("You Are Not Authorized Please Use /login")
        return
    sentm = await messsage.reply_text("Processing Your File....")
    s_time = time.time()
    try:
        filename = await messsage.download(progress=get_progress, progress_args=("Download Started ...", sentm, s_time))

    except Exception as e:
        LOGGER.error(e)

    if filename is not None:
        await sentm.edit("Downloading Complete !! Uplaoding File")
        loop = asyncio.get_event_loop()
        DriveLink = await loop.run_in_executor(None, gupload, filename, ID)
        # DriveLink = gupload(filename,ID)
        size = os.path.getsize(filename)
        if DriveLink is not None:
            await sentm.edit(f"Filename: `{os.path.basename(filename)}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
            os.remove(filename)
            LOGGER.info(f"Upload Complete {filename} Now Cleaning Disk")
        else:
            await sentm.edit("Uploading Failed !!")
            LOGGER.error(f"Telegram File {filename}Uploading error Removing File")
            os.remove(filename)
