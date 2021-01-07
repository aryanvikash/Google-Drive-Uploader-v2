import os
# from plugins.support import TEXT
import psycopg2
from bot import Post_url, Creds_path, LOGGER
from pyrogram import Client, filters

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


@Client.on_message(filters.command(["logout"]))
async def revoke(client, message):
    ID = str(message.from_user.id)
    chat_id = message.from_user.id
    conn = psycopg2.connect(Post_url)
    cur = conn.cursor()
    if os.path.isfile(os.path.join(Creds_path, ID)):
        # await message.reply_text(f"Logout Successfully 😊")
        os.remove(os.path.join(Creds_path, ID))
        cur.execute(
            '''SELECT AUTH FROM USERINFO WHERE chat_id = %s ''', (chat_id,))
        row = cur.fetchone()
        if row is not None:
            cur.execute(
                '''DELETE FROM USERINFO WHERE chat_id = %s ''', (chat_id,))
            # await bot.send_message(
            #     chat_id=update.chat.id,
            #     text="Deleted Your Auth token from database.",
            #     reply_to_message_id=update.message_id
            # )
            await message.reply_text("Logout Successfully 😊")
            LOGGER.info(f"{chat_id} : Removed From Database")
            conn.commit()
        else:
            # await bot.send_message(
            #     chat_id=update.chat.id,
            #     text="No auth token found in database.",
            #     reply_to_message_id=update.message_id
            # )
            await message.reply_text("No Auth Token Found In Database !!")
    else:
        # await bot.send_message(chat_id=update.chat.id, text="Revoke fail
        # text")
        await message.reply_text("You Have To Login First")
