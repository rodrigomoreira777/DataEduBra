import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


"""Acima são importadas as bibliotecas necessarias para criação de um dashboard com os dados obtidos.
A intenção foi carregar os dados de um planilha para não precisar executar o processo de busca mais de uma vez.
Dessa forma, o processo de gerar as visualizações se torna mais rapido.
"""

# Explicitando o caminho do arquivo e carregando do DataFrame pandas.
file_path = "data/ideb_merged_macro.xlsx"
data = pd.read_excel(file_path)

# Normalizando os nomes das categorias para evitar problemas com caracteres especiais.
data["Categoria"] = data["Categoria"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")

# Garantir que os anos sejam inteiros e remover valores não numéricos
data["ano"] = pd.to_numeric(data["ano"], errors="coerce")
data = data.dropna(subset=["ano"])
data["ano"] = data["ano"].astype(int)

# Configurar a página do Streamlit
st.set_page_config(layout="wide")
st.title("Dashboard de Análise do IDEB e Uso de Internet")

# Aplicando barra de filtros
st.sidebar.header("Filtros")

# Filtros interativos
ufs = st.sidebar.multiselect(
    "Selecione as UFs:",
    options=data[data["Categoria"] == "UF"]["Valor_Categoria"].unique(),
    default=data[data["Categoria"] == "UF"]["Valor_Categoria"].unique()
)

regioes = st.sidebar.multiselect(
    "Selecione as Regiões:",
    options=data[data["Categoria"] == "Regiao Br"]["Valor_Categoria"].unique(),
    default=data[data["Categoria"] == "Regiao Br"]["Valor_Categoria"].unique()
)

tipos_adm = st.sidebar.multiselect(
    "Selecione os Tipos de ADM:",
    options=data[data["Categoria"] == "Tipo de ADM"]["Valor_Categoria"].unique(),
    default=data[data["Categoria"] == "Tipo de ADM"]["Valor_Categoria"].unique()
)

localidades = st.sidebar.multiselect(
    "Selecione as Localidades:",
    options=data[data["Categoria"] == "Localidade"]["Valor_Categoria"].unique(),
    default=data[data["Categoria"] == "Localidade"]["Valor_Categoria"].unique()
)

# Filtrar os dados com base nos valores selecionados
data_filtrada = data[
    (data["Categoria"] == "UF") & (data["Valor_Categoria"].isin(ufs)) |
    (data["Categoria"] == "Regiao Br") & (data["Valor_Categoria"].isin(regioes)) |
    (data["Categoria"] == "Tipo de ADM") & (data["Valor_Categoria"].isin(tipos_adm)) |
    (data["Categoria"] == "Localidade") & (data["Valor_Categoria"].isin(localidades))
]

# Filtrar anos presentes na série temporal
data_filtrada = data_filtrada[data_filtrada["ano"].isin(data["ano"].unique())]

# Agrupar os dados por "ano" e "Faixa_IDEB" para acumular os valores
agrupados = data_filtrada.groupby(["ano", "Faixa_IDEB"]).agg({
    "QtdEscolas": "sum",
    "Pct_Internet": "mean"  # Percentual médio
}).reset_index()

# Criar os gráficos por faixa de IDEB
faixas_ideb = agrupados["Faixa_IDEB"].unique()
fig, axs = plt.subplots(len(faixas_ideb), 1, figsize=(12, 4 * len(faixas_ideb)), sharex=True)

if len(faixas_ideb) == 1:
    axs = [axs]  # Garantir que seja iterável quando há apenas uma faixa

for ax, faixa in zip(axs, faixas_ideb):
    dados_faixa = agrupados[agrupados["Faixa_IDEB"] == faixa]

    # Garantir que os anos aparecem apenas se presentes nos dados
    anos_presentes = sorted(dados_faixa["ano"].unique())

    # Gráfico de barras para QtdEscolas acumulado
    bars = ax.bar(
        dados_faixa["ano"],
        dados_faixa["QtdEscolas"],
        color="skyblue",
        label="Qtd. Escolas",
        alpha=0.7
    )

    # Adicionar valores acima das barras
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # Centro da barra
            bar.get_height() + 1,  # Acima da barra
            f'{bar.get_height()}',
            ha='center', va='bottom', fontsize=8
        )

    # Gráfico de linha para Pct_Internet acumulado
    ax2 = ax.twinx()  # Segundo eixo y
    ax2.plot(
        dados_faixa["ano"],
        dados_faixa["Pct_Internet"],  # Linha sem deslocamento
        color="darkblue",
        marker="o",
        label="% Internet"
    )

    # Configurar os ticks do eixo X para exibir apenas anos específicos
    ax.set_xticks([2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023])

    # Configurar o título e as legendas
    ax.set_title(f"Faixa de IDEB: {faixa}")
    ax.set_ylabel("Qtd. Escolas")
    ax2.set_ylabel("% Internet")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

# Configurar o eixo X
axs[-1].set_xlabel("Ano")

# Ajustar o layout
plt.tight_layout()

# Exibir os gráficos
st.pyplot(fig)

# Exibir a tabela filtrada
st.write("### Dados Filtrados")
st.dataframe(data_filtrada)
