from pymongo import MongoClient


def conectar_banco():
    cliente = MongoClient("mongodb://localhost:27017/")
    banco = cliente["job_tracker"]

    return banco