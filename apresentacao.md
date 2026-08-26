# Projeto Final - Sistema de Acompanhamento de Candidaturas

**Formandas:** Ana Carolina e Gessica

## 1. Título provisório

**Job Tracker - Sistema de Acompanhamento de Candidaturas**

## 2. Problema a resolver

O processo de candidatura a empregos pode envolver várias empresas, diferentes vagas e diferentes etapas, tornando difícil acompanhar todas as candidaturas realizadas.

O projeto pretende criar uma aplicação que permita **acompanhar o processo de candidatura**, facilitando a gestão das informações tanto do **candidato** quanto das **empresas e vagas**.

A aplicação permitirá saber quais candidaturas foram enviadas, em que estado se encontram e quais empresas estão associadas a cada candidatura.

## 3. Utilizador ou público-alvo

A aplicação será destinada principalmente a:

* Pessoas que estão à procura de emprego;
* Pessoas que realizam várias candidaturas simultaneamente;
* Utilizadores que pretendem organizar e acompanhar o estado das suas candidaturas.
* Empresas que estão orfertando vagas de emprego

## 4. Funcionalidades previstas para o MVP

O Produto Mínimo Viável terá as seguintes funcionalidades:

### Candidatos

* Cadastrar candidato;
* Listar candidatos;
* Consultar candidato;
* Atualizar dados do candidato;
* Remover candidato.

### Empresas

* Cadastrar empresa;
* Listar empresas;
* Consultar empresa;
* Atualizar dados da empresa;
* Remover empresa.

### Candidaturas

* Registar uma nova candidatura;
* Listar candidaturas;
* Consultar uma candidatura;
* Atualizar uma candidatura;
* Remover uma candidatura;
* Alterar o estado da candidatura;
* Filtrar candidaturas por estado.

### Estatísticas

* Número total de candidaturas;
* Número de candidaturas por estado;
* Número de candidaturas por empresa.

## 5. Dados que serão guardados

### Candidato

* Nome;
* Email;
* Telefone;
* Cidade;
* Competências.

### Empresa

* Nome;
* NIF;
* Localidade;
* Setor;
* Email.

### Candidatura

* Candidato;
* Empresa;
* Cargo;
* Data da candidatura;
* Estado;
* Salário;
* Observações.

Os dados serão armazenados utilizando **MongoDB**, através da biblioteca **PyMongo**.

## 6. Funções principais inicialmente previstas

A aplicação será organizada em funções com responsabilidades específicas, como:

* `cadastrar_candidato()`
* `listar_candidatos()`
* `atualizar_candidato()`
* `remover_candidato()`
* `cadastrar_empresa()`
* `listar_empresas()`
* `atualizar_empresa()`
* `remover_empresa()`
* `cadastrar_candidatura()`
* `listar_candidaturas()`
* `atualizar_candidatura()`
* `remover_candidatura()`
* `alterar_estado()`
* `mostrar_estatisticas()`

Também serão criadas funções para **validar os dados introduzidos pelo utilizador** e tratar possíveis erros durante a execução.

## 7. Extensões futuras

As seguintes funcionalidades poderão ser desenvolvidas depois da conclusão e dos testes do MVP:

* Pesquisa avançada de candidaturas;
* Cálculo da taxa de resposta às candidaturas;
* Cálculo do salário médio das vagas;
* Histórico de alterações do estado de uma candidatura;
* Filtros por período, empresa ou cargo;
* Relatórios e estatísticas mais detalhadas.
