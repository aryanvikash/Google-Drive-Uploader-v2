from pyrogram import Client, Filters, StopPropagation,InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(Filters.callback_data("test"))
async def dta_catch(c, m):
      cb_data = m.data
      print(cb_data)
      await c.answer_callback_query(
            callback_query_id=m.id,
            text="who are you? 🤪🤔🤔🤔",
            show_alert=True,
            cache_time=0
        )
        

# @Client.on_callback_query(Filters.callback_data("cancel"))
# async def cancel_aria(c, m):
#       cb_data = m.data
#       print(cb_data)
#       await c.answer_callback_query(
#             callback_query_id=m.id,
#             text="Cancel 🤪🤔🤔🤔",
#             show_alert=True,
#             cache_time=0
#         )