# ============================================
# EXERCÍCIOS DO MÓDULO 2 - Estruturas de Dados
# ============================================

# ----- EXERCÍCIO 1: Manipulando Listas -----

vips = ["Ana", "Bruno", "Carlos", "Daniela"]

vips.append("Fernanda")
vips.insert(2, "Gabriel")
vips.remove("Carlos")
vips.sort()

print(f"Clientes VIP: {vips}")
print(f"Total: {len(vips)} clientes")


# ----- EXERCÍCIO 2: CRUD com Dicionário -----

cliente = {
    "nome": "Bruno Silva",
    "email": "bruno@email.com",
    "idade": 28,
    "cidade": "São Paulo"
}

cliente["idade"] = 29
cliente["vip"] = True
del cliente["cidade"]

print("\n📋 Dados do Cliente:")
for chave, valor in cliente.items():
    print(f"   {chave}: {valor}")


# ----- EXERCÍCIO 3: Sets e Operações -----

campanha_1 = ["Ana", "Bruno", "Carla", "Daniel"]
campanha_2 = ["Bruno", "Daniel", "Elisa", "Fernanda"]

set_1 = set(campanha_1)
set_2 = set(campanha_2)

print(f"\nEm ambas: {set_1 & set_2}")
print(f"Só campanha 1: {set_1 - set_2}")
print(f"Todos únicos: {list(set_1 | set_2)}")


# ----- DESAFIO FINAL: Mini-Banco de Dados -----

produtos = [
    {"id": 1, "nome": "Mouse", "preco": 50.0, "categoria": "Periféricos", "estoque": 15},
    {"id": 2, "nome": "Teclado", "preco": 120.0, "categoria": "Periféricos", "estoque": 8},
    {"id": 3, "nome": "Monitor", "preco": 800.0, "categoria": "Monitores", "estoque": 5},
    {"id": 4, "nome": "Webcam", "preco": 200.0, "categoria": "Periféricos", "estoque": 20}
]

print("\n" + "=" * 40)
print("📊 MINI-BANCO DE DADOS")
print("=" * 40)

# Estoque baixo
print("\n⚠️ Estoque baixo:")
baixo_estoque = [p for p in produtos if p["estoque"] < 10]
for p in baixo_estoque:
    print(f"   {p['nome']}: {p['estoque']} unidades")

# Valor em estoque
print("\n💰 Valor em estoque:")
for p in produtos:
    total = p["preco"] * p["estoque"]
    print(f"   {p['nome']}: R${total:,.2f}")

# Categorias únicas
categorias = set(p["categoria"] for p in produtos)
print(f"\n📂 Categorias: {categorias}")

# Adicionar produto
produtos.append({
    "id": 5, "nome": "Headset", "preco": 150.0,
    "categoria": "Áudio", "estoque": 12
})

print(f"\n✅ Total de produtos: {len(produtos)}")
