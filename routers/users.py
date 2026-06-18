from fastapi import APIRouter, status, Depends, HTTPException
from schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt
from models import User
from sqlalchemy import select
from jwt_token import create_access_token

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass

@router.patch('/{user_id}')
async def update_user(user_id: int, user: UserUpdate):
    return user

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate,  db: AsyncSession = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    user = User(username=user.username, password=hashed_password, email=user.email)
    db.add(user)
    await db.commit()
    return UserResponse.model_validate(user)

@router.post('/login')
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = select(User).where(User.username == user.username)
    db_request = await db.execute(db_user)
    db_user = db_request.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    elif bcrypt.verify(user.password, db_user.password):
        return create_access_token({"sub": user.username})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный пароль')