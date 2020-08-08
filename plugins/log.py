from pyrogram import Client, Filters
from bot import adminList


@Client.on_message(Filters.command(["log", "logs"]) & Filters.user(adminList))
async def get_logs(c, m):
    await m.reply_document(document="log.txt")
