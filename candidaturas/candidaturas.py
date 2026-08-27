from database.conexao import conectar_banco


def testar_conexao():
    banco = conectar_banco()
    print("Banco:", banco.name)

def cadastrar_candidatura():
    banco = conectar_banco()
    candidatos_coll = banco["candidatos"]
    nome_busca = input("Digite o nome do candidato (ou parte dele): ").strip()
    resultados = list(candidatos_coll.find({"nome": {"$regex": nome_busca, "$options": "i"}}))
    print("==== CANDIDATOS ENCONTRADOS ====")
    for i, b in enumerate(resultados,1):
     print(f'{i} - {b["nome"]}')
    if not resultados:
       print("Nenhum candidato encontrado com este nome.")
       return
    opcao = int(input("Escolha o candidato pelo número: "))
    candidato_escolhido = resultados[opcao -1]
    candidato_id = candidato_escolhido["_id"]
    nome_candidato = candidato_escolhido["nome"]
    print(f'candidato escolhido: {nome_candidato}')
    empresa_coll = banco["empresas"]
    busca_empresa = input("Digite o nome da empresa (ou parte dela): ").strip()
    resultados_empresa = list(empresa_coll.find({"nome": {"$regex": busca_empresa, "$options": "i"}}))
    print("==== EMPRESAS ENCONTRADAS ====")
    for i, b in enumerate(resultados_empresa,1):
         print(f'{i} - {b["nome"]}')
    if not resultados_empresa:
           print("Nenhuma empresa encontrada com este nome.")
           return
    opcao_empresa = int(input("Escolha a empresa pelo número: "))
    empresa_escolhida = resultados_empresa[opcao_empresa -1]
    empresa_id = empresa_escolhida["_id"]
    nome_empresa = empresa_escolhida["nome"]
    print(f'empresa escolhida: {nome_empresa}')
    
