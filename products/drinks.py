import os

class BaseDrink:
    name:str = None
    price:str = None
    size:str = "33cм"
    img_path:str = None

    def __init__(self):
        self.img = self.get_pic()

    def get_pic(self):
        with open(self.img_path, "rb") as f:
            return f.read()

    @classmethod
    def parse(cls):
        return f"`назва:` **{cls.name}**\n" \
               f"`ціна:` **{cls.price}**\n" \
               f"`розмір:` **{cls.size}**"

class Cocacola(BaseDrink):
    name = "Coca cola"
    size = "1Л"
    price = "25₴"
    img_path = os.path.join("media", "drinks", "Cola.jpg")

class Pepsi(BaseDrink):
    name = "Pepsi"
    size = "1Л"
    price = "25₴"
    img_path = os.path.join("media", "drinks", "Pepsi.jpg")

class SadochokMultifrukt(BaseDrink):
    name = "Сік Садочок мультифрукт"
    size = "1Л"
    price = "28₴"
    img_path = os.path.join("media", "drinks", "SadochokMultifruit.jpg")

class SadochokMultivit(BaseDrink):
    name = "Сік Садочок мультивітамін"
    size = "1Л"
    price = "28₴"
    img_path = os.path.join("media", "drinks", "SadochokMultivitamin.jpg")

class SadochokAppleGrape(BaseDrink):
    name = "Сік Садочок яблучно-виноградний"
    size = "1Л"
    price = "28₴"
    img_path = os.path.join("media", "drinks", "SadochokAppleGrapes.jpg")

class SadochokGranatApple(BaseDrink):
    name = "Сік Садочок гранатово-яблучний"
    size = "1Л"
    price = "28₴"
    img_path = os.path.join("media", "drinks", "SadochokGranatApple.jpg")


drinks_list = [Cocacola, Pepsi, SadochokMultifrukt, SadochokMultivit, SadochokAppleGrape, SadochokGranatApple]