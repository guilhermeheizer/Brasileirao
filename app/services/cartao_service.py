from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cartao_models import Cartao
from app.models.clube_models import Clube
from app.services.clube_service import buscar_clube_sigla, consiste_serie, consiste_sigla
from typing import Optional
import re
from app.schemas.cartao_schema import (
    CartaoClubeSchema,
    ResponseCartaoClubeSchema, 
    ResponseCartaoSchema,
    CartaoSchema,
)


def listar_todos_cartoes(session: Session) -> ResponseCartaoSchema:
    """Lista todos os cartões registrados no banco de dados.

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conexão com o banco.

    Raises:
        HTTPException: Erro: 404 - Nenhum cartão encontrado.

    Returns:
        ResponseCartaoSchema: Lista de cartões registrados.
    """
    cartoes = session.query(Cartao).all()
    if not cartoes:
        raise HTTPException(status_code=404, detail="Nenhum cartão encontrado.")
    
    # Serializa os cartões na resposta
    cartoes_schema = [CartaoSchema(**cartao.as_dict()) for cartao in cartoes]

    return ResponseCartaoSchema(cartoes=cartoes_schema)


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
        ResponseCartaoSchema: Representação do cartão criado.
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


def atualizar_cartao(car_serie: str, car_ano: int, clube_clu_sigla: str, dados: CartaoSchema, session: Session) -> CartaoSchema:
    """Atualiza um registro de cartão existente.

    Args:
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
    consiste_serie(car_serie.upper())
    consiste_sigla(clube_clu_sigla.upper())

    # Busca o cartão no banco
    cartao = session.query(Cartao).filter(
        Cartao.__table__.c.car_serie == car_serie.upper(),
        Cartao.__table__.c.car_ano == car_ano,
        Cartao.__table__.c.clube_clu_sigla == clube_clu_sigla.upper(),
    ).first()

    if not cartao:
        raise HTTPException(
            status_code=404, detail=f"Cartão para o clube '{clube_clu_sigla}' na série '{car_serie}' do ano {car_ano} não encontrado."
        )

    # Atualiza os campos fornecidos
    if dados.car_qtd_vermelho is not None:
        cartao.car_qtd_vermelho = dados.car_qtd_vermelho

    if dados.car_qtd_amarelo is not None:
        cartao.car_qtd_amarelo = dados.car_qtd_amarelo

    if dados:
        session.commit()
        session.refresh(cartao)

    return CartaoSchema(**cartao.as_dict())


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


def buscar_cartao_sigla(retorna_exception: bool, clube_clu_sigla: str, session: Session) -> Optional[CartaoSchema]:
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
    cartao = session.query(Cartao).filter(Cartao.__table__.c.clube_clu_sigla == clube_clu_sigla).first()

    if cartao:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cartao.com sigla '{clube_clu_sigla}' já existe.")
        
    return CartaoSchema(**cartao.as_dict()) if cartao else None



def listar_cartoes_paginados(nome: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> ResponseCartaoClubeSchema:
    """Listar os cartões dos clubes pelo nome da clube (opcional) com paginação

    Args:
        nome (Optional[str]): Nome do clube a ser filtrado (opcional).
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
        Clube.__table__.c.clu_nome.label("clu_nome"),
        Cartao.__table__.c.car_qtd_vermelho,
        Cartao.__table__.c.car_qtd_amarelo,
    ).join(Clube, Cartao.__table__.c.clube_clu_sigla == Clube.__table__.c.clu_sigla)

    # Filtro opcional pelo nome do clube
    if nome:
        query = query.filter(Clube.__table__.c.clu_nome.ilike(f"%{nome}%"))

    # Paginação
    cartoes = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()

    # Caso nenhum clube seja encontrado
    if not cartoes:
        raise HTTPException(status_code=404, detail="Nenhum cartão encontrado.")

    # Serializar os cartoes no formato esperado
    cartoes_schema = [
        CartaoClubeSchema(
		    car_serie=cartao.car_serie,
			car_ano=cartao.car_ano,
            clube_clu_sigla=cartao.clube_clu_sigla,
            clube_nome=cartao.clu_nome,
            car_qtd_vermelho=cartao.car_qtd_vermelho,
            car_qtd_amarelo=cartao.car_qtd_amarelo,
        )
        for cartao in cartoes
    ]

    return ResponseCartaoClubeSchema(cartoes=cartoes_schema)