from bot import LOGGER
# from bot import Creds_path
from pyrogram import Filters
import aiohttp
# import requests


# def is_direct():
#     def direct_link_checker(flt, m):
#         url = m.text.strip()
#         LOGGER.info(f"Checking Direct Link : {url}")
#         h = requests.head(url, allow_redirects=True)
#         header = h.headers
#         content_type = header.get('content-type')
#         if 'text' in content_type.lower():
#             return False
#         if 'html' in content_type.lower():
#             return False
#         return True
#     return Filters.create(direct_link_checker, "DirectLinkFilterCreate")

def is_direct():
    async def direct_link_checker_async(flt, m):
        url = m.text.strip()
        LOGGER.info(f"Direct Link Checker : {url}")
        requests = aiohttp.ClientSession()
        h = await requests.head(url, allow_redirects=True)
        content_type = h.content_type
        await requests.close()
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    async def direct_link_checker(flt, m):
        return await direct_link_checker_async(flt, m)
    return Filters.create(direct_link_checker, "DirectLinkFilterCreate")
