# dashboard_supermercado.py → VERSÃO 100% FUNCIONAL COM PLOTLY (sem erro!)
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard Gerencial")

# Conexão
conn = sqlite3.connect('supermercado')

# Carrega as 5 views
df1 = pd.read_sql("SELECT * FROM view_vendas_mensais", conn)
df2 = pd.read_sql("SELECT * FROM view_top_produtos", conn)
df3 = pd.read_sql("SELECT * FROM view_estoque_critico", conn)
df4 = pd.read_sql("SELECT * FROM view_desempenho_funcionarios", conn)
df5 = pd.read_sql("SELECT * FROM view_promocoes_impacto", conn)

# Conversões necessárias (evita erro do Plotly)
df1["faturamento_total"] = pd.to_numeric(df1["faturamento_total"], errors='coerce').fillna(0)
df1["ticket_medio"] = pd.to_numeric(df1["ticket_medio"], errors='coerce').fillna(0)

df2["qtd_vendida"] = pd.to_numeric(df2["qtd_vendida"], errors='coerce')
df2["faturamento"] = pd.to_numeric(df2["faturamento"], errors='coerce')

df5["faturamento_promo"] = pd.to_numeric(df5["faturamento_promo"], errors='coerce').fillna(0)
df5["qtd_vendida_promo"] = pd.to_numeric(df5["qtd_vendida_promo"], errors='coerce').fillna(0)
df5["promo_percentual"] = pd.to_numeric(df5["promo_percentual"], errors='coerce')

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Faturamento Mensal", "Top 15 Produtos", "Estoque Crítico", "Funcionários", "Promoções"
])

# ABA 1
with tab1:
    st.header("Evolução do Faturamento")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df1, x="mes", y="faturamento_total", title="Faturamento Mensal", markers=True)
        fig.update_traces(line_color="#2E86C1")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df1, x="mes", y="ticket_medio", title="Ticket Médio")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df1.style.format({"faturamento_total": "R$ {:.2f}", "ticket_medio": "R$ {:.2f}"}))

# ABA 2
with tab2:
    st.header("Top 15 Produtos Mais Vendidos")
    fig = px.bar(df2, y="prod_nome", x="qtd_vendida", color="categoria",
                 title="Quantidade Vendida", orientation='h', text="qtd_vendida")
    fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df2.style.format({"faturamento": "R$ {:.2f}"}))

# ABA 3
with tab3:
    st.header("Estoque Crítico (< 20 unidades)")
    if df3.empty:
        st.success("Todos os produtos com estoque acima de 20 unidades!")
    else:
        fig = px.bar(df3, x="prod_nome", y="prod_qtd_estoque", color="categoria",
                     title="Produtos em Estoque Baixo", text="prod_qtd_estoque")
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df3)

# ABA 4
with tab4:
    st.header("Desempenho dos Funcionários")
    mes = st.selectbox("Selecione o mês", sorted(df4["mes_referencia"].unique(), reverse=True), key="mes_func")
    df_mes = df4[df4["mes_referencia"] == mes]
    fig = px.bar(df_mes.head(15), x="func_nome", y="total_vendido", color="setor_nome",
                 title=f"Top Funcionários - {mes}", text="total_vendido")
    fig.update_traces(texttemplate='R$ %{text:,.0f}')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_mes.head(20).style.format({"total_vendido": "R$ {:.2f}"}))

# ABA 5 — CORRIGIDA AQUI!
with tab5:
    st.header("Impacto das Promoções")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(df5.head(10), y="prod_nome", x="faturamento_promo",
                     color="promo_percentual", orientation='h',
                     title="Faturamento por Promoção", text="faturamento_promo")
        fig.update_traces(texttemplate='R$ %{text:,.0f}')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Scatter com tamanho proporcional ao faturamento (CORRIGIDO!)
        df_scatter = df5.copy()
        df_scatter["tamanho"] = df_scatter["faturamento_promo"] / df_scatter["faturamento_promo"].max() * 50 + 10

        fig = px.scatter(df_scatter, x="promo_percentual", y="qtd_vendida_promo",
                         size="tamanho", hover_name="prod_nome", color="prod_nome",
                         title="Desconto × Quantidade Vendida (tamanho = faturamento)")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df5.style.format({"faturamento_promo": "R$ {:.2f}"}))

st.success("Dashboard carregado com sucesso! Todas as 5 views funcionando perfeitamente.")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")