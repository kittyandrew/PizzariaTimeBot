from typing import List
import datetime
import pickle
import os


class BotSales:
    PATH = "discounts.pickle"
    def __init__(self):
        self.load_instance()

    def load_instance(self):
        if os.path.exists(self.PATH):
            with open(self.PATH, "rb") as _file:
                self.discounts = pickle.load(_file)
        else:
            self.discounts = []
            self.save()

    def save(self):
        with open(self.PATH, "wb") as _file:
            pickle.dump(self.discounts, _file)


class Discount:
    def __init__(self):
        self.text = ""
        self.hours = ""
        self._hours:List[datetime.datetime] = None
        self.everyday = True
        self.repetative = True
