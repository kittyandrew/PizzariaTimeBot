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

lists = {"🍕 Піца": pizzas_list,
         "🥤 Напої": drinks_list,
         "🍲 Соуси": sauces_list}
datas = {"🍕 Піца": "pizza",
         "🥤 Напої": "drinks",
         "🍲 Соуси": "sauces"}

async def init(bot, img_cache, global_bucket):
    @bot.on(events.NewMessage(pattern="^/(start|new)($|@.+)"))
    async def start_command(event:Event):
        global_bucket[str(event.chat_id)] = Basket()
        main_text = "Привіт, я бот **Pizzatime**! За допомогою мене ви можете оформити замовлення.\n" \
                    "**Оберіть категорію.**"
        await event.respond(main_text, buttons=buttons.main_menu)

    @bot.on(events.NewMessage(func=lambda x: x.text in ["🍕 Піца", "🍲 Соуси", "🥤 Напої"]))
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

    @bot.on(events.NewMessage(func=lambda x: x.text == "🛒 Перевірити кошик"))
    async def check_basket(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        await event.respond(basket.parse_products(), buttons=buttons.main_menu)

    @bot.on(events.NewMessage(func=lambda x: x.text == "📋 Оформити замовлення"))
    async def ask_contacts(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        if not len(basket):
            await event.respond("Ви не можете оформити порожнє замовлення..", buttons=buttons.main_menu)
            return
        await event.respond("Виберіть спосіб оплати", buttons=buttons.payment_button)

    @bot.on(events.NewMessage(func=lambda x: x.text == "💵 Оплата готівкою"))
    async def in_cash(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        basket.payment_method = "готівкою"
        await event.respond("Виберіть спосіб вводу контактів.", buttons=buttons.contacts_button)

    @bot.on(events.NewMessage(func=lambda x: x.text == "💳 Оплата на картку"))
    async def in_card(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        await event.respond("`Отримувач:`\nОлександр Андрійович\n`Картка:`\n5169360006344356")
        basket.payment_method = "на картку"
        await asyncio.sleep(3)
        await event.respond("Виберіть спосіб вводу контактів.", buttons=buttons.contacts_button)

    @bot.on(events.NewMessage(func=lambda x: x.text == "🍕 Піца з половинок"))
    async def half_pizzas(event: Event):
        await event.respond("Оберіть дві половинки:", buttons=buttons.halfs_menu())

    @bot.on(events.NewMessage(func=lambda x: x.text == "↪ Меню"))
    async def _main_menu(event: Event):
        await event.respond("**Головне меню**", buttons=buttons.main_menu)

    @bot.on(events.NewMessage(func=lambda x: any(x.text == item.name for item in halfs_pizzas)))
    async def waiting_part(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        for item in halfs_pizzas:
            if item.name == event.text:
                break
        basket.set_part(item())
        if basket.waiting_for_part:
            await event.respond("Оберіть іншу половинку:", buttons=buttons.halfs_menu(True))
        else:
            await event.respond("Піца з половинок додана до вашого кошика.\n**Головне меню**",
                                buttons=buttons.main_menu)

    @bot.on(events.NewMessage(func=lambda x: x.text == "📩 Контактна інформація"))
    async def contacts(event: Event):
        text = "Контактна інформація:\n`Тел.:` +380 96 744 222 4\n`Inst.:` pizzatimebc замовити в direct\n" \
               "`Web.:` [www.pizzatime.com.ua](https://www.pizzatime.com.ua/)\n\nСпівпраця та пропозиції:\n" \
               "`Email:` pizzatimebc.info@gmail.com"
        await event.respond(text, link_preview=False, buttons=buttons.main_menu)

    @bot.on(events.NewMessage(pattern="^Ввести номер телефону$"))
    async def ask_phone(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        basket.waiting_for_contacts = True
        await event.respond("Ваш телефон:", buttons=buttons.wait_for_input)
        raise events.StopPropagation()

    @bot.on(events.NewMessage(pattern="^Ввести адресу$"))
    async def ask_address(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        basket.waiting_for_address = True
        await event.respond("Ваша адреса:\n`Будь ласка, укажіть назву вулиці/номер будинку/під'їзд/квартиру`", buttons=buttons.wait_for_input)
        raise events.StopPropagation()

    # Global msg reader
    @bot.on(events.NewMessage)
    async def listen_to_chat(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
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
                first_name = event.chat.username
            else:
                first_name = 0
            if first_name is None:
                first_name = 0
            await event.respond("Підтвердіть замовлення\n(Щоб стерти замовлення введіть `/new`)",
                                buttons=buttons.accept_order(event.chat_id, first_name))
        elif basket.waiting_for_odd_info:
            basket.add_odd_info(event.text)
            basket.waiting_for_odd_info = False
            # Done
            await event.respond(basket.parse(),
                                parse_mode="html",
                                link_preview=False,
                                buttons=buttons.clear)
            if isinstance(event.chat, User):
                first_name = event.chat.first_name
            else:
                first_name = 0
            await event.respond("Підтвердіть замовлення\n(Щоб стерти замовлення введіть `/new`)",
                                buttons=buttons.accept_order(event.chat_id, first_name))

    # Accept geo or phone num
    @bot.on(events.NewMessage(func=lambda x: any([x.contact, x.geo])))
    async def shared_data(event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        if event.contact:
            basket.add_contacts(event.media.phone_number)
            await event.respond("Виберіть спосіб вводу адреси доставки.", buttons=buttons.address_buttons)
        elif event.geo:
            basket.add_address(event.geo)
            await event.respond("Вкажіть будинок/поверх/квартиру:", buttons=buttons.wait_for_input)

