import logging
import os
from pyaiodl import Downloader

import config

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(lineno)d -%(filename)s - %(levelname)s -%(message)s",
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pydrive").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)
# os.system("bash aria.sh")
adminList = config.adminList

currentdir = os.path.abspath(os.getcwd())

# Aio downloader
dl = Downloader()


def is_admin(uid):
    if uid in adminList:
        return True
    else:
        return False


# Post_url = os.environ.get("DATABASE_URL")
if os.environ.get("DATABASE_URL"):
    LOGGER.info("Env Database Avalible ")
    Post_url = os.environ.get("DATABASE_URL")

else:

    LOGGER.info("Envoriment Database Not Found  Using hardcoding method ")
    Post_url = "asdasddasdsd"  # testdb


DownloadDict = {}
TgFileDownloadlist = {}
MegaDownloadList = []
Creds_path = config.Creds_path
DOWNLOAD_LOCATION = config.DOWNLOAD_LOCATION
DOWNLOAD_LOCATION = currentdir

EDIT_TIME = 5

Creds_path = os.path.join(currentdir, Creds_path)

if not os.path.isdir(Creds_path):
    os.makedirs(Creds_path)
    LOGGER.info(f"Directory Created {Creds_path}")
