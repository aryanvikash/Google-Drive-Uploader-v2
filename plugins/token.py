from pyrogram import Client
from bot.drivefunc.Tokenverify import token_verify
from bot.drivefunc.Tokenverify import filter_token

@Client.on_message(filter_token())
async def tokenthings(c,m):
    await token_verify(c,m)