from bot.helper.utils import (is_magnet, is_url)
import os
from bot import (aria2, DownloadDict, DOWNLOAD_LOCATION,
                 EDIT_TIME, LOGGER, Creds_path)
from bot.ariaHelper.ariaDownload import add_url,add_torrent
from bot.ariaHelper.stauts import progress
import time
from bot.customFilters.admin_filter import is_admin
from pyrogram import Client, Filters, ContinuePropagation





@Client.on_message(Filters.regex(r"^magnet:\?xt=urn:btih:[a-zA-Z0-9]*")& is_admin())
async def torrent_(client, message):
    print("magnet added")
    current_user_id = message.from_user.id
    uid = current_user_id

    ID = str(message.from_user.id)
    message.message_id
    new_download_location = os.path.join(
        DOWNLOAD_LOCATION,
        str(current_user_id),
        str(time.time())
    )
    # if os.path.isfile(os.path.join(Creds_path, ID)):

    sentm = await message.reply_text(f"<code> Processing Your Uri ...</code>")

    msg = message.text.strip()
    msg = msg.split(" ")[-1]

    if msg is not None and is_magnet(msg):
        download = await add_torrent(aria2, msg, new_download_location)
        if download:
            DownloadDict[uid] = download  # Download contains gid
            print("UID:", message.from_user.id)
            await progress(aria2=aria2, gid=DownloadDict[uid], event=sentm, ID=current_user_id)

        # await message.reply_text("You Are Not Authorised use /login 😞")
