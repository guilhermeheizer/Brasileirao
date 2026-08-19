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
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseCriarRodadaSchema, JogoFormPlacarSchema, UltimaRodadaResponseSchema
from app.services.form.form_placar_rodada_service import rodada_lista, buscar_ultima_rodada_cadastrada, rodada_jogos_nao_finalizados_lista
from app.schemas.clube_schema import ResponseClubeSchema
from app.schemas.estadio_schema import EstadioCidadeOut
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


@rodada_form_router.get("/pesquisar-estadios", response_model=List[EstadioCidadeOut])
async def pesquisar_estadios(
    nome_estadio: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da estadio"),
    nome_cidade: Optional[str] = Query(None, 
                                max_length=100,
                                description="Busca parcial pelo nome da cidade"),
    uf: Optional[str] = Query(None, 
                              max_length=2,
                              description="Busca parcial pela UF da cidade"),
    session: Session = Depends(pegar_sessao)
    ):
    try:
        return listar_todos_estadios(nome_estadio, nome_cidade, uf, session)
    finally:
        session.close()

@rodada_form_router.get(
    "/buscar-placares/{serie}/{ano}/{rodada}",
    response_model=List[JogoFormPlacarSchema],
    summary="Busca os jogos de uma rodada.",
    description="Retorna jogos de uma rodada específica."
)
async def get_rodada_lista(
    serie: str,
    ano: int,
    rodada: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """Endpoint para buscar os jogos de uma rodada específica, ou jogos anteriores não realizados, para preenchimento de placares.
    Args:
        serie (str): Série do campeonato (ex.: 'A', 'B').
        ano (int): Ano do campeonato.
        rodada (int): Rodada a ser buscada (ex.: '1', '2', '3', etc.).
        carrega_nao_realizados (bool, optional): Quando verdadeiro, inclui jogos de rodadas anteriores que ainda não foram realizados. Defaults to False.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.    
    """
    try:
        return rodada_lista(
            db=session,
            serie=serie,
            ano=ano,
            rodada=rodada
            )
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar rodadas: {str(e)}")
    finally:
        session.close()

@rodada_form_router.get(
    "/buscar-jogos-nao-finalizados/{serie}/{ano}/{rodada}",
    response_model=List[JogoFormPlacarSchema],
    summary="Busca os jogos da rodada para preenchimento de placares",
    description="Retorna jogos não finalizados de uma rodada ou anteriores no formato esperado pelo front-end."
)
async def get_rodada_jogos_nao_finalizados_lista(
    serie: str,
    ano: int,
    rodada: int,
    carrega_rodada_anteriores: bool = Query(
        default=False,
        alias="carrega_jogos",
        description="Quando verdadeiro, inclui jogos de rodadas anteriores."),
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """Endpoint para buscar os jogos de uma rodada específica, ou jogos anteriores não realizados, para preenchimento de placares.
    Args:
        serie (str): Série do campeonato (ex.: 'A', 'B').
        ano (int): Ano do campeonato.
        rodada (int): Rodada a ser buscada (ex.: '1', '2', '3', etc.).
        carrega_rodada_anteriores (bool, optional): Quando verdadeiro, inclui jogos de rodadas anteriores que ainda não foram realizados. Defaults to False.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.    
    """
    try:
        return rodada_jogos_nao_finalizados_lista(
            db=session,
            serie=serie,
            ano=ano,
            rodada=rodada,
            carrega_rodada_anteriores=carrega_rodada_anteriores
            )
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar rodadas: {str(e)}")
    finally:
        session.close()

@rodada_form_router.get(
    "/buscar-ultima-rodada/{serie}/{ano}",
    response_model=UltimaRodadaResponseSchema,
    summary="Busca a última rodada cadastrada",
    description="Retorna qual é a última rodada cadastrada."
)
async def get_ultima_rodada(
    serie: str,
    ano: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """Endpoint para buscar o número da última rodada cadastrada.
    Args:
        serie (str): Série do campeonato (ex.: 'A', 'B').
        ano (int): Ano do campeonato.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.   
    """
    try:
        return buscar_ultima_rodada_cadastrada(
            db=session,
            serie=serie,
            ano=ano,
            )
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar última rodadas: {str(e)}")
    finally:
        session.close()