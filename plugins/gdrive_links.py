
from bot.drivefunc.gdriveUpload import mydrive
import asyncio
from bot.helper.utils import Human_size
from pyrogram import Client, Filters


@Client.on_message(Filters.regex(r"^https://drive.google.com"))
async def clone_to_gdrive(c, m):
    url = m.text.strip()
    ID = str(m.from_user.id)
    
    sentm = await m.reply_text("`Trying To clone Your Google  Drive File or Folder ... !!`")

    loop = asyncio.get_event_loop()
    name, size, drivelink, error = await loop.run_in_executor(None, driveclone, url, ID)

    if drivelink is not None:
        if size:
            await sentm.edit(f"Filename: `{name}`\nSize : `{Human_size(size)}`\nLink : {drivelink}")
        else:
            await sentm.edit(f"Folder: `{name}`\n\n{drivelink}")
    else:
        await sentm.edit("`Make Sure You Have Enough Permission For This file ....\n #error`")


def driveclone(url, ID):
    mdrive = mydrive(ID)
    name, size, link, e = mdrive.clone(url)
    return name, size, link, e
