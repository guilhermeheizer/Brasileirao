# Lógica para geração/validação de tokens JWT
from fastapi import Depends, HTTPException
from main import oauth2_scheme
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.dependencies import pegar_sessao
from app.models.usuario_models import Usuario


def criar_token(id_usuario: int, duracao_token=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Instalação do token – pip install PyJWT
    Josn Web Token – JWT: https://www.jwt.io/mmary_

    Args:
        id_usuario (int): ID do usuário para quem o token será criado.
        duracao_token (_type_, optional): Duração do token em minutos. Defaults to timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).

    Raises:
        ValueError: SECRET_KEY esta vazio ou não é uma string válida
        ValueError: ALGORITHM esta vazio ou não é uma string válida

    Returns:
        _type_: Retorna o token JWT como uma string.
    """
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    chave_secreta = settings.SECRET_KEY

    if not isinstance(chave_secreta, str) or not chave_secreta:
        raise ValueError("SECRET_KEY esta vazio ou não é uma string válida")

    if not isinstance(settings.ALGORITHM, str) or not settings.ALGORITHM:
        raise ValueError("ALGORITHM esta vazio ou não é uma string válida")

    dic_info = {"sub": str(id_usuario), "exp": data_expiracao} # Informação do token de acordo com o padrão JWT: https://www.jwt.io/
    token = jwt.encode(dic_info, chave_secreta, algorithm=settings.ALGORITHM)
    return token

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    """
    Verifica a validade do token JWT e retorna o usuário associado.
    Args:
        token (str, optional): Defaults to Depends(oauth2_scheme).
        session (Session, optional): Defaults to Depends(pegar_sessao).

    Raises:
        HTTPException: erro 500 - Chave secreta não configurada!
        HTTPException: erro 401 - Acesso não autorizado, verifique a validade do token!
        HTTPException: erro 401 - Acesso inválido!

    Returns:
        usuario: Retorna o usuário associado ao token válido.
    """
    if settings.SECRET_KEY is None:        
        raise HTTPException(status_code=500, detail="Chave secreta não configurada!")
    try:
        dic_info = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        id_usuario = dic_info.get("sub")
    except JWTError as erro:
        print(f"Erro ao decodificar o token: {erro}")
        raise HTTPException(status_code=401, detail="Acesso não autorizado, verifique a validade do token!")
    
    usuario = session.query(Usuario).filter(getattr(Usuario, "id") == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido!")
    
    return usuario