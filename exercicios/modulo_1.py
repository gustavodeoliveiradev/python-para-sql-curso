# ============================================
# EXERCÍCIOS DO MÓDULO 1 - Lógica de Programação
# ============================================

# ----- EXERCÍCIO 1: Variáveis -----
# Crie variáveis representando um cliente

id_cliente = 1
nome_cliente = "Ana Souza"
email_cliente = "ana@email.com"
idade_cliente = 32
eh_vip = True

print(f"Cliente: {nome_cliente}, Idade: {idade_cliente}, VIP: {eh_vip}")


# ----- EXERCÍCIO 2: Filtro de Clientes -----
# Reescreva a query SQL em Python

idade = 45
eh_vip = True

pode_ter_desconto = (idade >= 18 and idade <= 65) and eh_vip
print(f"Pode ter desconto? {pode_ter_desconto}")


# ----- EXERCÍCIO 3: Classificação -----
# Classifique cliente por gasto anual

gasto_anual = 15000

if gasto_anual < 1000:
    categoria = "Bronze"
elif gasto_anual < 5000:
    categoria = "Prata"
elif gasto_anual < 10000:
    categoria = "Ouro"
else:
    categoria = "Diamante"

print(f"Categoria: {categoria}")


# ----- EXERCÍCIO 4: Processando Query -----
# Simule resultado de query e verifique maioridade

resultado_query = [
    {"nome": "Ana", "idade": 25},
    {"nome": "Bruno", "idade": 17},
    {"nome": "Carla", "idade": 45},
    {"nome": "Daniel", "idade": 12}
]

print("\n📋 Relatório de Clientes:")
print("-" * 30)

for cliente in resultado_query:
    if cliente["idade"] >= 18:
        status = "Maior de idade ✅"
    else:
        status = "Menor de idade ❌"
    print(f"{cliente['nome']}: {cliente['idade']} anos - {status}")


# ----- EXERCÍCIO 5: Funções Úteis -----

def limpar_cpf(cpf):
    return cpf.replace(".", "").replace("-", "")

def email_valido(email):
    return "@" in email

def calcular_media(valores):
    return sum(valores) / len(valores)

print(f"\nCPF limpo: {limpar_cpf('123.456.789-00')}")
print(f"Email válido? {email_valido('ana@email.com')}")
print(f"Média: {calcular_media([10, 20, 30])}")


# ----- DESAFIO FINAL: Mini-Sistema -----

print("\n" + "=" * 40)
print("📊 RELATÓRIO DE CLIENTES")
print("=" * 40)

clientes = [
    {"nome": "Ana", "idade": 25, "gasto_anual": 800},
    {"nome": "Bruno", "idade": 45, "gasto_anual": 3500},
    {"nome": "Carla", "idade": 32, "gasto_anual": 7000},
    {"nome": "Daniel", "idade": 28, "gasto_anual": 15000},
    {"nome": "Elisa", "idade": 19, "gasto_anual": 200}
]

def classificar_cliente(gasto):
    if gasto < 1000:
        return "Bronze 🥉"
    elif gasto < 5000:
        return "Prata 🥈"
    elif gasto < 10000:
        return "Ouro 🥇"
    else:
        return "Diamante 💎"

for cliente in clientes:
    categoria = classificar_cliente(cliente["gasto_anual"])
    print(f"👤 {cliente['nome']} | {cliente['idade']} anos")
    print(f"   Gasto: R${cliente['gasto_anual']}")
    print(f"   Categoria: {categoria}")
    print("-" * 40)

print("✅ Relatório finalizado!")
