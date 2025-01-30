import os
import subprocess


"""1) Acima são importadas as bibliotecas necessarias para controlar o fluxo de código. O objetivo desse código
é controlar o fluxo de execução dos scripts já existentes."""


def executar_script(nome_script):
    """
    Função para tratar erros e executar um código pyhon.
    """
    try:
        subprocess.run(['python', nome_script], check=True)
    except subprocess.CalledProcessError:
        print(f"Erro: O script '{nome_script}' não pode ser executado.\n")
    except FileNotFoundError:
        print(f"Erro: O script '{nome_script}' não foi encontrado.\n")
    except Exception as e:
        print(f"Erro inesperado ao executar '{nome_script}': {e}\n")


def perguntar_insights():
    """
    Pergunta se usuário deseja gerar insights usando IA.
    A função tambem trata as respostas
    """
    resposta = input("Deseja utilizar recursos de IA para criar insights automaticamente? (sim/não): ")
    if resposta.strip().lower() == 'sim':
        executar_script('ia_insights.py')
    else:
        print("Os insights usando IA não serão gerados agora.\n")


def main():
    # Definindo o caminho para o arquivo 'ideb_merged_macro.xlsx' na pasta 'data/'
    caminho_arquivo = os.path.join('data', 'ideb_merged_macro.xlsx')

    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print("Arquivo 'ideb_merged_macro.xlsx' não encontrado. Iniciando processo de salvamento de dados.\n")
        executar_script('save_data.py')
    else:
        print("Arquivo 'ideb_merged_macro.xlsx' encontrado. Pulando a visualização.\n")

    # Executar o dashboard após garantir que o arquivo necessário está presente
    executar_script('dashboard.py')

    # Perguntar sobre geração de insights usando IA
    perguntar_insights()


if __name__ == "__main__":
    main()
