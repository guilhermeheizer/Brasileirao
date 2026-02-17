from fastapi import APIRouter, Depends
from app.schemas.usuario_schema import UsuarioSchema 
from app.core.dependencies import pegar_sessao
from app.services.usuario_service import criar_usuario_service

usuario_router = APIRouter(tags=["usuario"])

# Vamos usar decoradores para definir as rotas relacionadas a autenticação
@usuario_router.get("/")   
async def home():
    """
    Esta função simula uma rota de autenticação.
    Returns:
        _type_: _description_
    """
    return {"message": "acessou rota de autenticação", "autenticado": False} 

@usuario_router.post("/incluir", response_model=UsuarioSchema)
async def criar_usuario(usuario_schema: UsuarioSchema, session=Depends(pegar_sessao)):
    """
    Esta função simula a criação de uma conta de usuário.
    Returns:
        _type_: _description_
    """
    resultado = criar_usuario_service(usuario_schema=usuario_schema, session=session)
    return resultado
