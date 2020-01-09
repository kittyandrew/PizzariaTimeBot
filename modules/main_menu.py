from utils.buttons_menu import buttons
from telethon.tl.custom import Message
from my_types.basic import Basket
from products.pizzas import *
from products.drinks import *
from products.sauces import *
from telethon import events, Button
from telethon.tl.types import User
from typing import Union
import logging
import asyncio
Event = Union[Message, events.NewMessage]

lists = {"Піца": pizzas_list,
         "Напої": drinks_list,
         "Соуси": sauces_list}
datas = {"Піца": "pizza",
         "Напої": "drinks",
         "Соуси": "sauces"}

async def init(bot, img_cache, global_bucket):
    @bot.on(events.NewMessage(pattern="^/(start|new)($|@.+)"))
    async def start_command(event:Event):
        global_bucket[str(event.chat_id)] = Basket()
        main_text = "Привіт, я бот **Pizzatime**! За допомогою мене ви можете оформити замовлення.\n" \
                    "**Оберіть категорію.**"
        await event.respond(main_text, buttons=buttons.main_menu)

    @bot.on(events.NewMessage(pattern="^(Піца|Соуси|Напої)$"))
    async def pizza_menu(event: Event):
        _List = lists[event.text]
        _data = datas[event.text]
        try:
            await event.respond(_List[0].parse(),
                                file=img_cache[_List[0].__name__],
                                buttons=buttons.products_menu(len(_List) - 1, event.chat_id, 1, 0, _data))
        except KeyError:
            pass
        except Exception as e:
            file = await bot.upload_file(_List[0]().img)
            img_cache[_List[0].__name__] = file
            await event.respond(_List[0].parse(),
                                file=file,
                                buttons=buttons.products_menu(len(_List) - 1, event.chat_id, 1, 0, _data))
            raise e

    @bot.on(events.NewMessage(pattern="^Перевірити кошик$"))
    async def check_basket(event: Event):
        basket = global_bucket[str(event.chat_id)]
        await event.respond(basket.parse_products(), buttons=buttons.main_menu)

    @bot.on(events.NewMessage(pattern="^Оформити замовлення$"))
    async def ask_contacts(event: Event):
        basket = global_bucket[str(event.chat_id)]
        if not len(basket):
            await event.respond("Ви не можете оформити порожнє замовлення..", buttons=buttons.main_menu)
            return
        await event.respond("Виберіть спосіб вводу контактів.", buttons=buttons.contacts_button)

    @bot.on(events.NewMessage(pattern="^Ввести номер телефону$"))
    async def ask_phone(event: Event):
        basket = global_bucket[str(event.chat_id)]
        basket.waiting_for_contacts = True
        await event.respond("Ваш телефон:", buttons=buttons.wait_for_input)
        raise events.StopPropagation()

    @bot.on(events.NewMessage(pattern="^Ввести адресу$"))
    async def ask_address(event: Event):
        basket = global_bucket[str(event.chat_id)]
        basket.waiting_for_address = True
        await event.respond("Ваша адреса:", buttons=buttons.wait_for_input)
        raise events.StopPropagation()

    # Global msg reader
    @bot.on(events.NewMessage)
    async def listen_to_chat(event: Event):
        basket = global_bucket[str(event.chat_id)]
        if basket.waiting_for_contacts:
            basket.add_contacts(event.text)
            basket.waiting_for_contacts = False
            await event.respond("Виберіть спосіб вводу адреси доставки.", buttons=buttons.address_buttons)

        elif basket.waiting_for_address:
            basket.add_address(event.text)
            basket.waiting_for_address = False
            # Show details and ask last time
            await event.respond(basket.parse(),
                                parse_mode="html",
                                link_preview=False)
            if isinstance(event.chat, User):
                first_name = event.chat.first_name
            else:
                first_name = 0
            await event.respond("Підтвердіть замовлення\n(Щоб стерти замовлення введіть `/new`)",
                                buttons=buttons.accept_order(event.chat_id, first_name))

    # Accept geo or phone num
    @bot.on(events.NewMessage(func=lambda x: any([x.contact, x.geo])))
    async def shared_data(event):
        basket = global_bucket[str(event.chat_id)]
        if event.contact:
            basket.add_contacts(event.media.phone_number)
            await event.respond("Виберіть спосіб вводу адреси доставки.", buttons=buttons.address_buttons)
        elif event.geo:
            basket.add_address(event.geo)
            # Done
            await event.respond(basket.parse(),
                                parse_mode="html",
                                link_preview=False)
            if isinstance(event.chat, User):
                first_name = event.chat.first_name
            else:
                first_name = 0
            await event.respond("Підтвердіть замовлення\n(Щоб стерти замовлення введіть `/new`)",
                                buttons=buttons.accept_order(event.chat_id, first_name))


