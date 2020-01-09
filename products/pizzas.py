import os

class BasePizza:
    name:str = ""
    ingredients:list = None
    price:str = None
    weight:str = None
    size:str = "33cм"
    img_path:str = None
    img_id:str = None

    def __init__(self):
        self.img = self.get_pic()

    def get_pic(self):
        with open(self.img_path, "rb") as f:
            return f.read()

    @classmethod
    def parse(cls):
        parsed_ingredients = ', '.join(cls.ingredients)
        return f"`назва:` **{cls.name}**\n" \
               f"`склад:` **{parsed_ingredients}**\n" \
               f"`ціна:` {cls.price}\n" \
               f"`вага:` **{cls.weight}**\n" \
               f"`розмір:` **{cls.size}**"

class NizhnaPizza(BasePizza):
    name = "піца \"Ніжна\""
    ingredients = ["соус вершковий", "сир моцарела", "куряче філе", "гриби", "ананас", "кукурудза"]
    price = "158₴"
    weight = "720г"
    img_path = os.path.join("media", "pizzas", "Nizhna.png")

class SitnaPizza(BasePizza):
    name = "піца \"Ситна\""
    ingredients = ["соус томатний", "сир моцарела", "сир чеддер", "балик", "бекон", "гриби"]
    price = "168₴"
    weight = "710г"
    img_path = os.path.join("media", "pizzas", "Sitna.png")

class FourMeatPizza(BasePizza):
    name = "піца \"4 М'яса\""
    ingredients = ["соус томатний", "сир моцарела", "куряче філе", "бекон", "салямі", "мисливські ковбаски", "помідор"]
    price = "188₴"
    weight = "730г"
    img_path = os.path.join("media", "pizzas", "FourMeat.png")

class SokovitaPizza(BasePizza):
    name = "піца \"Соковита\""
    ingredients = ["соус томатний", "сир моцарела", "балик", "бекон", "гриби", "помідор", "сир фета"]
    price = "157₴"
    weight = "720г"
    img_path = os.path.join("media", "pizzas", "Sokovita.png")

class FourCheesePizza(BasePizza):
    name = "піца \"4 Сири\""
    ingredients = ["соус вершковий", "сир моцарела", "сир чеддер", "сир дроблю", "сир пармезан"]
    price = "175₴"
    weight = "585г"
    img_path = os.path.join("media", "pizzas", "FourCheese.png")

class SalyamiPizza(BasePizza):
    name = "піца \"Салямі\""
    ingredients = ["соус томатний", "сир моцарела", "салямі", "помідор"]
    price = "165₴"
    weight = "630г"
    img_path = os.path.join("media", "pizzas", "Salyami.png")

class ApetitnaPizza(BasePizza):
    name = "піца \"Апетитна\""
    ingredients = ["соус томатний", "сир моцарела", "мисливські ковбаски", "перець болгарський", "гриби", "огірок"]
    price = "162₴"
    weight = "700г"
    img_path = os.path.join("media", "pizzas", "Apetitna.png")

class PikantnaPizza(BasePizza):
    name = "піца \"Пікантна\""
    ingredients = ["соус вершковий", "сир моцарела", "бекон", "гриби", "цибуля синя (солодка)"]
    price = "160₴"
    weight = "660г"
    img_path = os.path.join("media", "pizzas", "Pikantna.png")

pizzas_list = [NizhnaPizza, SitnaPizza, FourMeatPizza, SokovitaPizza,
               FourCheesePizza, SalyamiPizza, ApetitnaPizza, PikantnaPizza]