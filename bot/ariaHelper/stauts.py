import asyncio
import os
from bot import EDIT_TIME,LOGGER
from bot.drivefunc.gdriveUpload import gupload
import asyncio
from bot import DOWNLOAD_LOCATION, Creds_path
from pyrogram import  InlineKeyboardButton, InlineKeyboardMarkup

async def progress(aria2, gid, event, ID, previous_message=None):
    previous_message = None
    try:
        file = aria2.get_download(gid)
        complete = file.is_complete
        if not complete:
            if not file.error_message:
                msg = ""
                # TODO: temporary workaround (by UK)
                downloading_dir_name = "N/A"
                try:
                    downloading_dir_name = str(file.name)
                except Exception:
                    pass
                #
                msg = f"\nDownloading File: `{downloading_dir_name}`"
                msg += f"\n\nSpeed: {file.download_speed_string()}"
                msg += f"\nProgress: {file.progress_string()}"
                msg += f"\nTotal Size: {file.total_length_string()}"
                # msg += f"\nStatus: {file.status}"
                msg += f"\nETA: {file.eta_string()}"
                msg += f"\n\n<code>/cancel {gid}</code>"
                # LOGGER.info(msg)
                if msg != previous_message:
                    Cancelbutton=InlineKeyboardMarkup([[InlineKeyboardButton("cancel", callback_data = f"cancel||{gid}")] ])
                    try:
                        
                        await event.edit(msg,reply_markup = Cancelbutton)
                        previous_message = msg
                    except Exception :
                        pass
            else:
                msg = file.error_message
                await event.edit(f"`{msg}`")
                return False
            await asyncio.sleep(EDIT_TIME)
            await progress(aria2, gid, event, ID, previous_message)
        else:
            await event.edit(f"Download Complete: `{file.name}`")
            # TODO  ADD Gdrive Upload Thing Here
            LOGGER.info(f"Dowload Location : {DOWNLOAD_LOCATION}{file.name}")
            try:
                msg = f"\nDownloading File: `{file.name}`"
                msg += f"\nTotal Size: `{file.total_length_string()}`"
                # msg += f"\nStatus: {file.status}"
                msg += f"\nStatus: `Uploading`"
                msg += f"\n\nGid: `{gid}`"
                await event.edit(msg)

                filePath = os.path.join(DOWNLOAD_LOCATION,file.name )
                IdPath =  os.path.join(Creds_path,str(ID))

                loop = asyncio.get_event_loop()
                try:
                    DriveLink = await loop.run_in_executor(None, gupload, filePath, str(ID))
                except Exception as e:
                    event.edit("Failed To upload Your File report @aryanvikash")
                    return
                
                DownloadButton=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=DriveLink)] ])
                
                await event.edit(f"<b>FileName : </b> <code>{file.name}</code>\n\n<b>Size : </b> <code>{file.total_length_string()}</code> ",reply_markup=DownloadButton)
                os.remove(file.name)
                LOGGER.info(f"Upload Completed And Removing file ")

             
            except Exception as e:
                LOGGER.error(e)
                
                return False

            return True
    except Exception as e:
        LOGGER.info(str(e))
        # TODO Improve Onstop Thing
        if " not found" in str(e) or "'file'" in str(e):
            try:
                await event.edit(f"Download Cancelled :\n`{file.name}` \n GID : `{gid}`")
            except Exception:
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
