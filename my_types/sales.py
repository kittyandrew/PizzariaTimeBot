from typing import Union, Dict
import datetime
import pickle
import os

class UserBuffer:
    _status_neutral = "neutral"
    _status_text = "text"
    _status_time = "time"
    statuses = [_status_text, _status_time]
    def __init__(self):
        self.buffer = ""
        self.status = "new"

    def null_status(self):
        self.status = self._status_neutral

    def set_status(self, status):
        if status in self.statuses:
            self.status = status

    def get_status(self):
        return self.status

    def fill_buffer(self, value):
        self.buffer += value

    def pop_buffer(self):
        result = self.buffer
        self.buffer = ""
        return result

class BotSales:
    ADMINS = [568292500, 688282351]
    PATH = "discounts.pickle"
    def __init__(self):
        self.load_instance()
        self.tmp_discounts = {}
        self.buffer = {}
        self.names_to_delete = []

    def add_del_name(self, name):
        self.names_to_delete.append(name)

    def is_status(self, user_id, status):
        if self.admin_detected(user_id):
            tmp = self.buffer.get(user_id, False)
            if tmp:
                 return status == tmp.get_status()

    def admin_detected(self, user_id):
        return user_id in self.ADMINS

    def init_buffer(self, key):
        self.buffer[key] = UserBuffer()

    def fill_buffer(self, key, value):
        self.buffer[key].fill_buffer(value)

    def pop_buffer(self, key):
        return self.buffer[key].pop_buffer()

    def do_actions(self):
        for discount in self.tmp_discounts.values():
            if discount.was_created:
                self.discounts["existing"].append(discount)

        vars = list(self.tmp_discounts.values())
        keys = list(self.tmp_discounts.keys())

        for discount in self.discounts["existing"]:
            if discount in vars:
                self.tmp_discounts.pop(keys[vars.index(discount)])
            if discount.name in self.names_to_delete:
                self.discounts["existing"].remove(discount)
                self.names_to_delete.remove(discount.name)
                continue

            if discount.active:
                if discount.time_passed:
                    discount.deactivate()
            else:
                if discount.is_time:
                    discount.activate()
        self.names_to_delete = []

    def add_discount(self, new_key, new_name):
        discount = Discount()
        discount.set_title(new_name)
        self.tmp_discounts[new_key] = discount
        self.buffer[new_key].set_status("text")

    def set_text(self, key, new_text):
        self.tmp_discounts[key].set_text(new_text)
        self.buffer[key].set_status("time")

    def set_time(self, key, new_time):
        self.tmp_discounts[key].set_time(new_time)
        # Idenify as "Created"
        self.tmp_discounts[key].finished_creation = True
        self.buffer[key].null_status()

    def load_instance(self):
        if os.path.exists(self.PATH):
            with open(self.PATH, "rb") as _file:
                self.discounts = pickle.load(_file)
        else:
            self.discounts = {"existing": []}
            self.save()

    def save(self):
        with open(self.PATH, "wb") as _file:
            pickle.dump(self.discounts, _file)

    def parse(self):
        separator = "`" + "~" * 18 + "`\n"
        result = "**Акційні пропозиції**\n"
        result += separator
        result += f"\n{separator}\n".join(
                    disc.parse() for disc in self.discounts["existing"]
                )
        if result == "**Акційні пропозиції**\n" + separator:
            result += "На жаль на даний момент немає ніяких акцій."
        return result

class Discount:
    tz = datetime.timezone(datetime.timedelta(hours=2))
    def __init__(self):
        self.name = ""
        self.text = ""
        # Format: "%h%h:%m%m-%h%h:%m%m"
        self.hours = ""
        self._hours: Dict[Union[datetime.timedelta, datetime.datetime], ...] = {}
        self.everyday = True
        self.repetative = True

        self.finished_creation = False
        self._active = False
        self._to_remove = False

    def set_title(self, new_name):
        self.name = new_name

    def set_text(self, new_text:str):
        self.text = new_text

    def set_time(self, new_time:Union[str, datetime.datetime]):
        if self.everyday:
            self.hours = new_time

            _time_1, _time_2 = new_time.split("-")
            _hours_1, _mins_1 = _time_1.split(":")
            _hours_2, _mins_2 = _time_2.split(":")
            _hours_1, _mins_1 = int(_hours_1), int(_mins_1)
            _hours_2, _mins_2 = int(_hours_2), int(_mins_2)
            if _hours_1 >= 24:
                _hours_1 -= 24
            if _hours_2 >= 24:
                _hours_2 -= 24

            self._hours["start"] = datetime.timedelta(hours=_hours_1, minutes=_mins_1)
            self._hours["finish"] = datetime.timedelta(hours=_hours_2, minutes=_mins_2)

    def activate(self):
        if not self.repetative:
            self._to_remove = True

    def deactivate(self):
        self._to_remove = False
        if self.remove:
            del self

    @property
    def active(self):
        return self._active

    @property
    def remove(self):
        return self._to_remove

    @property
    def was_created(self):
        return self.finished_creation

    @property
    def is_time(self):
        if self.everyday:
            is_before = datetime.datetime.now(self.tz) >= self._hours["start"]
            is_after = datetime.datetime.now(self.tz) >= self._hours["finish"]
            time = is_before and not is_after
            return not self.active and time

    @property
    def time_passed(self):
        if self.everyday:
            is_before = datetime.datetime.now(self.tz) >= self._hours["start"]
            is_after = datetime.datetime.now(self.tz) >= self._hours["finish"]
            time = is_before and not is_after
            return self.active and not time

    def parse(self):
        return f"`акція:` **\"{self.name}\"**\n" \
               f"{self.text}\n" \
               f"`діє:` {'кожного дня' if self.everyday else ''} {self.hours}\n"
