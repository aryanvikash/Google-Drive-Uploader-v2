# from pyrogram import Client, filters
# from bot import aria2, LOGGER, adminList
#
#
# # TODO Add all running downloads in status
#
#
# @Client.on_message(filters.command(["status"]) & filters.user(adminList))
# async def show_status(_, message):
#     files = aria2.get_downloads()
#
#     status_list = get_status_str(files)
#
#     try:
#
#         if len(status_list) > 4096:
#             LOGGER.error(" status length Exceeded")
#             await message.reply_text("length exceed")
#             with open("status.txt", "w") as f:
#                 f.write(status_list)
#
#             await message.reply_document(document="status.txt")
#         else:
#             try:
#                 await message.reply_text(status_list)
#             except Exception as e:
#                 await message.reply_text(e)
#             LOGGER.info("status send")
#
#     except Exception as e:
#         LOGGER.error(e)
#         await message.reply_text(e)
#
#
# def get_status_str(files):
#     status_list = "init \n"
#     for file in files:
#         msg = ""
#         try:
#             msg += f"\nDownloading File: `{file.name}`"
#         except ValueError:
#             msg += f"\nDownloading File: `N/A`"
#
#         msg += f"\nSpeed: {file.download_speed_string()}"
#         msg += f"\nProgress: {file.progress_string()}"
#         msg += f"\nTotal Size: {file.total_length_string()}"
#         msg += f"\nStatus: {file.status}"
#         msg += f"\nETA: {file.eta_string()}"
#         msg += f"\n<code>/cancel {file.gid}</code> \n"
#         if file.status == "active":
#             status_list += msg
#
#     return status_list
