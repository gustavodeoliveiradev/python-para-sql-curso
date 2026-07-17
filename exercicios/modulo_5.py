# ============================================
# EXERCÍCIOS DO MÓDULO 5 - Projeto Final & Desafios
# ============================================
#
# Rode este arquivo direto: python modulo_5.py
# As 8 missões (Bronze/Prata/Ouro/Diamante) + o Projeto Final, todas juntas.
# Usamos sqlite3 ":memory:" (banco temporário, na RAM), sem precisar
# configurar nada — e simulamos as variáveis de ambiente direto no código
# pra você poder rodar sem criar um .env.
#
# Precisa de pandas instalado: pip install pandas

import sqlite3
import pandas as pd
import logging
import os
from pathlib import Path
from datetime import date

logging.basicConfig(
    filename="projeto_final.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("=" * 50)
print("🏆 MÓDULO 5 - MISSÕES E PROJETO FINAL")
print("=" * 50)

# ============================================
# 🥉 MISSÃO BRONZE 1 - Classificando Clientes
# ============================================

def classificar_cliente(total_compras: float) -> str:
    if total_compras <= 100:
        return "Bronze"
    elif total_compras <= 500:
        return "Prata"
    else:
        return "Ouro"

print("\n🥉 Missão Bronze 1 — Classificando Clientes")
clientes_valores = [50, 250, 800, 99.90, 500]
for valor in clientes_valores:
    categoria = classificar_cliente(valor)
    print(f"  R${valor:.2f} -> {categoria}")


# ============================================
# 🥉 MISSÃO BRONZE 2 - Somando com Laços
# ============================================

def resumir_vendas(vendas: list) -> dict:
    total = 0
    maior = vendas[0]
    for valor in vendas:
        total += valor
        if valor > maior:
            maior = valor
    media = total / len(vendas)
    return {"total": total, "media": media, "maior_venda": maior}

print("\n🥉 Missão Bronze 2 — Somando com Laços")
vendas_exemplo = [120, 340, 89.90, 500, 75]
resumo = resumir_vendas(vendas_exemplo)
print(f"  Total: R${resumo['total']:.2f} | Média: R${resumo['media']:.2f} | Maior: R${resumo['maior_venda']:.2f}")


# ============================================
# 🥈 MISSÃO PRATA 1 - Catálogo com Dicionários
# ============================================

def estoque_baixo(produtos: list, limite: int = 5) -> list:
    return [p for p in produtos if p["estoque"] <= limite]

print("\n🥈 Missão Prata 1 — Catálogo com Dicionários")
produtos_catalogo = [
    {"nome": "Mouse", "preco": 50.0, "estoque": 15},
    {"nome": "Teclado", "preco": 120.0, "estoque": 3},
    {"nome": "Monitor", "preco": 800.0, "estoque": 0},
]
criticos = estoque_baixo(produtos_catalogo)
for p in criticos:
    print(f"  ⚠️ {p['nome']}: só {p['estoque']} unidade(s)")


# ============================================
# 🥈 MISSÃO PRATA 2 - Sets e Duplicados
# ============================================

print("\n🥈 Missão Prata 2 — Sets e Duplicados")
cidades_clientes = [
    "São Paulo", "Curitiba", "São Paulo", "Recife",
    "Curitiba", "São Paulo", "Porto Alegre"
]
cidades_unicas = set(cidades_clientes)
contagem = [(cidade, cidades_clientes.count(cidade)) for cidade in cidades_unicas]
contagem.sort(key=lambda item: item[1], reverse=True)
for cidade, qtd in contagem:
    print(f"  {cidade}: {qtd} cliente(s)")


# ============================================
# 🥇 MISSÃO OURO 1 - CRUD Seguro
# ============================================

print("\n🥇 Missão Ouro 1 — CRUD Seguro")
conexao_ouro1 = sqlite3.connect(":memory:")
cursor_ouro1 = conexao_ouro1.cursor()
cursor_ouro1.execute("""CREATE TABLE tarefas (
    id INTEGER PRIMARY KEY, titulo TEXT, feita INTEGER DEFAULT 0)""")

def criar(cursor, titulo):
    cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))

def marcar_feita(cursor, id_tarefa):
    cursor.execute("UPDATE tarefas SET feita = 1 WHERE id = ?", (id_tarefa,))

def remover(cursor, id_tarefa):
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

criar(cursor_ouro1, "Estudar Python")
criar(cursor_ouro1, "Revisar SQL")
marcar_feita(cursor_ouro1, 1)
remover(cursor_ouro1, 2)
conexao_ouro1.commit()
cursor_ouro1.execute("SELECT * FROM tarefas")
print(f"  Tarefas restantes: {cursor_ouro1.fetchall()}")
conexao_ouro1.close()


# ============================================
# 🥇 MISSÃO OURO 2 - Análise com pandas
# ============================================

print("\n🥇 Missão Ouro 2 — Análise com pandas")
conexao_ouro2 = sqlite3.connect(":memory:")
cursor_ouro2 = conexao_ouro2.cursor()
cursor_ouro2.execute("CREATE TABLE vendas (id INTEGER PRIMARY KEY, produto TEXT, valor REAL)")
cursor_ouro2.executemany("INSERT INTO vendas (produto, valor) VALUES (?, ?)", [
    ("Mouse", 50.0), ("Teclado", 120.0), ("Mouse", 50.0),
    ("Monitor", 800.0), ("Mouse", 50.0),
])
conexao_ouro2.commit()

df_ouro = pd.read_sql_query("SELECT * FROM vendas", conexao_ouro2)
conexao_ouro2.close()

mais_vendido = df_ouro["produto"].value_counts().idxmax()
qtd_vendida = df_ouro["produto"].value_counts().max()
ticket_medio = df_ouro["valor"].mean()
print(f"  🏆 Produto mais vendido: {mais_vendido} ({qtd_vendida}x)")
print(f"  💰 Ticket médio: R${ticket_medio:.2f}")


# ============================================
# 💎 MISSÃO DIAMANTE 1 - Pipeline com Logging
# ============================================

print("\n💎 Missão Diamante 1 — Pipeline com Logging")

def extract_diamante(conexao):
    return pd.read_sql_query("SELECT * FROM vendas", conexao)

def transform_diamante(df):
    return df.groupby("produto")["valor"].sum().reset_index()

def load_diamante(df, caminho):
    Path(caminho).parent.mkdir(exist_ok=True)
    df.to_csv(caminho, index=False)

try:
    conexao_diamante = sqlite3.connect(":memory:")
    cursor_diamante = conexao_diamante.cursor()
    cursor_diamante.execute("CREATE TABLE vendas (produto TEXT, valor REAL)")
    cursor_diamante.executemany("INSERT INTO vendas VALUES (?, ?)", [
        ("Mouse", 50.0), ("Teclado", 120.0), ("Mouse", 50.0)
    ])
    conexao_diamante.commit()

    df_transformado = transform_diamante(extract_diamante(conexao_diamante))
    load_diamante(df_transformado, "saida/total_por_produto.csv")
    conexao_diamante.close()

    logging.info("Missão Diamante 1 executada com sucesso")
    print("  ✅ Pipeline concluído! Veja saida/total_por_produto.csv")
except Exception as e:
    logging.error(f"Falha na Missão Diamante 1: {e}")
    print(f"  ❌ Erro: {e}")


# ============================================
# 💎 MISSÃO DIAMANTE 2 - Credenciais Seguras
# ============================================

print("\n💎 Missão Diamante 2 — Credenciais Seguras")

# Em um projeto real isso viria de um .env com python-dotenv.
# Aqui simulamos os.environ pra rodar sem precisar criar o arquivo:
os.environ["EMAIL_REMETENTE"] = "relatorios@empresa.com"
os.environ["EMAIL_SENHA"] = "uma_senha_de_app_aqui"

def obter_credencial(nome_variavel):
    valor = os.environ.get(nome_variavel)
    if not valor:
        raise ValueError(f"Variável de ambiente '{nome_variavel}' não configurada!")
    return valor

remetente = obter_credencial("EMAIL_REMETENTE")
senha = obter_credencial("EMAIL_SENHA")
print(f"  🔐 Pronto pra enviar como {remetente} (credenciais validadas)")


# ============================================
# 🏆 PROJETO FINAL - Sistema de Relatório de Vendas
# ============================================

print("\n" + "=" * 50)
print("🏆 PROJETO FINAL — Sistema de Relatório de Vendas")
print("=" * 50)

# 1. Dados modelados em Python (Módulos 1-2)
clientes = [
    {"id": 1, "nome": "Ana", "cidade": "São Paulo"},
    {"id": 2, "nome": "Bruno", "cidade": "Curitiba"},
    {"id": 3, "nome": "Carla", "cidade": "São Paulo"},
]
vendas_projeto = [
    (1, "Mouse", 50.0), (1, "Teclado", 120.0),
    (2, "Monitor", 800.0), (3, "Webcam", 200.0), (2, "Mouse", 50.0),
]

def setup_banco():
    # 2. Tabelas + queries parametrizadas (Módulo 3)
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE clientes (
        id INTEGER PRIMARY KEY, nome TEXT, cidade TEXT)""")
    cursor.execute("""CREATE TABLE vendas (
        id INTEGER PRIMARY KEY, cliente_id INTEGER, produto TEXT, valor REAL)""")

    cursor.executemany("INSERT INTO clientes VALUES (?, ?, ?)",
        [(c["id"], c["nome"], c["cidade"]) for c in clientes])
    cursor.executemany(
        "INSERT INTO vendas (cliente_id, produto, valor) VALUES (?, ?, ?)", vendas_projeto)
    conexao.commit()
    return conexao

def extract(conexao):
    # 3. JOIN direto no pandas (Módulo 3)
    return pd.read_sql_query("""
        SELECT c.nome, c.cidade, v.valor
        FROM vendas v JOIN clientes c ON c.id = v.cliente_id
    """, conexao)

def transform(df):
    por_cliente = df.groupby("nome")["valor"].sum().reset_index()
    por_cidade = df.groupby("cidade")["valor"].sum().reset_index()
    return por_cliente, por_cidade

def load(por_cliente, por_cidade):
    Path("saida").mkdir(exist_ok=True)
    por_cliente.to_csv("saida/vendas_por_cliente.csv", index=False)
    por_cidade.to_csv("saida/vendas_por_cidade.csv", index=False)

# 4-5. Pipeline com try/except, logging e .env (Módulo 4)
try:
    destinatario = os.environ.get("EMAIL_DESTINO", "financeiro@empresa.com")
    conexao_final = setup_banco()
    df_final = extract(conexao_final)
    conexao_final.close()

    por_cliente, por_cidade = transform(df_final)
    load(por_cliente, por_cidade)

    logging.info(f"Projeto final executado, relatório pronto pra {destinatario}")
    print("\n✅ Relatório gerado em saida/vendas_por_cliente.csv e saida/vendas_por_cidade.csv")
    print("\n💰 Total vendido por cliente:")
    print(por_cliente)
except Exception as e:
    logging.error(f"Falha no projeto final: {e}")
    print(f"\n❌ Erro: {e}")

print("\n" + "🎉🐍🎉" * 3)
print("Parabéns! Você concluiu todas as missões e o Projeto Final!")
print("🎉🐍🎉" * 3)
