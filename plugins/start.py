from pyrogram import Client, Filters, StopPropagation,InlineKeyboardButton, InlineKeyboardMarkup
from bot.helper.check_channel import inChannel
from bot.helper.send_join import sendJoinmsg


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    

    await message.reply_text(f"""Hey <b>{message.from_user.first_name}</b>
        \nCheck  /help Command for More info
        \nJoin @aryan_bots
        \n\nBug report: @aryanvikash""")
    raise StopPropagation
