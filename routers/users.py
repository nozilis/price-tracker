from fastapi import APIRouter, status
from schemas import UserCreate, UserUpdate

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass

@router.patch('/{user_id}')
async def update_user(user_id: int, user: UserUpdate):
    return user