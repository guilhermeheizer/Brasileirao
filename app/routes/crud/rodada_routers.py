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
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseCriarRodadaSchema
from app.services.rodada_service import (
    criar_rodada,
    atualizar_rodada,
    deletar_rodada,
    obter_rodada
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