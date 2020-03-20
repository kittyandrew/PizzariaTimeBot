import os

class BaseSauce:
    name:str = None
    price:str = "10₴"
    img_path:str = None

    def __init__(self):
        self.img = self.get_pic()

    def get_pic(self):
        with open(self.img_path, "rb") as f:
            return f.read()

    @classmethod
    def parse(cls):
        return f"`назва:` **{cls.name}**\n" \
               f"`ціна:` **{cls.price}**"

class BBQSauce(BaseSauce):
    name = "соус \"Барбекю\""
    img_path = os.path.join("media", "sauces", "bbq.png")

class Bittersweet(BaseSauce):
    name = "соус \"Кисло-солодкий\""
    img_path = os.path.join("media", "sauces", "bittersweet.png")

class Paprica(BaseSauce):
    name = "соус \"Паприка\""
    img_path = os.path.join("media", "sauces", "papric.png")

class Cheese(BaseSauce):
    name = "соус \"Сирний\""
    img_path = os.path.join("media", "sauces", "cheese.png")

class Tartar(BaseSauce):
    name = "соус \"Тартар\""
    img_path = os.path.join("media", "sauces", "tartar.png")

class Garlic(BaseSauce):
    name = "соус \"Часниковий\""
    img_path = os.path.join("media", "sauces", "garlic.png")

class HotChilly(BaseSauce):
    name = "соус \"Чилі гострий\""
    img_path = os.path.join("media", "sauces", "hotchilly.png")

class French(BaseSauce):
    name = "соус \"Французький\""
    img_path = os.path.join("media", "sauces", "french.png")

sauces_list = [BBQSauce, Bittersweet, Paprica, Cheese, Tartar, Garlic, HotChilly, French]