from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    products: Mapped[list['Product']] = relationship(secondary='user_products', back_populates='users')

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    article_number: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(300))
    current_price: Mapped[int] = mapped_column()
    users: Mapped[list['User']] = relationship(secondary='user_products', back_populates='products')

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    price: Mapped[int] = mapped_column()
    checked_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

class UserProduct(Base):
    __tablename__ = 'user_products'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)