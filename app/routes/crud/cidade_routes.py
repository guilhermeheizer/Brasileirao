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


cidade_router = APIRouter(tags=["Cidade"])

@cidade_router.get("/listar", response_model=ResponseCidadesSchema)
def listar_cidades(session: Session = Depends(pegar_sessao)):
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

Exemplo:
    Requisição:
        GET /cidade/listar

    Resposta (200):
        {
            "cidades": [
                {
                    "cid_id": 1,
                    "cid_nome": "São Paulo",
                    "cid_uf": "SP"
                },
                {
                    "cid_id": 2,
                    "cid_nome": "Rio de Janeiro",
                    "cid_uf": "RJ"
                }
            ]
        }
    """
    try:
        return listar_todas_cidades(session)
    except HTTPException as ex:
        raise ex

@cidade_router.post("/", response_model=CidadesSchema)
def criar_nova_cidade(cidade: CidadesSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Insere uma nova cidade no banco.
    """
    try:
        return criar_cidade(cidade, session)
    except HTTPException as ex:
        raise ex
    finally:
        session.close()


@cidade_router.put("/{cidade_id}", response_model=CidadesSchema)
def atualizar_cidade_por_id(cidade_id: int, cidade_atualizada: CidadesSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza uma cidade pelo ID.
    """
    try:
        return atualizar_cidade(cidade_id, cidade_atualizada, session)
    except HTTPException as ex:
        raise ex
    finally:
        session.close()

@cidade_router.delete("/{cidade_id}")
def deletar_cidade_por_id(cidade_id: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Remove uma cidade pelo ID.
    """
    try:
        deletar_cidade(cidade_id, session)
        return {"message": "Cidade deletada com sucesso"}
    except HTTPException as ex:
        raise ex
    finally:
        session.close()


@cidade_router.get("/listar-paginado", response_model=ResponseCidadesSchema)
def listar_cidades_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da cidade"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(10, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao),
):
    """
    Lista as cidades com paginação e busca por nome.
    """
    try:
        return listar_cidades_paginadas(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        raise ex