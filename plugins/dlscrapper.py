# https://github.com/AvinashReddy3108/PaperplaneExtended/blob/master/userbot/modules/direct_links.py

import aiohttp
from bot.ariaHelper.ariaDownload import add_url
from bot.ariaHelper.stauts import progress
from bot import aria2, DOWNLOAD_LOCATION, DownloadDict
from bs4 import BeautifulSoup as soup
from pyrogram import Client, Filters
import asyncio

from bot.helper.zippyshare import generate_zippylink

url = "https://www76.zippyshare.com/v/uJ844Wu1/file.html"


@Client.on_message(Filters.regex(r"\bhttps?://.*mediafire\.com\S") |
                   Filters.regex(r"\bhttps?://.*zippyshare\.com\S"))
async def scrapperdownload(c, message):

    url = message.text.strip()
    url = url.split(" ")[-1]
    uid = str(message.from_user.id)
    try:
        if "mediafire.com" in url:
            sentm = await message.reply_text("`Mediafire Link Processing ...`")
            directLink = await mediafireLink(url)
        else:
            sentm = await message.reply_text("`ZippyShare Link Processing ...`")
            directLink = await zippyLink(url)

        download = await add_url(aria2, directLink, DOWNLOAD_LOCATION)
        if download:
            DownloadDict[uid] = download  # Download contains gid
            await progress(aria2=aria2, gid=DownloadDict[uid], event=sentm, ID=uid)
    except Exception as e:
        print(e)
        await sentm.edit(e)


async def zippyLink(url):
    loop = asyncio.get_event_loop()
    
    return await loop.run_in_executor(None, generate_zippylink, url)




async def mediafireLink(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    page = soup(await response.text(), 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    await session.close()
    return dl_url



