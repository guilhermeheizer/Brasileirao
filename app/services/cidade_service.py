from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.cidade_schema import ResponseCidadesSchema, CidadesSchema
from app.models.cidade_models import Cidade
from typing import Optional
import re


def listar_todas_cidades(session: Session) -> ResponseCidadesSchema:
    """
    Serviço para listar todas as cidades no banco de dados.

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Quando não há cidades cadastradas no banco de dados.

    Returns:
        ResponseCidadesSchema: Contém uma lista de cidades no formato esperado na API.
    """
    # Obtemos todas as cidades do banco de dados
    cidades = session.query(Cidade).order_by(Cidade.__table__.c.cid_nome).all()

    # Validação quando não houver cidades cadastradas
    if not cidades:
        raise HTTPException(status_code=404, detail="Não há cidades cadastradas.")
    
    # Convertendo os objetos Cidade para o formato do schema
    cidades_schema = [CidadesSchema(**cidade.as_dict()) for cidade in cidades]

    return ResponseCidadesSchema(cidades=cidades_schema)

def criar_cidade(cidade: CidadesSchema, session: Session) -> CidadesSchema:
    """Criar registro na tabela de cidade

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
        cidade (CidadesSchema): Dados da cidade a ser criada.

    Returns:
        CidadesSchema: Dados da cidade criada.
    """
    if buscar_cidade_nome(False, cidade.cid_nome, session):  # Verifica se a cidade já existe
        raise HTTPException(status_code=404, detail=f"Cidade {cidade.cid_nome.title()} já cadastrada.")
    
    consiste_uf(cidade.cid_uf)  # Verifica se a UF é válida

    nova_cidade = Cidade(cid_nome=re.sub(r'\s+', ' ', cidade.cid_nome.strip()).title(), # Remove espaços extras
                         cid_uf=cidade.cid_uf.upper()) 

    session.add(nova_cidade)
    session.commit()
    session.refresh(nova_cidade)
    return CidadesSchema(**nova_cidade.as_dict())


def atualizar_cidade(cidade_id: int, cidade_atualizada: CidadesSchema, session: Session) -> CidadesSchema:
    """Atualizar registro na tabela de cidade

    Args:
        cidade_id (int): ID da cidade a ser atualizada.
        cidade_atualizada (CidadesSchema): Dados atualizados da cidade.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se a cidade não for encontrada no banco de dados.

    Returns:
        CidadesSchema: Dados da cidade atualizada.
    """
    cidade_db = session.query(Cidade).filter(Cidade.cid_id == cidade_id).first()

    if not cidade_db:
        raise HTTPException(status_code=404, detail="Cidade não encontrada.")
    
    if cidade_atualizada.cid_nome:
        # Normaliza o nome do clube (remove espaços duplicados e aplica Title Case)
        nome_normalizado = re.sub(r'\s+', ' ', cidade_atualizada.cid_nome.strip()).title()

        cidade_existente = buscar_cidade_nome(False, nome_normalizado, session)
        if cidade_existente and cidade_existente.cid_nome == nome_normalizado:
            raise HTTPException(status_code=404, detail=f"Cidade {cidade_atualizada.cid_nome.strip().title()} já cadastrada.")
        
        cidade_db.cid_nome = nome_normalizado

    if cidade_atualizada.cid_uf:
        consiste_uf(cidade_atualizada.cid_uf)  # Verifica se a UF é válida
        cidade_db.cid_uf = cidade_atualizada.cid_uf.upper()

    if cidade_atualizada:
        session.commit()
        session.refresh(cidade_db)

    return CidadesSchema(**cidade_db.as_dict())

def deletar_cidade(cidade_id: int, session: Session):
    """Deletar registro na tabela de cidade

    Args:
        cidade_id (int): ID da cidade a ser deletada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se a cidade não for encontrada no banco de dados.
    """
    cidade_db = session.query(Cidade).filter(Cidade.cid_id == cidade_id).first()
    if not cidade_db:
        raise HTTPException(status_code=404, detail="Cidade não encontrada.")
    
    session.delete(cidade_db)
    session.commit()
    return "Cidade excluida com sucesso"


def listar_cidades_paginadas(nome: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> ResponseCidadesSchema:
    """Listar as cidades pelo nome da cidade (opcional) com paginação

    Args:
        nome (Optional[str]): Nome da cidade a ser filtrada (opcional).
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma cidade for encontrada.

    Returns:
        ResponseCidadesSchema: Lista de cidades no formato esperado na API.
    """
    query = session.query(Cidade)
    if nome:
        query = query.filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome}%"))

    query = query.order_by(Cidade.__table__.c.cid_nome)
        
    cidades = (
        query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()
    )
    
    if not cidades:
        raise HTTPException(status_code=404, detail="Nenhuma cidade encontrada.")
    
    cidades_schema = [CidadesSchema(**cidade.as_dict()) for cidade in cidades]
    
    return ResponseCidadesSchema(cidades=cidades_schema)


def buscar_cidade_nome(retorna_exception: bool, nome: str, session: Session) -> Optional[CidadesSchema]:
    """
    Busca uma cidade pelo nome no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        nome (str): Nome da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadesSchema]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados (ignora case com ilike)
    cidade = session.query(Cidade).filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome}%")).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com nome '{nome}' não encontrada.")

    return CidadesSchema(**cidade.as_dict()) if cidade else None

def buscar_cidade_id(retorna_exception: bool, cidade_id: int, session: Session) -> Optional[CidadesSchema]:
    """
    Busca uma cidade pelo ID no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        cidade_id (int): ID da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadesSchema]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados
    cidade = session.query(Cidade).filter(Cidade.cid_id == cidade_id).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com ID '{cidade_id}' não encontrada.")

    return CidadesSchema(**cidade.as_dict()) if cidade else None

def buscar_cidade_uf(retorna_exception: bool, uf: str, session: Session) -> Optional[CidadesSchema]:
    """
    Busca uma cidade pela UF no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        uf (str): UF da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadesSchema]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados (ignora case com ilike)
    cidade = session.query(Cidade).filter(Cidade.__table__.c.cid_uf.ilike(f"%{uf.upper()}%")).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com UF '{uf}' não encontrada.")

    return CidadesSchema(**cidade.as_dict()) if cidade else None

def consiste_uf (uf: str) -> bool:
    """Verifica se a UF é válida.

    Args:
        uf (str): UF a ser verificada.

    Returns:
        bool: True se a UF for válida, False caso contrário.
    """
    ufs_validas = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    if uf.upper() in ufs_validas:
        return True
    else:
        raise HTTPException(status_code=404, detail=f"UF {uf} inválida.")