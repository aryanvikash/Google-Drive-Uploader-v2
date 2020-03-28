# import asyncio
import aria2p
import os
from bot import (DownloadDict, LOGGER, aria2, is_admin)
import time
from pyrogram import Client,Filters
from bot.customFilters.authchecker import is_auth

@Client.on_message(Filters.command(["cancel"]))
async def cancel(client, message):
    uid = message.from_user.id
    # gid = DownloadDict[uid]
    if len(message.command) > 1:
        gid = message.command[1]

        sentm = await message.reply_text("Searching Your Download 🔎")
        try:
            file = aria2.get_download(gid)
        except Exception as e:
            print(e)
            await sentm.edit("Download Not Found ❌")
            return
        complete = file.is_complete
        if file is not complete and uid in DownloadDict or file is not complete and is_admin(uid):
            file.remove(force=True)
            time.sleep(1)
            if file is not file.is_removed:
                await sentm.edit(f"Download Cancelled Successfully 🎉🎉")
                # DownloadDict[gid].remove()
                LOGGER.info(f"GID : {gid} cancelled Successfully  Cleaning Storage .. ")
                os.remove(file.name)
            else:
                await sentm.edit("Failed To Cancel Download ")
                LOGGER.info(f"Your File Is not Cancelled GID : {gid} ")
        else:
            await sentm.edit("You Don't Have any Active Download With This GID")
    else:
        await message.reply_text("Give Me GID of Your Downloads .. ")
        return
