# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import usuarios

# Inicializa o FastAPI
app = FastAPI(title="CRUD Básico FastAPI + MongoDB")


origins = [
    "*", # Permite todas as origens (use apenas para desenvolvimento!)
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


# Inclui as rotas do seu CRUD
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {"message": "API de CRUD de Usuários Simples está rodando. Acesse /docs para a documentação."}