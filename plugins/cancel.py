import os
from bot import (DownloadDict, LOGGER, aria2, is_admin)
import time
from pyrogram import Client, Filters
import asyncio


@Client.on_callback_query(Filters.regex("^cancel"))
async def cancel_aria(c, m):
    cb_data = m.data
    if cb_data.startswith("cancel"):
        gid = cb_data.split("||")[-1].strip()
        try:
            file = aria2.get_download(gid)
        except Exception as e:
            print(e)
            await c.answer_callback_query(
                callback_query_id=m.id,
                text="Download Not Found❌  ",
                show_alert=True,
                cache_time=0)
            return
        complete = file.is_complete
        if file is not complete:
            file.remove(force=True)
            await asyncio.sleep(1)
            if file is not file.is_removed:
                await c.answer_callback_query(
                    callback_query_id=m.id,
                    text="Download Cancelled ✅ ",
                    show_alert=True,
                    cache_time=0)

                # DownloadDict[gid].remove()
                LOGGER.info(f"GID : {gid} cancelled Successfully  Cleaning Storage .. ")
                os.remove(file.name)
            else:

                LOGGER.info(f"Your File Is not Cancelled GID : {gid} ")
                await m.reply_text("Failed To cancel")


@Client.on_message(Filters.command(["cancel"]))
async def cancel(_, message):
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
                await sentm.edit("Download Cancelled Successfully 🎉🎉")
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
