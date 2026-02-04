# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.core.dependencies import pegar_sessao, verificar_token
# from app.models.usuario_models import Usuario
# from app.schemas.rodada_schema import CriarRodadaSchema, ResponseRodadasSchema
# from app.services.rodada_service import carga_tabela
# from typing import List

# # Instância do APIRouter para organizar as rotas relacionadas ao formulário de cadastro de rodadas
# rodada_form_router = APIRouter(tags=["cadastra rodada"])


# @rodada_form_router.post("/", response_model=ResponseRodadasSchema)
# def carregar_tabelas(
#     rod_serie: str,
#     rod_ano: int,
#     session: Session = Depends(pegar_sessao),
# ):
#     """
#     Carrega tabelas a partir de um json
#     """
#     try:
#         return carga_tabela(db=session, rod_serie=rod_serie, rod_ano=rod_ano, session=session)
#     except HTTPException as ex:
#         log_erro = f"Erro: {ex.detail}"
#         raise HTTPException(status_code=ex.status_code, detail=log_erro)
#     except Exception as e:
#         # Captura outros erros inesperados e gera um erro 500
#         raise HTTPException(status_code=500, detail=f"Erro interno ao criar rodadas: {str(e)}")
#     finally:
#         session.close()