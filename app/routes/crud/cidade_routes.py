from fastapi import APIRouter, HTTPException, Depends
from app.schemas.cidade_schema import ResponseCidadesSchema, CidadesSchema 
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.services.cidade_service import (
    listar_todas_cidades,
    criar_cidade,
    atualizar_cidade,
    deletar_cidade,
    listar_cidades_paginadas,
)


cidade_router = APIRouter(tags=["cidade"])

@cidade_router.get("/listar", response_model=ResponseCidadesSchema)
async def listar_cidades(session: Session = Depends(pegar_sessao)):
    """
    Lista todas as cidades cadastradas no banco de dados.

    Args:
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI 
        via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se não houver cidades cadastradas no banco de dados 
        (status 404).

    Returns:
        ResponseCidadesSchema: Uma resposta no formato do esquema Pydantic `ResponseCidadesSchema`, 
        que contém uma lista de cidades no formato especificado por `CidadesSchema`.
    """
    try:
        return listar_todas_cidades(session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=500, detail=log_erro)
    finally:
        session.close()

@cidade_router.post("/incluir", response_model=CidadesSchema)
async def criar_nova_cidade(cidade: CidadesSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """Insere uma nova cidade no banco.

    Args:
        cidade (CidadesSchema): cidade: Dados da cidade a ser criada.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a criação da cidade.

    Returns:
        CidadesSchema: A cidade criada.
    """
    try:
        return criar_cidade(cidade, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()


@cidade_router.put("/alterar/{cidade_id}", response_model=CidadesSchema)
async def atualizar_cidade_por_id(cidade_id: int, cidade_atualizada: CidadesSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """Atualiza cidade

    Args:
        cidade_id (int): informe o ID da cidade a ser atualizada.
        cidade_atualizada (CidadesSchema): Dados para atualizar a cidade.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a atualização da cidade.
    Returns:
        CidadesSchema: A cidade atualizada.
    """
    try:
        return atualizar_cidade(cidade_id, cidade_atualizada, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()

@cidade_router.delete("/deletar/{cidade_id}")
async def deletar_cidade_por_id(cidade_id: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """Deleção de uma cidade

    Args:
        cidade_id (int): Informe o ID da cidade a ser deletada.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a exclusão da cidade.
    Returns:
        CidadesSchema: A cidade excluída.
    """
    try:
        deletar_cidade(cidade_id, session)
        return {"message": "Cidade excluida com sucesso"}
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()


@cidade_router.get("/listar-paginado", response_model=ResponseCidadesSchema)
async def listar_cidades_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da cidade"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista as cidades com paginação e busca por nome.

    Args:
        nome (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome da cidade").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem das cidades.

    Returns: ResponseCidadesSchema: Uma resposta no formato do esquema Pydantic `ResponseCidadesSchema`, 
             que contém uma lista de cidades no formato especificado por `CidadesSchema`.
    """
    try:
        return listar_cidades_paginadas(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()