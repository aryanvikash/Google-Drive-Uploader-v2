from pyrogram import Client, filters
from bot import adminList


@Client.on_message(filters.command(["log", "logs"]) & filters.user(adminList))
async def get_logs(c, m):
    await m.reply_document(document="log.txt")
