from pyrogram import Client,Filters
from bot.customFilters.authchecker import is_auth
import os
@Client.on_message(Filters.command(["start"]))
async def start(client, message):
    print(os.system("ls"))
    await message.reply_text(f"""Hey <b>{message.from_user.first_name}</b>
        \nCheck  /help Command for More info
        \nJoin @aryan_bots
        \n\nBug report: @aryanvikash""")
