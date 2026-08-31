from flask import Flask, render_template, request, redirect, url_for
from database.conexao import conectar_banco
from bson.objectid import ObjectId
from utils.validators import *

app = Flask(__name__)

@app.route("/")
def home():
    banco = conectar_banco()
    
    # Contagem de registros em cada coleção
    total_cand = banco["candidatos"].count_documents({})
    total_emp = banco["empresas"].count_documents({})
    total_cand_vagas = banco["candidaturas"].count_documents({})
    
    return render_template(
        "index.html", 
        total_candidatos=total_cand,
        total_empresas=total_emp,
        total_candidaturas=total_cand_vagas
    )

@app.route("/candidaturas")
def listar_candidaturas():
    banco = conectar_banco()
    candidaturas = list(banco["candidaturas"].find())
    return render_template("candidaturas.html", candidaturas=candidaturas)

@app.route("/candidaturas/nova", methods=["GET", "POST"])
def cadastrar_candidatura():
    banco = conectar_banco()
    candidatos_coll = banco["candidatos"]
    empresas_coll = banco["empresas"]
    candidaturas_coll = banco["candidaturas"]

    erro = None
    candidatos = list(candidatos_coll.find())
    empresas = list(empresas_coll.find())

    if request.method == "POST":
        candidato_id = request.form.get("candidato_id")
        empresa_id = request.form.get("empresa_id")
        vaga = request.form.get("vaga", "").strip()
        status = request.form.get("status", "Em Análise").strip()

        if not candidato_id or not empresa_id or not vaga:
            erro = "Por favor, preencha todos os campos obrigatórios."
        else:
            cand = candidatos_coll.find_one({"_id": ObjectId(candidato_id)})
            emp = empresas_coll.find_one({"_id": ObjectId(empresa_id)})

            if not cand or not emp:
                erro = "Candidato ou empresa selecionada não foram encontrados."
            else:
                from datetime import datetime

                candidaturas_coll.insert_one({
                    "candidato_id": ObjectId(candidato_id),
                    "candidato_nome": cand.get("nome", "Sem Nome"),
                    "empresa_id": ObjectId(empresa_id),
                    "empresa_nome": emp.get("nome", "Sem Nome"),
                    "vaga": vaga,
                    "status": status,
                    "data": datetime.now().strftime("%d/%m/%Y")
                })
                return redirect(url_for("listar_candidaturas"))

    return render_template("nova_candidatura.html", candidatos=candidatos, empresas=empresas, erro=erro)

@app.route("/empresas")
def listar_empresas():
    banco = conectar_banco()
    empresas = list(banco["empresas"].find())
    return render_template("empresas.html", empresas=empresas)

@app.route("/empresas/nova", methods=["GET", "POST"])
def cadastrar_empresa():
    banco = conectar_banco()
    empresas_coll = banco["empresas"]
    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        rua = request.form.get("rua", "").strip()
        numero = request.form.get("numero", "").strip()
        cidade = request.form.get("cidade", "").strip()
        cp = request.form.get("cp", "").strip()
        nif = request.form.get("nif", "").strip()
        setor = request.form.get("setor", "").strip()
        email = request.form.get("email", "").strip()

        # Validações de NIF, Email e Morada
        if not validar_nif(nif):
            erro = "NIF inválido. Certifique-se de que possui exatamente 9 dígitos."
        elif nif_existe(nif, empresas_coll):
            erro = "Este NIF já está cadastrado no sistema."
        elif not validar_email(email):
            erro = "Endereço de e-mail inválido."
        elif email_existe(email, empresas_coll):
            erro = "Este e-mail já está cadastrado no sistema."
        elif not validar_cp(cp):
            erro = "Código Postal inválido. Use o formato XXXX-YYY."

        if erro:
            return render_template("nova_empresa.html", setores=SETORES, erro=erro)

        empresa = {
            "nome": nome,
            "localidade": {
                "rua": rua,
                "numero": numero,
                "cidade": cidade,
                "cp": cp
            },
            "nif": nif,
            "setor": setor,
            "email": email
        }

        empresas_coll.insert_one(empresa)
        return redirect(url_for("listar_empresas"))

    return render_template("nova_empresa.html", setores=SETORES)

@app.route("/candidatos")
def listar_candidatos():
    banco = conectar_banco()
    candidatos = list(banco["candidatos"].find())
    return render_template("candidatos.html", candidatos=candidatos)

@app.route("/candidatos/novo", methods=["GET", "POST"])
def cadastrar_candidato():
    banco = conectar_banco()
    candidatos_coll = banco["candidatos"]
    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        cidade = request.form.get("cidade", "").strip()
        area = request.form.get("area", "").strip()
        competencias = request.form.getlist("competencias")  # Pega todas as opções marcadas

        if not validar_nome(nome):
            erro = "O nome é obrigatório."
        elif not validar_email(email):
            erro = "E-mail inválido."
        elif email_existe(email, candidatos_coll):
            erro = "Este e-mail já está cadastrado para outro candidato."
        elif telefone and not validar_telefone(telefone):
            erro = "Telefone inválido."

        if erro:
            return render_template("novo_candidato.html", competencias=COMPETENCIAS_DISPONIVEIS, erro=erro)

        candidatos_coll.insert_one({
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cidade": cidade,
            "area": area,
            "competencias": competencias
        })
        return redirect(url_for("listar_candidatos"))

    return render_template("novo_candidato.html", competencias=COMPETENCIAS_DISPONIVEIS)

@app.route("/empresas/excluir/<id>", methods=["POST"])
def excluir_empresa(id):
    banco = conectar_banco()
    banco["empresas"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("listar_empresas"))


@app.route("/empresas/editar/<id>", methods=["GET", "POST"])
def editar_empresa(id):
    banco = conectar_banco()
    empresas_coll = banco["empresas"]
    
    # Busca a empresa atual pelo ID
    empresa = empresas_coll.find_one({"_id": ObjectId(id)})
    if not empresa:
        return redirect(url_for("listar_empresas"))

    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        rua = request.form.get("rua", "").strip()
        numero = request.form.get("numero", "").strip()
        cidade = request.form.get("cidade", "").strip()
        cp = request.form.get("cp", "").strip()
        nif = request.form.get("nif", "").strip()
        setor = request.form.get("setor", "").strip()
        email = request.form.get("email", "").strip()

        # Validações básicas
        if not validar_nif(nif):
            erro = "NIF inválido. Certifique-se de que possui exatamente 9 dígitos."
        # Checa duplicidade Apenas se NIF/Email mudaram em relação ao valor atual
        elif nif != empresa.get("nif") and nif_existe(nif, empresas_coll):
            erro = "Este NIF já está cadastrado para outra empresa."
        elif not validar_email(email):
            erro = "Endereço de e-mail inválido."
        elif email != empresa.get("email") and email_existe(email, empresas_coll):
            erro = "Este e-mail já está cadastrado para outra empresa."
        elif not validar_cp(cp):
            erro = "Código Postal inválido. Use o formato XXXX-YYY."

        if erro:
            return render_template("editar_empresa.html", empresa=empresa, setores=SETORES, erro=erro)

        # Atualiza no MongoDB
        empresas_coll.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nome": nome,
                "localidade": {
                    "rua": rua,
                    "numero": numero,
                    "cidade": cidade,
                    "cp": cp
                },
                "nif": nif,
                "setor": setor,
                "email": email
            }}
        )
        return redirect(url_for("listar_empresas"))

    return render_template("editar_empresa.html", empresa=empresa, setores=SETORES)

@app.route("/candidatos/excluir/<id>", methods=["POST"])
def excluir_candidato(id):
    banco = conectar_banco()
    banco["candidatos"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("listar_candidatos"))

@app.route("/candidatos/editar/<id>", methods=["GET", "POST"])
def editar_candidato(id):
    banco = conectar_banco()
    candidatos_coll = banco["candidatos"]
    
    candidato = candidatos_coll.find_one({"_id": ObjectId(id)})
    if not candidato:
        return redirect(url_for("listar_candidatos"))

    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        cidade = request.form.get("cidade", "").strip()
        area = request.form.get("area", "").strip()
        competencias = request.form.getlist("competencias")

        if not validar_nome(nome):
            erro = "O nome é obrigatório."
        elif not validar_email(email):
            erro = "E-mail inválido."
        # Checa duplicidade Apenas se o email mudou
        elif email != candidato.get("email") and email_existe(email, candidatos_coll):
            erro = "Este e-mail já está cadastrado para outro candidato."
        elif telefone and not validar_telefone(telefone):
            erro = "Telefone inválido."

        if erro:
            return render_template("editar_candidato.html", candidato=candidato, competencias=COMPETENCIAS_DISPONIVEIS, erro=erro)

        candidatos_coll.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cidade": cidade,
                "area": area,
                "competencias": competencias
            }}
        )
        return redirect(url_for("listar_candidatos"))

    return render_template("editar_candidato.html", candidato=candidato, competencias=COMPETENCIAS_DISPONIVEIS)

@app.route("/candidaturas/excluir/<id>", methods=["POST"])
def excluir_candidatura(id):
    banco = conectar_banco()
    banco["candidaturas"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("listar_candidaturas"))

@app.route("/candidaturas/editar/<id>", methods=["GET", "POST"])
def editar_candidatura(id):
    banco = conectar_banco()
    candidaturas_coll = banco["candidaturas"]
    candidatos_coll = banco["candidatos"]
    empresas_coll = banco["empresas"]

    candidatura = candidaturas_coll.find_one({"_id": ObjectId(id)})
    if not candidatura:
        return redirect(url_for("listar_candidaturas"))

    erro = None
    candidatos = list(candidatos_coll.find())
    empresas = list(empresas_coll.find())
    
    # Lista de status possíveis para a vaga
    status_opcoes = ["Em Análise", "Entrevista Agendada", "Em Teste Técnico", "Aprovado", "Rejeitado"]

    if request.method == "POST":
        candidato_id = request.form.get("candidato_id")
        empresa_id = request.form.get("empresa_id")
        vaga = request.form.get("vaga", "").strip()
        status = request.form.get("status", "").strip()

        if not candidato_id or not empresa_id or not vaga:
            erro = "Por favor, preencha todos os campos obrigatórios."
        else:
            cand = candidatos_coll.find_one({"_id": ObjectId(candidato_id)})
            emp = empresas_coll.find_one({"_id": ObjectId(empresa_id)})

            if not cand or not emp:
                erro = "Candidato ou Empresa inválidos."
            else:
                candidaturas_coll.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {
                        "candidato_id": ObjectId(candidato_id),
                        "candidato_nome": cand["nome"],
                        "empresa_id": ObjectId(empresa_id),
                        "empresa_nome": emp["nome"],
                        "vaga": vaga,
                        "status": status
                    }}
                )
                return redirect(url_for("listar_candidaturas"))

    return render_template(
        "editar_candidatura.html",
        candidatura=candidatura,
        candidatos=candidatos,
        empresas=empresas,
        status_opcoes=status_opcoes,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)