from database.conexao import conectar_banco


banco = conectar_banco()

print("Conexão com MongoDB realizada!")
print("Banco:", banco.name)