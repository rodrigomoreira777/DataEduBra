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

