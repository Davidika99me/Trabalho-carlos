# routers/usuarios.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioLogin
from ..database import usuarios_collection 
from pydantic import ValidationError
from ..security import hash_password, verify_password

router = APIRouter(prefix="/usuarios", tags=["Usuários CRUD Básico"])


def serialize_usuario(usuario: dict) -> UsuarioOut:

    if '_id' in usuario:
         usuario['_id'] = str(usuario['_id'])
    
    try:

        return UsuarioOut.model_validate(usuario) 
    except ValidationError as e:
        print("Erro de validação ao serializar usuário:", e)

        raise HTTPException(status_code=500, detail="Erro de serialização do servidor.")


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_user(usuario: UsuarioCreate):

    if usuarios_collection.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")

    usuario_data = usuario.model_dump()
    
    usuario_data["password"] = hash_password(usuario_data["password"]) 
    
    resultado = usuarios_collection.insert_one(usuario_data)
    
    novo_usuario = usuarios_collection.find_one({"_id": resultado.inserted_id})
    
    return serialize_usuario(novo_usuario)

@router.get("/", response_model=List[UsuarioOut])
def list_users():
    usuarios = usuarios_collection.find()
    return [serialize_usuario(doc) for doc in usuarios]

@router.get("/{username}", response_model=UsuarioOut)
def get_user(username: str):
    

    usuario = usuarios_collection.find_one({"username": username})
    
    if usuario is None:
   
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
    
    return serialize_usuario(usuario)


@router.put("/{username}", response_model=UsuarioOut)
def update_user(username: str, usuario_data: UsuarioUpdate):
    
    dados_atualizados = usuario_data.model_dump(exclude_none=True)

    if "username" in dados_atualizados:
        del dados_atualizados["username"]
        
    if not dados_atualizados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização.")
        
    resultado = usuarios_collection.update_one(
        {"username": username},
        {"$set": dados_atualizados}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
    
    usuario_atualizado = usuarios_collection.find_one({"username": username})
    
    return serialize_usuario(usuario_atualizado)


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str):
    

    resultado = usuarios_collection.delete_one({"username": username})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
        
    return

@router.post("/login")
def login_user(usuario: UsuarioLogin):
    
    usuario_db = usuarios_collection.find_one({"username": usuario.username})
    
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário ou Senha Inválidos"
        )

    if not verify_password(usuario.password, usuario_db.get("password")): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário ou Senha Inválidos"
        )
        
    return {"message": "Login realizado com sucesso!", "username": usuario.username}