
from bot.drivefunc.gdriveUpload import mydrive
import asyncio
from bot.helper.utils import Human_size
from pyrogram import Client, Filters


@Client.on_message(Filters.regex(r"^https://drive.google.com"))
async def clone_to_gdrive(c, m):
    url = m.text.strip()
    ID = str(m.from_user.id)
    if "/folders/" in url:
        await m.reply_text("` Currently Folder Clone Is not avalible ... !!`")
        return
    sentm = await m.reply_text("`Trying To clone Your Google  Drive File ... !!`")

    loop = asyncio.get_event_loop()
    name, size, drivelink, error = await loop.run_in_executor(None, driveclone, url, ID)

    if drivelink is not None:
        await sentm.edit(f"Filename: `{name}`\n Size : `{Human_size(size)}`\nLink : {drivelink}")
    else:
        await sentm.edit("`Make Sure You Have Enough Permission For This file ....\n #error`")


def driveclone(url, ID):
    mdrive = mydrive(ID)
    name, size, link, e = mdrive.clone(url)
    return name, size, link, e
