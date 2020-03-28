from pyrogram import Filters


def is_m3u8():
    def m3u8_checker(flt, m):
        if m.text.endswith("m3u8"):
            return True
        else:
           
            return False
    return Filters.create(m3u8_checker, "m3u8FilterCreate")
