from fastapi import APIRouter, status, Depends
from schemas import UserCreate, UserUpdate, UserResponse
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt
from models import User

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

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate,  db: AsyncSession = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    user = User(username=user.username, password=hashed_password, email=user.email)
    db.add(user)
    await db.commit()
    return UserResponse.model_validate(user)