from bot.util.utils import (is_url)
import os
from bot import (aria2, DownloadDict, DOWNLOAD_LOCATION,
                 LOGGER)
from bot.ariaHelper.ariaDownload import add_url
from bot.ariaHelper.status import progress
import time
from pyrogram import Client, Filters,ContinuePropagation
import aiohttp


# async def direct_link_checker_async(_, m):
#     url = m.text.strip()
#     if url.endswith("m3u8"):
#         return False
#     LOGGER.info(f"Direct Link Checker : {url}")
#
#     requests = aiohttp.ClientSession()
#     h = await requests.head(url, allow_redirects=True)
#     content_type = h.content_type
#     await requests.close()
#     if 'text' in content_type.lower():
#         return False
#     if 'html' in content_type.lower():
#         return False
#     if 'torrent' in content_type.lower():
#         return False
#     return True


@Client.on_message(Filters.regex(r"^(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"))
async def mirror(_, message):
    if "zippyshare.com" in message.text or "mediafire" in message.text:
        print("link zip")
        raise  ContinuePropagation
    # is_direct = await direct_link_checker_async(client, message)
    # if not is_direct:
    #     print("Not direct link")
    #     # await message.reply_text(f"<code> `Send Me a direct Link 😒 `")
    #     raise ContinuePropagation
    user_id = str(message.from_user.id)

    new_download_location = os.path.join(
        DOWNLOAD_LOCATION,
        user_id,
        str(time.time())
    )
    # if os.path.isfile(os.path.join(Creds_path, user_id)):

    sentm = await message.reply_text("<code> Processing Your Uri ...</code>")

    msg = message.text.strip()

    if msg is not None and is_url(msg):
        download = await add_url(aria2, msg, new_download_location)
        if download:
            DownloadDict[user_id] = download  # Download contains gid
            LOGGER.info(f"download Added by :",download)
            await progress(aria2=aria2, gid=DownloadDict[user_id], event=sentm, user_id=user_id)

        # await message.reply_text("You Are Not Authorised use /login 😞")
