from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str

    @classmethod
    @model_validator(mode='before')
    def check_it_benefits(cls, data: dict):
        if data['password'] != data['confirm_password']:
            raise ValueError('Поля регистрации заполнены неверно!')
        return data

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str