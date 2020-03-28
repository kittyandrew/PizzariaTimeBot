from utils.buttons_menu import buttons
from telethon.tl.custom import Message
from my_types.basic import Basket
from products.pizzas import *
from products.drinks import *
from products.sauces import *
from products.meals import *
from telethon import events, Button
from telethon.tl.types import User
from typing import Union
import logging
import asyncio
import re
Event = Union[Message, events.NewMessage]

lists = {"🍕 Піца": pizzas_list,
         "🥤 Напої": drinks_list,
         "🍲 Соуси": sauces_list,
         "🍗 Снеки": meals_list}
datas = {"🍕 Піца": "pizza",
         "🥤 Напої": "drinks",
         "🍲 Соуси": "sauces",
         "🍗 Снеки": "meals"}

async def init(bot, img_cache, global_bucket, sales_obj):
    @bot.on(events.NewMessage(pattern="^/(start|new)($|@pizzatimebcbot$)"))
    async def start_command(event:Event):
        global_bucket[str(event.chat_id)] = Basket()
        main_text = "Привіт, я бот **Pizzatime**! За допомогою мене ви можете оформити замовлення.\n" \
                    "**Оберіть категорію.**\n\nПерегляньте доступні акції за допомогою команди /offers"
        await event.respond(main_text, buttons=buttons.main_menu)

    @bot.on(events.NewMessage(pattern=r"^/offers($|@pizzatimebcbot$)"))
    async def offers_handler(event:Event):
        await event.respond(sales_obj.parse(), buttons=buttons.main_menu)

    @bot.on(events.NewMessage(pattern=r"^/new_offer($|@pizzatimebcbot$)"))
    async def new_offer_handler(event:Event):
        if sales_obj.admin_detected(event.chat_id):
            sales_obj.init_buffer(event.chat_id)
            await event.respond("Створення нової акції.", buttons=buttons.clear)
            await event.respond("**Введіть назву:**", buttons=buttons.wait_for_input)
            raise events.StopPropagation()

    @bot.on(events.NewMessage(pattern=r"^/del_offer(|@pizzatimebcbot) .+"))
    async def del_offer_handler(event: Event):
        if sales_obj.admin_detected(event.chat_id):
            sales_obj.add_del_name(re.sub("r^/del_offer(|@pizzatimebcbot)", "", event.text))
            await event.respond("Акція з такою назвою буде видалена через декілька секунд!")
            raise events.StopPropagation()

    @bot.on(events.NewMessage(func=lambda x: x.text))
    async def offer_title_handler(event:Event):
        if sales_obj.is_status(event.chat_id, "new"):
            await event.respond("**Введіть текст акції:**\n"
                                "`Цей текст має надати користувачу уявленя про зміст акції`",
                                buttons=buttons.wait_for_input)
            sales_obj.add_discount(event.chat_id, event.text)
            raise events.StopPropagation()

    @bot.on(events.NewMessage(func=lambda x: x.text))
    async def offer_text_handler(event:Event):
        if sales_obj.is_status(event.chat_id, "text"):
            await event.respond("**Введіть час дії акції:**\n"
                                "`Необхідний формат:` чч:мм-чч:мм",
                                buttons=buttons.wait_for_input)
            sales_obj.set_text(event.chat_id, event.text)
            raise events.StopPropagation()

    @bot.on(events.NewMessage(func=lambda x: x.text))
    async def offer_time_handler(event: Event):
        if sales_obj.is_status(event.chat_id, "time"):
            await event.respond("**Акція була успішно додана! Зміни можна буде побачити через декілька секунд**",
                                buttons=buttons.clear)
            await event.respond("**Головне меню**\n\nДля перегляду доступних акцій введіть /offers",
                                buttons=buttons.main_menu)
            sales_obj.set_time(event.chat_id, event.text)
            raise events.StopPropagation()

    @bot.on(events.NewMessage(func=lambda x: x.text in ["🍕 Піца", "🍲 Соуси", "🥤 Напої", "🍗 Снеки"]))
    async def pizza_menu(event: Event):
        _List = lists[event.text]
        _data = datas[event.text]
        try:
            await event.respond(_List[0].parse(),
                                file=img_cache[_List[0].__name__],
                                buttons=buttons.products_menu(len(_List) - 1, event.chat_id, 1, 0, _data))
        except KeyError as e:
            print(e)
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
        await event.respond(f"`Сума до оплати:`\n{basket.price} грн.\n`Отримувач:`\nОлександр Андрійович\n`Картка:`\n5169360006344356")
        basket.payment_method = "на картку"
        await asyncio.sleep(3)
        await event.respond("Виберіть спосіб вводу контактів.", buttons=buttons.contacts_button)

    @bot.on(events.NewMessage(func=lambda x: x.text == "🍕 Піца з половинок"))
    async def half_pizzas(event: Event):
        await event.respond("Оберіть дві половинки:", buttons=buttons.halfs_menu())

    @bot.on(events.NewMessage(func=lambda x: x.text == "🍕 Конструктор піци"))
    async def pizza_constructor(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        basket.set_pizza()
        await event.respond("Оберіть соус-основу для піци.", buttons=buttons.pizza_basement)

    @bot.on(events.NewMessage(pattern=r"Томатний соус|Вершковий соус"))
    async def pizza_construction(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        if event.text == "Томатний соус":
            basket.set_sauce("tomato")
        elif event.text == "Вершковий соус":
            basket.set_sauce("vershkovii")

        await event.respond("Оберіть сир-основу для піци.", buttons=buttons.pizza_basement_cheese)

    @bot.on(events.NewMessage(pattern=r"сир Моцарелла|сир Сулугуні"))
    async def middle_constructor(event: Event):
        try:
            basket = global_bucket[str(event.chat_id)]
        except:
            global_bucket[str(event.chat_id)] = Basket()
            basket = global_bucket[str(event.chat_id)]
        if event.text == "сир Моцарелла":
            basket.set_cheese("mozarella")
        elif event.text == "сир Сулугуні":
            basket.set_cheese("sylygyni")

        msg1, msg2 = basket.parse_pizza_from_scratch(0)
        await event.respond(msg1)
        await event.respond(msg2, buttons=buttons.pizza_from_scratch(len(Ingredient.products), event.chat_id, 1, 0, message_id=event.id))

    @bot.on(events.NewMessage(func=lambda x: x.text == "↪ Меню"))
    async def _main_menu(event: Event):
        await event.respond("**Головне меню**\n\nДля перегляду доступних акцій введіть /offers", buttons=buttons.main_menu)

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
        text = "Контактна інформація:\n`Тел.:` +380 96 744 222 4\n" \
               "`Inst.:` [pizzatimebc](https://www.instagram.com/pizzatimebc/) (замовляти в direct)\n" \
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

