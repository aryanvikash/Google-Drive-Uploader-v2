import os
from pydrive.auth import GoogleAuth
import psycopg2
from pyrogram import filters
from bot import Post_url, Creds_path, LOGGER

# conn = psycopg2.connect(DATABASE_URL)
conn = psycopg2.connect(Post_url)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS USERINFO
    (
    id serial NOT NULL PRIMARY KEY UNIQUE,
    chat_id INTEGER,
    AUTH TEXT
    );'''
            )
conn.commit()


def filter_token():
    def is_token(_, m):
        token = m.text
        token = token.split()[-1]
        TLEN = len(token)
        if TLEN == 57:
            if token[1] == "/":
                return True
            else:
                return False
        else:
            return False

    return filters.create(is_token, "TokenFilterCreate")


# def is_token(m):
#     token = m.text
#     # token = token.split()[-1]
#
#     if len(token) == 57:
#         if token[1] == "/":
#             return True
#         else:
#             return False
#     else:
#         return False


# @Client.on_message(filter_token())
async def token_verify(_, message):
    token = message.text.strip()
    user_id = str(message.from_user.id)
    try:
        gauth = GoogleAuth()
        gauth.Auth(token)
        gauth.SaveCredentialsFile(os.path.join(Creds_path, user_id))
        a = await message.reply_text("Authorized successfully 🥳🥳")
        try:

            if os.path.isfile(os.path.join(Creds_path, user_id)):
                chat_id = message.from_user.id,
                conn = psycopg2.connect(Post_url)
                cur = conn.cursor()
                file = open(os.path.join(Creds_path, str(user_id)), 'r')
                Auth = file.read()
                file.close()
                cur.execute(
                    '''SELECT AUTH FROM USERINFO WHERE chat_id = %s ''', (chat_id,))
                row = cur.fetchone()
                if row is None:
                    query = "INSERT INTO USERINFO (chat_id, AUTH) VALUES (%s,%s)"
                    cur.execute(query, (chat_id, Auth))
                conn.commit()
                # await a.edit("Token added to database.")
                LOGGER.info(f"{chat_id}: Token Added To database")
        except Exception as e:
            await a.edit(e)
    except Exception as e:
        print("Auth Error :", e)
        # TODO Auth error msg
        await message.reply_text(f"Auth Error: \n `{e}`\n\n #error ")


def token_make(_, message):

    user_id = str(message.from_user.id)
    if not os.path.isfile(os.path.join(Creds_path, str(user_id))):
        conn = psycopg2.connect(Post_url)
        cur = conn.cursor()
        cur.execute(
            '''SELECT AUTH FROM USERINFO WHERE chat_id = %s''', (user_id,))
        row = cur.fetchone()
        if row is not None:
            A = row[0]
            # os.mknod(os.path.join(Creds_path,str(user_id)))
            f = open(os.path.join(Creds_path, str(user_id)), "w")
            f.write(A)
            f.close()
            LOGGER.info(f"{user_id} : Token File Created")
            return True
        else:
            return False
    else:
        return True
