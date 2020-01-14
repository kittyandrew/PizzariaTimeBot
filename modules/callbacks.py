from utils.buttons_menu import buttons
from my_types.basic import Basket, Counter
from products.pizzas import *
from products.drinks import *
from products.sauces import *
from telethon import events, Button
import config as c
import logging
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

lists = {"pizza": pizzas_list,
         "drinks": drinks_list,
         "sauces": sauces_list}

counter = Counter()

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(c.LOGIN, c.PASSWORD)

def is_connected(conn):
    try:
        status = conn.noop()[0]
    except:  # smtplib.SMTPServerDisconnected
        status = -1
    return True if status == 250 else False

def ensure_connection():
    global server
    if not is_connected(server):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(c.LOGIN, c.PASSWORD)

async def post_order(bot, basket, user_id, chat):
    ensure_connection()
    basket.set_order_time()
    text = basket.parse_finally(user_id, chat)
    email = MIMEMultipart('alternative')
    email["Subject"] = f"Замовлення ботом #{counter.get()}"
    email['From'] = c.LOGIN
    email['To'] = c.TARGET
    email_text = f"""\
<html>
  <head></head>
  <body>
  {text}
    </body>
</html>
"""
    email.attach(MIMEText(email_text, "html"))
    # Sending via mail
    server.sendmail(c.LOGIN, c.TARGET, email.as_string())

async def init(bot, img_cache, global_bucket):
    @bot.on(events.CallbackQuery)
    async def callback_query(event):
        data:str = event.data.decode("utf-8")

        _List = lists.get(data.split("|")[0], None)

        if data == "back to main":
            await event.delete()
            text = "**Головне меню**"
            await event.respond(text, buttons=buttons.main_menu)
        elif "back to main" in data:
            await event.delete()
            _id = data.split("|")[-1]
            await bot.delete_messages(event.chat_id, int(_id) + 1)
            text = "**Головне меню**"
            await event.respond(text, buttons=buttons.main_menu)
        elif "pizza is ready" in data:
            bucket = global_bucket[data.split("|")[-1]]
            bucket.accept_pizza()
            msg_id = data.split("|")[-2]
            await event.delete()
            await bot.delete_messages(event.chat_id, int(msg_id) + 1)
            await event.answer("Товар був доданий до вашого кошика")
            text = "Піца додана до вашого кошика!\n**Головне меню**"
            await event.respond(text, buttons=buttons.main_menu)
        elif "i_prev" in data or "i_next" in data:
            index = int(data.split("|")[-1])
            msg_id = data.split("|")[-2]
            if index < 0:
                index = 19
            elif index > 19:
                index = 0
            item, cost = Ingredient(index).show()
            msg = f"`Вибір інгредієнтів {index + 1}/20`\n"
            msg += f"`Назва:` {item}\n"
            msg += f"`Ціна:` {cost}"
            await event.edit(msg,
                             buttons=buttons.pizza_from_scratch(index - 1,
                                                                event.chat_id,
                                                                index + 1,
                                                                index,
                                                                message_id=msg_id))
        elif "ingredient" in data:
            _, _msg_id, _chat_id, curr_index = data.split("|")
            bucket = global_bucket[_chat_id]
            bucket.add_ingredient(int(curr_index))
            msg1, msg2 = bucket.parse_pizza_from_scratch(int(curr_index))
            await bot.edit_message(int(_chat_id), int(_msg_id) + 1, msg1)
            await event.edit(msg2,
                             buttons=buttons.pizza_from_scratch(int(curr_index) - 1,
                                                                event.chat_id,
                                                                int(curr_index) + 1,
                                                                int(curr_index),
                                                                message_id=_msg_id))
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
            await event.respond("🎉 Готово! Очікуйте замовлення найближчим часом.", buttons=buttons.main_menu)
            global_bucket[chat_id] = Basket()
