import aria2p
import sys
import logging
import os
import config
from pyrogram import Client , Filters

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(lineno)d -%(filename)s - %(levelname)s -%(message)s" ,
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


LOGGER = logging.getLogger(__name__)
# os.system("bash aria.sh")
adminList = config.adminList
currentdir = os.path.abspath(os.getcwd())
try:
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret="",
        )
    )


except Exception:
    print("Start Your Aria Rpc")
    sys.exit()


def is_admin(uid):
    if uid in adminList:
        return True
    else:
        return False

# for download in downloads:
#         msg = msg + "File: `" + str(download.name) + "`\nSpeed: " + str(download.download_speed_string()) + "\nProgress: " + str(download.progress_string(
#         )) + "\nTotal Size: " + str(download.total_length_string()) + "\nStatus: " + str(download.status) + "\nETA:  " + str(download.eta_string()) + "\n\n"
#         print(msg)


# Post_url = os.environ.get("DATABASE_URL")
if os.environ.get("DATABASE_URL"):
    LOGGER.info("Env Database Avalible ")
    Post_url = os.environ.get("DATABASE_URL")
    
else:

    LOGGER.info("Envoriment Database Not Found  Using hardcoding method ")
    Post_url = "postgres://skezdjjc:9YAl2TfIpCKfufEh6MzRVaaocu93bcth@ruby.db.elephantsql.com:5432/skezdjjc" #testdb
    # Post_url = "postgres://mrifmlre:anINuwfZgJRFc_7YXfbW6XqJ4RhcEg17@salt.db.elephantsql.com:5432/mrifmlre"

DownloadDict = {}
TgFileDownloadlist= []
MegaDownloadList = []
Creds_path = config.Creds_path
DOWNLOAD_LOCATION = config.DOWNLOAD_LOCATION
DOWNLOAD_LOCATION = currentdir

EDIT_TIME = 5


Creds_path = os.path.join(currentdir,Creds_path)


if not os.path.isdir(Creds_path):
    os.makedirs(Creds_path)
    LOGGER.info(f"Directory Created {Creds_path}")
