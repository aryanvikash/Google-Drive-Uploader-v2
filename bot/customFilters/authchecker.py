from bot import Creds_path
from pyrogram import Filters
import os
from bot.drivefunc.Tokenverify import token_make


def is_auth():
    def is_auth_checker(_, m):
        if os.path.isfile(os.path.join(Creds_path, str(str(m.from_user.id)))):
            return True
        else:
            return token_make(None, m)

    return Filters.create(is_auth_checker, "AuthFilterCreate")


def is_auth_user(user_id):
    if os.path.isfile(os.path.join(Creds_path, str(user_id))):
        return True
    else:
        #    await  m.reply_text("You Are Not Authorised Please /login")
        return False
