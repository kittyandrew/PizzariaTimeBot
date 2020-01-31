from telethon.tl.custom import Message
from telethon import events, Button
from typing import Union
import time

chats = {}
MSG = \
"""По питанням підтримки звертатися за адресою `pizzatimebc.info@gmail.com`

`author:` [Ändrew Pythonista](@kitty_andrew)
`fiverr:` [buy bot](https://www.fiverr.com/kitty_andrew?up_rollout=true)"""

async def init(bot, *args, **kwargs):
    @bot.on(events.NewMessage(pattern=r"^/support($|@pizzatimebcbot$)"))
    async def support_handler(event):
        if chats.get(event.chat_id, False):
            delta = chats[event.chat_id] - time.time()
            if delta > 60:
                await event.respond(MSG, link_preview=False)
        else:
            chats[event.chat_id] = time.time()
            await event.respond(MSG, link_preview=False)

        try:
            await event.delete()
        except:
            pass