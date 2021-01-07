from pyrogram import Client, filters, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["start"]), group=-2)
async def start(_, message):
    join_button = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Channel", url="https://t.me/aryan_bots")],
            [InlineKeyboardButton("Report Bugs 😊", url="https://t.me/aryanvikash")],
        ]
    )

    welcome_msg = f"Hey <b>{message.from_user.first_name}</b>\n/help for More info"
    s = await message.reply_text(welcome_msg, reply_markup=join_button)

    raise StopPropagation
