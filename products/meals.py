from typing import Union
import os


class MealBase:
    name: str = ""
    price: str = None
    weight: str = None
    amount: str = None
    img_path: str = None
    img_id: str = None

    def __init__(self):
        self.img = self.get_pic()

    def get_pic(self):
        with open(self.img_path, "rb") as f:
            return f.read()

    @classmethod
    def parse(cls):
        return f"`назва:` **{cls.name}**\n" \
               f"`ціна:` {cls.price}\n" \
               f"`{'вага' if cls.weight else 'кількість'}:` **{cls.weight if cls.weight else cls.amount}**\n"


class FrenchFries(MealBase):
    name = "Картопля фрі"
    price = "38₴"
    weight = "150г"
    img_path = os.path.join("media", "meals", "french_fries.png")


class MeatStripes6(MealBase):
    name = "М'ясні стріпси (Середня порція)"
    price = "83₴"
    amount = "6 шт."
    img_path = os.path.join("media", "meals", "meat_stripes.png")


class MeatStripes9(MealBase):
    name = "М'ясні стріпси (Велика порція)"
    price = "118₴"
    amount = "9 шт."
    img_path = os.path.join("media", "meals", "meat_stripes.png")


class SpicyPotato(MealBase):
    name = "Картопля зі спеціями"
    price = "42₴"
    weight = "300г"
    img_path = os.path.join("media", "meals", "spicy_potatoes.png")


class MeatNuggets6(MealBase):
    name = "М'ясні нагетси (Середня порція)"
    price = "47₴"
    amount = "6 шт."
    img_path = os.path.join("media", "meals", "meat_nuggets.png")


class MeatNuggets9(MealBase):
    name = "М'ясні нагетси (Велика порція)"
    price = "72₴"
    amount = "9 шт."
    img_path = os.path.join("media", "meals", "meat_nuggets.png")


class PotatoDips(MealBase):
    name = "Картопляні діпи"
    price = "39₴"
    weight = "230г"
    img_path = os.path.join("media", "meals", "potato_dips.png")


class CheeseBalls(MealBase):
    name = "Сирні кульки"
    price = "95₴"
    amount = "10 шт."
    img_path = os.path.join("media", "meals", "cheese_balls.png")


class ChickenLeg2(MealBase):
    name = "Куряча ніжка (Середня порція)"
    price = "48₴"
    amount = "2 шт."
    img_path = os.path.join("media", "meals", "chicken_leg.png")


class ChickenLeg4(MealBase):
    name = "Куряча ніжка (Велика порція)"
    price = "88₴"
    amount = "4 шт."
    img_path = os.path.join("media", "meals", "chicken_leg.png")


class PotatoBalls(MealBase):
    name = "Картопляні кульки"
    price = "36₴"
    amount = "20 шт."
    img_path = os.path.join("media", "meals", "potato_balls.png")


class OnionRings(MealBase):
    name = "Цибулеві кільця"
    price = "42₴"
    amount = "10 шт."
    img_path = os.path.join("media", "meals", "onion_rings.png")


class CheeseSticks(MealBase):
    name = "Сирні палички"
    price = "75₴"
    amount = "5 шт."
    img_path = os.path.join("media", "meals", "cheese_sticks.png")


meals_list = [FrenchFries, MeatStripes6, MeatStripes9, MeatNuggets6, MeatNuggets9,
              ChickenLeg2, ChickenLeg4, CheeseBalls, CheeseSticks, PotatoDips,
              PotatoBalls, SpicyPotato, OnionRings]