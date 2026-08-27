from flask import Flask, render_template, request, redirect, url_for
from database.conexao import conectar_banco
from bson.objectid import ObjectId

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
        
        # Busca os nomes para salvar um documento completo na coleçãofrom bson.objectid import ObjectId
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

    # GET: Busca listas para preencher os <select> no formulário    candidatos = list(banco["candidatos"].find())
 empresas = list(banco["empresas"].find())
 candidatos = list(banco["candidatos"].find())
 return render_template("nova_candidatura.html", candidatos=candidatos, empresas=empresas)

if __name__ == "__main__":
    app.run(debug=True)
