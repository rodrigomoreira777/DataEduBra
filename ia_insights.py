import openai
import pandas as pd


""" Esse script tem como objetivo solicitar insights automaticos utilizando prompts automaticos para o 
Chat GPT em seu modelo gpt-4. Esse código utliza funções para apresentar uma visão geral para o modelo
e fornece-las no prompt"""


def gerar_resumo_por_categoria(df, categoria):
    """
    Gera um resumo agregado dos dados para uma categoria específica.
    """
    resumo = df.groupby(['Categoria', 'Valor_Categoria', 'Faixa_IDEB']).agg(
        QtdEscolas=('QtdEscolas', 'sum'),
        QtdEscolasInternet=('QtdEscolasInternet', 'sum')
    ).reset_index()

    # Calcular o percentual
    resumo['Pct_Internet'] = (resumo['QtdEscolasInternet'] / resumo['QtdEscolas']) * 100

    # Filtrar para a categoria específica
    resumo_categoria = resumo[resumo['Categoria'] == categoria]

    return resumo_categoria


def obter_insights(prompt, model="gpt-4", max_tokens=500):
    """
    Envia o prompt para a API da OpenAI e retorna a resposta gerada pelo ChatGPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um analista de dados especializado em educação."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Erro ao obter insights: {e}"


def formatar_prompt(resumo, categoria):
    """
    Formata o prompt a ser enviado para o ChatGPT, e inclui explicações das colunas para ajudar na interpretação.
    """
    # Descrição das colunas
    descricao_colunas = """
    - **Categoria**: Tipo da categoria de agregação (por exemplo, UF, Regiao Br, Localidade, Tipo de ADM).
    - **Valor_Categoria**: Valor específico da categoria (por exemplo, 'SP' para UF, 'Norte' para Regiao Br).
    - **ano**: Ano de referência dos dados.
    - **Faixa_IDEB**: Faixa de valores IDEB (Índice de Desenvolvimento da Educação Básica separado em cortes de valor).
    - **QtdEscolas**: Quantidade de escolas na faixa de IDEB para o periodo.
    - **QtdEscolasInternet**: Quantidade de escolas que utilizam internet em seus processos de ensino.
    - **Pct_Internet**: Percentual de escolas que utilizam internet em seus processos de ensino.
    """

    # Formatar o resumo em uma tabela markdown
    tabela = resumo.to_markdown(index=False)

    # Construir o prompt completo
    prompt = f"""
    Aqui estão os dados agregados para a categoria **{categoria}**:

    **Descrição das Colunas:**
    {descricao_colunas}

    **Dados Agregados:**
    {tabela}

    Com base nesses dados, por favor:
    1. Resuma os principais insights.
    2. Identifique possíveis padrões ou tendências.
    3. Sugira melhorias ou ações que podem ser tomadas para melhorar o IDEB nas diferentes faixas.
    """
    return prompt


# Definindo minha chave de api
openai.api_key = 'minha chave' # Obs: não compatilharei essa chave.

# Carregando a tabela 'ideb_merged_macro.xlsx' para solicitar insights.
try:
    df_macro = pd.read_excel('ideb_merged_macro.xlsx')
    print("Tabela 'ideb_merged_macro.xlsx' carregada com sucesso.")
except FileNotFoundError:
    print("Erro: O arquivo 'ideb_merged_macro.xlsx' não foi encontrado no diretório especificado.")
    exit()

# Definir as categorias disponíveis
categorias = df_macro['Categoria'].unique()

# Inicializar um dicionário para armazenar os insights
insights = {}

for categoria in categorias:
    print(f"\nProcessando a categoria: {categoria}")
    resumo_categoria = gerar_resumo_por_categoria(df_macro, categoria)

    # Verificar se há dados para a categoria
    if resumo_categoria.empty:
        print(f"Nenhum dado encontrado para a categoria '{categoria}'. Pulando para a próxima.")
        continue

    prompt = formatar_prompt(resumo_categoria, categoria)
    resposta = obter_insights(prompt)

    insights[categoria] = resposta
    print(f"Insights para '{categoria}' obtidos.\n")

# Exibir os insights
for categoria, texto in insights.items():
    print(f"===== Insights para {categoria} =====")
    print(texto)
    print("\n")

# Salvar os insights em um arquivo de texto:
try:
    with open('insights_ideb_merged_macro.txt', 'w', encoding='utf-8') as f:
        for categoria, texto in insights.items():
            f.write(f"===== Insights para {categoria} =====\n")
            f.write(f"{texto}\n\n")
    print("Os insights foram salvos no arquivo 'insights_ideb_merged_macro.txt'.")
except Exception as e:
    print(f"Erro ao salvar os insights: {e}")
