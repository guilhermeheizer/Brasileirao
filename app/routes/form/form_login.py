from fastapi import APIRouter, Depends
from app.schemas.form_login_schema import LoginSchema
from app.services.login_service import gerar_tokens
from app.services.login_service import gerar_tokens
from app.core.dependencies import pegar_sessao
from app.services.login_service import autenticar_usuario, gerar_tokens
from app.schemas.form_login_schema import LoginSchema
from app.utils.token import criar_token, verificar_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.usuario_models import Usuario
from datetime import timedelta


login_router = APIRouter(tags=["login"])

@login_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
    Esta função simula o login de um usuário.
    Returns:
        _type_: _description_
    """
    usuario = autenticar_usuario(session, login_schema.email, login_schema.senha)
    tokens = gerar_tokens(usuario)
    return tokens
    # usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    # if not usuario:
    #     raise HTTPException(status_code=400, detail="Usuário não encontrado ou login inválido!")
    # else:
    #     access_token = criar_token(getattr(usuario, "id"))
    #     refresh_token = criar_token(getattr(usuario, "id"), duracao_token=timedelta(days=7))  # Token de atualização com duração de 1 dia (1440 minutos) 
    #     return {
    #         "access_token": access_token,
    #         "refresh_token": refresh_token,
    #         "token_type": "Bearer"
    #     }

@login_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """
    Esta função simula o login de um usuário.
    Returns:
        _type_: _description_
    """
    usuario = autenticar_usuario(session, dados_formulario.username, dados_formulario.password)
    usurio_id = getattr(usuario, "id")
    token = criar_token(usurio_id)
    return {
            "access_token": token,
            "token_type": "Bearer"
        }
    # usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    # # logging.debug(f"Usuário encontrado: {usuario}")
    # if not usuario:
    #     raise HTTPException(status_code=400, detail="Usuário não encontrado ou login inválido!")
    # else:
    #     access_token = criar_token(getattr(usuario, "id"))
    #     return {
    #         "access_token": access_token,
    #         "token_type": "Bearer"
    #     }

@login_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    """
    Esta função simula a renovação do token de acesso.
    Returns:
        _type_: _description_
    """
    acess_token = criar_token(getattr(usuario, "id"))
    return {
        "access_token": acess_token,
        "token_type": "Bearer"
    }