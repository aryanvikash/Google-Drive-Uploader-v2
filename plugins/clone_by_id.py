from googleapiclient.errors import HttpError

from bot import LOGGER
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.drivefunc.gdrive_clone_func import GdriveClone

from tpool.pool import run_in_thread

@Client.on_message(filters.command("clone"))
async def clone_by_gdriveid(_, m):

    file_id = m.command[1]

    user_id = m.from_user.id
    sentm = await m.reply_text("`Trying To clone Your Google  Drive File or Folder ... !!`")

    try:

        cloned_file = await _driveclone(file_id, str(user_id))
        if cloned_file['mimeType'] == "application/vnd.google-apps.folder":
            drive_folder_baseurl = f"https://drive.google.com/drive/folders/{cloned_file['id']}"
            download_button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Download 📁", url=drive_folder_baseurl)],
                ]
            )
        else:
            drive_file_baseurl = f"https://drive.google.com/open?id={cloned_file['id']}"
            download_button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Download 📄", url=drive_file_baseurl)]
                ]
            )
        await sentm.edit(f"Name: `{cloned_file['title']}`\n\n#copied", reply_markup=download_button)
    except HttpError as e:
        LOGGER.error(e)
        await sentm.edit(f"` {e._get_reason()}\n #copyerror`")
        return


    except Exception as e:
        LOGGER.error(e)
        await sentm.edit(f"`{e}\n #copyerror`")




@run_in_thread
def _driveclone(file_id, user_id):
    clone = GdriveClone(user_id)
    drive_url = clone.copyHandler(file_id)
    return drive_url
