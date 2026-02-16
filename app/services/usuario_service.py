from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.models.usuario_models import Usuario
from app.schemas.usuario_schema import UsuarioSchema
from app.core.dependencies import pegar_sessao
from hashlib import sha256

def criar_usuario_service(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Serviço para criar um novo usuário no banco de dados.

    Args:
        email (str): Email do novo usuário
        senha (str): Senha do novo usuário
        nome (str): Nome do novo usuário
        session (Session): Sessão ativa do banco de dados

    Returns:
        dict: Mensagem indicando sucesso ou erro na criação do usuário.
    """
    # Verifica se o email já está registrado
    usuario = session.query(Usuario).filter(getattr(Usuario, "email") == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=404, detail="Email já cadastrado!")

    # Cria uma instância de usuário
    hash_senha = sha256(usuario_schema.senha.encode()).hexdigest()
    novo_usuario = Usuario(
            usuario_schema.nome,
            usuario_schema.email,
            hash_senha,
            usuario_schema.ativo if usuario_schema.ativo is not None else False,
            usuario_schema.admin if usuario_schema.admin is not None else False
    )

    # Adiciona o novo usuário ao banco de dados
    try:
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário criado com sucesso!"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")