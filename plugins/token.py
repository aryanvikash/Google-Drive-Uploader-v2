from pyrogram import Client,Filters
from bot.drivefunc.Tokenverify import token_verify


@Client.on_message(Filters.regex(r"\w\/(.{55})"))
async def token_things(c, m):
    await token_verify(c, m)
