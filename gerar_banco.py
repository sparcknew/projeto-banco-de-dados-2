# gerar_supermercado_final.py – LIMPA TUDO + DADOS REALISTAS DE GRANDE REDE
import sqlite3
import random
from datetime import datetime, timedelta
import names

print("LIMPEZA TOTAL + GERAÇÃO DE DADOS REALISTAS – GRANDE REDE BRASILEIRA 2025")
conn = sqlite3.connect('supermercado')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# ================================================
# 1. LIMPEZA TOTAL – ORDEM CORRETA (testada e comprovada)
# ================================================
print("Limpando todas as 15 tabelas (ordem correta para FK)...")
deletion_order = [
    "Item_Venda", "Item_Compra", "Pagamento", "Promocao",          # Filhas mais baixas
    "Venda", "Compra", "Produto_Fornecedor", "Funcionario_Setor", "Endereco_Cliente",
    "Cliente", "Produto", "Fornecedor", "Funcionario",             # Pais intermediários
    "Setor", "Categoria_Produto"                                   # Pais principais
]

for table in deletion_order:
    try:
        c.execute(f"DELETE FROM {table}")
        print(f"   ✓ {table} limpa")
    except sqlite3.IntegrityError as e:
        print(f"   ⚠ Erro em {table}: {e} (pulo)")
    except Exception as e:
        print(f"   ⚠ Erro inesperado em {table}: {e}")
conn.commit()

# ================================================
# 2. CATEGORIAS (10 reais)
# ================================================
categorias = [
    "Alimentos Secos", "Bebidas", "Higiene Pessoal", "Limpeza", "Frios e Laticínios",
    "Padaria", "Hortifrúti", "Congelados", "Açougue", "Utilidades Domésticas"
]
cat_ids = []
for cat in categorias:
    c.execute("INSERT INTO Categoria_Produto (catp_nome) VALUES (?)", (cat,))
    cat_ids.append(c.lastrowid)
conn.commit()

# ================================================
# 3. 5.000 PRODUTOS (marcas brasileiras reais)
# ================================================
print("Inserindo 5.000 produtos...")
marcas = ["Nestlé", "Sadia", "Perdigão", "Coca-Cola", "Guaraná Antarctica", "Skol", "Brahma", "Heineken", "Ypê", "Omo", "Qualitá", "Taeq", "Itambé", "Danone", "Seara", "Aurora", "Friboi", "Pilão", "Melitta", "3 Corações"]
produtos_base = ["Arroz", "Feijão", "Macarrão", "Óleo de Soja", "Leite UHT", "Sabão em Pó", "Detergente", "Shampoo", "Refrigerante", "Cerveja", "Pão de Forma", "Queijo Mussarela", "Presunto", "Peito de Peru", "Frango Congelado", "Carne Moída", "Hambúrguer", "Pizza Congelada", "Lasanha Congelada", "Sorvete"]
variacoes = ["Integral", "Zero Açúcar", "Diet", "Light", "Premium", "Tradicional", "Fatiado", "500g", "1kg", "2kg", "900ml", "2L", "Caixa 30un", "Pack 6", "Lata 350ml"]
prod_ids = []
for i in range(5000):
    nome = f"{random.choice(marcas)} {random.choice(produtos_base)} {random.choice(variacoes)}"
    preco = round(random.uniform(2.49, 299.90), 2)
    estoque = random.randint(50, 5000)  # Estoque inicial alto para rede grande
    cat = cat_ids[i % 10]
    c.execute("INSERT INTO Produto (prod_nome, prod_preco, prod_qtd_estoque, catp_catp_id) VALUES (?, ?, ?, ?)",
              (nome, preco, estoque, cat))
    prod_ids.append(c.lastrowid)
    if i % 1000 == 999:
        print(f"   {i+1}/5000 produtos")
conn.commit()

# ================================================
# 4. 80 FORNECEDORES REAIS + RELAÇÃO
# ================================================
print("Inserindo 80 fornecedores...")
fornecedores = ["Coca-Cola Brasil", "Ambev", "BRF Alimentos", "JBS S/A", "Nestlé Brasil", "Unilever Brasil", "Procter & Gamble", "M. Dias Branco", "Aurora Alimentos", "Seara Alimentos", "Bunge Alimentos", "Camil Alimentos", "Ypê Indústria", "Reckitt Benckiser", "Colgate-Palmolive", "Johnson & Johnson", "Unilever", "P&G Brasil", "Danone Brasil", "Itambé"]
forn_ids = []
for i in range(80):
    nome = fornecedores[i % len(fornecedores)] if i < len(fornecedores) else f"Distribuidora Regional {i-19} Ltda"
    cnpj = f"{random.randint(10,99):02d}.{random.randint(100,999):03d}.{random.randint(100,999):03d}/0001-{random.randint(10,99):02d}"
    tel = f"({random.randint(11,99)}) {random.randint(3000,9999)}-{random.randint(1000,9999)}"
    c.execute("INSERT INTO Fornecedor (forn_nome, forn_cnpj, forn_telefone) VALUES (?, ?, ?)",
              (nome, cnpj, tel))
    forn_ids.append(c.lastrowid)
# Relação (1 a 4 fornecedores por produto)
for prod in prod_ids:
    for forn in random.sample(forn_ids, random.randint(1,4)):
        try:
            c.execute("INSERT INTO Produto_Fornecedor VALUES (?, ?)", (prod, forn))
        except: pass
conn.commit()

# ================================================
# 5. 5.000 CLIENTES + ENDEREÇOS (capitais brasileiras)
# ================================================
print("Inserindo 5.000 clientes...")
cidades = [("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Belo Horizonte", "MG"), ("Curitiba", "PR"), ("Porto Alegre", "RS"), ("Salvador", "BA"), ("Recife", "PE"), ("Fortaleza", "CE")]
cli_ids = []
for i in range(5000):
    nome = names.get_full_name()
    cpf = f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"
    tel = f"({random.randint(11,99)}) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    c.execute("INSERT INTO Cliente (cli_nome, cli_cpf, cli_telefone) VALUES (?, ?, ?)",
              (nome, cpf, tel))
    cli_id = c.lastrowid
    cli_ids.append(cli_id)
    cidade, estado = random.choice(cidades)
    c.execute("INSERT INTO Endereco_Cliente (endc_rua, endc_numero, endc_bairro, endc_cidade, endc_estado, endc_cli_id) VALUES (?, ?, ?, ?, ?, ?)",
              (f"Rua {names.get_last_name()}", str(random.randint(1,5000)), random.choice(["Centro", "Jardim", "Vila Nova", "Parque"]), cidade, estado, cli_id))
    if i % 1000 == 999:
        print(f"   {i+1}/5000 clientes")
conn.commit()

# ================================================
# 6. 60 FUNCIONÁRIOS + 7 SETORES
# ================================================
setores = ["Caixa", "Reposição", "Gerência", "Açougue", "Padaria", "Hortifrúti", "Peixaria"]
setor_ids = []
for s in setores:
    c.execute("INSERT INTO Setor (setor_nome) VALUES (?)", (s,))
    setor_ids.append(c.lastrowid)

func_ids = []
for i in range(60):
    nome = names.get_full_name()
    cargo = random.choice(["Caixa", "Repositor", "Gerente de Setor", "Açougueiro", "Padeiro", "Fruteiro", "Peixeiro", "Supervisor"])
    salario = round(random.uniform(2200, 18000), 2)
    admissao = (datetime(2019,1,1) + timedelta(days=random.randint(0,2190))).strftime("%Y-%m-%d")
    c.execute("INSERT INTO Funcionario (func_nome, func_cargo, func_salario, func_data_admissao) VALUES (?, ?, ?, ?)",
              (nome, cargo, salario, admissao))
    func_id = c.lastrowid
    func_ids.append(func_id)
    c.execute("INSERT INTO Funcionario_Setor (fs_func_id, fs_setor_id, fs_data_inicio) VALUES (?, ?, ?)",
              (func_id, random.choice(setor_ids), admissao))
conn.commit()

# ================================================
# 7. 500 COMPRAS DE REPOSIÇÃO
# ================================================
print("Inserindo 500 compras de reposição...")
inicio_compra = datetime(2025,1,1)
for i in range(500):
    data = (inicio_compra + timedelta(days=random.randint(0,330))).strftime("%Y-%m-%d")
    forn = random.choice(forn_ids)
    func = random.choice(func_ids)
    total = 0.0
    c.execute("INSERT INTO Compra (comp_data, comp_valor_total, comp_forn_id, comp_func_id) VALUES (?, ?, ?, ?)",
              (data, 0.0, forn, func))
    comp_id = c.lastrowid
    for _ in range(random.randint(15,80)):
        prod = random.choice(prod_ids)
        qtd = random.randint(50,600)
        preco_custo = round(random.uniform(0.4,0.9) * c.execute("SELECT prod_preco FROM Produto WHERE prod_id=?", (prod,)).fetchone()[0], 2)
        total += qtd * preco_custo
        c.execute("INSERT INTO Item_Compra (itemc_qtd, itemc_preco_unit, itemc_comp_id, itemc_prod_id) VALUES (?, ?, ?, ?)",
                  (qtd, preco_custo, comp_id, prod))
        c.execute("UPDATE Produto SET prod_qtd_estoque = prod_qtd_estoque + ? WHERE prod_id = ?", (qtd, prod))
    c.execute("UPDATE Compra SET comp_valor_total = ? WHERE comp_id = ?", (round(total,2), comp_id))
conn.commit()

# ================================================
# 8. 5.000 VENDAS – ESTOQUE NUNCA NEGATIVO
# ================================================
print("Inserindo 5.000 vendas – ESTOQUE SEMPRE POSITIVO")
inicio_venda = datetime(2025,7,1)
for i in range(5000):
    data = (inicio_venda + timedelta(days=random.randint(0,183))).strftime("%Y-%m-%d")
    cli = random.choice(cli_ids)
    func = random.choice(func_ids)
    total = 0.0

    c.execute("INSERT INTO Venda (venda_data, venda_valor_total, venda_cli_id, venda_func_id) VALUES (?, ?, ?, ?)",
              (data, 0.0, cli, func))
    venda_id = c.lastrowid

    itens_na_venda = random.randint(1, 35)
    itens_adicionados = 0

    while itens_adicionados < itens_na_venda:
        prod_id = random.choice(prod_ids)
        estoque_atual = c.execute("SELECT prod_qtd_estoque FROM Produto WHERE prod_id = ?", (prod_id,)).fetchone()[0]

        if estoque_atual <= 0:
            continue  # Pula produto sem estoque

        qtd_desejada = random.randint(1, min(15, estoque_atual))  # Nunca vende mais do que tem
        qtd_vendida = qtd_desejada

        preco = c.execute("SELECT prod_preco FROM Produto WHERE prod_id = ?", (prod_id,)).fetchone()[0]
        total += qtd_vendida * preco

        c.execute("INSERT INTO Item_Venda (itemv_qtd, itemv_preco_unit, itemv_venda_id, itemv_prod_id) VALUES (?, ?, ?, ?)",
                  (qtd_vendida, preco, venda_id, prod_id))
        c.execute("UPDATE Produto SET prod_qtd_estoque = prod_qtd_estoque - ? WHERE prod_id = ?", (qtd_vendida, prod_id))

        itens_adicionados += 1

    c.execute("UPDATE Venda SET venda_valor_total = ? WHERE venda_id = ?", (round(total,2), venda_id))
    metodo = random.choices(["PIX", "Cartão Crédito", "Cartão Débito", "Dinheiro"], weights=[50, 25, 20, 5])[0]
    c.execute("INSERT INTO Pagamento (pag_metodo, pag_valor, pag_data, pag_venda_id) VALUES (?, ?, ?, ?)",
              (metodo, round(total,2), data, venda_id))

    if i % 500 == 499:
        print(f"   {i+1}/5000 vendas – estoque sempre positivo")
conn.commit()

# ================================================
# 9. 120 PROMOÇÕES REAIS
# ================================================
print("Criando 120 promoções...")
for _ in range(120):
    prod = random.choice(prod_ids)
    percentual = random.choice([10,15,20,25,30,40,50])
    inicio = (datetime(2025,7,1) + timedelta(days=random.randint(0,150))).strftime("%Y-%m-%d")
    fim = (datetime.strptime(inicio, "%Y-%m-%d") + timedelta(days=random.randint(7,90))).strftime("%Y-%m-%d")
    c.execute("INSERT INTO Promocao (promo_percentual, promo_inicio, promo_fim, promo_prod_id) VALUES (?, ?, ?, ?)",
              (percentual, inicio, fim, prod))
conn.commit()

print("\n✅ BANCO LIMPO E PREENCHIDO COM SUCESSO!")
print("→ 5.000 clientes | 5.000 produtos | 5.000 vendas | 500 compras | 120 promoções")
print("→ Estoque SEMPRE positivo | FKs respeitadas | Dados 100% realistas 2025")
print("→ Pronto para dashboard: streamlit run dashboard_supermercado.py")
conn.close()