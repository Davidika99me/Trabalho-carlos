# database.py
from pymongo import MongoClient


MONGO_URI = "mongodb+srv://Empreendedorismo_DB:rpv12345@cluster0.gkjvrbx.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "trabalho_carlos_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


usuarios_collection = db["usuarios"]
