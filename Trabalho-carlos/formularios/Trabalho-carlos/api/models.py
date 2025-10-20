# models.py
from pydantic import BaseModel, Field
from typing import Optional


class UsuarioBase(BaseModel):
    username: str = Field(..., example="joao_silva")
    email: str = Field(..., example="joao@exemplo.com")
    

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., example="SenhaForte123")


class UsuarioUpdate(UsuarioBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UsuarioLogin(BaseModel):
    username: str = Field(..., example="joao_silva")
    password: str = Field(..., example="SenhaForte123")
    

class UsuarioOut(UsuarioBase):

    id: str = Field(..., alias="_id", example="66f3d0ecbecc8009a8322352")
    password: str = Field(..., example="SenhaForte123")
    

    class Config:
        populate_by_name = True 
        from_attributes = True