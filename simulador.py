import numpy_financial as npf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ===== Funções =====
def gerar_tabela(VP, taxa, max_parcelas):
    dados = []
    for n in range(1, max_parcelas + 1):
        pmt = npf.pmt(taxa, n, -VP)
        total_pago = pmt * n
        dados.append({
            "Parcelas": n,
            "Valor Parcela": f"R$ {pmt:,.2f}",
            "Total Pago": f"R$ {total_pago:,.2f}"
        })
    return pd.DataFrame(dados)

# ===== Interface =====
st.set_page_config(page_title="Simulador de Parcelas", page_icon="🌱", layout="centered")

st.title("RED Rural 🌱")
st.markdown("Simule crédito com taxas flexíveis e possibilidade de entrada.")

# Entradas do usuário
valor_total = st.number_input("Valor Total (R$)", min_value=0.0, value=100_000.0, step=1000.0)
entrada = st.number_input("Valor de Entrada (R$)", min_value=0.0, max_value=valor_total, value=0.0, step=500.0)
taxa_mensal = st.number_input("Taxa mensal (%)", min_value=0.0, value=2.5, step=0.1) / 100

# Valor presente financiado após entrada
VP = valor_total - entrada

# Conversões de taxas equivalentes
taxa_trimestral = (1 + taxa_mensal) ** 3 - 1
taxa_semestral = (1 + taxa_mensal) ** 6 - 1

# Geração das tabelas
tabela_mensal = gerar_tabela(VP, taxa_mensal, 36)
tabela_trimestral = gerar_tabela(VP, taxa_trimestral, 12)
tabela_semestral = gerar_tabela(VP, taxa_semestral, 6)

# Exibição das taxas equivalentes com 2 casas decimais
st.subheader("📊 Taxas Equivalentes")

tabela_markdown = """
| Periodicidade | Taxa (%) |
|---------------|----------|
| Mensal        | {:.2f}%  |
| Trimestral    | {:.2f}%  |
| Semestral     | {:.2f}%  |
""".format(taxa_mensal*100, taxa_trimestral*100, taxa_semestral*100)

st.markdown(tabela_markdown)

# Valor financiado
st.info(f"💵 Valor financiado após entrada: R$ {VP:,.2f}")

# Gráfico comparativo
st.subheader("📈 Comparativo do valor das parcelas")

# Converter valores das parcelas para float
parcelas_mensal = tabela_mensal["Valor Parcela"].str.replace("R\$|,", "", regex=True).astype(float)
parcelas_trimestral = tabela_trimestral["Valor Parcela"].str.replace("R\$|,", "", regex=True).astype(float)
parcelas_semestral = tabela_semestral["Valor Parcela"].str.replace("R\$|,", "", regex=True).astype(float)

# Total pago acumulado correto
total_acumulado_mensal = parcelas_mensal * tabela_mensal["Parcelas"]
total_acumulado_trimestral = parcelas_trimestral * tabela_trimestral["Parcelas"]
total_acumulado_semestral = parcelas_semestral * tabela_semestral["Parcelas"]

# Criar figura
fig = go.Figure()

# Linhas das parcelas
fig.add_trace(go.Scatter(
    x=tabela_mensal["Parcelas"], y=parcelas_mensal,
    mode='lines+markers', name='Parcela Mensal'
))
fig.add_trace(go.Scatter(
    x=tabela_trimestral["Parcelas"], y=parcelas_trimestral,
    mode='lines+markers', name='Parcela Trimestral'
))
fig.add_trace(go.Scatter(
    x=tabela_semestral["Parcelas"], y=parcelas_semestral,
    mode='lines+markers', name='Parcela Semestral'
))

# Linhas do total pago
fig.add_trace(go.Scatter(
    x=tabela_mensal["Parcelas"], y=total_acumulado_mensal,
    mode='lines', name='Total Pago Mensal', line=dict(dash='dot')
))
fig.add_trace(go.Scatter(
    x=tabela_trimestral["Parcelas"], y=total_acumulado_trimestral,
    mode='lines', name='Total Pago Trimestral', line=dict(dash='dot')
))
fig.add_trace(go.Scatter(
    x=tabela_semestral["Parcelas"], y=total_acumulado_semestral,
    mode='lines', name='Total Pago Semestral', line=dict(dash='dot')
))

# Layout
fig.update_layout(
    title='Simulação de Parcelas e Total Pago',
    xaxis_title='Número de Parcelas',
    yaxis_title='Valor (R$)',
    yaxis_tickprefix='R$ ',
    template='plotly_white',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Abas para as tabelas
aba1, aba2, aba3 = st.tabs(["📅 Mensal", "📅 Trimestral", "📅 Semestral"])
with aba1:
    st.dataframe(tabela_mensal, use_container_width=True)
with aba2:
    st.dataframe(tabela_trimestral, use_container_width=True)
with aba3:
    st.dataframe(tabela_semestral, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Reduto Capital 🚀")
