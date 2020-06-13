
from bot.drivefunc.gdriveUpload import mydrive
import asyncio
from bot.helper.utils import Human_size
from pyrogram import Client, Filters,StopPropagation
from bot.helper.check_channel import inChannel
from bot.helper.send_join import sendJoinmsg


@Client.on_message(Filters.regex(r"^https://drive.google.com"))
async def clone_to_gdrive(c, m):
    
    url = m.text.strip()
    ID = str(m.from_user.id)
    
    sentm = await m.reply_text("`Trying To clone Your Google  Drive File or Folder ... !!`")

    loop = asyncio.get_event_loop()
    try:
        name, size, drivelink, error = await loop.run_in_executor(None, driveclone, url, ID)
    except Exception as e:
        await sentm.edit("`Make Sure You Have Enough Permission For This file ....\n #error`")
        return

    
    if size:
            await sentm.edit(f"Filename: `{name}`\nSize : `{Human_size(size)}`\nLink : {drivelink}")
    else:
            await sentm.edit(f"Folder: `{name}`\n\n{drivelink}")
    


def driveclone(url, ID):
    mdrive = mydrive(ID)
    try:
        name, size, link, e = mdrive.clone(url)
    except Exception as e:
        raise e
    return name, size, link, e
