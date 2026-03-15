"""
rodada_routers.py

Este módulo define as rotas da API relacionadas às operações de rodada do Campeonato Brasileiro.
Utiliza FastAPI para expor endpoints de inclusão, atualização, deleção e consulta de rodadas.

Principais funcionalidades:
- Endpoint para inclusão de rodada
- (Estrutura para endpoints de atualização, deleção e consulta)
- Integração com autenticação de usuário e sessão do banco

Endpoints principais:
- POST /incluir: Cria uma nova rodada
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseAlterarRodadaSchema, ResponseCriarRodadaSchema, AlterarJogoRodadaSchema, ResponseCriarRodadaSchema
from app.services.rodada_service import (
    criar_rodada,
    atualizar_jogo_rodada,
    deletar_rodada
)


rodada_router = APIRouter(tags=["rodada"])

@rodada_router.post("/incluir", response_model=ResponseCriarRodadaSchema)
async def criar_rodada_endpoint(
    rodada: CriarRodadaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """
    Endpoint para criar uma nova rodada.
    Recebe os dados da rodada, valida e insere no banco de dados.
    Requer autenticação de usuário.
    Args:
        rodada (CriarRodadaSchema): Dados da rodada a ser criada.
        session (Session): Sessão do banco de dados (injeção de dependência).
        usuario (Usuario): Usuário autenticado (injeção de dependência).
    Returns:
        ResponseCriarRodadaSchema: Dados da rodada criada.
    Raises:
        HTTPException: Em caso de erro de validação ou banco de dados.
    """
    try:
        nova_rodada = criar_rodada(rodada, session)
        return nova_rodada
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@rodada_router.put("/atualizar_jogo/{serie}/{ano}/{rodada_numero}/{sequencia}", response_model=ResponseAlterarRodadaSchema)
async def atualizar_jogo_rodada_endpoint(
    serie: str,
    ano: int,
    rodada_numero: int,
    sequencia: int,
    jogo_atualizado: AlterarJogoRodadaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Atualiza os dados de um jogo específico em uma rodada.

    Args:
        serie (str): Informe a série do jogo a ser atualizado.
        ano (int): Informe o ano do jogo a ser atualizado.
        rodada_numero (int): Informe o número da rodada do jogo a ser atualizado.
        sequencia (int): Informe a sequência do jogo a ser atualizado.
        jogo_atualizado (CriarRodadaSchema): Dados atualizados do jogo.
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).
        usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a atualização do jogo.

    Returns:
        ResponseCriarRodadaSchema: O jogo atualizado.
    """
    try:
        jogo_atualizado = atualizar_jogo_rodada(serie, ano, rodada_numero, sequencia, jogo_atualizado, session)
        return jogo_atualizado
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()

@rodada_router.delete("/deletar/{serie}/{ano}/{rodada_numero}/{sequencia}")
async def deletar_rodada_endpoint(
    serie: str,
    ano: int,
    rodada_numero: int,
    sequencia: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):
    """
    Remove uma rodada com base na série, ano, número da rodada e sequência.

    Args:
    series (str): Informe a série da rodada a ser deletada.
    ano (int): Informe o ano da rodada a ser deletada.
    rodada_numero (int): Informe o número da rodada a ser deletada.
    sequencia (int): Informe a sequência da rodada a ser deletada.
    session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                 via dependência de injeção (Depends(pegar_sessao)).
    usuario (Usuario, optional): Defaults to Depends(verificar_token).

    Raises:
    HTTPException: Lançada se ocorrer um erro durante a exclusão da rodada.

    Returns:
    ResponseCriarRodadaSchema: A rodada excluída.
    """
    try:
        return deletar_rodada(serie, ano, rodada_numero, sequencia, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro) 
    finally:
        session.close()