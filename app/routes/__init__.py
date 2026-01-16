# from fastapi import APIRouter
# from app.routes.crud.cidade_routes import cidade_router
# from app.routes.crud.estado import router as estado_router
# from app.routes.crud.clube import router as clube_router
# from app.routes.crud.rodada import router as rodada_router
# from app.routes.crud.classificacao import router as classificacao_router
# from app.routes.crud.usuario import router as usuario_router
# from app.routes.endpoints.login import router as login_router
# from app.routes.endpoints.cadastro import router as cadastro_router

# Criação de um roteador principal para agrupar as rotas
# api_router = APIRouter()

# Incluindo todas as rotas no roteador principal
# api_router.include_router(cidade_router, prefix="/cidade", tags=["Cidade"])
# api_router.include_router(estado_router, prefix="/estado", tags=["Estado"])
# api_router.include_router(clube_router, prefix="/clube", tags=["Clube"])
# api_router.include_router(rodada_router, prefix="/rodada", tags=["Rodada"])
# api_router.include_router(classificacao_router, prefix="/classificacao", tags=["Classificação"])
# api_router.include_router(usuario_router, prefix="/usuario", tags=["Usuário"])
# api_router.include_router(login_router, prefix="/login", tags=["Login"])
# api_router.include_router(cadastro_router, prefix="/cadastro", tags=["Cadastro"])