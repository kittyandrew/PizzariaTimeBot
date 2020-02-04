from utils.sales_func import discounts_job
from products.pizzas import pizzas_list
from products.drinks import drinks_list
from products.sauces import sauces_list
from my_types.sales import BotSales
from telethon import TelegramClient
import config as c
import modules
import logging
import asyncio

logger = logging.getLogger()
fh = logging.FileHandler('logging.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)
logger.setLevel(logging.ERROR)

class PizzaBot:

    def __init__(self, loop=None):
        self.loop = loop
        self.client = TelegramClient(session=f'pizza_bot', api_hash=c.API_HASH, api_id=c.API_ID, loop=self.loop)
        self.img_cache = {}
        self.global_bucket = {}
        self.sales_obj = BotSales()

        self.start()

    def start(self):

        ## register handlers
        modules.init(self.client, self.img_cache, self.global_bucket, self.sales_obj)

        ## register background events
        asyncio.ensure_future(discounts_job(self.client, self.sales_obj))

        # Start
        self.client.start(bot_token=c.TOKEN)

        asyncio.ensure_future(self.cache_imgs())

        self.client.run_until_disconnected()

    async def cache_imgs(self):
        print("Start caching imgs..")
        _list = [*pizzas_list, *drinks_list, *sauces_list]
        for each in _list:
            file = await self.client.upload_file(each().img)
            self.img_cache[each.__name__] = file
            print(f"Cached {each.__name__}")
        print("Imgs cached.")

if __name__ == "__main__":
    PizzaBot()
