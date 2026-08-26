from database.conexao import conectar_banco


def testar_conexao():
    banco = conectar_banco()
    print("Banco:", banco.name)