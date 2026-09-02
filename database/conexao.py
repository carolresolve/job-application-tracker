import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def conectar_banco():
    client = MongoClient(MONGO_URI)
    return client["job_tracker"]