from database.conexao import conectar_banco
from datetime import datetime #importanto para validar data de nascimento
import re

competencias_disponiveis = [
    "Python",
    "SQL",
    "MongoDB",
    "HTML/CSS",
    "JavaScript",
    "Java",
    "C",
    "Git/GitHub"
]

def validar_nome(nome):
    if nome.strip() == "":
        return False
    return True

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_genero(genero):
    generos_validos = ["F", "M", "OUTRO", "PREFIRO NÃO INFORMAR"]
    if genero in generos_validos:
        return True
    return False

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if re.match(padrao, email):
        return True
    return False

def validar_telefone(telefone):
    if telefone.isdigit():
        return True
    return False

def validar_cidade(cidade):
    if len(cidade.strip()) != 0:
        return True
    return False

def menu_competencias():
    print("\n=== COMPETÊNCIAS === ")
    for n, c in enumerate(competencias_disponiveis, 1):
        print(f'{n} - {c}')

def email_existe(email, candidatos):
    resultado = candidatos.find_one({"email": email})

    if resultado:
        return True
    return False


def cadastrar_candidato():
    banco = conectar_banco()

    candidatos = banco["candidatos"] #seleciona a coleção: candidatos no banco
    candidato = {}

    nome = input("Digite o nome: ")

    while not validar_nome(nome):
        print("Nome inválido!")
        nome = input("Digite o nome: ")

    candidato["nome"] = nome

    data = input("Digite a data de nascimento (DD/MM/AAAA): ")

    while not validar_data(data):
        print("Data de nascimento inválida!")
        data = input("Digite a data de nascimento (DD/MM/AAAA): ")

    candidato["data_nascimento"] = data

    genero = input('Gênero [F/M/OUTRO/PREFIRO NÃO INFORMAR]: ').upper()

    while not validar_genero(genero):
        print("Gênero inválido!")
        genero = input("Gênero [F/M/OUTRO/PREFIRO NÃO INFORMAR]: ").upper()

    candidato["genero"] = genero

    email = input("Digite um email: ")

    while not validar_email(email) or email_existe(email, candidatos):
        print("Email inválido ou já cadastrado!")
        email = input("Digite um email: ")

    candidato["email"] = email

    telefone = input("Digite um telefone: ")

    while not validar_telefone(telefone):
        print('Telefone inválido!')
        telefone = input("Digite um telefone: ")

    candidato["telefone"] = telefone

    cidade = input("Digite uma cidade: ")

    while not validar_cidade(cidade):
        print('Cidade inválida!')
        cidade = input("Digite uma cidade: ")

    candidato["cidade"] = cidade

    print("")
    menu_competencias()
    competencias = input("Escolha as competências separadas por vírgula: ")

    resposta_competencias = competencias.split(",")
    candidato["competencias"] = []

    for c in resposta_competencias:
        indice = int(c) - 1
        candidato["competencias"].append(competencias_disponiveis[indice])

    preferencia_area = input("Área de preferência (opcional): ")

    candidato["preferencia_area"] = preferencia_area

    agora = datetime.now()

    candidato["data_criacao"] = agora
    candidato["data_atualizacao"] = agora

    candidatos.insert_one(candidato) #manda dicionário para o MongoDB.

    print("Candidato cadastrado com sucesso!")


def listar_candidatos():
    banco = conectar_banco()
    
    candidatos_coll = banco["candidatos"] #Faz a conexao com python

    candidatos = list(candidatos_coll.find())  # Busca todos os candidatos na coleção e converte para lista Python

    if not candidatos:
        print("\n Nenhum candidato encontrado no sistema.")

    print("\n==================== LISTA DE CANDIDATOS ====================")
    for c in candidatos:
        competencias_str = ", ".join(c.get("competencias", [])) # Junta a lista de competências em uma string separada por vírgula (usa lista vazia se o campo não existir)
        preferencia = c.get("preferencia_area", "Não informada")

        print(f"Nome:            {c.get('nome')}")
        print(f"E-mail:          {c.get('email')}")
        print(f"Telefone:        {c.get('telefone')}")
        print(f"Cidade:          {c.get('cidade')}")
        print(f"Gênero:          {c.get('genero')}")
        print(f"Competências:    {competencias_str}")
        print(f"Pref. Área:      {preferencia}")
        print("-" * 60)

def procurar_candidato():
    banco = conectar_banco()
    candidatos_coll = banco["candidatos"]
    print("\n=== BUSCAR UM CANDIATO? ===")
    print("\n1 - Buscar por Nome ")
    print("\n2 - Buscar por E-mail ")
    escolha = input("\nComo você deseja buscar esse candidato? [Digite 1 ou 2] ")
    if escolha not in ["1", "2"]:
        print("Digite uma opção válida.")
        return
    if escolha == "1":
        nome_busca = input("Digite o nome do candidato (ou parte dele): ").strip()
        resultados = list(candidatos_coll.find({"nome": {"$regex": nome_busca, "$options": "i"}}))
        if not resultados:
            print("Nenhum candidato encontrado com este nome.")
            return
        print("==== CANDIDATOS ENCONTRADOS ====")
        for i, b in enumerate(resultados,1):
            print(f'{i} - {b["nome"]}')

    elif escolha == "2":
        email_busca = input("Digite o email do candidato (ou parte dele): ").strip()
        resultados_email = list(candidatos_coll.find({"email": {"$regex": email_busca, "$options": "i"}}))
        if not resultados_email:
            print("Nenhum candidato encontrado com este email.")
            return
        print("==== CANDIDATOS ENCONTRADOS ====")
        for i, b in enumerate(resultados_email,1):
            print(f'{i} - {b["nome"]} ({b["email"]})')