from pyrogram import Client, Filters, StopPropagation


@Client.on_message(Filters.command(["help"]), group=-2)
async def help_text(c, m):
    msg = ""
    msg += "/login - `Login Account` \n"
    msg += "/logout - `Logout Account`\n"
    msg += "/info - `User Account Information`\n\n"
    msg += "Supported Host :  \n-Mega.nz \n-MediaFire \n-Zippyshare \n\n"
    msg += "Report Any Bug @aryanvikash\n\n"
    msg += "Join @aryan_bots For Updates"

    await m.reply_text(msg)
    raise StopPropagation
