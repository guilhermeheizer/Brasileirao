from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseRodadasSchema
from app.services.form.form_cadastra_rodada_service import criar_rodada
from typing import List

# Instância do APIRouter para organizar as rotas relacionadas ao formulário de cadastro de rodadas
rodada_form_router = APIRouter(tags=["cadastra rodada"])


@rodada_form_router.post("/", response_model=ResponseRodadasSchema)
def criar_rodadas(
    rod_serie: str,
    rod_ano: int,
    jogos_data: List[CriarRodadaSchema],
    session: Session = Depends(pegar_sessao),
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
        ResponseRodadasSchema: Retorna os dados das rodadas criadas.
    """
    try:
        return criar_rodada(db=session, rod_serie=rod_serie, rod_ano=rod_ano, jogos_data=jogos_data, session=session)
    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:
        session.close()