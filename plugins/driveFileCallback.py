from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import (LOGGER, TgFileDownloadlist)
from bot.drivefunc.gdriveUpload import mydrive


@Client.on_callback_query(filters.regex("^delete"))
async def deleteDriveFile(c, m):
        fileId = m.data.split("||")[-1].strip()
        userDrive = mydrive(str(m.from_user.id))
        try:
            # Permanent Delete
            userDrive.deleteFile(fileId,True)
            await m.edit_message_text(f"`{fileId}` Deleted permanently ")
        except Exception as e:
            LOGGER.error(e)
            await m.edit_message_text(f"`Error : {e}`")



#  Move To Trash

@Client.on_callback_query(filters.regex("^trash"))
async def trashDriveFile(c, m):
        fileId = m.data.split("||")[-1].strip()
        userDrive = mydrive(str(m.from_user.id))
        try:
            # Moving to trash
            userDrive.deleteFile(fileId)
            restoreButton  = InlineKeyboardMarkup([
               [InlineKeyboardButton( "Restore", callback_data=f"restore||{fileId}")]
               ])
            await m.edit_message_reply_markup(restoreButton)

        except Exception as e:
            LOGGER.error(e)
            await m.edit_message_text(f"`Error : {e}`")

@Client.on_callback_query(filters.regex("^restore"))
async def restoreDriveFile(c, m):
    fileId = m.data.split("||")[-1].strip()

    try:
        userDrive = mydrive(str(m.from_user.id))
        userDrive.restore(fileId)
        TrashButton  = InlineKeyboardMarkup([
               [InlineKeyboardButton( "Permanent Delete", callback_data=f"delete||{fileId}")],
               [InlineKeyboardButton( "Trash", callback_data=f"trash||{fileId}")]
               ])
        await m.edit_message_reply_markup(TrashButton)
    except Exception as e:
        LOGGER.error(e)
        await m.edit_message_text(f"`Error : {e}`")