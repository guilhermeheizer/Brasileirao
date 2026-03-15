from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError
import jwt
from app.core.config import settings
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.usuario_models import Usuario

''' Módulo de dependências para autenticação e acesso ao banco de dados 
   Define as dependências para obter a sessão do banco de dados e verificar o token de autenticação.
   A função 'verificar_token' decodifica o token JWT, extrai o ID do usuário e verifica se o usuário existe no banco de dados.
   Se o token for inválido ou o usuário não existir, uma exceção HTTP é levantada.'''
pegar_sessao = get_db

auth2_scheme = OAuth2PasswordBearer(tokenUrl="login/login-form")

def verificar_token(token: str = Depends(auth2_scheme), session: Session = Depends(pegar_sessao)):
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
