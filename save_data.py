import basedosdados as bd
import pandas as pd
import os


""" Acima são importadas as bibliotecas necessarias para levantar os dados e salva-los em um arquivo. Exportar o
os dados para um arquivo é um estrategia interessante para deixar o carregamento do dashboard (gerado posterioermente)
mais rapido. Além disso, tambem me permitiu uma visão geral dos dados de trabalho"""


"""Abaixo, define-se algumas funções para faciliar a escrita fo fluxo de código"""


def ler_query(caminho_query):
    """Função basica para ler caminho do arquivo"""
    try:
        with open(caminho_query, 'r', encoding='utf-8') as file:
            query = file.read()
        print(f"Query '{caminho_query}' lida com sucesso.")
        return query
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_query}' não foi encontrado.")
        exit()
    except Exception as e:
        print(f"Erro ao ler a query '{caminho_query}': {e}")
        exit()


def categorizar_faixa_ideb(ideb):
    """Função basica para determinar o categoria de um ideb"""
    if 0.0 <= ideb < 2.5:
        return "0.0 <= IDEB < 2.5"
    elif 2.5 <= ideb < 5.0:
        return "2.5 <= IDEB < 5.0"
    elif 5.0 <= ideb < 7.5:
        return "5.0 <= IDEB < 7.5"
    elif 7.5 <= ideb <= 10.0:
        return "7.5 <= IDEB <= 10.0"
    else:
        return "Faixa Desconhecida"


# Especificando meu billing_id
billing_id = "dataedu-449122"

# Abaixo, define-se os caminhos e o diretorio das queries usadas
caminho_query_censo = os.path.join("queries", "censo_query.sql")
caminho_query_ideb = os.path.join("queries", "ideb_query.sql")

# Aplica-se função definida anteriormente para ler as queries
query_censo = ler_query(caminho_query_censo)
query_ideb = ler_query(caminho_query_ideb)

# Executando a query "censo_query.sql" que pesquisa valores da base de dados de Censo Escolar
df_censo = bd.read_sql(query=query_censo, billing_project_id=billing_id)
print("Query do Censo Escolar concluída. Número de registros:", len(df_censo))

# Executando a query "ideb_query.sql" que pesquisa valores da base de dados de IDEB por escola
df_ideb = bd.read_sql(query=query_ideb, billing_project_id=billing_id)
print("Query do IDEB concluída. Número de registros:", len(df_ideb))

"""Para esse projeto, utiliza-se combinações das duas tabelas. Dessa forma, utilizou-se como chave a combinação
das colunas "ano" e "ide_escola" para combinar dados de aplicação de recursos de internet na aprendizagem
(provenientes da base de dados do Censo Escolar) com o desempenho da respectiva escola no IDEB"""
ideb_merged = pd.merge(
    df_ideb,
    df_censo[['ano', 'id_escola', 'tipo_localizacao', 'internet_aprendizagem', 'rede']],
    on=['ano', 'id_escola'],
    how='left',
    suffixes=('_ideb', '_censo')  # Para diferenciar as colunas 'rede' de cada tabela
)
print("Merge concluído. Número de registros após o merge:", len(ideb_merged))

# Tratando as colunas duplicadas de "rede"
# RemoveNDO a coluna "rede_ideb" e renomear "rede_censo" para "rede"
if 'rede_ideb' in ideb_merged.columns:
    ideb_merged.drop(columns=['rede_ideb'], inplace=True)
if 'rede_censo' in ideb_merged.columns:
    ideb_merged.rename(columns={'rede_censo': 'rede'}, inplace=True)

# Para tratar colunar com valores vazios em "internet_aprendizagem" da tabela de Censo Escola, optou-se por atribuir 0.
ideb_merged['internet_aprendizagem'] = ideb_merged['internet_aprendizagem'].fillna(0)

# Criando a coluna 'Faixa_IDEB para permitir que se possa analisar os dados de maneira mais macro
ideb_merged['Faixa_IDEB'] = ideb_merged['ideb'].apply(categorizar_faixa_ideb)

# Para possibilitar analises mais pontuais, vamos dividir as colunas "sigla_uf" em diferentes regioes do Brasil
regiao_map = {
    # Norte
    'AC': 'Norte',
    'AP': 'Norte',
    'AM': 'Norte',
    'PA': 'Norte',
    'RO': 'Norte',
    'RR': 'Norte',
    'TO': 'Norte',
    # Nordeste
    'AL': 'Nordeste',
    'BA': 'Nordeste',
    'CE': 'Nordeste',
    'MA': 'Nordeste',
    'PB': 'Nordeste',
    'PE': 'Nordeste',
    'PI': 'Nordeste',
    'RN': 'Nordeste',
    'SE': 'Nordeste',
    # Centro-Oeste
    'DF': 'Centro-Oeste',
    'GO': 'Centro-Oeste',
    'MT': 'Centro-Oeste',
    'MS': 'Centro-Oeste',
    # Sudeste
    'ES': 'Sudeste',
    'MG': 'Sudeste',
    'RJ': 'Sudeste',
    'SP': 'Sudeste',
    # Sul
    'PR': 'Sul',
    'RS': 'Sul',
    'SC': 'Sul'
}
ideb_merged['Regiao'] = ideb_merged['sigla_uf'].map(regiao_map)

# Verificando se existem siglas não mapeadas. Caso exista, vamos avisar o usuario.
siglas_nao_mapeadas = ideb_merged[ideb_merged['Regiao'].isnull()]['sigla_uf'].unique()
if len(siglas_nao_mapeadas) > 0:
    print("Existem siglas de UF não mapeadas para regiões:")

""" Além de regiões do BR, vamos aproveitar para classificar todas as categorias adicionais.
Isso permite segmetar ainda mais as analises."""
categorias = {
    'UF': 'sigla_uf',
    'Regiao Br': 'Regiao',
    'Localidade': 'tipo_localizacao',
    'Tipo de ADM': 'rede'
}

# Inicializando apenas de uma Lista para Armazenar os DataFrames Agregados
macro_list = []

# Iterando sobre sada categoria para agregar os dados
for categoria, coluna in categorias.items():
    df_temp = ideb_merged.groupby(['ano', 'Faixa_IDEB', coluna]).agg(
        QtdEscolas=('id_escola', 'count'),
        QtdEscolasInternet=('internet_aprendizagem', 'sum')
    ).reset_index()

    """ Como a quantidade absoluta de escolas é diferente em cada região, vamos utilizar o percentual de escolas que
     utilizam internet como recurso de aprendizagem para normalizar os dados"""
    df_temp['Pct_Internet'] = (df_temp['QtdEscolasInternet'] / df_temp['QtdEscolas']) * 100

    # Adicinando as Colunas 'Categoria' e 'Valor_Categoria'. Isso facilitará na criação de filtros do dashboard.
    df_temp['Categoria'] = categoria
    df_temp.rename(columns={coluna: 'Valor_Categoria'}, inplace=True)

    # Reordenando colunas
    df_temp = df_temp[
        ['Categoria', 'Valor_Categoria', 'ano', 'Faixa_IDEB', 'QtdEscolas', 'QtdEscolasInternet', 'Pct_Internet']]

    # Adicionando lista
    macro_list.append(df_temp)

# Concatenando todos os DataFrames agregados
ideb_merged_macro = pd.concat(macro_list, ignore_index=True)

# Exportando DataFrame para um arquivo Excel
ideb_merged_macro.to_excel("ideb_merged_macro.xlsx", index=False)

print("Fim!")
