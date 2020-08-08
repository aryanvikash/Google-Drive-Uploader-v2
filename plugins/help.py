from pyrogram import Client, Filters, StopPropagation


@Client.on_message(Filters.command(["help"]), group=-2)
async def help_text(_, m):
    msg = ""
    msg += "/login - `Login Account` \n"
    msg += "/logout - `Logout Account`\n"
    msg += "/info - `User Account Information`\n\n"
    msg += "Supported Host :  \n-Mega.nz (don't complain about it)\n-MediaFire \n-Zippyshare \n\n"
    msg += "Google Drive Clone (send drivelink or /clone <id>)"
    msg += "Report  @aryanvikash\n\n"

    await m.reply_text(msg)
    raise StopPropagation
