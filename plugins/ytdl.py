import subprocess
import asyncio
import os
from bot import LOGGER, DOWNLOAD_LOCATION
from bot.helper.utils import Human_size
from bot.drivefunc.gdriveUpload import gupload
from pyrogram import Client, Filters
from bot.customFilters.m3u8_filter import is_m3u8
# url = "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8"


@Client.on_message(is_m3u8())
async def ytdl(c, m):
    ID = str(m.from_user.id)
    url = m.text.strip()
    if url.endswith("m3u8"):
        command = ['youtube-dl', "--no-warnings",
                   "--youtube-skip-dash-manifest", url]
        sentm = await m.reply_text("Trying to download m3u8 file ...!!")
        process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE, )
        stdout, stderr = await process.communicate()
        filename = await m3u8_path(stdout)
        path = os.path.join(DOWNLOAD_LOCATION, filename)
        loop = asyncio.get_event_loop()
        LOGGER.info(f"M3u8 File Download complete :{path}")
        await sentm.edit("Download Complete !! now Uploading")
        DriveLink = await loop.run_in_executor(None, gupload, path, ID)
        size = os.path.getsize(path)
        await sentm.edit(f"Filename: `{filename}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
        LOGGER.info(f" m3u8 : {filename} Upload Complete cleaning file")
        os.remove(path)

    else:
        pass


async def m3u8_path(out):
    output = out.decode('utf-8').strip()
    print(output, "\n")
    output = output.split("into")[1]
    path = output.split("\n")[0].replace('"', " ").strip()
    return path
