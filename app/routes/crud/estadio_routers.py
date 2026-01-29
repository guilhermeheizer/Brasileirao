from fastapi import APIRouter, HTTPException, Depends
from app.schemas.estadio_schema import ResponseEstadioSchema, EstadioSchema, ResponseEstadioCidadeSchema
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.services.estadio_service import (
    listar_todos_estadios,
    criar_estadio,
    atualizar_estadio,
    deletar_estadio,
    listar_estadios_paginadas,
)

estadio_router = APIRouter(tags=["estadio"])


@estadio_router.get("/listar", response_model=ResponseEstadioSchema)
def listar_estadios(session: Session = Depends(pegar_sessao)):
    """
    Lista todos os estadios cadastrados.

    Args:
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI 
    via dependência de injeção (Depends(pegar_sessao)).

    Raises:
    HTTPException: Lançada se não houver estadios cadastrados no banco de dados 
    (status 404).

    Returns:
    ResponseEstadioSchema: Uma resposta no formato do esquema Pydantic `ResponseEstadioSchema`, 
    que contém uma lista de estadio no formato especificado por `EstadioSchema`.
    """
    try:
        return listar_todos_estadios(session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)    
    finally:
        session.close()


@estadio_router.post("/", response_model=EstadioSchema)
def criar_novo_estadio(estadio: EstadioSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Cria um novo estadio no banco de dados.

    Args:
    estadio (EstadioSchema): estadio: Dados da estadio a ser criado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                    via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a criação da estadio.

    Returns:
    EstadioSchema: A estadio criado.
    """
    try:
        return criar_estadio(estadio, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@estadio_router.put("/{est_id}", response_model=EstadioSchema)
def atualizar_estadio_por_sigla(
    est_id: int,
    estadio_atualizado: EstadioSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza os dados de um estadio específico.

    Args:
    estadio_id (int): informe o ID da estadio a ser atualizado.
    estadio_atualizado (EstadioSchema): Dados para atualizar a estadio.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a atualização da estadio.

    Returns:
    EstadioSchema: A estadio atualizada.
    """
    try:
        return atualizar_estadio(est_id, estadio_atualizado, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@estadio_router.delete("/{est_id}")
def deletar_estadio_por_id(
    est_id: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Remove um estadio com base na sigla e no ID da estadio.

    Args:
    estadio_id (int): Informe o ID da estadio a ser deletado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a exclusão da estadio.

    Returns:
    EstadiosSchema: O estadio excluído.
    """
    try:
        return deletar_estadio(est_id, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()

    
@estadio_router.get("/listar-paginado", response_model=ResponseEstadioCidadeSchema)
def listar_estadios_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da estadio"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista os estadios com paginação e busca por nome.

    Args:
        nome (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome do estadio").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem dos estadios.

    Returns: ResponseEstadiosSchema: Uma resposta no formato do esquema Pydantic `ResponseEstadiosSchema`, 
             que contém uma lista de estadios no formato especificado por `EstadioSchema`.
    """
    try:
        return listar_estadios_paginadas(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()