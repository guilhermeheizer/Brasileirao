from fastapi import APIRouter, HTTPException, Depends
from app.schemas.estadio_schema import EstadioCreate, EstadioUpdate, EstadioCidadeOut
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Query
from app.services.estadio_service import (
    listar_todos_estadios,
    criar_estadio,
    atualizar_estadio,
    deletar_estadio,
    listar_estadios_paginadas,
)

estadio_router = APIRouter(tags=["estadio"])


@estadio_router.get("/listar", response_model=List[EstadioCidadeOut])
async def listar_estadios(
    nome_estadio: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da estadio"),
    nome_cidade: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da cidade"),
    uf: Optional[str] = Query(None, 
                              max_length=2,
                              description="Busca parcial pela UF da cidade"),
    session: Session = Depends(pegar_sessao)):
    """
    Lista todos os estadios cadastrados.

    Args:
        nome_estadio (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome da estadio").
        nome_cidade (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome da cidade").
        uf (Optional[str], optional): Defaults to Query(None, description="Busca parcial pela UF da cidade").
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI 
        via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se não houver estadios cadastrados no banco de dados 
        (status 404).

    Returns:
        List[EstadioCidadeOut]: Uma resposta no formato do esquema Pydantic `EstadioCidadeOut`, 
        que contém uma lista de estadios no formato especificado por `EstadioCidadeOut`.
    """
    try:
        return listar_todos_estadios(nome_estadio, nome_cidade, uf, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")  
    finally:
        session.close()


@estadio_router.post("/incluir", response_model=EstadioCreate)
async def criar_novo_estadio(estadio: EstadioCreate, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Cria um novo estadio no banco de dados.

    Args:
    estadio (EstadioCreate): estadio: Dados da estadio a ser criado.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                    via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a criação da estadio.

    Returns:
    EstadioCreate: A estadio criado.
    """
    try:
        return criar_estadio(estadio, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()


@estadio_router.put("/alterar", response_model=EstadioUpdate)
def atualiza_estadio(
    estadio_atualizado: EstadioUpdate,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza os dados de um estadio específico.

    Args:
    estadio_atualizado (EstadioUpdate): Dados para atualizar a estadio.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a atualização da estadio.

    Returns:
    EstadioUpdate: A estadio atualizado.
    """
    try:
        return atualizar_estadio(estadio_atualizado, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()


@estadio_router.delete("/deletar/{est_id}")
async def deletar_estadio_por_id(
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
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()

    
@estadio_router.get("/listar-paginado", response_model=List[EstadioCidadeOut])
async def listar_estadios_paginacao(
    nome_estadio: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da estadio"),
    nome_cidade: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da cidade"),
    uf: Optional[str] = Query(None, 
                              max_length=2,
                              description="Busca parcial pela UF da cidade"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista os estadios com paginação e busca por nome.

    Args:
        nome_estadio (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome do estadio").
        nome_cidade (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome da cidade").
        uf (Optional[str], optional): Defaults to Query(None, description="Busca parcial pela UF da cidade").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem dos estadios.

    Returns: List[EstadioCidadeOut]: Uma resposta no formato do esquema Pydantic `List[EstadioCidadeOut]`, 
             que contém uma lista de estadios no formato especificado por `EstadioCidadeOut`.
    """
    try:
        return listar_estadios_paginadas(nome_estadio, nome_cidade, uf, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()