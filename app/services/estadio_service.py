from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.estadio_models import Estadio
from app.models.cidade_models import Cidade
from app.schemas.estadio_schema import ResponseEstadioSchema, EstadioSchema, EstadioCidadeSchema, ResponseEstadioCidadeSchema
from app.services.cidade_service import buscar_cidade_id
from typing import List
from typing import Optional
import re


def listar_todos_estadios(session: Session) -> ResponseEstadioSchema:
    """Lista todos os estadios

    Args:
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Erro: 404 - Nenhum estadio encontrado.

    Returns:
        ResponseEstadioSchema: Representação dos estadios encontrados.
    """
    estadios = session.query(Estadio).order_by(Estadio.__table__.c.est_nome).all()
    if not estadios:
        raise HTTPException(status_code=404, detail="Nenhum estadio encontrado.")
    
    estadios_schema = [EstadioSchema(**estadio.as_dict()) for estadio in estadios]
    return ResponseEstadioSchema(estadios=estadios_schema)


def criar_estadio(estadio: EstadioSchema, session: Session) -> EstadioSchema:
    """Criar registro na tabela de estadio

    Args:
        estadio (EstadioSchema): Dados do estadior a ser criado.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
    Raises:
        HTTPException: Erro: 404 - Estadio já cadastrado.
        HTTPException: Erro: 404 - Cidade não encontrada.

    Returns:
        EstadioSchema: Representação do estadio criado.
    """
    buscar_estadio_nome(True, estadio.est_nome, session)  # Verifica se o nome do estadio já existe
    buscar_estadio_id(True, estadio.est_id, session)  # Verifica se a iddo estadio já existe
    buscar_cidade_id(True, estadio.cidade_cid_id, session)  # Verifica se a cidade existe

    novo_estadio = Estadio(
        est_nome= re.sub(r'\s+', ' ', estadio.est_nome.strip()).title(), # Remove espaços extras
        cidade_cid_id=estadio.cidade_cid_id
    )
    session.add(novo_estadio)
    session.commit()
    session.refresh(novo_estadio)
    return EstadioSchema(**novo_estadio.as_dict())


def atualizar_estadio(est_id: int, estadio_atualizado: EstadioSchema, session: Session) -> EstadioSchema:
    estadio_db = session.query(Estadio).filter(Estadio.__table__.c.est_id == est_id).first()

    if not estadio_db:
        raise HTTPException(status_code=404, detail="Estadio não encontrado.")


    if estadio_atualizado.cidade_cid_id:
        buscar_cidade_id(True, estadio_atualizado.cidade_cid_id, session)  # Verifica se a cidade existe

    # Atualização condicional dos campos (apenas os fornecidos pelo cliente)
    if estadio_atualizado.est_nome:
        # Normaliza o nome do estadio (remove espaços duplicados e aplica Title Case)
        nome_normalizado = re.sub(r'\s+', ' ', estadio_atualizado.est_nome.strip()).title()

        # Verifica se já existe outro estadio com o mesmo nome
        estadio_existente = buscar_estadio_nome(False, nome_normalizado, session)
        if estadio_existente and estadio_existente.est_nome != nome_normalizado:
            raise HTTPException(status_code=404, detail=f"Já existe um estadio com o nome '{nome_normalizado}.'")

        estadio_db.est_nome = nome_normalizado  # Atualiza o nome no banco

    if estadio_atualizado.cidade_cid_id:
        # Atualiza o ID da cidade associada
        estadio_db.cidade_cid_id = estadio_atualizado.cidade_cid_id

    # Commit das alterações e atualização do estado do objeto
    if estadio_atualizado:
        session.commit()
        session.refresh(estadio_db)

    # Retorna o esquema atualizado
    return EstadioSchema(**estadio_db.as_dict())


def deletar_estadio(est_id: int, session: Session):
    estadio = session.query(Estadio).filter(Estadio.__table__.c.est_id == est_id).first()
    if not estadio:
        raise HTTPException(status_code=404, detail="Estadio não encontrado.")

    session.delete(estadio)
    session.commit()
    return "Estadio excluído com sucesso."

def buscar_estadio_nome(retorna_exception: bool, nome: str, session: Session) -> Optional[EstadioSchema]:
    """
    Busca uma estadio pelo nome no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a estadio não seja encontrada.
        nome (str): Nome da estadio a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a estadio não seja encontrada.

    Returns:
        Optional[EstadiosSchema]: Representação da estadio encontrada ou None se não encontrada.
    """

    # Busca pela estadio no banco de dados (ignora case com ilike)
    estadio = session.query(Estadio).filter(Estadio.__table__.c.est_nome.ilike(f"%{nome}%")).first()
 
    if estadio:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Já existe estadio com nome '{nome}' informado.")

    return EstadioSchema(**estadio.as_dict()) if estadio else None

def buscar_estadio_id(retorna_exception: bool, estadio_id: int, session: Session) -> Optional[EstadioSchema]:
    """
    Busca uma estadio pelo ID no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a estadio não seja encontrado.
        estadio_id (int): ID do estadio a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a estadio não seja encontrado.

    Returns:
        Optional[EstadioSchema]: Representação do estadio encontrado ou None se não encontrado.
    """
    # Busca pelo estadio no banco de dados
    estadio = session.query(Estadio).filter(Estadio.__table__.c.est_id == estadio_id).first()

    if estadio:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Estadio com sigla '{estadio_id}' já existe.")
    return EstadioSchema(**estadio.as_dict()) if estadio else None


def listar_estadios_paginadas(nome: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> ResponseEstadioCidadeSchema:
    """Listar os estadios pelo nome da estadio (opcional) com paginação

    Args:
        nome (Optional[str]): Nome do estadio a ser filtrado (opcional).
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma estadio for encontrada.

    Returns:
        ResponseEstadiosSchema: Lista de estadios no formato esperado na API.
    """
    query = session.query(
        Estadio.__table__.c.est_id,
        Estadio.__table__.c.est_nome,
        Estadio.__table__.c.cidade_cid_id,
        Cidade.__table__.c.cid_nome.label("cid_nome"),
        Cidade.__table__.c.cid_uf.label("cid_uf"),
    ).join(Cidade, Estadio.__table__.c.cidade_cid_id == Cidade.__table__.c.cid_id)

    # Filtro opcional pelo nome do estadio
    if nome:
        query = query.filter(Estadio.__table__.c.est_nome.ilike(f"%{nome}%"))

    query = query.order_by(Estadio.__table__.c.est_nome)
    
    # Paginação
    estadios = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()

    # Caso nenhum estadio seja encontrado
    if not estadios:
        raise HTTPException(status_code=404, detail="Nenhum estadio encontrado.")

    # Serializar os estadios no formato esperado
    estadios_schema = [
        EstadioCidadeSchema(
            est_id=estadio.est_id,
            est_nome=estadio.est_nome,
            cidade_cid_id=estadio.cidade_cid_id,
            cidade_nome=estadio.cid_nome,
            cidade_uf=estadio.cid_uf,
        )
        for estadio in estadios
    ]

    return ResponseEstadioCidadeSchema(estadios=estadios_schema)