from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import datetime
import pickle
import os
geolocator = Nominatim()

class Basket:
    def __init__(self):
        self.items = []
        self.address = None
        self.contacts = None
        self.waiting_for_address = False
        self.waiting_for_contacts = False
        self.waiting_for_odd_info = False
        self.odd_address_info = None
        self.need_extra_info = False
        self.waiting_for_part = False
        self.first_half = None
        self.order_time = None
        self.payment_method = None

    def set_part(self, part):
        if self.first_half is None:
            self.waiting_for_part = True
            self.first_half = part
        else:
            self.add_item(self.first_half + part)
            self.waiting_for_part = False
            self.first_half = None

    def add_item(self, item):
        self.items.append(item)

    def add_contacts(self, contacts):
        self.contacts = contacts

    def add_address(self, address):
        if isinstance(address, str):
            self.address = address
        else:
            try:
                location = geolocator.reverse(f"{address.lat}, {address.long}", timeout=15)
            except GeocoderTimedOut:
                location = "Карта"
            self.address = f'<a href="https://maps.google.com/maps?q={address.lat},{address.long}&z=16">' \
                           f'{location.address}</a>'
            self.need_extra_info = True
            self.waiting_for_odd_info = True

    def add_odd_info(self, address):
        self.odd_address_info = address

    def set_order_time(self):
        tz = datetime.timezone(datetime.timedelta(hours=2))
        self.order_time = datetime.datetime.now(tz)

    def is_ready(self):
        return all(self.address, self.contacts)

    def parse_products(self):
        if not len(self.items):
            return "Ваш кошик пустий, спочатку замовте щось!"

        _tmp = {}
        for each in self.items:
            _count = _tmp.get(each, None)
            if _count is None:
                _tmp[each] = 1
            else:
                _tmp[each] = _count + 1
        result = "`Ваше замовлення:`\n"
        for item, count in _tmp.items():
            result += f"{item.name} `×` {count} шт.\n"
        return result

    def parse(self):
        price = 0
        _tmp = {}
        for each in self.items:
            _count = _tmp.get(each, None)
            if _count is None:
                _tmp[each] = 1
            else:
                _tmp[each] = _count + 1
        result = "<code>Замовлення:</code>\n"
        for item, count in _tmp.items():
            result += f"{item.name} <code>×</code> {count} шт.\n"
            price += int(item.price.strip("₴")) * count
        result += "\n"
        result += f"<code>Ціна:</code> {price} грн.\n"
        result += f"<code>Спосіб оплати:</code> {self.payment_method}\n"
        if self.need_extra_info:
            result += f"<code>Адреса:</code> {self.address}\n"
            result += f"<code>Точні дані:</code> {self.odd_address_info}\n"
        else:
            result += f"<code>Адреса:</code> {self.address}\n"
        result += f"<code>Контактні дані:</code> {self.contacts}\n"
        return result

    def parse_finally(self, user_id, chat=None):
        result = self.parse()
        result = result.replace("\n", "<br>")
        if chat:
            result += f"<code>Користувач:</code> <a href=\"https://t.me/{chat}\">{chat}</a><br>"
        result += f"<code>Дата замовлення:</code> {self.order_time.strftime('%d/%m/%Y, %H:%M:%S')}"
        return result

    def __len__(self):
        return len(self.items)

class Counter:
    file_name = "counter.pickle"
    def __init__(self):
        self.load_state()

    def load_state(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "rb") as _file:
                self.counter = pickle.load(_file)
        else:
            self.counter = 0
            self.save()

    def save(self):
        with open(self.file_name, "wb") as _file:
            pickle.dump(self.counter, _file)

    def get(self):
        self.counter += 1
        self.save()
        return self.counter
