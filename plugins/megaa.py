from mega import Mega
import os
import asyncio
from bot.helper.utils import Human_size
from bot import DOWNLOAD_LOCATION, LOGGER, Creds_path,MegaDownloadList
from bot.drivefunc.gdriveUpload import gupload
from pyrogram import Client, Filters


@Client.on_message(Filters.regex(r"^https://mega."))
async def mega_download(c, message):
    os.system("megals")
    ID = str(message.from_user.id)
    url = message.text.strip()
    # await message.reply_text("No Support For Mega links😒 ")
    # return
    if ID in MegaDownloadList:
        await message.reply_text("`currently We Limit Mega Download To single Download At a Time !! Please Wait For Complete It ....`")
        return

    sentm = await message.reply_text("Downloading... Mega Link Was Always Slow..😒 ")
    loop = asyncio.get_event_loop()
    
    try:
        # mega Download
        # MegaDownloadList.append(ID)
        name,megaerror = await megatool(url)
        
        if megaerror:
                print("something goging wrong")
                # name = await loop.run_in_executor(None, async_megadl, url)
                
        filename = os.path.join(DOWNLOAD_LOCATION, name)
        print(filename)
        print(type(filename))
        await sentm.edit("Mega Download Complete ....!! Now Uploading !!")
        # MegaDownloadList.remove(ID)
        # Uploading
        DriveLink = await loop.run_in_executor(None, gupload, filename, ID)
        LOGGER.info(f"mega : {name} : Upload complete")
        size = os.path.getsize(filename)
        await sentm.edit(f"Filename: `{name}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
        os.remove(filename)
    except Exception as e:
        # MegaDownloadList.remove(ID)
        LOGGER.error(e)

        await sentm.edit(f"Wew You Got An Error 😮!! \n\n`{e}`\n\nMake Sure It was a file Link \n\n#error")
        return


def async_megadl(url):
    mega = Mega()
    mag = mega.login("bearyan8@yandex.com", "bearyan8@yandex.com")
    try:
        name = mag.download_url(url)
    except Exception as e:
        LOGGER.error(e)
    LOGGER.info(f"Mega  {name} Download Completed Now uploading...")

    return name

    # await loop.run_in_executor(None, gupload,filename,ID)




async def megatool(link):
    command  = ['megadl',"--no-progress","--print-names",link]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    error = stderr.decode().strip()
    filename = stdout.decode().strip()
    print(" Mega error :",error)
    print("files :" ,filename)
    print(type(filename))
    return filename ,error
