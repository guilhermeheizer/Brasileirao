from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.cidade_schema import CidadeCreate, CidadeOut, CidadeUpdate
from app.models.cidade_models import Cidade
from app.services.clube_service import buscar_clube_por_cidade_id
from app.services.estadio_service import buscar_estadio_por_cidade_id
from typing import Optional, List
import re


def listar_todas_cidades(nome: Optional[str], uf: Optional[str], session: Session) -> List[CidadeOut]:
    """
    Serviço para listar todas as cidades no banco de dados.

    Args:
        nome (Optional[str]): Nome da cidade a ser filtrada (opcional).
        uf (Optional[str]): UF da cidade a ser filtrada (opcional).
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Quando não há cidades cadastradas no banco de dados.

    Returns:
        CidadeCreate: Contém uma lista de cidades no formato esperado na API.
    """
    # Obtemos todas as cidades do banco de dados
    query = session.query(Cidade)
    if nome:
        nome = (
            nome.strip()
            .replace("%", "\\%")
            .replace("_", "\\_")
        )

        query = query.filter(
            Cidade.cid_nome.ilike(
                f"%{nome}%",
                escape="\\"
            )
        )

    if uf:
        uf = uf.strip().upper()

        query = query.filter(
            Cidade.cid_uf == uf
        )

    query = query.order_by(
        Cidade.cid_nome
    ).all()

    # Validação quando não houver cidades cadastradas
    if not query:
        raise HTTPException(status_code=404, detail="Não há cidades cadastradas.")
    
    return [
        CidadeOut(
                cid_id = c.cid_id,
                cid_nome = c.cid_nome,
                cid_uf = c.cid_uf,
        )
        for c in query
    ]

def criar_cidade(cidade: CidadeCreate, session: Session) -> CidadeCreate:
    """Criar registro na tabela de cidade

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
        cidade (CidadeCreate): Dados da cidade a ser criada.

    Returns:
        CidadeCreate: Dados da cidade criada.
    """
    if buscar_cidade_nome(False, cidade.cid_nome, session):  # Verifica se a cidade já existe
        raise HTTPException(status_code=404, detail=f"Cidade {cidade.cid_nome.title()} já cadastrada.")
    
    consiste_uf(cidade.cid_uf)  # Verifica se a UF é válida

    nova_cidade = Cidade(cid_nome=re.sub(r'\s+', ' ', cidade.cid_nome.strip()).title(), # Remove espaços extras
                         cid_uf=cidade.cid_uf.upper()) 

    session.add(nova_cidade)
    session.commit()
    session.refresh(nova_cidade)
    return CidadeCreate(**nova_cidade.as_dict())


def atualizar_cidade(cidade_atualizada: CidadeUpdate, session: Session) -> CidadeUpdate:
    """Atualizar registro na tabela de cidade

    Args:
        cidade_atualizada (CidadeUpdate): Dados atualizados da cidade.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se a cidade não for encontrada no banco de dados.

    Returns:
        CidadeUpdate: Dados da cidade atualizada.
    """
    cidade_db = session.query(Cidade).filter(Cidade.cid_id == cidade_atualizada.cid_id).first()

    if not cidade_db:
        raise HTTPException(status_code=404, detail="Cidade não encontrada.")
    
    if cidade_atualizada.cid_nome:
        # Normaliza o nome do clube (remove espaços duplicados e aplica Title Case)
        nome_normalizado = re.sub(r'\s+', ' ', cidade_atualizada.cid_nome.strip()).title()

        cidade_existente = buscar_cidade_nome(False, nome_normalizado, session)
        if cidade_existente and cidade_existente.cid_nome == nome_normalizado and cidade_existente.cid_id != cidade_atualizada.cid_id:
            raise HTTPException(status_code=404, detail=f"Cidade {cidade_atualizada.cid_nome.strip().title()} já cadastrada.")
        
        cidade_db.cid_nome = nome_normalizado

    if cidade_atualizada.cid_uf:
        consiste_uf(cidade_atualizada.cid_uf)  # Verifica se a UF é válida
        cidade_db.cid_uf = cidade_atualizada.cid_uf.upper()

    if cidade_atualizada:
        session.commit()
        session.refresh(cidade_db)

    return CidadeUpdate(**cidade_db.as_dict())

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
    
    clube_associado_cidade = buscar_clube_por_cidade_id(False, cidade_id, session)
    if clube_associado_cidade:
        raise HTTPException(status_code=404, detail=f"Não é possível excluir a cidade pois existe clube associado a ela: {clube_associado_cidade.clu_nome}.")

    estadio_associado_cidade = buscar_estadio_por_cidade_id(False, cidade_id, session)
    if estadio_associado_cidade:
        raise HTTPException(status_code=404, detail=f"Não é possível excluir a cidade pois existe estádio associado a ela: {estadio_associado_cidade.est_nome}.")
    
    session.delete(cidade_db)
    session.commit()
    return "Cidade excluida com sucesso"


def listar_cidades_paginadas(nome: Optional[str], uf: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> List[CidadeOut]:
    """Listar as cidades pelo nome da cidade (opcional) com paginação

    Args:
        nome (Optional[str]): Nome da cidade a ser filtrada (opcional).
        uf (Optional[str]): UF da cidade a ser filtrada (opcional).
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma cidade for encontrada.

    Returns:
        List[CidadeCreate]: Lista de cidades no formato esperado na API.
    """
    query = session.query(Cidade)
    if nome:
        query = query.filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome}%"))

    if uf:
        query = query.filter(Cidade.__table__.c.cid_uf.ilike(f"%{uf.upper()}%"))

    query = query.order_by(Cidade.__table__.c.cid_nome)
        
    cidades = (
        query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()
    )
    
    if not cidades:
        raise HTTPException(status_code=404, detail="Nenhuma cidade encontrada.")
    
    return [
        CidadeOut(
            cid_id = c.cid_id,
            cid_nome = c.cid_nome,
            cid_uf = c.cid_uf,
        )
        for c in cidades
    ]


def buscar_cidade_nome(retorna_exception: bool, nome: str, session: Session) -> Optional[CidadeOut]:
    """
    Busca uma cidade pelo nome no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        nome (str): Nome da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadeCreate]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados (ignora case com ilike)
    cidade = session.query(Cidade).filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome}%")).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com nome '{nome}' não encontrada.")

    return CidadeOut(**cidade.as_dict()) if cidade else None

def buscar_cidade_id(retorna_exception: bool, cidade_id: int, session: Session) -> Optional[CidadeOut]:
    """
    Busca uma cidade pelo ID no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        cidade_id (int): ID da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadeOut]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados
    cidade = session.query(Cidade).filter(Cidade.cid_id == cidade_id).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com ID '{cidade_id}' não encontrada.")

    return CidadeOut(**cidade.as_dict()) if cidade else None

def buscar_cidade_uf(retorna_exception: bool, uf: str, session: Session) -> Optional[CidadeOut]:
    """
    Busca uma cidade pela UF no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a cidade não seja encontrada.
        uf (str): UF da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a cidade não seja encontrada.

    Returns:
        Optional[CidadeCreate]: Representação da cidade encontrada ou None se não encontrada.
    """
    # Busca pela cidade no banco de dados (ignora case com ilike)
    cidade = session.query(Cidade).filter(Cidade.__table__.c.cid_uf.ilike(f"%{uf.upper()}%")).first()

    if not cidade:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Cidade com UF '{uf}' não encontrada.")

    return CidadeOut(**cidade.as_dict()) if cidade else None

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