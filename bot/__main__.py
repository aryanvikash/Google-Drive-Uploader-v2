
import config
from pyrogram import Client



DOWNLOAD_LOCATION = "./Downloads"
BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH
AUTH_CHANNEL = config.AUTH_GROUP
Admin_list = config.adminList

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


