"""
form_classificacao_rodada_routers.py

Este módulo define a rota da API para copiar a classificação geral de uma rodada específica do Campeonato Brasileiro.
Utiliza FastAPI para expor endpoint de cópia da classificação ao final de cada rodada.

Funcionalidade principal:
- Copiar e salvar a classificação geral de uma rodada ao término de todos os jogos

O endpoint utiliza injeção de dependências para sessão do banco e autenticação de usuário.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import pegar_sessao, verificar_token
from app.services.form.form_classificacao_rodada_service import copia_classificacao_por_rodada, recalcular_classificacao

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

    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:        
        db.close()

@router_classificacao_rodada.post("/recalcular/{serie}/{ano}")
def recalcular_classificacao_geral(
    serie: str,
    ano: int,
    db: Session = Depends(get_db),
    usuario = Depends(verificar_token)
):
    """Endpoint para recalcular a classificação geral de uma rodada específica.

    Args:        
        serie (str): Série do campeonato (ex.: 'A', 'B').
        ano (int): Ano do campeonato.
        db (Session): Sessão do SQLAlchemy gerenciada pelo FastAPI via `Depends(get_db)`.
        usuario: Objeto do usuário autenticado, gerenciado pelo middleware `verificar_token`.    
    """
    try:
        # Chama o serviço para recalcular classificação
        recalcular_classificacao(db, serie, ano)
        return {"message": f"Classificação da série {serie}/{ano} recalculada com sucesso!"}

    except HTTPException as ex:
        log_erro = f"Erro: {ex.detail}"
        raise HTTPException(status_code=ex.status_code, detail=log_erro)
    except Exception as e:
        # Captura outros erros inesperados e gera um erro 500
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
    finally:        
        db.close()