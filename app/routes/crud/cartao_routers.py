from fastapi import APIRouter, HTTPException, Depends
from app.schemas.cartao_schema import ResponseCartaoSchema, CartaoSchema, ResponseCartaoClubeSchema
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.services.cartao_service import (
    listar_todos_cartoes,
    criar_cartao,
    atualizar_cartao,
    deletar_cartao,
    listar_cartoes_paginados,
)

cartao_router = APIRouter(tags=["cartao"])


@cartao_router.get("/listar", response_model=ResponseCartaoSchema)
def listar_cartoes(session: Session = Depends(pegar_sessao)):
    """
    Lista todos os cartões cadastrados.

    Args:
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI 
    via dependência de injeção (Depends(pegar_sessao)).

    Raises:
    HTTPException: Lançada se não houver cartões cadastrados no banco de dados 
    (status 404).

    Returns:
    ResponseCartaoSchema: Uma resposta no formato do esquema Pydantic `ResponseCartaoSchema`, 
    que contém uma lista de dos cartoes dos clubes no formato especificado por `CartaoSchema`.
    """
    try:
        return listar_todos_cartoes(session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)    
    finally:
        session.close()


@cartao_router.post("/", response_model=CartaoSchema)
def criar_novo_cartao(cartao: CartaoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Cria um novo cartão no banco de dados.

    Args:
    cartao (CartaoSchema): cartao: Dados do cartão a ser criado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                    via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a criação da cartao.

    Returns:
    CartaoSchema: Cartão criado.
    """
    try:
        return criar_cartao(cartao, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@cartao_router.put("/{serie}/{ano}/{clu_sigla}", response_model=CartaoSchema)
def atualizar_cartao_por_serie_ano_sigla(
    serie: str,
    ano: int,
    clu_sigla: str,
    cartao_atualizado: CartaoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza os dados de um cartao específico.

    Args:
    serie (str): Informe a série do cartão a ser atualizado.
    ano (int): Informe o ano do cartão a ser atualizado.
    clu_sigla (str): Informe a sigla do clube do cartão a ser atualizado.
    cartao_atualizado (CartaoSchema): Dados para atualizar do cartao.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a atualização do cartao.

    Returns:
    CartaoSchema: Cartão atualizado.
    """
    try:
        return atualizar_cartao(serie, ano, clu_sigla, cartao_atualizado, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@cartao_router.delete("/{serie}/{ano}/{clu_sigla}")
def deletar_cartao_por_sigla(
    serie: str,
    ano: int,
    clu_sigla: str,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Exclui um cartão com base na série, ano e sigla do clube.

    Args:
    serie (str): Informe a série do cartão a ser deletado.
    ano (int): Informe o ano do cartão a ser deletado.
    clu_sigla (str): Informe a sigla do clube do cartão a ser deletado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a exclusão da cartão.

    Returns:
    CartaosSchema: O cartão excluído.

    """
    try:
        return deletar_cartao(serie, ano, clu_sigla, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()

    
@cartao_router.get("/listar-paginado", response_model=ResponseCartaoClubeSchema)
def listar_cartoes_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da clube"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista os cartões com paginação e busca por nome.

    Args:
        nome (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome do clube").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem dos cartões.

    Returns: ResponseCartaoClubeSchema: Uma resposta no formato do esquema Pydantic `ResponseCartaoClubeSchema`, 
             que contém uma lista de cartões no formato especificado por `CartaoSchema`.
    """
    try:
        return listar_cartoes_paginados(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()