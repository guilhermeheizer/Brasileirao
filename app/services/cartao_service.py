from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from fastapi import HTTPException
from app.models.cartao_models import Cartao
from app.models.clube_models import Clube
from app.services.clube_service import buscar_clube_sigla, consiste_serie, consiste_sigla
from typing import Optional, List
from bs4 import BeautifulSoup
import httpx
import certifi
import unicodedata
from app.schemas.cartao_schema import (
    CartaoClubeOut,
    CartaoSchema,
)


def listar_todos_cartoes(serie:str, ano:int, session: Session) -> List[CartaoClubeOut] | None:
    """Lista todos os cartões registrados no banco de dados.

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conexão com o banco.

    Raises:
        HTTPException: Erro: 404 - Nenhum cartão encontrado.

    Returns:
        List[CartaoClubeOut] | None: Lista de cartões registrados ou None se nenhum for encontrado.
    """
    query = session.query(
	    Cartao.__table__.c.car_serie,
		Cartao.__table__.c.car_ano,
        Cartao.__table__.c.clube_clu_sigla,
        Clube.__table__.c.clu_link_escudo.label("clube_link_escudo"),
        Clube.__table__.c.clu_nome.label("clube_nome"),
        Cartao.__table__.c.car_qtd_vermelho,
        Cartao.__table__.c.car_qtd_amarelo,
    ).join(Clube, Cartao.__table__.c.clube_clu_sigla == Clube.__table__.c.clu_sigla).filter(Cartao.__table__.c.car_ano == ano, Cartao.__table__.c.car_serie == serie.upper())

    query = query.order_by(Cartao.__table__.c.clube_clu_sigla).all()  # Ordena pela sigla do clube
  
    if not query:
        raise HTTPException(status_code=404, detail=f"Nenhum cartão encontrado para a série {serie} e ano {ano} especificados.")
    
    return [
        CartaoClubeOut(
            car_serie=cartao.car_serie,
            car_ano=cartao.car_ano,
            clube_clu_sigla=cartao.clube_clu_sigla,
            clube_link_escudo=cartao.clube_link_escudo,
            clube_nome=cartao.clube_nome,
            car_qtd_vermelho=cartao.car_qtd_vermelho,
            car_qtd_amarelo=cartao.car_qtd_amarelo
        )
        for cartao in query
    ]


def criar_cartao(dados: CartaoSchema, session: Session) -> CartaoSchema:
    """Cria um novo registro de cartão no banco.

    Args:
        dados (CartaoSchema): Dados para criação do cartão.
        session (Session): Sessão ativa do SQLAlchemy para conexão com o banco.

    Raises:
        HTTPException: Erro: 404 - Clube associado não encontrado.
        HTTPException: Erro: 404 - Cartão já existente.
        HTTPException: Erro: 404 - Clube com sigla '{clube_sigla}' já existe.

    Returns:
        CartaoSchema: Representação do cartão criado.
    """
    consiste_serie(dados.car_serie.upper())
    consiste_sigla(dados.clube_clu_sigla.upper())

    if not buscar_clube_sigla(False, dados.clube_clu_sigla.upper(), session):
        raise HTTPException(status_code=404, detail=f"Clube com sigla '{dados.clube_clu_sigla}' não encontrado.")

    # Verifica se o clube existe
    clube = session.query(Clube).filter(Clube.__table__.c.clu_sigla == dados.clube_clu_sigla.upper()).first()
    if not clube:
        raise HTTPException(status_code=404, detail=f"Clube com sigla '{dados.clube_clu_sigla.upper()}' não encontrado.")

    # Verifica se já existe um cartão com o mesmo conjunto de chaves primárias
    cartao_existente = session.query(Cartao).filter(
        Cartao.__table__.c.car_serie == dados.car_serie.upper(),
        Cartao.__table__.c.car_ano == dados.car_ano,
        Cartao.__table__.c.clube_clu_sigla == dados.clube_clu_sigla.upper(),
    ).first()
    if cartao_existente:
        raise HTTPException(
            status_code=404, 
            detail=f"Cartão para o clube '{dados.clube_clu_sigla.upper()}' na série '{dados.car_serie.upper()}' do ano {dados.car_ano} já existe."
        )

    qtd_vermelho = dados.car_qtd_vermelho if dados.car_qtd_vermelho is not None else 0
    qtd_amarelo = dados.car_qtd_amarelo if dados.car_qtd_amarelo is not None else 0
    # Cria um novo registro de cartão
    novo_cartao = Cartao(
        car_serie=dados.car_serie.upper(),
        car_ano=dados.car_ano,
        clube_clu_sigla=dados.clube_clu_sigla.upper(),
        car_qtd_vermelho=qtd_vermelho,
        car_qtd_amarelo=qtd_amarelo,
    )
    
    session.add(novo_cartao)
    session.commit()
    session.refresh(novo_cartao)

    return CartaoSchema(**novo_cartao.as_dict())


def criar_cartoes_para_clubes(serie: str, ano: int, session: Session) -> dict:
    """
    Cria registros na tabela 'cartao' para todos os clubes de uma determinada série e ano,
    com os contadores de cartões zerados (qtd vermelho e amarelo).
    
    Args:
        db (Session): Sessão do banco de dados.
        serie (str): Série do campeonato ('A' ou 'B').
        ano (int): Ano do campeonato.

    Raises:
        HTTPException: Caso já existam registros com a mesma série e ano ou algum erro do banco de dados.

    Returns:
        dict: Mensagem indicando que os registros foram criados com sucesso.
    """
    consiste_serie(serie.upper())
    
    # Verificar se já existem registros na tabela `cartao` para a série e ano fornecidos
    cartao_verifica_query = text("""
        SELECT COUNT(*)
        FROM cartao
        WHERE car_serie = :serie
        AND car_ano = :ano
    """)
    registros_existentes = session.execute(cartao_verifica_query, {"serie": serie.upper(), "ano": ano}).scalar()
    
    if registros_existentes and registros_existentes > 0:
        raise HTTPException(
            status_code=404,
            detail=f"Os cartões amarelos e vermelhos já foram gerados para a série '{serie.upper()}' e ano '{ano}'."
        )
    
    # Buscar todos os clubes da série
    clube_query = text("""
        SELECT
            clu_sigla,
            clu_nome,
            clu_serie,
            clu_link_escudo,
            cidade_cid_id
        FROM clube
        WHERE clu_serie = :serie
    """)
    clubes_resultados = session.execute(clube_query, {"serie": serie.upper()}).fetchall()

    if not clubes_resultados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum clube encontrado para a série '{serie.upper()}'."
        )

    # Preparar e executar os inserts na tabela `cartao`
    try:
        for clube in clubes_resultados:
            insert_cartao_query = text("""
                INSERT INTO cartao (
                    car_serie,
                    car_ano,
                    clube_clu_sigla,
                    car_qtd_vermelho,
                    car_qtd_amarelo
                ) VALUES (
                    :serie,
                    :ano,
                    :clube_clu_sigla,
                    0,
                    0
                )
            """)
            session.execute(insert_cartao_query, {
                "serie": serie.upper(),
                "ano": ano,
                "clube_clu_sigla": clube.clu_sigla
            })
        
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao inserir os registros na tabela 'cartao': {str(e)}"
        )
    
    return {"message": f"Registros de cartões criados com sucesso para a série '{serie.upper()}' e ano '{ano}'."}


def atualizar_cartao(cartao: CartaoSchema, session: Session) -> CartaoSchema:
    """Atualiza um registro de cartão existente.

    Args:
        altera_qtd_menor (bool): Indica se deve diminuir a quantidade de cartões.
        car_serie (str): Série do cartão.
        car_ano (int): Ano da competição.
        clube_clu_sigla (str): Sigla do clube associado ao cartão.
        dados (AtualizarCartaoSchema): Dados atualizados do cartão.
        session (Session): Sessão ativa do SQLAlchemy para conexão com o banco.

    Raises:
        HTTPException: Erro: 404 - Cartão não encontrado.

    Returns:
        CartaoSchema: Representação do cartão atualizado.
    """
    serie = cartao.car_serie.upper()
    sigla = cartao.clube_clu_sigla.upper()
    consiste_serie(serie)
    consiste_sigla(sigla)

    # Busca o cartão no banco
    cartao_existente = session.query(Cartao).filter(
        Cartao.__table__.c.car_serie == serie,
        Cartao.__table__.c.car_ano == cartao.car_ano,
        Cartao.__table__.c.clube_clu_sigla == sigla,
    ).first()

    if not cartao_existente:
        raise HTTPException(
            status_code=404, detail=f"Cartão para o clube '{sigla}' na série '{serie}' do ano {cartao.car_ano} não encontrado."
        )

    dados_atualizacao = cartao
    cartao = cartao_existente

    # Atualiza os campos fornecidos
    if dados_atualizacao.car_qtd_vermelho is not None:
        cartao.car_qtd_vermelho = dados_atualizacao.car_qtd_vermelho

    if dados_atualizacao.car_qtd_amarelo is not None:
        cartao.car_qtd_amarelo = dados_atualizacao.car_qtd_amarelo

    if cartao:
        session.commit()
        session.refresh(cartao)

    return CartaoSchema(**cartao.as_dict())


def obter_url_cbf(car_serie: str, car_ano: int) -> str:
    """Retorna a URL correspondente à série e ano."""
    if car_serie == "A":
        return f"https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/{car_ano}"
    elif car_serie == "B":
        return f"https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-b/{car_ano}"
    else:
        raise HTTPException(status_code=404, detail="Série inválida. Use 'A' ou 'B' para a série.")


def coletar_dados_cartoes(url: str) -> list[dict]:
    """Faz o scraping no site da CBF e retorna os dados estruturados de cartões."""
    # response = requests.get(url)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        r = httpx.Client(http2=True, verify=certifi.where(), headers=headers)
        response = r.get(url)
    except Exception as ex:
        #print(f"cartao_service.py - coletar_dados_cartoes - Erro ao acessar a página: {url}. Erro: {ex}")
        raise HTTPException(status_code=500, detail=f"Erro ao acessar a página {url}, Descr.Erro: {ex}")
    
    # print(f"response.text: {response.text}")
    # print(f"response.status_code: {response.status_code}")

    if response.status_code != 200:
        # print(f"cartao_service.py - coletar_dados_cartoes - Falha ao acessar a página: {url}. Status code: {response.status_code}")
        raise HTTPException(status_code=500, detail=f"Falha ao acessar a página {url}.")
    # print(f"cartao_service.py - coletar_dados_cartoes - Página acessada com sucesso: {url}. Iniciando parsing do conteúdo...")

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    section = soup.find("section", class_="styles_container__L5dGB")
    if not section:
        raise HTTPException(status_code=500, detail="Seção da tabela não encontrada no site da CBF.")
    tbody = section.find("tbody")
    if not tbody:
        raise HTTPException(status_code=500, detail="Tabela não encontrada no site da CBF.")
    
    # print("cartao_service.py - coletar_dados_cartoes - Tabela encontrada, iniciando extração dos dados...")
    resultados = []
    for tr in tbody.find_all("tr"):
        try:
            td_nome_clube = tr.find("td", class_="styles_teamPosition__CFIvz")
            if not td_nome_clube:
                raise HTTPException(status_code=500, detail="Nome do clube não encontrado. Tag extraída: {td_nome_clube}")

            nome_clube = td_nome_clube.find_all("strong")[1].text.strip()
            cartoes_amarelos = int(tr.find_all("td")[9].text.strip())
            cartoes_vermelhos = int(tr.find_all("td")[10].text.strip())
            print(f"cartao_service.py - coletar_dados_cartoes - Dados extraídos para o clube '{nome_clube}': {cartoes_amarelos} amarelos, {cartoes_vermelhos} vermelhos.")
            resultados.append({
                "clube": normalizar_texto(nome_clube),
                "cartoes_amarelos": cartoes_amarelos,
                "cartoes_vermelhos": cartoes_vermelhos,
            })
        except Exception as e:
            # print(f"Erro ao processar uma linha: {e}")
            continue
    # print(f"cartao_service.py - coletar_dados_cartoes - Dados coletados: {resultados}. Finalizando...")
    return resultados

def normalizar_texto(texto: str) -> str:
    """
    Normaliza um texto convertendo para minúsculas e removendo acentuação.
    """
    # Converte para minúsculas
    texto = texto.lower()

    # Decompõe caracteres acentuados em base + combining
    texto = unicodedata.normalize('NFD', texto)

    # Remove caracteres combining (acentos, cedilha etc.)
    texto = ''.join(caractere for caractere in texto if not unicodedata.combining(caractere))

    return texto

def normalizar_dados_clubes(serie: str, resultados: list[dict]) -> list[dict]:
    """Substitui nomes dos clubes por suas respectivas siglas."""
    if serie == "A":
        clubes_para_siglas = {
            "palmeiras": "PAL",
            "sao paulo": "SAO",
            "fluminense": "FLU",
            "bahia": "BAH",
            "athletico paranaense": "CAP",
            "red bull bragantino": "RBB",
            "chapecoense": "CHA",
            "mirassol": "MIR",
            "coritiba saf": "CFC",
            "flamengo": "FLA",
            "botafogo": "BOT",
            "corinthians": "COR",
            "gremio": "GRE",
            "vitoria": "VIT",
            "atletico mineiro": "CAM",
            "remo": "REM",
            "vasco da gama saf": "VAS",
            "santos fc": "SAN",
            "internacional": "INT",
            "cruzeiro": "CRU",
        }
    elif serie == "B":
        clubes_para_siglas = {
            "botafogo": "BSP",
            "londrina saf": "LEC",
            "goias": "GOI",
            "avai": "AVA",
            "athletic saf": "ATH",
            "operario": "OPE",
            "criciuma": "CRI",
            "crb": "CRB",
            "vila nova": "VNO",
            "sao bernardo saf": "SBD",
            "ceara": "CEA",
            "cuiaba": "CUI",
            "sport recife": "SPT",
            "ponte preta": "PON",
            "atletico goianiense saf": "ACG",
            "nautico": "NAU",
            "america": "AME",
            "gremio novorizontino - saf": "NOV",
            "juventude": "JUV",
            "fortaleza saf": "FOR",
        }

    nova_lista = []
    for item in resultados:
        nome_clube = item["clube"]
        sigla = clubes_para_siglas.get(nome_clube, "N/A")
        print(f"cartao_service.py - coletar_dados_cartoes - Nome do clube: {nome_clube}, Sigla: {sigla}")
        nova_lista.append({
            "clube": sigla,
            "cartoes_amarelos": item["cartoes_amarelos"],
            "cartoes_vermelhos": item["cartoes_vermelhos"],
        })

    return nova_lista


def atualizar_dados_cartoes(nova_lista: list[dict], car_serie: str, car_ano: int, session: Session) -> list[CartaoSchema]:
    """Atualiza os dados no banco de dados com base na lista normalizada."""
    erros = []
    cartoes_atualizados = []

    for item in nova_lista:
        try:
            cartao = session.query(Cartao).filter(
                Cartao.__table__.c.car_serie == car_serie,
                Cartao.__table__.c.car_ano == car_ano,
                Cartao.__table__.c.clube_clu_sigla == item["clube"],
            ).first()

            if not cartao:
                raise HTTPException(
                    status_code=404,
                    detail=f"Cartão para o clube '{item['clube']}' na série '{car_serie}' do ano {car_ano} não encontrado."
                )

            cartao.car_qtd_vermelho = item["cartoes_vermelhos"]
            cartao.car_qtd_amarelo = item["cartoes_amarelos"]

            session.commit()
            session.refresh(cartao)

            cartoes_atualizados.append(CartaoSchema(
                car_serie=car_serie,
                car_ano=car_ano,
                clube_clu_sigla=item["clube"],
                car_qtd_vermelho=item["cartoes_vermelhos"],
                car_qtd_amarelo=item["cartoes_amarelos"],
            ))

        except HTTPException as http_error:
            erros.append(f"Erro: {http_error.detail}. Clube: {item['clube']}")
            session.rollback()
        except Exception as e:
            erros.append(f"Erro inesperado no clube {item['clube']}: {str(e)}")
            session.rollback()

    if erros:
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreram erros durante a atualização dos cartões: {'; '.join(erros)}"
        )

    return cartoes_atualizados


def atualizar_cartao_cbf(car_serie: str, car_ano: int, session: Session) -> list[CartaoSchema]:
    """Função principal para atualizar os cartões."""
    # 1. Valida a série e obtém a URL correspondente
    # print(f"cartao_service.py - atualizar_cartao_cbf - Iniciando atualização para série '{car_serie.upper()}' e ano {car_ano}...")
    url = obter_url_cbf(car_serie.upper(), car_ano)

    # 2. Coleta os dados de cartões do site
    # print(f"cartao_service.py - atualizar_cartao_cbf - URL obtida: {url}. Iniciando coleta dos dados...")
    resultados = coletar_dados_cartoes(url)

    # 3. Normaliza os dados dos clubes para utilizar siglas
    # print(f"cartao_service.py - atualizar_cartao_cbf - Dados coletados: {resultados}. Iniciando normalização dos dados...")
    nova_lista = normalizar_dados_clubes(car_serie, resultados)

    # 4. Atualiza os dados no banco de dados
    # print(f"cartao_service.py - atualizar_cartao_cbf - Dados normalizados: {nova_lista}. Iniciando atualização no banco de dados...")
    return atualizar_dados_cartoes(nova_lista, car_serie.upper(), car_ano, session)

def deletar_cartao(car_serie: str, car_ano: int, clube_clu_sigla: str, session: Session):
    """Deleta um registro de cartão do banco.

    Args:
        car_serie (str): Série do cartão.
        car_ano (int): Ano da competição.
        clube_clu_sigla (str): Sigla do clube associado ao cartão.
        session (Session): Sessão ativa do SQLAlchemy para conexão com o banco.

    Raises:
        HTTPException: Erro: 404 - Cartão não encontrado.

    Returns:
        str: Mensagem de sucesso ao excluir o cartão.
    """
    consiste_serie(car_serie.upper())
    consiste_sigla(clube_clu_sigla.upper())

    cartao = session.query(Cartao).filter(
        Cartao.__table__.c.car_serie == car_serie.upper(),
        Cartao.__table__.c.car_ano == car_ano,
        Cartao.__table__.c.clube_clu_sigla == clube_clu_sigla.upper(),
    ).first()

    if not cartao:
        raise HTTPException(
            status_code=404, detail=f"Cartão para o clube '{clube_clu_sigla.upper()}' na série '{car_serie.upper()}' do ano {car_ano} não encontrado."
        )

    session.delete(cartao)
    session.commit()
    return "Cartão excluído com sucesso."


def buscar_cartao_sigla(retorna_exception: bool, car_ano: int,clube_clu_sigla: str, session: Session) -> Optional[CartaoSchema]:
    """
    Busca uma cartao por serie, ano, sigla no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cartao não seja encontrado.
        serie (str) : série
		ano (int) : ano 
		sigla (str) : sigla do clube
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cartão não seja encontrado.

    Returns:
        Optional[Cartao.chema]: Representação do cartão do clube encontrado ou None se não encontrado.
    """
    # Busca pelo cartao no banco de dados
    cartao = session.query(Cartao).filter(Cartao.__table__.c.car_ano == car_ano, Cartao.__table__.c.clube_clu_sigla == clube_clu_sigla).first()

    if cartao and retorna_exception:
        raise HTTPException(status_code=404, detail=f"Cartao.com sigla '{clube_clu_sigla}' já existe.")
        
    return CartaoSchema(**cartao.as_dict()) if cartao else None

def listar_cartoes_paginados(serie: str, ano: int, pagina: int, tamanho_pagina: int, session: Session) -> List[CartaoClubeOut]:
    """Listar os cartões dos clubes pelo nome da clube (opcional) com paginação

    Args:
        serie (str): Série do campeonato.
        ano (int): Ano do campeonato.
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma clube for encontrada.

    Returns:
        ResponseCartaoClubeSchema: Lista dos cartões dos clubes no formato esperado na API.
    """
    query = session.query(
	    Cartao.__table__.c.car_serie,
		Cartao.__table__.c.car_ano,
        Cartao.__table__.c.clube_clu_sigla,
        Clube.__table__.c.clu_link_escudo.label("clube_link_escudo"),
        Clube.__table__.c.clu_nome.label("clube_nome"),
        Cartao.__table__.c.car_qtd_vermelho,
        Cartao.__table__.c.car_qtd_amarelo,
    ).join(Clube, Cartao.__table__.c.clube_clu_sigla == Clube.__table__.c.clu_sigla).filter(Cartao.__table__.c.car_ano == ano, Cartao.__table__.c.car_serie == serie.upper())

    query = query.order_by(Cartao.__table__.c.clube_clu_sigla)  # Ordena pelo nome do clube

    # Paginação
    cartoes = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()

    # Caso nenhum clube seja encontrado
    if not cartoes:
        raise HTTPException(status_code=404, detail="Nenhum cartão encontrado.")

    # Serializar os cartoes no formato esperado
    cartoes_schema = [
        CartaoClubeOut(
		    car_serie=cartao.car_serie,
			car_ano=cartao.car_ano,
            clube_clu_sigla=cartao.clube_clu_sigla,
            clube_link_escudo=cartao.clube_link_escudo,
            clube_nome=cartao.clube_nome,
            car_qtd_vermelho=cartao.car_qtd_vermelho,
            car_qtd_amarelo=cartao.car_qtd_amarelo,
        )
        for cartao in cartoes
    ]

    return cartoes_schema