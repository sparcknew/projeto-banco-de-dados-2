-- ==========================================
-- VIEWS - RELATÓRIOS GERENCIAIS
-- ==========================================

-- VIEW 1: Vendas Mensais (Evolução de Faturamento)
CREATE VIEW IF NOT EXISTS view_vendas_mensais AS
SELECT 
    strftime('%Y-%m', venda_data) AS mes,
    COUNT(venda_id) AS total_vendas,
    SUM(venda_valor_total) AS faturamento_total,
    AVG(venda_valor_total) AS ticket_medio
FROM Venda
GROUP BY strftime('%Y-%m', venda_data)
ORDER BY mes;

-- VIEW 2: Top 15 Produtos Mais Vendidos
CREATE VIEW IF NOT EXISTS view_top_produtos AS
SELECT 
    p.prod_nome,
    c.catp_nome AS categoria,
    SUM(iv.itemv_qtd) AS qtd_vendida,
    SUM(iv.itemv_qtd * iv.itemv_preco_unit) AS faturamento,
    ROUND(AVG(iv.itemv_preco_unit), 2) AS preco_medio_venda
FROM Item_Venda iv
JOIN Produto p ON iv.itemv_prod_id = p.prod_id
JOIN Categoria_Produto c ON p.catp_catp_id = c.catp_id
GROUP BY p.prod_id
ORDER BY qtd_vendida DESC
LIMIT 15;

-- VIEW 3: Estoque Crítico (abaixo de 20 unidades)
CREATE VIEW IF NOT EXISTS view_estoque_critico AS
SELECT 
    p.prod_id,
    p.prod_nome,
    c.catp_nome AS categoria,
    p.prod_qtd_estoque,
    f.forn_nome AS fornecedor_principal
FROM Produto p
JOIN Categoria_Produto c ON p.catp_catp_id = c.catp_id
LEFT JOIN Produto_Fornecedor pf ON p.prod_id = pf.pf_prod_id
LEFT JOIN Fornecedor f ON pf.pf_forn_id = f.forn_id
WHERE p.prod_qtd_estoque < 20
ORDER BY p.prod_qtd_estoque ASC;

-- VIEW 4: Desempenho dos Funcionários (Vendas)
CREATE VIEW IF NOT EXISTS view_desempenho_funcionarios AS
SELECT 
    f.func_id,
    f.func_nome,
    f.func_cargo,
    s.setor_nome,
    COUNT(v.venda_id) AS vendas_realizadas,
    SUM(v.venda_valor_total) AS total_vendido,
    ROUND(AVG(v.venda_valor_total), 2) AS media_por_venda,
    strftime('%Y-%m', v.venda_data) AS mes_referencia
FROM Venda v
JOIN Funcionario f ON v.venda_func_id = f.func_id
LEFT JOIN Funcionario_Setor fs ON f.func_id = fs.fs_func_id AND fs.fs_data_fim IS NULL
LEFT JOIN Setor s ON fs.fs_setor_id = s.setor_id
GROUP BY f.func_id, strftime('%Y-%m', v.venda_data)
ORDER BY mes_referencia DESC, total_vendido DESC;

-- VIEW 5: Impacto das Promoções Ativas
CREATE VIEW IF NOT EXISTS view_promocoes_impacto AS
SELECT 
    pr.promo_id,
    pr.promo_percentual,
    p.prod_nome,
    pr.promo_inicio,
    COALESCE(pr.promo_fim, 'Ativa') AS promo_fim,
    COUNT(iv.itemv_venda_id) AS vendas_durante_promocao,
    SUM(iv.itemv_qtd) AS qtd_vendida_promo,
    SUM(iv.itemv_qtd * iv.itemv_preco_unit) AS faturamento_promo,
    ROUND(
        SUM(iv.itemv_qtd * iv.itemv_preco_unit) / 
        NULLIF(SUM(iv.itemv_qtd), 0), 2
    ) AS preco_medio_promo
FROM Promocao pr
JOIN Produto p ON pr.promo_prod_id = p.prod_id
JOIN Item_Venda iv ON iv.itemv_prod_id = p.prod_id
JOIN Venda v ON iv.itemv_venda_id = v.venda_id
WHERE v.venda_data BETWEEN pr.promo_inicio 
       AND COALESCE(pr.promo_fim, date('now', '+1 day'))
GROUP BY pr.promo_id
ORDER BY faturamento_promo DESC;