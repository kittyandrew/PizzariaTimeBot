from telethon import Button
from products.pizzas import *

class buttons:
    main_menu = [[Button.text("🍕 Піца", resize=True, single_use=True), Button.text("🍕 Піца з половинок")],
                  [Button.text("🍲 Соуси"), Button.text("🥤 Напої")],
                 [Button.text("🛒 Перевірити кошик"), Button.text("📋 Оформити замовлення")],
                 [Button.text("📩 Контактна інформація")]]

    @staticmethod
    def halfs_menu(single_click = False):
        if single_click:
            btn = Button.text(HalfNizhna.name, resize=True, single_use=True)
        else:
            btn = Button.text(HalfNizhna.name, resize=True, selective=True)
        return [[ btn,
                   Button.text(HalfApetitna.name),
                   Button.text(HalfSitna.name)],
               [Button.text(HalfSalyami.name),
                   Button.text(HalfSokovita.name),
                   Button.text(HalfFourChese.name)],
               [Button.text(HalfPikantna.name),
                   Button.text(HalfFourMeat.name),
                   Button.text("↪ Меню")]]

    @staticmethod
    def products_menu(previous, chat_id, next, curr_index, product_type = None):
        return [[Button.inline("⬅ Попередня", f"{product_type}|previous|{previous}".encode("utf-8")),
                Button.inline("↪ Меню", "back to main".encode("utf-8")),
                Button.inline("➡ Наступна", f"{product_type}|next|{next}".encode("utf-8"))],
                [Button.inline("🛒 В кошик", f"{product_type}|choice|{chat_id}|{curr_index}".encode("utf-8"))]]

    address_buttons = [Button.text("Ввести адресу", resize=True, single_use=True),
                       Button.request_location("Відправити геоданні")]

    contacts_button = [Button.text("Ввести номер телефону", resize=True, single_use=True),
                       Button.request_phone("Використати телефон аккаунтa")]

    payment_button = [Button.text("💵 Оплата готівкою", resize=True, single_use=True),
                      Button.text("💳 Оплата на картку")]

    wait_for_input = Button.force_reply()

    clear = Button.clear()

    @staticmethod
    def accept_order(chat_id, first_name):
        return Button.inline("✅ Підтвердити", f"order confirmed|{chat_id}|{first_name}")