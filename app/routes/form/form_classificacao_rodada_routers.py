from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import pegar_sessao, verificar_token
from app.services.form.form_classificacao_rodada_service import copia_classificacao_por_rodada

router_classificacao_rodada = APIRouter(tags=["copiar classificacao por rodada"])

@router_classificacao_rodada.post("/copiar/{serie}/{ano}/{rodada}")
def copiar_classificacao_por_rodada(
    serie: str,
    ano: int,
    rodada: str,
    db: Session = Depends(get_db),
    usuario = Depends(verificar_token)
):
    """Endpoint para copiar a classificação geral de uma rodada específica.
       Executar este endpoint quando a rodada finalizar, ou seja, todos os jogos da rodada tiverem sido concluídos, 
       para salvar a classificação geral daquela rodada antes de iniciar a próxima.

    Args:        
        serie (str): Série do campeonato (ex.: 'A', 'B').
        ano (int): Ano do campeonato.
        rodada (str): Rodada a ser copiada (ex.: '1', '2', '3', etc.).
        db (Session): Sessão do SQLAlchemy gerenciada pelo FastAPI via `Depends(get_db)`.
        usuario: Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.    
    """
    try:
        # Chama o serviço para copiar classificação
        copia_classificacao_por_rodada(db, rodada, ano, serie)
        return {"message": f"Classificação da rodada {rodada} salva com sucesso!"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao copiar classificação por rodada: {str(e)}"
        )