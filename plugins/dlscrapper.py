# https://github.com/AvinashReddy3108/PaperplaneExtended/blob/master/userbot/modules/direct_links.py

import re
import aiohttp
from bot.ariaHelper.ariaDownload import add_url
from bot.ariaHelper.stauts import progress
from bot import aria2, DOWNLOAD_LOCATION, DownloadDict
from bs4 import BeautifulSoup as soup
from pyrogram import Client ,Filters
from bot.customFilters.authchecker import is_auth

url = "https://www76.zippyshare.com/v/uJ844Wu1/file.html"

@Client.on_message(Filters.regex(r"\bhttps?://.*mediafire\.com\S")& is_auth() | 
                Filters.regex(r"\bhttps?://.*zippyshare\.com\S") & is_auth())
async def scrapperdownload(c, message):
    
    url = message.text.strip()
    url = url.split(" ")[-1]
    uid = str(message.from_user.id)
    try:
        if "mediafire.com" in url:
            sentm = await message.reply_text("`Mediafire Link Processing ...`")
            directLink = await mediafireLink(url)
        else :
            sentm = await message.reply_text("`ZippyShare Link Processing ...`")
            directLink= await zippyLink(url)
        
        download = await add_url(aria2, directLink, DOWNLOAD_LOCATION)
        if download:
            DownloadDict[uid] = download  # Download contains gid
            await progress(aria2=aria2, gid=DownloadDict[uid], event=sentm, ID=uid)
    except Exception as e:
        print(e)
        await sentm.edit(e)


async def zippyLink(url):
    session = aiohttp.ClientSession()
    base_url = re.search('http.+.com', url).group()
    response = await session.get(url)
    page_soup = soup(await response.text(), "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search('= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);', script.text).group('url')
            math = re.search('= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);', script.text).group('math')
            dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    await session.close()
    return dl_url


async def mediafireLink(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)

        page = soup(await response.text(), 'lxml')
        info = page.find('a', {'aria-label': 'Download file'})
        dl_url = info.get('href')
        await session.close()
        # size = re.findall(r'\(.*\)', info.text)[0]
        # name = page.find('div', {'class': 'filename'}).text
        # reply += f'[{name} {size}]({dl_url})\n'
        
        return dl_url


# async def sourceforge(url: str) -> str:
#     """ SourceForge direct links generator """
#     try:
#         link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
#     except IndexError:
#         reply = "`No SourceForge links found`\n"
#         return reply

#     file_path = re.findall(r'files(.*)/download', link)[0]
#     reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
#     project = re.findall(r'projects?/(.*?)/files', link)[0]
#     mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
#         f'projectname={project}&filename={file_path}'
#     page = soup(requests.get(mirrors).content, 'html.parser')
#     info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
#     for mirror in info[1:]:
#         name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
#         dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
#         reply += f'[{name}]({dl_url}) '
#     return reply


# async def yandex_disk(url: str) -> str:
#     """ Yandex.Disk direct links generator
#     Based on https://github.com/wldhx/yadisk-direct"""
#     reply = ''
#     try:
#         link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
#     except IndexError:
#         reply = "`No Yandex.Disk links found`\n"
#         return reply
#     api = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={link}'
#     try:
#         session = aiohttp.ClientSession()
#         response = await session.get(api)
#         dl_url = await response.text().json()['herf']
#         # dl_url = requests.get(api.format(link)).json()['href']
#         name = dl_url.split('filename=')[1].split('&disposition')[0]
#         reply += f'[{name}]({dl_url})\n'
#     except KeyError:
#         reply += '`Error: File not found / Download limit reached`\n'
#         return reply
#     return reply
