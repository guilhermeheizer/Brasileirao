"""
form_cadastra_rodada_routers.py

Este módulo define a rota da API para cadastro de rodadas completas do Campeonato Brasileiro.
Utiliza FastAPI para expor endpoint de criação de rodada, recebendo uma lista de jogos.

Funcionalidade principal:
- Criar uma rodada completa (10 jogos) a partir de dados enviados pelo front-end

O endpoint utiliza injeção de dependências para sessão do banco e autenticação de usuário.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseCriarRodadaSchema
from app.schemas.clube_schema import ResponseClubeSchema
from app.schemas.estadio_schema import ResponseEstadioSchema
from app.services.form.form_cadastra_rodada_service import criar_rodada
from typing import List, Annotated
from app.services.clube_service import listar_todos_clubes
from app.services.estadio_service import listar_todos_estadios
from typing import Optional
from fastapi import Query

# Instância do APIRouter para organizar as rotas relacionadas ao formulário de cadastro de rodadas
rodada_form_router = APIRouter(tags=["cadastra rodada"])


@rodada_form_router.post("/criar-rodada", response_model=List[ResponseCriarRodadaSchema])
async def criar_rodadas(
    jogos_data: List[CriarRodadaSchema],
    session: Annotated[Session, Depends(pegar_sessao)],
    usuario: Annotated[Usuario, Depends(verificar_token)]
):
    """
    Cria uma rodada completa com base na série, ano, e uma lista de 10 jogos.

    Args:
        rod_serie (str): Série do campeonato (ex.: 'A', 'B').
        rod_ano (int): Ano do campeonato.
        jogos_data (List[CriarRodadaSchema]): Lista de 10 jogos, conforme o esquema `CriarRodadaSchema`.
        session (Session): Sessão do SQLAlchemy gerenciada pelo FastAPI via `Depends(pegar_sessao)`.
        usuario (Usuario): Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.

    Returns:
        ResponseCriarRodadaSchema: Retorna os dados das rodadas criadas.
    """
    try:
        return criar_rodada(jogos_data, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()


@rodada_form_router.get("/pesquisar-clubes", response_model=ResponseClubeSchema)
async def pesquisar_clubes(
    serie: Optional[str] = Query(None),
    nome: Optional[str] = Query(None),
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    try:
        return listar_todos_clubes(serie, nome, session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()


@rodada_form_router.get("/pesquisar-estadios", response_model=ResponseEstadioSchema)
async def pesquisar_estadios(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    try:
        return listar_todos_estadios(session)
    finally:
        session.close()