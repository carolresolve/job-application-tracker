#from database.conexao import conectar_banco
from candidatos.candidatos import cadastrar_candidato
from empresas.empresas import cadastrar_empresa
from candidaturas.candidaturas import cadastrar_candidatura

#banco = conectar_banco()
#Primeiro: testei a conexão com banco.. coloquei como coment pois foi ok
#print("Conexão com MongoDB realizada!")
#print("Banco:", banco.name)
#cadastrar_candidato()
#cadastrar_empresa()
cadastrar_candidatura()
