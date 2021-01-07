import asyncio
import os

from pyaiodl.errors import InvalidId, DownloadNotActive
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import dl, EDIT_TIME, LOGGER, DOWNLOAD_LOCATION

from bot.uploadHandler.upload import upload_handler


async def progress(sentm, uuid):
    prev_msg = None
    CancelButton = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("cancel", callback_data=f"cancel||{uuid}")]])
    try:
        while await dl.is_active(uuid):
            file = await dl.status(uuid)

            msg = _gen_status_string(file)

            await sentm.edit(msg)
            if msg != prev_msg and msg is not None:

                try:

                    await sentm.edit(msg, reply_markup=CancelButton)
                    prev_msg = msg
                except:
                    pass
            # let him breath  for a second:P
            await asyncio.sleep(EDIT_TIME)

    # If You are putting uuid  manually Than its better handle This Exception
    except InvalidId:
        await sentm.edit("No Downloads are Active !!")
        return

    # Check if There is any error
    error = await dl.iserror(uuid)
    if error:
        await sentm.edit(f"{str(error)} \n #error")
        return
    else:
        # Else Upload :)
        try:
            _file = await dl.status(uuid)
            # upload File if completed

            await _send_uplaod_status(file=_file, sentm=sentm)
            file_path = os.path.join(DOWNLOAD_LOCATION, _file['filename'])
            await upload_handler(file_path, sentm)

        except Exception as e:
            LOGGER.error(e)





def _gen_status_string(file):
    msg = f"\nDownloading File: `{file['filename']}`"
    msg += f"\n\nSpeed: {file['download_speed']}"
    msg += f"\nProgress: {file['progress']} %"
    msg += f"\nStatus: `Downloading`"
    msg += f"\nDownloaded : {file['downloaded_str']}"
    msg += f"\nTotal Size: {file['total_size_str']}"

    return msg


async def _send_uplaod_status(file, sentm):

    msg = f"\nDownloading File: `{file['filename']}`"
    msg += f"\nTotal Size: `{file['total_size_str']}`"
    msg += f"\nStatus: `Uploading`"

    await sentm.edit(msg)
