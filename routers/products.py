from fastapi import APIRouter, status, Depends, HTTPException
from parser import ProductParser
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product, UserProduct
from schemas import ProductCreate, ProductResponse
from sqlalchemy import select

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/')
async def get_all_products(db: AsyncSession = Depends(get_db), user: AsyncSession = Depends(get_current_user)):
    result = await db.execute(select(Product).join(UserProduct, UserProduct.product_id == Product.id).where(UserProduct.user_id == user.id))
    db_products = result.scalars().all()
    if not db_products:
        raise HTTPException(status_code=404, detail="Нет отслеживаемых товаров")
    return [ProductResponse.model_validate(p) for p in db_products]

@router.post('/')
async def add_product(product: ProductCreate, db: AsyncSession = Depends(get_db), user: AsyncSession = Depends(get_current_user)):
    article_id, title, url, price = await ProductParser(product.url)
    existing_product = await db.execute(select(Product).where(Product.article_number == article_id))
    db_product = existing_product.scalar_one_or_none()
    if not db_product:
        db_product = Product(article_number=article_id, title=title, url=url, current_price=price)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
    existing_link = await db.execute(select(UserProduct).where(UserProduct.user_id == user.id, UserProduct.product_id == db_product.id))
    if existing_link.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Товар уже отслеживается")
    user_to_product = UserProduct(user_id=user.id, product_id=db_product.id)
    db.add(user_to_product)
    await db.commit()
    return {'message': 'Товар успешно добавлен'}

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db), user: AsyncSession = Depends(get_current_user)):
    result = await db.execute(select(UserProduct).where(UserProduct.user_id == user.id, UserProduct.product_id == product_id))
    user_product = result.scalar_one_or_none()
    if not user_product:
        raise HTTPException(status_code=404, detail="Запрошенный товар отсутствует")
    else:
        await db.delete(user_product)
        await db.commit()
        remaining = await db.execute(select(UserProduct).where(UserProduct.product_id == product_id))
        if not remaining.scalars().all():
            product = await db.execute(select(Product).where(Product.id == product_id))
            db_product = product.scalar_one_or_none()
            await db.delete(db_product)
            await db.commit()