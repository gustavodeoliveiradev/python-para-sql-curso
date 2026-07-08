# ============================================
# EXERCÍCIOS DO MÓDULO 4 - Automação & Scripts Úteis
# ============================================
#
# Rode este arquivo direto: python modulo_4.py
# Não usamos e-mail/agendamento de verdade aqui (só simulamos o log),
# pra você poder rodar sem configurar nada.

import sqlite3
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(
    filename="automacao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----- EXERCÍCIO 1: Organizando arquivos -----

pasta_relatorios = Path("relatorios_2026")
pasta_relatorios.mkdir(exist_ok=True)
print(f"Exercício 1: pasta pronta em {pasta_relatorios.resolve()}")

pasta_atual = Path(".")
arquivos_py = list(pasta_atual.glob("*.py"))
print(f"{len(arquivos_py)} arquivo(s) .py encontrado(s) na pasta atual:")
for arquivo in arquivos_py:
    tamanho_kb = arquivo.stat().st_size / 1024
    print(f"  - {arquivo.name}: {tamanho_kb:.1f} KB")


# ----- EXERCÍCIO 2: Pipeline com tratamento de erros -----

def extract(conexao):
    return pd.read_sql_query("SELECT * FROM produtos", conexao)

def transform(df):
    df["valor_total"] = df["preco"] * df["estoque"]
    return df

def load(df, caminho):
    Path(caminho).parent.mkdir(exist_ok=True)
    df.to_csv(caminho, index=False)

try:
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE produtos (
        id INTEGER PRIMARY KEY, nome TEXT, preco REAL, estoque INTEGER)""")
    cursor.executemany(
        "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
        [("Mouse", 50.0, 15), ("Teclado", 120.0, 8), ("Monitor", 800.0, 5)]
    )
    conexao.commit()

    df = extract(conexao)
    df = transform(df)
    load(df, "saida/produtos_valorizados.csv")
    conexao.close()

    logging.info("Pipeline executado com sucesso")
    print("\nExercício 2: ✅ Pipeline concluído! Veja saida/produtos_valorizados.csv")
except Exception as e:
    logging.error(f"Falha no pipeline: {e}")
    print(f"\nExercício 2: ❌ Erro: {e}")


# ----- EXERCÍCIO 3: Protegendo credenciais (simulado) -----
# Em um projeto real, isso viria de um arquivo .env com python-dotenv:
#
#   from dotenv import load_dotenv
#   load_dotenv()
#   usuario_banco = os.environ["DB_USUARIO"]
#
# Aqui simulamos os.environ pra rodar sem precisar criar o .env:

import os
os.environ["DB_USUARIO"] = "admin"          # normalmente viria do .env
os.environ["DB_SENHA"] = "senha_super_secreta_123"  # idem

usuario_banco = os.environ["DB_USUARIO"]
senha_banco = os.environ["DB_SENHA"]

print(f"\nExercício 3: conectando como '{usuario_banco}' (senha lida de variável de ambiente) ✅")


# ----- DESAFIO FINAL: Relatório diário (rotina completa) -----

from datetime import date

def rotina_diaria():
    try:
        conexao = sqlite3.connect(":memory:")
        cursor = conexao.cursor()
        cursor.execute("""CREATE TABLE vendas (
            id INTEGER PRIMARY KEY, data TEXT, valor REAL)""")
        cursor.executemany(
            "INSERT INTO vendas (data, valor) VALUES (?, ?)", [
            ("2026-07-01", 150.0), ("2026-07-01", 200.0), ("2026-07-02", 300.0),
        ])
        conexao.commit()

        df = pd.read_sql_query("SELECT * FROM vendas", conexao)
        df["dia"] = pd.to_datetime(df["data"]).dt.date
        resumo = df.groupby("dia")["valor"].sum().reset_index()
        conexao.close()

        Path("saida").mkdir(exist_ok=True)
        caminho = f"saida/relatorio_{date.today().isoformat()}.csv"
        resumo.to_csv(caminho, index=False)

        logging.info(f"Relatório diário gerado em {caminho}")
        print(f"\n🏆 Desafio: relatório diário gerado em {caminho}")
        print(resumo)
    except Exception as e:
        logging.error(f"Falha na rotina diária: {e}")
        print(f"\n🏆 Desafio: ❌ Erro: {e}")

rotina_diaria()

print("\n✅ Todos os exercícios do Módulo 4 rodaram! Confira a pasta saida/ e o arquivo automacao.log")
