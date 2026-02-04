from fastapi import APIRouter, HTTPException, Depends
from app.schemas.clube_schema import ResponseClubeSchema, ClubeSchema, ResponseClubeCidadeSchema
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.services.clube_service import (
    listar_todos_clubes,
    criar_clube,
    atualizar_clube,
    deletar_clube,
    listar_clubes_paginadas,
)

clube_router = APIRouter(tags=["clube"])


@clube_router.get("/listar", response_model=ResponseClubeSchema)
async def listar_clubes(session: Session = Depends(pegar_sessao)):
    """
    Lista todos os clubes cadastrados.

    Args:
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI 
    via dependência de injeção (Depends(pegar_sessao)).

    Raises:
    HTTPException: Lançada se não houver clubes cadastrados no banco de dados 
    (status 404).

    Returns:
    ResponseClubeSchema: Uma resposta no formato do esquema Pydantic `ResponseClubeSchema`, 
    que contém uma lista de clube no formato especificado por `ClubeSchema`.
    """
    try:
        return listar_todos_clubes(session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)    
    finally:
        session.close()


@clube_router.post("/", response_model=ClubeSchema)
async def criar_novo_clube(clube: ClubeSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Cria um novo clube no banco de dados.

    Args:
    clube (ClubeSchema): clube: Dados da clube a ser criado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                    via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a criação da clube.

    Returns:
    ClubeSchema: A clube criado.
    """
    try:
        return criar_clube(clube, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@clube_router.put("/{clu_sigla}", response_model=ClubeSchema)
async def atualizar_clube_por_sigla(
    clu_sigla: str,
    clube_atualizado: ClubeSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza os dados de um clube específico.

    Args:
    clube_id (int): informe o ID da clube a ser atualizado.
    clube_atualizado (ClubeSchema): Dados para atualizar a clube.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a atualização da clube.

    Returns:
    ClubeSchema: A clube atualizada.
    """
    try:
        return atualizar_clube(clu_sigla, clube_atualizado, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()


@clube_router.delete("/{clu_sigla}")
async def deletar_clube_por_sigla(
    clu_sigla: str,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Remove um clube com base na sigla e no ID da clube.

    Args:
    clube_sigla: Informe a sigla do clube a ser deletado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a exclusão da clube.

    Returns:
    ClubesSchema: O clube excluído.
    """
    try:
        return deletar_clube(clu_sigla, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()

    
@clube_router.get("/listar-paginado", response_model=ResponseClubeCidadeSchema)
async def listar_clubes_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da clube"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista os clubes com paginação e busca por nome.

    Args:
        nome (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome do clube").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem dos clubes.

    Returns: ResponseClubesSchema: Uma resposta no formato do esquema Pydantic `ResponseClubesSchema`, 
             que contém uma lista de clubes no formato especificado por `ClubeSchema`.
    """
    try:
        return listar_clubes_paginadas(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()