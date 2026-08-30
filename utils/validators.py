import re

SETORES = [
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
    return bool(nome and nome.strip())

def validar_rua(rua):
    return bool(rua and rua.strip())

def validar_numero(numero):
    return str(numero).isdigit()

def validar_cidade(cidade):
    return bool(cidade and cidade.strip())

def validar_cp(cp):
    cp = cp.strip()
    if "-" not in cp:
        return False
    cp_limpo = cp.replace("-", "")
    return len(cp_limpo) == 7 and cp_limpo.isdigit()

def validar_nif(nif):
    nif = str(nif).strip()
    return len(nif) == 9 and nif.isdigit()

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(padrao, email))

def email_existe(email, colecao_empresas):
    return colecao_empresas.find_one({"email": email}) is not None

def nif_existe(nif, colecao_empresas):
    return colecao_empresas.find_one({"nif": nif}) is not None