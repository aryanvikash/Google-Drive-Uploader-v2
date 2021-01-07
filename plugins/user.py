
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from bot import Creds_path
import os
import os.path as path
from bot.util.utils import Human_size
from pyrogram import Client, filters, StopPropagation
from bot.drivefunc.Tokenverify import token_make


@Client.on_message(filters.command(["info"]), group=-2)
async def user_info(c, m):
    token_make(c, m)
    ID = str(m.from_user.id)
    is_login = False
    if os.path.isfile(os.path.join(Creds_path, ID)):

        drive:GoogleDrive

        gauth:drive.GoogleAuth = GoogleAuth()

        gauth.LoadCredentialsFile(path.join(Creds_path, ID))

        if gauth.credentials is None:
            is_login = False

        elif gauth.access_token_expired:
            gauth.Refresh()
            gauth.SaveCredentialsFile(path.join(Creds_path, ID))
            is_login = True
        else:
            gauth.Authorize()
            is_login = True

        drive = GoogleDrive(gauth)
        user = drive.GetAbout()
        msg = ""
        msg += f"Name: {m.from_user.first_name} {m.from_user.last_name}\n"
        msg += f"UserId :`{m.from_user.id}`\n"
        msg += f"Username: `{m.from_user.username}`\n"
        # msg += f'Name : `{user["name"]}`\n'
        msg += f'Email : `{user["user"]["emailAddress"]}`\n'
        msg += f'Quota Type :`{user["quotaType"]}`\n'
        msg += f'Total :`{Human_size(user["quotaBytesTotal"])}`\n'
        msg += f'Used :`{Human_size(user["quotaBytesUsed"])}`\n'
        msg += f'Trash : `{Human_size(user["quotaBytesUsedInTrash"])}`\n'
        msg += f'Login :`{is_login}`\n'
        await m.reply_text(msg)

    else:

        msg = ""
        msg += f"Name: {m.from_user.first_name} {m.from_user.last_name}\n"
        msg += f"Username: `{m.from_user.username}`\n"
        msg += f"UserId :`{m.from_user.id}` \n"
        msg += f"Login : `{is_login}`"
        await m.reply_text(msg)
    raise StopPropagation

#     {
#   'name': 'Roberta Donaldson',
#   'user': {
#     'kind': 'drive#user',
#     'displayName': 'Roberta Donaldson',
#     'isAuthenticatedUser': True,
#     'permissionId': '07054440001227544979',
#     'emailAddress': 'rdonaldson3392@student.egcc.edu'
#   },
#   'quotaBytesTotal': '24492595861283',
#   'quotaBytesUsed': '13497479583523',
#   'quotaBytesUsedAggregate': '13497479583523',
#   'quotaBytesUsedInTrash': '11304742331245',
#   'quotaType': 'UNLIMITED',

# }
