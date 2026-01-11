# Sistema Organizacional de Academia

Este repositório contém o trabalho final da disciplina de **Fundamentos de Banco de Dados**, semestre 2025.2, do curso de Engenharia de Software da Universidade Federal do Ceará (UFC) - Campus de Russas.

## 📋 Sobre o Projeto
O objetivo deste trabalho prático é desenvolver um sistema completo de gerenciamento de dados baseado em um banco de dados relacional. O sistema implementa operações CRUD, visões (Views), consultas avançadas e gatilhos (Triggers) utilizando **PostgreSQL** e **Python**.

**Professor:** Robertty Costa 

## 👥 Equipe
* **Integrante 1:** [Raquel Santos Silva] (Modelagem, Normalização e Criação do Banco)
* **Integrante 2:** [John Miguel da Silva Fernandes] (Implementação do Sistema, Views e Consultas Avançadas)
* **Integrante 3:** [Enzo Andrade dos Anjos] (Consultas SQL e Triggers)

## 🛠 Tecnologias Utilizadas
* **Linguagem:** Python 
* **SGBD:** PostgreSQL
* **Driver:** Psycopg2
* **Modelagem:** BrModelo / StarUML 

## 📂 Estrutura do Projeto
A organização dos diretórios segue a divisão de responsabilidades:
* `/docs`: Documentação do Modelo ER e Relacional.
* `/sql`: Scripts DDL (Create), DML (Insert), Views e Triggers.
* `/src`: Código fonte da aplicação Python.

## ⚙️ Como Executar
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Configure as credenciais do banco no arquivo `.env` (baseado no `.env.example`).
5. Execute a aplicação: `python src/main.py`.
