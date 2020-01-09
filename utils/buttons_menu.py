from telethon import Button

class buttons:
    main_menu = [[Button.text("Піца", resize=True, single_use=True), Button.text("Соуси"), Button.text("Напої")],
                 [Button.text("Перевірити кошик"), Button.text("Оформити замовлення")]]

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

    wait_for_input = Button.force_reply()

    @staticmethod
    def accept_order(chat_id, first_name):
        return Button.inline("✅ Підтвердити", f"order confirmed|{chat_id}|{first_name}")