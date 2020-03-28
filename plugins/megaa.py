from mega import Mega
import os
import asyncio
from bot.helper.utils import Human_size
from bot import DOWNLOAD_LOCATION, LOGGER, Creds_path
from bot.drivefunc.gdriveUpload import gupload
from pyrogram import Client,Filters
from bot.customFilters.authchecker import is_auth

@Client.on_message(Filters.regex(r"^https://mega.") & is_auth())
async def mega_download(c, message):
    # await message.reply_text("No Support For Mega links😒 ")
    # return
    sentm = await message.reply_text("Downloading... Mega Link Was Always Slow..😒 ")

    url = message.text.strip()
    ID = str(message.from_user.id)
    loop = asyncio.get_event_loop()
    try:
        # mega Download
        name = await loop.run_in_executor(None, async_megadl, url)
        filename = os.path.join(DOWNLOAD_LOCATION, name)
        await sentm.edit("Mega Download Complete ....!! Now Uploading !!")
        # Uploading
        DriveLink = await loop.run_in_executor(None, gupload, filename, ID)
        LOGGER.info(f"mega : {name} : Upload complete")
        size = os.path.getsize(filename)
        await sentm.edit(f"Filename: `{name}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
        os.remove(filename)
    except Exception as e:
        LOGGER.error(e)
        await sentm.edit(f"Wew You Got An Error 😮!! \n\n`{e}`\n\nMake Sure It was a file Link \n\n#error")
        return


def async_megadl(url):
    mega = Mega()
    mag = mega.login("bearyan8@yandex.com", "bearyan8@yandex.com")
    try:
        name = mag.download_url(url)
    except Exception as e:
        LOGGER.error(e)
    LOGGER.info(f"Mega  {name} Download Completed Now uploading...")

    return name

    # await loop.run_in_executor(None, gupload,filename,ID)
