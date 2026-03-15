## Para executar: python -m app.teste_rotas.lista_classificacao_geral

import os
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from app.services.form.form_placar_rodada_service import lista_classificacao_geral, rodada_lista
from app.services.estadio_service import listar_estadios_paginadas
from app.core.database import get_db

# Configurações
SERIE = "A"
ANO = 2026
OUTPUT_HTML_FILE = "D:\\PythonMeusProjetos\\Brasileirao\\app\\teste_rotas\\classificacao_geral_serie_a_2026.html"
OUTPUT_ESTADIOS_HTML_FILE = "D:\\PythonMeusProjetos\\Brasileirao\\app\\teste_rotas\\stadios_brasileirao_2026.html"
OUTPUT_RODADA_HTML_FILE = "D:\\PythonMeusProjetos\\Brasileirao\\app\\teste_rotas\\rodadas_brasileirao_2026.html"
TEMPLATE_DIR = "D:\\PythonMeusProjetos\\Brasileirao\\app\\teste_rotas"
TEMPLATE_CLASSIFICACAO = "classificacao_template.html"
TEMPLATE_ESTADIOS = "estadios_template.html"
TEMPLATE_RODADA = "rodada_template.html"

def gerar_html_classificacao(dados_classificacao):
    """
    Gera um arquivo HTML com base nos dados de classificação geral.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_CLASSIFICACAO)
    html_content = template.render(
        serie=SERIE,
        ano=ANO,
        classificacao=dados_classificacao
    )

    with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    print(f"Página HTML de Classificação Geral gerada com sucesso em: {OUTPUT_HTML_FILE}")

def gerar_html_estadios(dados_estadios):
    """
    Gera um arquivo HTML com os estádios listados.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_ESTADIOS)
    html_content = template.render(
        ano=ANO,
        estadios=dados_estadios
    )

    with open(OUTPUT_ESTADIOS_HTML_FILE, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    print(f"Página HTML dos Estádios gerada com sucesso em: {OUTPUT_ESTADIOS_HTML_FILE}")

def gerar_html_rodada(dados_rodada):
    """
    Gera o arquivo HTML para exibir os jogos de uma rodada específica.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_RODADA)

    html_content = template.render(
        serie=dados_rodada.serie,
        ano=dados_rodada.ano,
        rodada_numero=dados_rodada.rodada,
        jogos=dados_rodada.jogos_da_rodada
    )

    output_file_path = os.path.join(
        TEMPLATE_DIR,
        f"rodada_brasileirao_{dados_rodada.serie.lower()}_{dados_rodada.ano}_rodada_{dados_rodada.rodada}.html"
    )
    print(f"Gerando arquivo HTML da Rodada em: {output_file_path}")
    with open(output_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    print(f"Página HTML da Rodada gerada com sucesso em: {output_file_path}")

def menu_principal():
    """
    Exibe o menu principal de opções no terminal e processa as escolhas.
    """
    while True:
        print("\nMenu do Brasileirão 2026")
        print("1. CG - Classificação Geral")
        print("2. ES - Estádios")
        print("3. RO - Lista Rodada")
        print("4. S - Sair")
        opcao = input("Escolha uma opção: ").strip().upper()

        if opcao == "CG":
            listar_classificacao_geral()
        elif opcao == "ES":
            listar_estadios()
        elif opcao == "RO":
            listar_rodada()
        elif opcao == "S":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def listar_classificacao_geral():
    """
    Recupera a classificação geral da base de dados e gera um HTML.
    """
    session: Session = next(get_db())
    try:
        dados_classificacao = lista_classificacao_geral(session, SERIE, ANO)
        gerar_html_classificacao(dados_classificacao)
    except Exception as e:
        print(f"Erro ao listar Classificação Geral: {e}")
    finally:
        session.close()

def listar_estadios():
    """
    Recupera a lista de estádios da base de dados e gera um HTML.
    """
    session: Session = next(get_db())
    try:
        nome_estadio = input("Digite o nome do estádio (ou deixe vazio para listar todos): ").strip()
        pagina = int(input("Digite o número da página: ").strip())
        tamanho_pagina = int(input("Digite o tamanho da página: ").strip())

        resultado = listar_estadios_paginadas(nome_estadio, pagina, tamanho_pagina, session)
        gerar_html_estadios(resultado.estadios)
    except Exception as e:
        print(f"Erro ao listar Estádios: {e}")
    finally:
        session.close()

def listar_rodada():
    """
    Recupera a rodada da base de dados e gera um HTML com os jogos correspondentes.
    """
    session: Session = next(get_db())
    try:
        serie = input(f"Digite a série ( {ANO}): ").upper().strip()
        rodada_numero = int(input(f"Digite o número da rodada ({serie} - {ANO}): ").strip())
        dados_rodada = rodada_lista(session, serie, ANO, rodada_numero, False)

        gerar_html_rodada(dados_rodada)
    except Exception as e:
        print(f"Erro ao listar Rodada: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    menu_principal()