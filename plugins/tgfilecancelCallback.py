
from pyrogram import Client, filters
from bot import (LOGGER, TgFileDownloadlist)


@Client.on_callback_query(filters.regex(r"^tgcancel||"))
async def cancel_tgfile(c, m):
    cancelUserid = m.data.split("||")[-1].strip()
    try:
        TgFileDownloadlist[cancelUserid]= False
        await c.answer_callback_query(
                callback_query_id=m.id,
                text="Download cancelled",
                show_alert=True,
                cache_time=0)
    except KeyError:
        await c.answer_callback_query(
                callback_query_id=m.id,
                text="Download Not Found ❌ ",
                show_alert=True,
                cache_time=0)