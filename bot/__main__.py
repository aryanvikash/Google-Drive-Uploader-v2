
import os
import config
from pyrogram import Client, Filters, MessageHandler, CallbackQueryHandler
# from bot.plugins.mirror import mirror
# from bot.plugins.auth import Auth
# from bot.plugins.logout import revoke
# from bot.plugins.cancel import cancel
# from bot.drivefunc.Tokenverify import *
# from bot.plugins.start import start
# from bot.plugins.document import Document_Downloader
# from bot.customFilters.authchecker import is_auth
# from bot.customFilters.directlinkFilter import is_direct
# from bot.plugins.megaa import mega_download
# from bot.plugins.user import user_info
# from bot.plugins.help import help_text
# from bot.customFilters.admin_filter import is_admin
# from bot.customFilters.m3u8_filter import is_m3u8
# from bot.plugins.dlscrapper import scrapperdownload 
# from bot.plugins.status import show_status
# from bot.customFilters.zippychecker import is_zippy
# from bot.plugins.log import get_logs
# from bot.plugins.ytdl import ytdl
# from bot.plugins.gdrive_links import clone_to_gdrive

DOWNLOAD_LOCATION = "./Downloads"
BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH
AUTH_CHANNEL = config.AUTH_GROUP
Admin_list = config.adminList
# if __name__ == "__main__":
#     # create download directory, if not exist
#     # if not os.path.isdir(DOWNLOAD_LOCATION):
#     #     os.makedirs(DOWNLOAD_LOCATION)
#     # s


plugins = dict(
    root="plugins",
)

app = Client(
    "GdriveBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    workers=300
).run()


    #
    # incoming_message_handler = MessageHandler(
    #     mirror,
    #     filters=Filters.command(["leech"]) & Filters.chat(chats=AUTH_CHANNEL)
    # )
    # incoming_message_handler = MessageHandler(
    #     mirror,
    #     filters=Filters.command(["leech"] & is_auth())
    # )


# On Mega Link
#     mega_handler = MessageHandler(mega_download,
#                                   filters=Filters.regex(r"^https://mega.") & is_auth())
#     app.add_handler(mega_handler)

# # On Gdrive Link 
#     gdrive_handler = MessageHandler(clone_to_gdrive ,
#      filters =Filters.regex(r"^https://drive.google.com")& is_auth())
#     app.add_handler(gdrive_handler)
    
# # On zippyshare Link
# # TODO need to implememt regex In zippy link dedection
#     zippyshare_handler = MessageHandler(scrapperdownload,
#                                         filters=Filters.regex(r"\bhttps?://.*zippyshare\.com\S") & is_auth())
#     app.add_handler(zippyshare_handler)

# # On Mediafire Link
#     mediafire_handler = MessageHandler(scrapperdownload,filters=Filters.regex(r"\bhttps?://.*mediafire\.com\S")& is_auth())
#     app.add_handler(mediafire_handler)


# # On User Info
#     user_info_handler = MessageHandler(
#         user_info, filters=Filters.command(["info"]))
#     app.add_handler(user_info_handler)


# # On Help
#     help_handler = MessageHandler(help_text, filters=Filters.command(["help"]))
#     app.add_handler(help_handler)

# # On direct Link
#     mirror_handler = MessageHandler(mirror,
#                                     filters=Filters.regex(r"^(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+")& is_auth())
#     app.add_handler(mirror_handler)


# # On cancel Handler
#     cancel_handler = MessageHandler(
#         cancel,
#         filters=Filters.command(["cancel"])
#     )
#     app.add_handler(cancel_handler)


# # On Status Handler
#     status_handler = MessageHandler(
#         show_status,
#         filters=Filters.command(["status"]) & is_admin())
#     app.add_handler(status_handler)

# # On Any Document Send
#     document_handler = MessageHandler(
#         Document_Downloader, filters=Filters.media & is_auth())
#     app.add_handler(document_handler)


# # Auth link
#     auth_handler = MessageHandler(Auth, filters=Filters.command(["login"]))
#     app.add_handler(auth_handler)

# # # m3u8 handler

#     m3u8_handler = MessageHandler(ytdl, filters=is_m3u8()& is_auth())
#     app.add_handler(m3u8_handler)
# # Revoke Handler
#     logout_handler = MessageHandler(
#         revoke, filters=Filters.command(["logout"]))
#     app.add_handler(logout_handler)

# # Token Handler
#     token_handler = MessageHandler(token_verify, filters=filter_token())
#     app.add_handler(token_handler)

# # Start Handler
#     start_handler = MessageHandler(start, filters=Filters.command(["start"]))
#     app.add_handler(start_handler)

# # Logs
#     log_handler = MessageHandler(get_logs, filters=Filters.command(["log"])&is_admin())
#     app.add_handler(log_handler)

    
#     app.run()
