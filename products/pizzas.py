from typing import Union
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

class NapoliPikantnaPizza(BasePizza):
    name = "піца \"Наполі\""
    ingredients = ["соус томатний", "сир моцарела", "ковбаса наполі пікантна", "перець болгарський жовтий", "оливки чорні"]
    price = "170₴"
    weight = "610г"
    img_path = os.path.join("media", "pizzas", "Napoli.png")

pizzas_list = [NizhnaPizza, SitnaPizza, FourMeatPizza, SokovitaPizza,
               FourCheesePizza, SalyamiPizza, ApetitnaPizza, PikantnaPizza, NapoliPikantnaPizza]

class FullHalfPizza:
    def __init__(self, obj1, obj2):
        self.name = f"піца {obj1.name}|{obj2.name}"
        self.price = str(int(obj1.price.strip("₴")) + int(obj2.price.strip("₴"))) + "₴"

class HalfPizza:
    name = None
    half = None
    price = None

    def __add__(self, other):
        return FullHalfPizza(self, other)

class HalfNizhna(HalfPizza):
    name = "0.5 \"Ніжна\""
    price = "87₴"

class HalfSitna(HalfPizza):
    name = "0.5 \"Ситна\""
    price = "92₴"

class HalfFourMeat(HalfPizza):
    name = "0.5 \"4 М'яса\""
    price = "102₴"

class HalfSokovita(HalfPizza):
    name = "0.5 \"Соковита\""
    price = "87₴"

class HalfPikantna(HalfPizza):
    name = "0.5 \"Пікантна\""
    price = "88₴"

class HalfApetitna(HalfPizza):
    name = "0.5 \"Апетитна\""
    price = "89₴"

class HalfSalyami(HalfPizza):
    name = "0.5 \"Салямі\""
    price = "91₴"

class HalfFourChese(HalfPizza):
    name = "0.5 \"4 Сири\""
    price = "95₴"

class HalfNapoliPikantna(HalfPizza):
    name = "0.5 \"Наполі\""
    price = "93₴"

class HalfPekelna(HalfPizza):
    name = "0.5 \"Пекельна\""
    price = "89₴"

halfs_pizzas = [HalfApetitna, HalfSalyami, HalfSitna, HalfSokovita,
         HalfFourChese, HalfFourMeat, HalfPikantna, HalfNizhna, HalfNapoliPikantna, HalfPekelna]

class Ingredient:
    _hryvnya = "₴"
    normal_grams = 50
    item1, grams1, cost1 = "Пармезан", 25, 0.65
    item2, cost2 = "Дорблю", 0.7
    item3, cost3 = "Оливки", 0.4
    item4, grams4, cost4 = "Кріп", 5, 0.5
    item5, cost5 = "Гриби", 0.18
    item6, cost6 = "Філе Куряче", 0.6
    item7, cost7 = "Ананаси", 0.26
    item8, cost8 = "Кукурудза", 0.16
    item9, cost9 = "Бекон", 0.45
    item10, cost10 = "Салямі", 0.65
    item11, cost11 = "Мисливські к.", 0.4
    item12, cost12 = "Помідори", 0.3
    item13, cost13 = "Чедер", 0.53
    item14, cost14 = "Балик", 0.5
    item15, cost15 = "Сир фета", 0.42
    item16, cost16 = "Перець болгарський", 0.3
    item17, cost17 = "Огірок кислий", 0.18
    item18, cost18 = "Цибуля синя", 0.12
    item19, cost19 = "Перець чилі", 0.34
    item20, cost20 = "Сулугуні", 0.5
    item21, cost21 = "Перець жовтий", 0.3
    item22, cost22 = "Наполі пікантна", 0.8
    products = [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11,
                item12, item13, item14, item15, item16, item17, item18, item19, item20, item21, item22]
    costs = [cost1, cost2, cost3, cost4, cost5, cost6, cost7, cost8, cost9, cost10, cost11,
             cost12, cost13, cost14, cost15, cost16, cost17, cost18, cost19, cost20, cost21, cost22]
    grams = [grams1] * 3 + [grams4] + [normal_grams] * 18

    def __init__(self, index):
        self.id = index
        self.product = self.products[index]
        self.gram = self.grams[index]
        self.cost = self.costs[index] * self.gram

    def __str__(self):
        return f"{self.product} {self.gram} г"

    def increase(self):
        self.gram += self.grams[self.id]
        self.cost += self.costs[self.id] * self.grams[self.id]

    def show(self):
        return str(self), str(self.cost) + self._hryvnya

class PizzaFromScratch:
    name = "Піца з інгредієнтів"
    _hryvnya = "₴"
    cost_tisto = 0.1 * 290
    cost_mozarela = 0.41 * 110
    mozarela_cheese = "Моцарела 110 г"
    cost_sylygyni = 0.5 * 110
    sylygyni_cheese = "Сулугуні 110 г"
    cost_tomato_sauce = 0.15 * 100
    tomato_sauce = "Томатний соус 100 г"
    cost_vershkovii_sauce = 0.15 * 80
    vershkovii_sauce = "Вершковий соус 80 г"
    null_text = "\n  `(Додайте інгредієнти..)`"

    def __init__(self):
        self.base_ingredients = ["Тісто 290 г", ]
        self.pizza_base = "`Ваша піца:`\n  " + "\n  ".join(self.base_ingredients)
        self.ingredients = list()
        self.price = self.cost_tisto

    def decide_sauce(self, sauce_type):
        if sauce_type == "tomato":
            self.base_ingredients.append(self.tomato_sauce)
            self.price += self.cost_tomato_sauce
        elif sauce_type == "vershkovii":
            self.base_ingredients.append(self.vershkovii_sauce)
            self.price += self.cost_vershkovii_sauce
        self.pizza_base = "`Ваша піца:`\n  " + "\n  ".join(self.base_ingredients)

    def decide_cheese(self, cheese_type):
        if cheese_type == "mozarella":
            self.base_ingredients.append(self.mozarela_cheese)
            self.price += self.cost_mozarela
        elif cheese_type == "sylygyni":
            self.base_ingredients.append(self.sylygyni_cheese)
            self.price += self.cost_sylygyni
        self.pizza_base = "`Ваша піца:`\n  " + "\n  ".join(self.base_ingredients)

    def add(self, index):
        new = True
        for item in self.ingredients:
            if index == item.id:
                new = False
                break
        if new:
            _new = Ingredient(index)
            self.ingredients.append(_new)
            self.price += _new.cost
        else:
            item.increase()
            self.price += Ingredient(index).cost

    def user_parse(self):
        result = self.pizza_base
        if not self.ingredients:
            result += self.null_text
        else:
            result += "\n"
            for each in self.ingredients:
                result += f"  {each}\n"
        result += "\n\n`Ціна:` " + str(self.price) + self._hryvnya
        return result

    def show_item(self, index):
        _item = Ingredient(index)
        return str(_item), str(_item.cost) + self._hryvnya

    def item_with_idencies(self, index) -> Union[int, str, int]:
        result = Ingredient(index)
        _smol = index - 1
        _big = index + 1
        if _smol < 0:
            _smol = len(self.ingredients) - 1
        if _big >= len(self.ingredients):
            _big = 0
        return _smol, result, _big

    def parse_ingredients(self):
        _list = self.base_ingredients + self.ingredients
        return "    " + "\n    ".join([str(i) for i in _list]) + "\n"