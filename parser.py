from urllib.parse import urlparse  
from schemas import ProductCreate
from curl_cffi.requests import AsyncSession    
from fastapi import HTTPException

def get_basket_host(vol: int) -> int:
    ranges = [
        (143, 1),
        (287, 2),
        (431, 3),
        (719, 4),
        (1007, 5),
        (1061, 6),
        (1115, 7),
        (1169, 8),
        (1313, 9),
        (1601, 10),
        (1655, 11),
        (1919, 12),
        (2045, 13),
        (2189, 14),
        (2405, 15),
        (2621, 16),
        (2837, 17),
        (3053, 18),
        (3269, 19),
        (3485, 20),
        (3701, 21),
        (3917, 22),
        (4133, 23),
        (4349, 24),
    ]
    for limit, host in ranges:
        if vol <= limit:
            return host
    return 25

CARD_ENDPOINTS = [
    "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={}",
    "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1&spp=30&nm={}",
]

async def ProductParser(product: ProductCreate):
    product_url = product.url
    parsed_url = urlparse(product_url)
    article_id = int(parsed_url.path.split("/")[2])
    vol = article_id // 100000
    host = get_basket_host(vol)
    part = article_id // 1000
    url = f"https://basket-{host:02d}.wbbasket.ru/vol{vol}/part{part}/{article_id}/info/ru/card.json"   
    async with AsyncSession() as session:
        await session.get("https://www.wildberries.ru", impersonate="chrome120")
        card_data = None
        for endpoint in CARD_ENDPOINTS:
            card_response = await session.get(endpoint.format(article_id), impersonate="chrome120")
            if card_response.status_code == 200:
                data = card_response.json()
                products = data.get("data", {}).get("products", [])
                if products:
                    card_data = products[0]
                    break
        if card_data:
            title = card_data["name"]
            price = card_data["sizes"][0]["price"]["product"] 
        else:
            truth_host = None
            for candidate in range(1, 26):
                url = f"https://basket-{candidate:02d}.wbbasket.ru/vol{vol}/part{part}/{article_id}/info/ru/card.json"
                response = await session.get(url, impersonate="chrome120")
                if response.status_code == 200:
                    truth_host = candidate
                    break
            if truth_host is None:
                raise HTTPException(status_code=404, detail="Товар не найден на Wildberries")
            price_response = await session.get(f"https://basket-{truth_host:02d}.wbbasket.ru/vol{vol}/part{part}/{article_id}/info/price-history.json", impersonate="chrome120")
            data = response.json()
            title = data["imt_name"]
            price_data = price_response.json()
            price = price_data[-1]["price"]["RUB"]
    return article_id, title, product_url, price