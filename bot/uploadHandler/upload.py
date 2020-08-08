import logging as LOGGER
from  pyrogram import  InlineKeyboardButton,InlineKeyboardMarkup
import os

from googleapiclient.errors import HttpError

from bot.drivefunc.gdriveUpload import mydrive
from bot.helper.utils import Human_size
from tpool.pool import run_in_thread


async def upload_handler(file_path, sentm):
    user_id = str(sentm.chat.id)
    try:
        _uploadedFile = await __finalUpload(file_path, user_id)

        download_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Download", url=f"https://drive.google.com/open?id={_uploadedFile['id']}")]
        ])
        await sentm.edit(f"Filename: `{_uploadedFile['title']}`\nSize: `{Human_size(_uploadedFile['fileSize'])}`",reply_markup=download_button)
    except HttpError as e:
        LOGGER.error(e)
        await sentm.edit(e._get_reason())
    except Exception as e:
        LOGGER.error(e)
        await sentm.edit(f"`{e}`\n#error")
    finally:
        os.remove(file_path)
        LOGGER.info("file Removed from disk")



@run_in_thread
def __finalUpload(file_path, user_id):
    if os.path.isdir(file_path):
        LOGGER.info(" Folder upload Init.. (not implemented lel)")
        pass
    if os.path.isfile(file_path):
        dr = mydrive(user_id)
        return dr.upload(file_path)
