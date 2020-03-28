from bot import Creds_path
from pyrogram import Filters
import os
import requests


def is_zippy():
    def zippy_link_checker(flt, m):
        url = m.text.strip()
        if "zippyshare.com" in url:
            return True
        else:
            return False
    return Filters.create(zippy_link_checker, "ZippyFilterCreate")
