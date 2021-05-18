
import os
import asyncio

from bot import DOWNLOAD_LOCATION, LOGGER, MegaDownloadList
from bot.drivefunc.gdriveUpload import mydrive
from pyrogram import Client, filters

from bot.uploadHandler.upload import upload_handler


@Client.on_message(filters.regex(r"^https://mega."))
async def mega_download(c, message):
    user_id = str(message.from_user.id)
    url = message.text.strip()
    await message.reply_text("Bot No Longer support mega 😒 ")
    return
    if user_id in MegaDownloadList:
        await message.reply_text(
            "`currently We Limit Mega Download To single Download At a Time !! Please Wait For Complete It ....`")
        return

    sentm = await message.reply_text("Downloading... keep patients You will get an error or file 😘 ")
    # loop = asyncio.get_event_loop()

    name, megaerror, isFolder = await megaTool(url)

    if megaerror:
        LOGGER.error(megaerror)
        await sentm.edit("`Wow you got an error 😮!!\n possible : Server Ip or file Download limit Over\n\n`#error")
        return
    if isFolder:
        await sentm.edit("`uploading Folder`")
        for filename in name:
            await upload_handler(filename, sentm)
            LOGGER.info("mega Upload complete", filename)
    else:
        await sentm.edit("`Wait uploading File !!`")
        filename = os.path.join(DOWNLOAD_LOCATION, name)
        await upload_handler(filename, sentm)

    return


# def async_megadl(url):
#     mega = Mega()
#     mag = mega.login("bearyan8@yandex.com", "bearyan8@yandex.com")
#     try:
#         name = mag.download_url(url)
#     except Exception as e:
#         LOGGER.error(e)
#
#     LOGGER.info(f"Mega  {name} Download Completed Now uploading...")
#
#     return name
#
#      await loop.run_in_executor(None, gupload,filename,ID)


def driveupload(path, ID):
    mdrive = mydrive(ID)
    drivelink = mdrive.uploadfile(path)
    return drivelink


async def megaTool(url):
    if "folder/" in url:
        link = url.replace("#", "!").replace("folder/", "#F!")
    elif "file/" in url:
        link = url.replace("#", "!").replace("file/", "#!")
    else:
        link = url
    command = ['megadl', "--no-progress", "--print-names", link]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    error = stderr.decode().strip()
    filename = stdout.decode().strip()
    print(" Mega error :", error)
    filenames = filename.split("\n")
    if "/#F!" in link:
        return filenames, error, True

    else:
        return filename, error, False
