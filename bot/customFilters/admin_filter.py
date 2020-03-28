from bot import adminList
from pyrogram import Filters


def is_admin():
    def admin_checker(flt, m):
        if m.from_user.id in adminList:
            return True
        else:
            #    await  m.reply_text("You Are Not Authorised Please /login")
            return False
    return Filters.create(admin_checker, "AdminFilterCreate")
