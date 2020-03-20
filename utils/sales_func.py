import asyncio

async def discounts_job(client, sales_obj):
    while True:
        sales_obj.do_actions()
        await asyncio.sleep(60)