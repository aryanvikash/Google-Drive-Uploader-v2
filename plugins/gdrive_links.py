from googleapiclient.errors import HttpError

from bot import LOGGER
from bot.drivefunc.gdrive_clone_func import GdriveClone

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tpool.pool import run_in_thread


@Client.on_message(filters.regex(r"^https://drive.google.com"))
async def clone_to_gdrive(_, m):
    user_id = m.from_user.id

    sentm = await m.reply_text("`Trying To clone Your Google  Drive File or Folder ... !!`")

    try:

        cloned_file = await driveclone(m.text, str(user_id))

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
        await sentm.edit(f"`{e._get_reason()}\n #copyerror`")

    except Exception as e:
        LOGGER.error(e)
        await sentm.edit(f"`{e}\n #copyerror`")
        return


@run_in_thread
def driveclone(url, user_id):
    clone = GdriveClone(user_id)
    driveurl = clone.copyHandler(getId(url))
    print("cloning ends")
    return driveurl


def getId(link):
    link = link.translate({ord('&'): None}).replace("export=download", " ").strip()

    if link.find("id=") != -1:
        file_id = link.split("=")[-1].strip()
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    elif link.find("file/d/") != -1:
        file_id = link.split("/")[-1].strip()
    elif link.find("/folders/") != -1:
        file_id = link.split("folders/")[-1].strip()
    elif link.find("view") != -1:
        file_id = link.split('/')[-2]
    else:
        file_id = 'not found'

    return file_id
