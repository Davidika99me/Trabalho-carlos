# models.py
from pydantic import BaseModel, Field
from typing import Optional

# Base para criar/ler
class UsuarioBase(BaseModel):
    username: str = Field(..., example="joao_silva")
    email: str = Field(..., example="joao@exemplo.com")
    
# Para criar um novo usuário (inclui o campo necessário para criação, ex: senha)
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., example="SenhaForte123")

# Para atualizar um usuário (todos os campos são opcionais)
class UsuarioUpdate(UsuarioBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UsuarioLogin(BaseModel):
    username: str = Field(..., example="joao_silva")
    password: str = Field(..., example="SenhaForte123")
    
# Para retornar um usuário (exclui campos sensíveis como a senha)
class UsuarioOut(UsuarioBase):
    # 'id' é o nome do campo no Pydantic
    # '_id' é o nome do campo no MongoDB (ObjectId)
    id: str = Field(..., alias="_id", example="66f3d0ecbecc8009a8322352")
    password: str = Field(..., example="SenhaForte123")
    
class Config:
        # Permite que o Pydantic use nomes de campo definidos por alias (como '_id')
        populate_by_name = True  
        # Permite a criação a partir de instâncias ou dicionários
        from_attributes = True