from sqlalchemy import select
from parser import ProductParser
import asyncio
from models import Product, PriceHistory
from celery import shared_task
from database import async_session_maker
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from decouple import config

email_sending_config = ConnectionConfig(
    MAIL_USERNAME="Price Tracker",
    MAIL_PASSWORD=config('MAIL_PASSWORD'),
    MAIL_FROM=config('MAIL_FROM'),
    MAIL_PORT=config('MAIL_PORT', cast=int),
    MAIL_SERVER=config('MAIL_SERVER'),
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

async def send_price_update_email(email, product_title, recent_price, current_price):
    message = MessageSchema(
        subject="Price update notification",
        recipients=[email],
        body="<h1>Hello from Price Tracker</h1>" \
        f"<p>Добрый день, цена на товар {product_title} изменилась с {recent_price} на {current_price}</p>",
        subtype=MessageType.html
    )
    await FastMail(email_sending_config).send_message(message)

@shared_task
def price_check():
    asyncio.run(_price_check_async())

async def _price_check_async():
    async with async_session_maker() as session:
        db_products = await session.execute(select(Product).options(selectinload(Product.users))) 
        rows = db_products.scalars().all()
        for product in rows:
            *_, price = await ProductParser(product.url)
            price_note = PriceHistory(product_id = product.id, price = price, checked_at = datetime.now(timezone.utc))
            session.add(price_note)
            if product.current_price != price:
                recent_price = product.current_price
                product.current_price = price
                for user in product.users:
                    await send_price_update_email(user.email, product.title, recent_price, price)
            await session.commit()