# !/usr/bin/env python3
# https://github.com/Sorrow446/ZS-DL

from pyrogram import Client, Filters

from bot import dl, DOWNLOAD_LOCATION, DownloadDict, LOGGER


# zippy
import re
import time

from bot.downloader_helper.handler import progress
from tpool.pool import run_in_thread
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote
import requests


@Client.on_message(Filters.regex(r"zippyshare\.com\S"))
async def zippy(_, message):
    url = message.text.strip()
    url = url.split(" ")[-1]
    user_id = str(message.from_user.id)
    sentm = await message.reply_text("`ZippyShare Link Processing ...`")

    directLink = await _zippylink(url)

    uuid = await dl.download(directLink)
    await progress(sentm=sentm,uuid=uuid)





def check_url(url):
    regex = r'https://www(\d{1,3}).zippyshare.com/v/([a-zA-Z\d]{8})/file.html'
    match = re.match(regex, url)
    if match:
        return match.group(1), match.group(2)
    raise ValueError("Invalid URL: " + str(url))


def extract(url, server, i_d, session):
    regex = (
        r'document.getElementById\(\'dlbutton\'\).href = "/d/'
        r'([a-zA-Z\d]{8})/" \+ \((\d*) % (\d*) \+ (\d*) % '
        r'(\d*)\) \+ "/(.*)";'
    )
    for _ in range(3):
        r = session.get(url)
        if r.status_code != 500:
            break
        time.sleep(1)
    r.raise_for_status()
    meta = re.search(regex, r.text)
    if not meta:
        raise Exception('Failed to get file URL. Down?')
    num_1 = int(meta.group(2))
    num_2 = int(meta.group(3))
    num_3 = int(meta.group(4))
    num_4 = int(meta.group(5))
    enc_fname = meta.group(6)
    final_num = num_1 % num_2 + num_3 % num_4
    file_url = "https://www{}.zippyshare.com/d/{}/{}/{}".format(server,
                                                                i_d,
                                                                final_num,
                                                                enc_fname)
    fname = unquote(enc_fname)
    return file_url, fname


@run_in_thread
def _zippylink(url):
    s = requests.Session()
    s.headers.update({
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/75.0.3770.100 Safari/537.36"
    })
    server, id = check_url(url)
    file_url, fname = extract(url, server, id, s)
    LOGGER.info(file_url, fname)
    return file_url

# if __name__ == '__main__':
#
#     try:
#         _zippylink("https://www10.zippyshare.com/v/dyh988sh/file.html")
#     except Exception as e:
#         print(e)
