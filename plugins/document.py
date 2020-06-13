from bot.helper.progress_pyro import get_progress
import time
import os
from bot.drivefunc.gdriveUpload import gupload
from bot.helper.utils import Human_size
import asyncio
from bot import LOGGER , TgFileDownloadlist
from pyrogram import Client, Filters,StopPropagation , InlineKeyboardButton, InlineKeyboardMarkup
from bot.drivefunc.Tokenverify import token_make
from bot.helper.check_channel import inChannel
from bot.helper.send_join import sendJoinmsg


@Client.on_message(Filters.media)
async def Document_Downloader(client, message):
    
    # channel check
    if not await inChannel(client ,message):
        await sendJoinmsg(message)
        raise StopPropagation
    
    
    # Auth check 
    if not token_make(client, message):
        await message.reply_text("You havn't authenticated me. Use /login to authorize me.")
        raise StopPropagation
    
        
    ID = str(message.from_user.id)
    if ID in TgFileDownloadlist:
        await message.reply_text("`Multiple Telegram File Download is Not allowed at a same time !!\nPlease Wait For Complete Your Download `")
        return
    sentm = await message.reply_text("Processing Your File....")
    s_time = time.time()
    try:
        TgFileDownloadlist.append(ID)
        filename = await message.download(progress=get_progress, progress_args=("Download Started ...", sentm, s_time))
        TgFileDownloadlist.remove(ID)

    except Exception as e:
        TgFileDownloadlist.remove(ID)
        LOGGER.error(e)

    if filename is not None:
        await sentm.edit("Downloading Complete !! Uplaoding File")
        loop = asyncio.get_event_loop()
        try:
            DriveLink = await loop.run_in_executor(None, gupload, filename, ID)
        except Exception as e:
            LOGGER.info(f"Document Upload error : {e} ")
            await sentm.edit("Failed To upload Your Telegram File  !!")
            return
            
        
        # DriveLink = gupload(filename,ID)
        size = os.path.getsize(filename)
        if DriveLink is not None:
            DownloadButton=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=DriveLink)] ])
            await sentm.edit(f"Filename: `{os.path.basename(filename)}` \n\nSize : `{Human_size(size)}` " ,reply_markup=DownloadButton)
            
            LOGGER.info(f"Upload Complete {filename} Now Cleaning Disk")
        else:
            await sentm.edit("Uploading Failed !!")
            LOGGER.error(f"Telegram File {filename}Uploading error Removing File")
            
        try:
            os.remove(filename)
        except Exception as  e:
            LOGGER.error(f"Telegram File remove {e} Uploading error Removing File")
