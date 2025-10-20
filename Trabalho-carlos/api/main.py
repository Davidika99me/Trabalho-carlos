# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importe o Middleware
from .routers import usuarios

# Inicializa o FastAPI
app = FastAPI(title="CRUD Básico FastAPI + MongoDB")

# Configurações de CORS para desenvolvimento
# (Permite qualquer origem, cabeçalho e método)
origins = [
    "*", # Permite todas as origens (use apenas para desenvolvimento!)
    # Se você quiser restringir, poderia ser: "http://localhost", "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# Inclui as rotas do seu CRUD
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {"message": "API de CRUD de Usuários Simples está rodando. Acesse /docs para a documentação."}