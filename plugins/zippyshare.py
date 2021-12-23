# !/usr/bin/env python3
# https://github.com/mansuf/zippyshare-downloader

from pyrogram import Client, filters

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

from bs4 import BeautifulSoup
import io
import math
import aiohttp


# zippy
ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}


@Client.on_message(filters.regex(r"zippyshare\.com\S"))
async def zippy(_, message):
    url = message.text.strip()
    url = url.split(" ")[-1]
    # user_id = str(message.from_user.id)
    sentm = await message.reply_text("`ZippyShare Link Processing ...`")

    try:
        file_directlink = await _zippylink(url)
    except Exception as e:
        await sentm.edit_text(f"`Error: {e}`")
        return

    uuid = await dl.download(file_directlink)
    await progress(sentm=sentm, uuid=uuid)




def evaluate(expression):
    """Evaluate a math expression."""

    # Compile the expression
    code = compile(expression, "<string>", "eval")

    # Validate allowed names
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
                raise NameError("The use of '%s' is not allowed. Expression used: %s" % (name, expression))

    return eval(code, {"__builtins__": {}}, ALLOWED_NAMES)

def pattern3(body_string, url):
    # Getting download button javascript code
    parser = BeautifulSoup(body_string, 'html.parser')
    for script in parser.find_all('script'):
        if 'document.getElementById(\'dlbutton\').href' in script.decode_contents():
            scrapped_script = script.decode_contents()
            break
        else:
            scrapped_script = None
    if scrapped_script is None:
        raise Exception('download button javascript cannot be found')

    scripts = io.StringIO(scrapped_script).readlines()
    _vars = {}
    init_url = None
    numbers_pattern = None
    file_url = None
    for script in scripts:
        # Finding variables that contain numbers
        re_var = re.compile(r'(var ([a-zA-Z]) = )([0-9%]{1,})(;)')
        found = re_var.search(script)
        if found:
            _name = found.group(2)
            _value = found.group(3)
            _vars[_name] = _value
        # Finding url download button
        if script.strip().startswith('document.getElementById(\'dlbutton\')'):
            string_re_dlbutton = r'(document\.getElementById\(\'dlbutton\'\)\.href = \")' \
                                '(\/[a-zA-Z]\/[a-zA-Z0-9]{1,}\/)\"\+' \
                                '(\([a-zA-Z] \+ [a-zA-Z] \+ [a-zA-Z] - [0-9]\))\+\"(\/.{1,})\";'
            re_dlbutton = re.compile(string_re_dlbutton)
            result = re_dlbutton.search(script)
            if result:
                init_url = result.group(2)
                numbers_pattern = result.group(3)
                file_url = result.group(4)
            else:
                raise Exception('Invalid regex pattern when finding url dlbutton')

    if not _vars:
        raise Exception('Cannot find required variables in dlbutton script')
    else:
        for var_name, var_value in _vars.items():
            numbers_pattern = numbers_pattern.replace(var_name, var_value)
        final_numbers = str(evaluate(numbers_pattern))
    return url[:url.find('.')] + '.zippyshare.com' + init_url + final_numbers + file_url





async def _zippylink(url):
    
    aiohttp_session = aiohttp.ClientSession()
    async with aiohttp_session as session:
        # header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        
        async with session.get(url,headers=headers) as resp:
            if resp.status == 200:
                body = await resp.text()
                file_directlink = pattern3(body, url)
                return file_directlink
            else:
                raise Exception('Invalid response status')

