from sqlalchemy.orm import Session
from app.models.usuario_models import Usuario
from app.utils.token import criar_token
from fastapi import HTTPException
from datetime import timedelta
from fastapi import HTTPException
from hashlib import sha256
from app.models.usuario_models import Usuario


def autenticar_usuario(session: Session, email: str, senha: str) -> Usuario:
    """
    Autentica o usuário, verificando e-mail e senha.
    
    Args:
        session (Session): Sessão do banco de dados.
        email (str): E-mail do usuário.
        senha (str): Senha fornecida pelo usuário.

    Returns:
        Usuario: Usuário autenticado se as credenciais estiverem corretas.

    Raises:
        HTTPException: Erro 400 - Login inválido ou senha!
    """
    usuario = session.query(Usuario).filter(getattr(Usuario, "email") == email).first()
    
    if not usuario or getattr(usuario, "senha", None) != sha256(senha.encode()).hexdigest():
        raise HTTPException(status_code=400, detail="Login inválido ou senha!")
    # else:
    #     access_token = criar_token(getattr(usuario, "id"))
    #     return {
    #         "access_token": access_token,
    #         "token_type": "Bearer"
    #     }
    
    return usuario

def gerar_tokens(usuario: Usuario) -> dict:
    """
    Gera tokens de acesso e atualização para o usuário autenticado.
    
    Args:
        usuario (Usuario): Usuário autenticado.

    Returns:
        dict: Dicionário contendo os tokens.
    """
    usuario_id = getattr(usuario, "id")
    access_token = criar_token(usuario_id)  # Token de acesso (curta duração)
    refresh_token = criar_token(usuario_id, duracao_token=timedelta(days=7))  # Token de atualização (7 dias)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

