# https://github.com/SpEcHiDe/AnyDLBot/blob/13a16b8cb0922c277c309e05578310827288f599/helper_funcs/display_progress.py#L25
import math
import time

from bot import LOGGER,TgFileDownloadlist

from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
async def get_progress(
    current,
    total,
    ud_type,
    message,
    start,
    client,
    userid
):
    LOGGER.info("Telegram File Download Started ")
    if TgFileDownloadlist[userid] == False:
            LOGGER.info(f"Telegram File Downloading Cancelled By {userid}")
            client.stop_transmission()
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n Percentage: `{2}`%\n".format(
            ''.join(["●" for _ in range(math.floor(percentage / 5))]),
            ''.join(["○" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + f"`{humanbytes(current)}` of `{humanbytes(total)}`\nSpeed: `{humanbytes(speed)}`/s\nETA: `{estimated_total_time if estimated_total_time != '' else '0 s'}`\n"


        try:
            cancelButton = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data = f"tgcancel||{userid}" )]
            ]
        )
            await message.edit(text=f"{ud_type}\n {tmp}",reply_markup=cancelButton)
        except Exception:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
