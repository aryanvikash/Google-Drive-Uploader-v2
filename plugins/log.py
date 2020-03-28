from bot.customFilters.admin_filter import is_admin
from pyrogram import Client , Filters

@Client.on_message(Filters.command(["log"])&is_admin())
async def get_logs(c,m):
    await m.reply_document(document="log.txt")