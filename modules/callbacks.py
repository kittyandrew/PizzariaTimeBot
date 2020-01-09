from utils.buttons_menu import buttons
from my_types.basic import Basket
from products.pizzas import *
from products.drinks import *
from products.sauces import *
from telethon import events, Button
import config as c
import logging
import asyncio

lists = {"pizza": pizzas_list,
         "drinks": drinks_list,
         "sauces": sauces_list}

async def post_order(bot, basket, user_id, chat):
    text = basket.parse_finally(user_id, chat)
    await bot.send_message(c.CHANNEL_ID, text,
                           parse_mode="html",
                           link_preview=False)
    basket = Basket()

async def init(bot, img_cache, global_bucket):
    @bot.on(events.CallbackQuery)
    async def callback_query(event):
        data:str = event.data.decode("utf-8")

        _List = lists.get(data.split("|")[0], None)

        if data == "back to main":
            await event.delete()
            text = "**Головне меню**"
            await event.respond(text, buttons=buttons.main_menu)
        elif "previous" in data or "next" in data:
            index = int(data.split("|")[-1])
            if index < 0:
                index = len(_List) - 1
            elif index >= len(_List):
                index = 0
            product_type = data.split("|")[0]
            try:
                await event.edit(_List[index].parse(),
                                 file=img_cache[_List[index].__name__],
                                 buttons=buttons.products_menu(index - 1, event.chat_id, index + 1, index, product_type))
            except KeyError:
                pass
            except Exception as e:
                await event.edit(_List[index].parse(),
                                 file=_List[index]().img,
                                 buttons=buttons.products_menu(index - 1, event.chat_id, index + 1, index,
                                                               product_type))
            raise e

        elif "choice" in data:
            *_, _chat_id, index = data.split("|")
            global_bucket[_chat_id].add_item(_List[int(index)])
            await event.answer("Товар був доданий до вашого кошика")

        elif "order confirmed" in data:
            _, chat_id, first_name = data.split("|")
            if first_name == "0":
                first_name = None
            text = global_bucket[chat_id].parse()
            await post_order(bot, global_bucket[chat_id], chat_id, first_name)
            await event.delete()
            await event.respond("Готово! Очікуйте замовлення найближчим часом.")
