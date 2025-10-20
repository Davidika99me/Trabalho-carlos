# routers/usuarios.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId # Não vamos mais precisar disso, mas mantive para referência

# Importa as ferramentas
from ..models import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioLogin
from ..database import usuarios_collection 

router = APIRouter(prefix="/usuarios", tags=["Usuários CRUD Básico"])

# Função auxiliar para converter ObjectId para str e garantir o modelo de saída
def serialize_usuario(usuario: dict) -> UsuarioOut:
    # **PASSO CRUCIAL:** Converte o ObjectId para string
    # Isso deve acontecer ANTES de validar com o Pydantic
    if '_id' in usuario:
         usuario['_id'] = str(usuario['_id'])
    
    try:
        # Usa model_validate() para criar o modelo a partir do dicionário
        # O Pydantic mapeará o '_id' (agora string) para o campo 'id' graças ao alias
        return UsuarioOut.model_validate(usuario) 
    except ValidationError as e:
        print("Erro de validação ao serializar usuário:", e)
        # Se falhar, pode retornar o dicionário cru (para fins de debug) ou levantar o erro.
        raise HTTPException(status_code=500, detail="Erro de serialização do servidor.")

# ----------------- CREATE (C) -----------------
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_user(usuario: UsuarioCreate):
    # Verifica se o username (que agora é o ID lógico) já existe
    if usuarios_collection.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")

    usuario_data = usuario.model_dump() 
    
    resultado = usuarios_collection.insert_one(usuario_data)
    
    novo_usuario = usuarios_collection.find_one({"_id": resultado.inserted_id})
    
    return serialize_usuario(novo_usuario)

# ----------------- READ (R) - Listar todos -----------------
@router.get("/", response_model=List[UsuarioOut])
def list_users():
    usuarios = usuarios_collection.find()
    return [serialize_usuario(doc) for doc in usuarios]

# ----------------- READ (R) - Buscar por USERNAME -----------------
# A rota agora usa o 'username' como o identificador na URL
@router.get("/{username}", response_model=UsuarioOut)
def get_user(username: str):
    
    # Busca o documento usando o campo 'username'
    usuario = usuarios_collection.find_one({"username": username})
    
    if usuario is None:
        # Se não encontrar, retorna 404
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
    
    return serialize_usuario(usuario)

# ----------------- UPDATE (U) -----------------
# A rota agora usa o 'username'
@router.put("/{username}", response_model=UsuarioOut)
def update_user(username: str, usuario_data: UsuarioUpdate):
    
    # Pega apenas os campos que foram preenchidos (diferente de None)
    dados_atualizados = usuario_data.model_dump(exclude_none=True)
    
    # Remove o username dos dados de atualização para evitar que ele seja alterado.
    # Se o objetivo fosse permitir a alteração do username, a lógica seria mais complexa.
    if "username" in dados_atualizados:
        del dados_atualizados["username"]
        
    if not dados_atualizados:
        raise HTTPException(status_code=400, detail="Nenhum campo fornecido para atualização.")
        
    # Atualiza o documento usando o campo 'username' para filtrar
    resultado = usuarios_collection.update_one(
        {"username": username},
        {"$set": dados_atualizados}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
    
    # Busca o documento atualizado para retornar
    usuario_atualizado = usuarios_collection.find_one({"username": username})
    
    return serialize_usuario(usuario_atualizado)

# ----------------- DELETE (D) -----------------
# A rota agora usa o 'username'
@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str):
    
    # Deleta o documento usando o campo 'username'
    resultado = usuarios_collection.delete_one({"username": username})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Usuário '{username}' não encontrado")
        
    return

@router.post("/login")
def login_user(usuario: UsuarioLogin):
    
    # 1. Busca o usuário no MongoDB pelo username
    usuario_db = usuarios_collection.find_one({"username": usuario.username})
    
    if not usuario_db:
        # Usuário não existe
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário ou Senha Inválidos"
        )

    # 2. Verifica se a senha fornecida é igual à senha armazenada
    # ATENÇÃO: Em produção, NUNCA armazene senhas em texto puro! 
    # Use sempre hash (bcrypt, Argon2, etc.).
    if usuario.password != usuario_db.get("password"):
        # Senha incorreta
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário ou Senha Inválidos"
        )
        
    # Se chegou aqui, o login foi bem-sucedido
    return {"message": "Login realizado com sucesso!", "username": usuario.username}