from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
geolocator = Nominatim()

class Basket:
    def __init__(self):
        self.items = []
        self.address = None
        self.contacts = None
        self.waiting_for_address = False
        self.waiting_for_contacts = False

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
        result += f"<code>Ціна:</code> {price}₴\n"
        result += f"<code>Адреса:</code> {self.address}\n"
        result += f"<code>Контакти:</code> {self.contacts}\n"
        return result

    def parse_finally(self, user_id, chat=None):
        result = self.parse()
        if chat:
            result += f"<code>Користувач:</code> <a href=\"tg://user?id={user_id}\">{chat}</a>"
        return result

    def __len__(self):
        return len(self.items)


