import os
import time

from pyrogram import Client, filters, ContinuePropagation

from bot import (dl, DOWNLOAD_LOCATION,
                 LOGGER)
from bot.downloader_helper.handler import progress
from bot.util.utils import (is_url)


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


@Client.on_message(filters.regex(r"^(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"))
async def mirror(_, message):
    if "zippyshare.com" in message.text or "mediafire" in message.text:
        raise ContinuePropagation
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
        uuid = await dl.download(url=msg)
        LOGGER.info(f"{uuid} Download Added !!")
        await progress(sentm=sentm, uuid=uuid)

