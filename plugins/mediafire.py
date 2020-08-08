# https://github.com/AvinashReddy3108/PaperplaneExtended/blob/master/userbot/modules/direct_links.py

import aiohttp
from bs4 import BeautifulSoup as soup
from pyrogram import Client, Filters

from bot import aria2, DOWNLOAD_LOCATION, DownloadDict
from bot.ariaHelper.ariaDownload import add_url
from bot.ariaHelper.status import progress


@Client.on_message(Filters.regex(r"mediafire\.com\S"))
async def mediafire(_, message):
    url = message.text.strip()
    url = url.split(" ")[-1]
    user_id = str(message.from_user.id)
    sentm = await message.reply_text("`Mediafire Link Processing ...`")
    try:
        directLink = await mediafireLink(url)
        download = await add_url(aria2, directLink, DOWNLOAD_LOCATION)
        if download:
            DownloadDict[user_id] = download  # Download contains gid
            await progress(aria2=aria2, gid=DownloadDict[user_id], event=sentm, user_id=user_id)
    except Exception as e:
        print(e)
        await sentm.edit(e)


async def mediafireLink(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    page = soup(await response.text(), 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    await session.close()
    return dl_url
