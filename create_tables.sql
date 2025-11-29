-- ==========================================
-- CRIAÇÃO DAS TABELAS - SUPERMERCADO
-- SQLITE
-- ==========================================

PRAGMA foreign_keys = ON;

CREATE TABLE Categoria_Produto (
    catp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    catp_nome TEXT NOT NULL
);

CREATE TABLE Produto (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_nome TEXT NOT NULL,
    prod_preco REAL NOT NULL,
    prod_qtd_estoque INTEGER NOT NULL,
    catp_catp_id INTEGER,
    FOREIGN KEY (catp_catp_id) REFERENCES Categoria_Produto(catp_id)
);

CREATE TABLE Fornecedor (
    forn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    forn_nome TEXT NOT NULL,
    forn_cnpj TEXT UNIQUE NOT NULL,
    forn_telefone TEXT
);

CREATE TABLE Produto_Fornecedor (
    pf_prod_id INTEGER,
    pf_forn_id INTEGER,
    PRIMARY KEY (pf_prod_id, pf_forn_id),
    FOREIGN KEY (pf_prod_id) REFERENCES Produto(prod_id),
    FOREIGN KEY (pf_forn_id) REFERENCES Fornecedor(forn_id)
);

CREATE TABLE Cliente (
    cli_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cli_nome TEXT NOT NULL,
    cli_cpf TEXT UNIQUE NOT NULL,
    cli_telefone TEXT
);

CREATE TABLE Endereco_Cliente (
    endc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    endc_rua TEXT NOT NULL,
    endc_numero TEXT NOT NULL,
    endc_bairro TEXT NOT NULL,
    endc_cidade TEXT NOT NULL,
    endc_estado TEXT NOT NULL,
    endc_cli_id INTEGER,
    FOREIGN KEY (endc_cli_id) REFERENCES Cliente(cli_id)
);

CREATE TABLE Funcionario (
    func_id INTEGER PRIMARY KEY AUTOINCREMENT,
    func_nome TEXT NOT NULL,
    func_cargo TEXT NOT NULL,
    func_salario REAL NOT NULL,
    func_data_admissao TEXT NOT NULL
);

CREATE TABLE Setor (
    setor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setor_nome TEXT NOT NULL
);

CREATE TABLE Funcionario_Setor (
    fs_func_id INTEGER,
    fs_setor_id INTEGER,
    fs_data_inicio TEXT NOT NULL,
    fs_data_fim TEXT,
    PRIMARY KEY (fs_func_id, fs_setor_id, fs_data_inicio),
    FOREIGN KEY (fs_func_id) REFERENCES Funcionario(func_id),
    FOREIGN KEY (fs_setor_id) REFERENCES Setor(setor_id)
);

CREATE TABLE Venda (
    venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_data TEXT NOT NULL,
    venda_valor_total REAL NOT NULL,
    venda_cli_id INTEGER,
    venda_func_id INTEGER,
    FOREIGN KEY (venda_cli_id) REFERENCES Cliente(cli_id),
    FOREIGN KEY (venda_func_id) REFERENCES Funcionario(func_id)
);

CREATE TABLE Item_Venda (
    itemv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    itemv_qtd INTEGER NOT NULL,
    itemv_preco_unit REAL NOT NULL,
    itemv_venda_id INTEGER,
    itemv_prod_id INTEGER,
    FOREIGN KEY (itemv_venda_id) REFERENCES Venda(venda_id),
    FOREIGN KEY (itemv_prod_id) REFERENCES Produto(prod_id)
);

CREATE TABLE Compra (
    comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comp_data TEXT NOT NULL,
    comp_valor_total REAL NOT NULL,
    comp_forn_id INTEGER,
    comp_func_id INTEGER,
    FOREIGN KEY (comp_forn_id) REFERENCES Fornecedor(forn_id),
    FOREIGN KEY (comp_func_id) REFERENCES Funcionario(func_id)
);

CREATE TABLE Item_Compra (
    itemc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    itemc_qtd INTEGER NOT NULL,
    itemc_preco_unit REAL NOT NULL,
    itemc_comp_id INTEGER,
    itemc_prod_id INTEGER,
    FOREIGN KEY (itemc_comp_id) REFERENCES Compra(comp_id),
    FOREIGN KEY (itemc_prod_id) REFERENCES Produto(prod_id)
);

CREATE TABLE Pagamento (
    pag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pag_metodo TEXT NOT NULL,
    pag_valor REAL NOT NULL,
    pag_data TEXT NOT NULL,
    pag_venda_id INTEGER,
    FOREIGN KEY (pag_venda_id) REFERENCES Venda(venda_id)
);

CREATE TABLE Promocao (
    promo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    promo_percentual REAL NOT NULL,
    promo_inicio TEXT NOT NULL,
    promo_fim TEXT NOT NULL,
    promo_prod_id INTEGER,
    FOREIGN KEY (promo_prod_id) REFERENCES Produto(prod_id)
);
