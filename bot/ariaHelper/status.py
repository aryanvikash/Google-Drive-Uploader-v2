import asyncio
import os

from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import DOWNLOAD_LOCATION
from bot import EDIT_TIME, LOGGER
from bot.uploadHandler.upload import upload_handler


async def progress(aria2, gid, event, user_id, previous_message=None):
    try:
        file = aria2.get_download(gid)
        complete = file.is_complete
        if not complete:
            if not file.error_message:
                msg = ""

                downloading_dir_name = "N/A"
                try:
                    downloading_dir_name = str(file.name)
                except:
                    pass
                #
                msg = await gen_status_string(file,downloading_dir_name,gid)

                if msg != previous_message and msg is not None:
                    Cancelbutton = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("cancel", callback_data=f"cancel||{gid}")]])
                    try:

                        await event.edit(msg, reply_markup=Cancelbutton)
                        previous_message = msg
                    except Exception:
                        pass
            else:
                msg = file.error_message
                await event.edit(f"`{msg}`")
                return False
            await asyncio.sleep(EDIT_TIME)
            await progress(aria2, gid, event, user_id, previous_message)
        else:
            await event.edit(f"Download Complete: `{file.name}`")

            LOGGER.info(f"Dowload Location : {DOWNLOAD_LOCATION}{file.name}")
            try:
                #upload File if completed
                await send_uplaod_status(event, file, gid)
                file_path = os.path.join(DOWNLOAD_LOCATION, file.name)
                await upload_handler(file_path, event)

            except Exception as e:
                LOGGER.error(e)

                return False

            return True
    except Exception as e:
        LOGGER.info(str(e))

        if " not found" in str(e) or "'file'" in str(e):
            try:
                await event.edit(f"Download Cancelled :\n`{file.name}` \n GID : `{gid}`")
            except:
                await event.edit(f"Download Cancelled :\n GID : `{gid}`")
            return False

        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit("Download Stopped \n`{file.name}`")
            return False
        else:
            LOGGER.info(str(e))
            await event.edit("<u>error</u> :\n`{}` \n\n#error".format(str(e)))
            return


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164


async def send_uplaod_status(event, file, gid):
    msg = f"\nDownloading File: `{file.name}`"
    msg += f"\nTotal Size: `{file.total_length_string()}`"
    # msg += f"\nStatus: {file.status}"
    msg += f"\nStatus: `Uploading`"
    msg += f"\n\nGid: `{gid}`"
    await event.edit(msg)


async  def gen_status_string(file,dl_path,gid):
    msg = f"\nDownloading File: `{dl_path}`"
    msg += f"\n\nSpeed: {file.download_speed_string()}"
    msg += f"\nProgress: {file.progress_string()}"
    msg += f"\nTotal Size: {file.total_length_string()}"
    # msg += f"\nStatus: {file.status}"
    msg += f"\nETA: {file.eta_string()}"
    msg += f"\n\n<code>/cancel {gid}</code>"
    return msg