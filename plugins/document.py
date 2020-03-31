from bot.helper.progress_pyro import get_progress
import time
import os
from bot.drivefunc.gdriveUpload import gupload
from bot.helper.utils import Human_size
import asyncio
from bot import LOGGER , TgFileDownloadlist
from pyrogram import Client, Filters


@Client.on_message(Filters.media)
async def Document_Downloader(client, messsage):
    ID = str(messsage.from_user.id)
    if ID in TgFileDownloadlist:
        await messsage.reply_text("`Multiple Telegram File Download is Not allowed at a same time !!\nPlease Wait For Complete Your Download `")
        return
    sentm = await messsage.reply_text("Processing Your File....")
    s_time = time.time()
    try:
        TgFileDownloadlist.append(ID)
        filename = await messsage.download(progress=get_progress, progress_args=("Download Started ...", sentm, s_time))
        TgFileDownloadlist.remove(ID)

    except Exception as e:
        TgFileDownloadlist.remove(ID)
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
