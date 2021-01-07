import os

from pyaiodl.errors import DownloadNotActive
from pyrogram import Client, filters
from bot import (LOGGER, dl)


@Client.on_callback_query(filters.regex("^cancel"))
async def cancel_aria(c, m):
    cb_data = m.data
    if cb_data.startswith("cancel"):
        uuid = cb_data.split("||")[-1].strip()
        file = await dl.status(uuid)
        try:
            await dl.cancel(uuid)
        except DownloadNotActive:
            await c.answer_callback_query(
                callback_query_id=m.id,
                text="Download Not Found ❌ ",
                show_alert=True,
                cache_time=0)
            return
        if not file["complete"]:
            LOGGER.info(f"GID : {uuid} cancelled Successfully  Cleaning Storage .. ")
            os.remove(file["download_path"])
        else:
            await c.answer_callback_query(
                callback_query_id=m.id,
                text=" Download Already Completed 😁",
                show_alert=True,
                cache_time=0)
            LOGGER.info(f"{uuid}  is Already Completed ")
