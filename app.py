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
    # Busca todas as candidaturas no MongoDB
    candidaturas = list(banco["candidaturas"].find())
    return render_template("candidaturas.html", candidaturas=candidaturas)

@app.route("/candidaturas/nova", methods=["GET", "POST"])
def cadastrar_candidatura():   
    banco = conectar_banco()
    
    if request.method == "POST":
        candidato_id = request.form.get("candidato_id")
        empresa_id = request.form.get("empresa_id")
        status = request.form.get("status")
        
        # Busca os nomes para salvar um documento completo na coleção
        candidato = banco["candidatos"].find_one({"_id": ObjectId(candidato_id)})
        empresa = banco["empresas"].find_one({"_id": ObjectId(empresa_id)})
        
        banco["candidaturas"].insert_one({
            "candidato_id": ObjectId(candidato_id),
            "nome_candidato": candidato["nome"],
            "empresa_id": ObjectId(empresa_id),
            "nome_empresa": empresa["nome"],
            "status": status
        })
        
        return redirect(url_for("listar_candidaturas"))

    # GET: Busca listas para preencher os <select> no formulário
    candidatos = list(banco["candidatos"].find())
    empresas = list(banco["empresas"].find())
    return render_template("nova_candidatura.html", candidatos=candidatos, empresas=empresas)

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

        # Validações de NIF e Email
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

        # Se tudo estiver correto, insere no MongoDB
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
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        area = request.form.get("area", "").strip()

        if nome and email:
            banco = conectar_banco()
            banco["candidatos"].insert_one({
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "area": area
            })
            return redirect(url_for("listar_candidatos"))

    return render_template("novo_candidato.html")



if __name__ == "__main__":
    app.run(debug=True, port=5001)