from datetime import datetime
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

COMPETENCIAS_DISPONIVEIS = [
    "Python",
    "SQL",
    "MongoDB",
    "HTML/CSS",
    "JavaScript",
    "Java",
    "C",
    "Git/GitHub"
]

GENEROS_VALIDOS = ["F", "M", "OUTRO", "PREFIRO NÃO INFORMAR"]


# --- Validações Gerais e Campos de Texto ---

def validar_nome(nome):
    return bool(nome and nome.strip())

def validar_rua(rua):
    return bool(rua and rua.strip())

def validar_numero(numero):
    return str(numero).isdigit()

def validar_cidade(cidade):
    return bool(cidade and cidade.strip())

def validar_email(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(padrao, email))


# --- Validações de Documentos e Contato ---

def validar_cp(cp):
    cp = cp.strip()
    if "-" not in cp:
        return False
    cp_limpo = cp.replace("-", "")
    return len(cp_limpo) == 7 and cp_limpo.isdigit()

def validar_nif(nif):
    nif = str(nif).strip()
    return len(nif) == 9 and nif.isdigit()

def validar_telefone(telefone):
    telefone_limpo = str(telefone).strip().replace(" ", "").replace("+", "")
    return telefone_limpo.isdigit() if telefone_limpo else True

def validar_data(data):
    if not data:
        return True  # Campo opcional
    try:
        datetime.strptime(data, "%Y-%m-%d")  # Formato padrão do <input type="date">
        return True
    except ValueError:
        try:
            datetime.strptime(data, "%d/%m/%Y")  # Formato DD/MM/AAAA
            return True
        except ValueError:
            return False

def validar_genero(genero):
    if not genero:
        return True
    return genero.upper() in GENEROS_VALIDOS


# --- Checagens de Duplicidade no MongoDB ---

def email_existe(email, colecao):
    return colecao.find_one({"email": email}) is not None

def nif_existe(nif, colecao_empresas):
    return colecao_empresas.find_one({"nif": nif}) is not None