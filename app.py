from flask import Flask, render_template
from database.conexao import conectar_banco

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

if __name__ == "__main__":
    app.run(debug=True)