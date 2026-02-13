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

@rodada_router.post("/criar-rodada", response_model=ResponseCriarRodadaSchema)
async def criar_rodada_endpoint(
    rodada: CriarRodadaSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    try:
        nova_rodada = criar_rodada(rodada, session)
        return nova_rodada
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))