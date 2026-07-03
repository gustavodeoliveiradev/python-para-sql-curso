# ============================================
# EXERCÍCIOS DO MÓDULO 3 - Python + SQL (A Ponte)
# ============================================
#
# Rode este arquivo direto: python modulo_3.py
# Usamos sqlite3 ":memory:" (banco temporário, na RAM) pra você
# poder rodar o exercício quantas vezes quiser sem gerar arquivo .db.
#
# Precisa de pandas instalado: pip install pandas

import sqlite3
import pandas as pd

# ----- EXERCÍCIO 1: Cadastrando Produtos -----

conexao = sqlite3.connect(":memory:")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        preco REAL,
        estoque INTEGER
    )
""")

produtos = [
    ("Mouse", 50.0, 15),
    ("Teclado", 120.0, 8),
    ("Monitor", 800.0, 5),
]

cursor.executemany(
    "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
    produtos
)
conexao.commit()

print(f"Exercício 1: {cursor.rowcount} produtos inseridos! ✅")


# ----- EXERCÍCIO 2: Relatório com pandas -----

df = pd.read_sql_query("SELECT * FROM produtos", conexao)

df["valor_total"] = df["preco"] * df["estoque"]

print("\n📊 Produtos:")
print(df)

print("\n⚠️ Estoque baixo (< 10):")
print(df[df["estoque"] < 10])

top = df.loc[df["valor_total"].idxmax()]
print(f"\n🏆 Maior valor em estoque: {top['nome']} (R${top['valor_total']:.2f})")

conexao.close()


# ----- DESAFIO FINAL: Mini-Sistema de Vendas -----

conexao = sqlite3.connect(":memory:")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY, nome TEXT, cidade TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY, cliente_id INTEGER, produto TEXT, valor REAL)""")

cursor.executemany("INSERT INTO clientes (nome, cidade) VALUES (?, ?)", [
    ("Ana", "São Paulo"), ("Bruno", "Curitiba"), ("Carla", "Recife")
])
cursor.executemany(
    "INSERT INTO vendas (cliente_id, produto, valor) VALUES (?, ?, ?)", [
    (1, "Mouse", 50.0), (1, "Teclado", 120.0), (2, "Monitor", 800.0),
    (3, "Webcam", 200.0), (2, "Mouse", 50.0)
])
conexao.commit()

# JOIN direto no pandas
df_vendas = pd.read_sql_query("""
    SELECT c.nome, c.cidade, v.produto, v.valor
    FROM vendas v
    JOIN clientes c ON c.id = v.cliente_id
""", conexao)
conexao.close()

print("\n" + "=" * 40)
print("📊 MINI-SISTEMA DE VENDAS")
print("=" * 40)

total_por_cliente = df_vendas.groupby("nome")["valor"].sum().reset_index()
total_por_cliente.columns = ["cliente", "total_vendido"]

print("\n💰 Total vendido por cliente:")
print(total_por_cliente)

# Descomente pra gerar o CSV de verdade:
# total_por_cliente.to_csv("relatorio_vendas.csv", index=False)

print("\n✅ Desafio concluído!")
