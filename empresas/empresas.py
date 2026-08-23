from database.conexao import conectar_banco
import re

setores = [
    "Tecnologia",
    "Saúde",
    "Educação",
    "Comércio",
    "Indústria",
    "Construção",
    "Finanças",
    "Turismo",
    "Transportes",
    "Outro"
]

def validar_nome(nome):
    if nome.strip() == "":
        return False
    return True

def validar_rua(rua):
    if rua.strip() == "":
        return False
    return True

def validar_numero(numero):
    if numero.isdigit():
        return True
    return False

def validar_cidade(cidade):
    if cidade.strip() == "":
        return False
    return True


def validar_cp(cp):

    cp = cp.strip()

    if "-" not in cp:
        return False
    cp = cp.replace("-", "")
    if len(cp) == 7 and cp.isdigit():
        return True
    return False

def validar_nif(nif):
    nif = nif.strip()
    if len(nif) == 9 and nif.isdigit():
        return True
    return False

def menu_setores():
    print("\nEscolha o setor da empresa: ")
    for n,s in enumerate(setores,1):
        print(f'{n} - {s}')

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if re.match(padrao, email):
        return True
    return False

def email_existe(email, empresas):
    resultado = empresas.find_one({"email": email})

    if resultado:
        return True
    return False

def nif_existe(nif, empresas):
    resultado = empresas.find_one({"nif": nif})
    if resultado:
        return True
    return False

def cadastrar_empresa():
    banco = conectar_banco()
    empresas = banco["empresas"]

    empresa = {}

    #cadastrando o nome da empresa
    nome = input('Digite o nome da empresa: ')
    while not validar_nome(nome):
        print("Nome inválido!")
        nome = input('Digite o nome da empresa: ')

    empresa["nome"] = nome

    #cadastrando morada da empresa
    #localidade vai ser um dic, dentro do dic empresa
    localidade = {}
    empresa["localidade"] = localidade

    rua = input('Digite o nome da rua: ')
    while not validar_rua(rua):
        print('Nome de rua Inválido!')
        rua = input('Digite o nome da rua: ')

    localidade["rua"] = rua


    numero = input('Digite o número: ')
    while not validar_numero(numero):
        print('Número Inválido!')
        numero = input('Digite o número: ')

    localidade["numero"] = numero

    cidade = input('Digite o nome da cidade: ')
    while not validar_cidade(cidade):
        print('Cidade Inválida!')
        cidade = input('Digite o nome da cidade: ')

    localidade["cidade"] = cidade

    cp=input('Digite o código postal: [XXXX-YYY]: ')
    while not validar_cp(cp):
        print('Código postal Inválido!')
        cp=input('Digite o código postal:  [XXXX-YYY]: ')

    localidade["cp"] = cp

    nif = input('Digite seu NIF: ')
    while not validar_nif(nif) or nif_existe(nif,empresas):
        print('NIF inválido ou NIF já cadastrado ')
        nif = input('Digite seu NIF: ')

    empresa['nif'] = nif

    menu_setores()
    num_setores = int(input("Escolha um setor da empresa")) 
    empresa['setor'] = setores[num_setores-1]

    email = input("Digite um email: ")
    
    while not validar_email(email) or email_existe(email, empresas):
            print("Email inválido ou já cadastrado!")
            email = input("Digite um email: ")
    
    empresa["email"] = email

    empresas.insert_one(empresa)
    print("Empresa cadastrada com sucesso!")