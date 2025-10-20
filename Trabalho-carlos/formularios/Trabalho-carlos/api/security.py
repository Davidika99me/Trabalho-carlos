# security.py
from passlib.context import CryptContext

# Define o contexto de hash, usando bcrypt como algoritmo padrão
# bcrypt é um algoritmo lento e seguro, ideal para hash de senhas.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera o hash da senha."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

# Exemplo de uso:
# hash = hash_password("minhasenha123")
# print(verify_password("minhasenha123", hash)) # Deve retornar True