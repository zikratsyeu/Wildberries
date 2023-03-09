import asyncio
import re

import aiohttp
from pydantic import BaseModel


class ProductInfo(BaseModel):
    article: str
    brand: str
    title: str


async def fetch_product_info(article):
    url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            brand = re.search(r'"brand":\s*"([^"]+)"', text).group(1)
            title = re.search(r'"name":\s*"([^"]+)"', text).group(1)
            return ProductInfo(article=article, brand=brand, title=title)


def get_product_info(article):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_product_info(article))
    return result.dict()
