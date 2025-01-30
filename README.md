# Análise de Dados Educacionais - Censo Escolar

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Este repositório tem como objetivo armazenar os arquivos utilizados para a realização do **Desafio Case: Análise de Dados Educacionais - Censo Escolar**. O projeto envolve a coleta, processamento e análise de dados educacionais provenientes do Censo Escolar e do IDEB (Índice de Desenvolvimento da Educação Básica), culminando na geração de dashboards informativos e insights automatizados utilizando Inteligência Artificial.

## 📁 Estrutura do Projeto

```plaintext
DataEduBra/
│
├── save_data.py        # Script para buscar e processar os dados do Censo Escolar e IDEB
├── dashboard.py        # Script para gerar dashboards a partir dos dados processados
├── ia_insights.py      # Script para gerar insights utilizando IA (OpenAI)
├── main.py             # Script principal que controla a execução dos demais scripts
├── queries/
│   ├── censo_query.sql  # Query SQL para obter dados do Censo Escolar
│   └── ideb_query.sql   # Query SQL para obter dados do IDEB
├── data/
│   └── ideb_merged_macro.xlsx  # Arquivo de dados processados e agregados
├── requirements.txt    # Lista de dependências do projeto
├── README.md           # Este arquivo de documentação
└── .gitignore          # Arquivo para ignorar arquivos e pastas no Git
🛠️ Pré-requisitos
Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

Python 3.8 ou superior
pip (gerenciador de pacotes do Python)
📦 Instalação
Clone este repositório:

bash
Copiar
git clone <URL_DO_REPOSITÓRIO>
cd ideb_project
Instale as dependências necessárias:

bash
Copiar
pip install -r requirements.txt
📂 Organização das Pastas
queries/: Contém os arquivos SQL utilizados para buscar os dados do Censo Escolar e IDEB.

censo_query.sql: Query para obter dados do Censo Escolar.
ideb_query.sql: Query para obter dados do IDEB.
data/: Diretório onde os dados processados e agregados serão armazenados.

ideb_merged_macro.xlsx: Arquivo resultante da junção e agregação dos dados do Censo Escolar e IDEB.
📝 Descrição dos Scripts
1. save_data.py
Este script é responsável por:

Ler as queries SQL armazenadas na pasta queries/.
Executar as queries utilizando a biblioteca basedosdados.
Processar os dados obtidos, realizando merges e transformações necessárias.
Gerar o arquivo ideb_merged_macro.xlsx na pasta data/.
Como Executar:

bash
Copiar
python save_data.py
2. dashboard.py
Este script gera dashboards informativos a partir dos dados processados em ideb_merged_macro.xlsx.

Funcionalidades:

Criação de gráficos e visualizações para análise dos dados.
Salva os gráficos na pasta data/ para fácil acesso e visualização.
Como Executar:

bash
Copiar
python dashboard.py
3. ia_insights.py
Este script utiliza a API do OpenAI para gerar insights automatizados a partir dos dados processados.

Funcionalidades:

Análise dos dados agregados.
Geração de resumos, identificação de padrões e sugestões de melhorias utilizando Inteligência Artificial.
Como Executar:

bash
Copiar
python ia_insights.py
4. main.py
Este é o script principal que controla a execução dos demais scripts de forma automatizada.

Fluxo de Execução:

Verificação do Arquivo ideb_merged_macro.xlsx:

Se não existir: Executa save_data.py para gerar o arquivo.
Se existir: Pula a execução de save_data.py.
Execução do Dashboard:

Executa dashboard.py para criar o dashboard a partir dos dados.
Geração de Insights com IA:

Após a criação do dashboard, pergunta ao usuário se deseja gerar insights utilizando IA.
Se a resposta for "sim" (em qualquer combinação de maiúsculas/minúsculas): Executa ia_insights.py.
Caso contrário: Informa que os insights não serão gerados no momento.
Como Executar:

bash
Copiar
python main.py
📋 Instruções de Uso
Executar o Processo Completo:

O script main.py gerencia todo o fluxo de execução. Ao rodá-lo, ele verificará se os dados já foram processados e, caso contrário, executará os scripts necessários para gerar os dados, criar o dashboard e, opcionalmente, gerar insights utilizando IA.

bash
Copiar
python main.py
Gerar Insights Manualmente:

Caso deseje gerar insights utilizando IA de forma independente, você pode executar diretamente o script ia_insights.py:

bash
Copiar
python ia_insights.py
🔧 Configurações Adicionais
Configuração da API do OpenAI:

Para utilizar os recursos de IA, certifique-se de ter uma chave de API válida do OpenAI. Insira sua chave diretamente no script ia_insights.py ou configure-a como uma variável de ambiente para maior segurança.

Atualização das Queries:

As queries SQL estão armazenadas na pasta queries/. Para modificar ou atualizar as consultas, edite os arquivos censo_query.sql e ideb_query.sql conforme necessário.

📄 Licença
Este projeto está licenciado sob os termos da licença MIT.
