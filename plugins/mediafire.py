# https://github.com/AvinashReddy3108/PaperplaneExtended/blob/master/userbot/modules/direct_links.py

import aiohttp
from bs4 import BeautifulSoup as soup
from pyrogram import Client, filters

from bot import  DOWNLOAD_LOCATION, DownloadDict,dl
from bot.downloader_helper.handler import progress
@Client.on_message(filters.regex(r"mediafire\.com\S"))
async def mediafire(_, message):
    url = message.text.strip()
    url = url.split(" ")[-1]
    user_id = str(message.from_user.id)
    sentm = await message.reply_text("`Mediafire Link Processing ...`")

    #Downloader
    directLink = await mediafireLink(url)
    uuid = await dl.download(directLink)
    await progress(sentm=sentm,uuid=uuid)


async def mediafireLink(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    page = soup(await response.text(), 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    await session.close()
    return dl_url
