from mega import Mega
import os
import asyncio
from bot.helper.utils import Human_size
from bot import DOWNLOAD_LOCATION, LOGGER, Creds_path,MegaDownloadList
from bot.drivefunc.gdriveUpload import gupload,mydrive
from pyrogram import Client, Filters


@Client.on_message(Filters.regex(r"^https://mega."))
async def mega_download(c, message):
    ID = str(message.from_user.id)
    url = message.text.strip()
    # await message.reply_text("No Support For Mega links😒 ")
    # return
    if ID in MegaDownloadList:
        await message.reply_text("`currently We Limit Mega Download To single Download At a Time !! Please Wait For Complete It ....`")
        return

    sentm = await message.reply_text("Downloading... Mega Link Was Always Slow..😒 ")
    loop = asyncio.get_event_loop()
    

    name,megaerror,isFolder= await megatool(url)
    
    if megaerror:
            print("something goging wrong")
            await sentm.edit(f"Wew You Got An Error 😮!! \n\n\nMake Sure It was a file Link \n\n#error")
            return
    if isFolder:
        filenames = name
        print("folder Downloadzz:",name)
        for filename in filenames:
            DriveLink = await loop.run_in_executor(None, driveupload, filename, ID)
            LOGGER.info(f"mega : {name} : Upload complete")
            size = os.path.getsize(filename)
            file = os.path.basename(filename)
            await message.reply_text(f"Filename: `{file}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
            os.remove(filename)

    
    else:
        filename = os.path.join(DOWNLOAD_LOCATION, name)
        print("file downloaded")
        DriveLink = await loop.run_in_executor(None, driveupload, filename, ID)
        LOGGER.info(f"mega : {name} : Upload complete")
        size = os.path.getsize(filename)
        await sentm.edit(f"Filename: `{name}`\n Size : `{Human_size(size)}`\nLink : {DriveLink}")
        os.remove(filename)

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


def driveupload(path,ID):
        mdrive = mydrive(ID)
        drivelink = mdrive.uploadfile(path)
        return drivelink



async def megatool(url):
    if "folder/" in url :
        link = url.replace("#", "!").replace("folder/","#F!")
    else:
        link  = url
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
    filenames  = filename.split("\n")
    if "/#F!" in link :
            return filenames ,error ,True
    
    else:
        return filename,error ,False



    
