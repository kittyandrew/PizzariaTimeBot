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

class SandoraOrange(BaseDrink):
    name = "Сік апельсиновий SANDORA"
    size = "1Л"
    price = "35₴"
    img_path = os.path.join("media", "drinks", "SandoraOrange.jpg")

class SandoraMultivit(BaseDrink):
    name = "Сік мультивітамін SANDORA"
    size = "1Л"
    price = "35₴"
    img_path = os.path.join("media", "drinks", "SandoraMultivit.jpg")

class SandoraCherry(BaseDrink):
    name = "Сік вишневий SANDORA"
    size = "1Л"
    price = "35₴"
    img_path = os.path.join("media", "drinks", "SandoraCherry.jpg")

drinks_list = [Cocacola, Pepsi, SandoraOrange, SandoraMultivit, SandoraCherry]