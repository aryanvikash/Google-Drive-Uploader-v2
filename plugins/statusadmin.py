from bot import aria2
from pyrogram import Client, Filters
from bot.customFilters.admin_filter import is_admin
# TODO Add all running downloads in status


@Client.on_message(Filters.command(["status"]) & is_admin)
async def show_status(client, message):
    files = aria2.get_downloads()
    status_List = ""

    for file in files:
        msg = ""
        msg += f"\nDownloading File: `{file.name}`"
        msg += f"\nSpeed: {file.download_speed_string()}"
        msg += f"\nProgress: {file.progress_string()}"
        msg += f"\nTotal Size: {file.total_length_string()}"
        msg += f"\nStatus: {file.status}"
        msg += f"\nETA: {file.eta_string()}"
        msg += f"\n<code>/cancel {file.gid}</code> \n"
        if file.status == "active":
            status_List += msg

    try:
        if not status_List:
            await message.reply_text("no active Download")
        else:
            if len(status_List) > 4096:
                with open("status.txt", "w") as f:
                    f.write(status_List)

                print("length Exceeded")
                await message.reply_document(document="status.txt")
            else:
                try:
                    await message.reply_text(status_List)
                except Exception as e:
                    await message.reply_text(e)
                print("Status Sent")

    except Exception as e:
        await message.reply_text(e)
