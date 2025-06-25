###### DIGITE NO TERMINAL: streamlit run dinamica4.py ########



import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tabela e Gráfico Dinâmico", layout="wide")

st.title("📊 Tabela Dinâmica com Gráfico Interativo (Excel + Streamlit) - by: Valter Gomes")

# Upload do Excel
arquivo = st.file_uploader("📂 Carregue seu arquivo Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.subheader("📄 Dados da Planilha:")
    st.dataframe(df)

    # ----------------------
    # 🔸 TABELA DINÂMICA
    # ----------------------
    st.markdown("---")
    st.header("🧮 Tabela Dinâmica")

    col_linhas = st.selectbox("🔠 Coluna para Linhas:", df.columns, key="linhas")
    col_colunas = st.selectbox("🔠 Coluna para Colunas:", df.columns, key="colunas")
    col_valores = st.selectbox("🔢 Coluna de Valores:", df.columns, key="valores")
    operacao_tabela = st.selectbox("⚙️ Operação (Tabela):", ['sum', 'mean', 'count', 'min', 'max'], key="operacao_tabela")

    tabela = pd.pivot_table(
        df,
        index=col_linhas,
        columns=col_colunas,
        values=col_valores,
        aggfunc=operacao_tabela,
        fill_value=0
    )

    st.subheader("📋 Resultado:")
    st.dataframe(tabela)

    # ----------------------
    # 🔸 GRÁFICO DINÂMICO
    # ----------------------
    st.markdown("---")
    st.header("📈 Gráfico Dinâmico")

    # Coluna de data e filtro de período (somente para o gráfico)
    col_data = st.selectbox("📅 Escolha a coluna de Data (somente para o gráfico):", df.columns)

    try:
        df[col_data] = pd.to_datetime(df[col_data])
    except:
        st.error("❌ A coluna selecionada não contém datas válidas.")
        st.stop()

    data_inicio, data_fim = st.date_input(
        "📆 Selecione o período:",
        value=(df[col_data].min(), df[col_data].max()),
        min_value=df[col_data].min(),
        max_value=df[col_data].max()
    )

    df_periodo = df[(df[col_data] >= pd.to_datetime(data_inicio)) & (df[col_data] <= pd.to_datetime(data_fim))]

    # Campos do gráfico
    tipo_grafico = st.selectbox("📊 Tipo de gráfico:", ["Barra", "Linha", "Pizza"])
    categoria = st.selectbox("🧩 Categoria (eixo X):", df.columns, key="categoria")
    valor = st.selectbox("💰 Valor (eixo Y):", df.select_dtypes(include='number').columns, key="valor")
    operacao_grafico = st.selectbox("⚙️ Operação (Gráfico):", ['sum', 'mean', 'count', 'min', 'max'], key="operacao_grafico")
    top_n = st.number_input("🔢 Quantidade de itens no eixo X (Top N):", min_value=1, max_value=100, value=5)

    # Agrupamento e cálculo conforme operação selecionada
    if operacao_grafico == "sum":
        dados_agrupados = df_periodo.groupby(categoria)[valor].sum().reset_index()
    elif operacao_grafico == "mean":
        dados_agrupados = df_periodo.groupby(categoria)[valor].mean().reset_index()
    elif operacao_grafico == "count":
        dados_agrupados = df_periodo.groupby(categoria)[valor].count().reset_index()
    elif operacao_grafico == "min":
        dados_agrupados = df_periodo.groupby(categoria)[valor].min().reset_index()
    elif operacao_grafico == "max":
        dados_agrupados = df_periodo.groupby(categoria)[valor].max().reset_index()

    dados_agrupados = dados_agrupados.sort_values(by=valor, ascending=False).head(top_n)

    # Geração do gráfico
    titulo = f"{tipo_grafico} - {operacao_grafico} de {valor} por {categoria} (Top {top_n})"
    subtitulo = f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"

    if tipo_grafico == "Barra":
        fig = px.bar(dados_agrupados, x=categoria, y=valor, title=f"{titulo}<br><sup>{subtitulo}</sup>")
    elif tipo_grafico == "Linha":
        fig = px.line(dados_agrupados, x=categoria, y=valor, title=f"{titulo}<br><sup>{subtitulo}</sup>")
    elif tipo_grafico == "Pizza":
        fig = px.pie(dados_agrupados, names=categoria, values=valor, title=titulo)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬆️ Por favor, carregue um arquivo Excel para começar.")
