from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.estadio_models import Estadio
from app.models.cidade_models import Cidade
from app.models.rodada_models import Rodada
from app.schemas.rodada_schema import RodadaSchema
from app.schemas.estadio_schema import EstadioCreate, EstadioUpdate, EstadioCidadeOut
from typing import List, Optional
import re


def listar_todos_estadios(nome_estadio: Optional[str], nome_cidade: Optional[str], uf: Optional[str], session: Session) -> List[EstadioCidadeOut]:
    """Lista todos os estadios

    Args:
        nome_estadio (Optional[str]): Nome do estadio a ser buscado.
        nome_cidade (Optional[str]): Nome da cidade a ser buscada.
        uf (Optional[str]): UF da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Erro: 404 - Nenhum estadio encontrado.

    Returns:
        List[EstadioCidadeOut]: Representação dos estadios encontrados.
    """
    query = session.query(
        Estadio.__table__.c.est_id,
        Estadio.__table__.c.est_nome,
        Estadio.__table__.c.cidade_cid_id,
        Cidade.__table__.c.cid_nome.label("cid_nome"),
        Cidade.__table__.c.cid_uf.label("cid_uf"),
    ).join(Cidade, Estadio.__table__.c.cidade_cid_id == Cidade.__table__.c.cid_id)

    # Filtro opcional pelo nome do estadio
    if nome_estadio:
        query = query.filter(Estadio.__table__.c.est_nome.ilike(f"%{nome_estadio}%"))

    # Filtro opcional pela cidade
    if nome_cidade:
        query = query.filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome_cidade}%"))

    # Filtro opcional pela UF
    if uf:
        query = query.filter(Cidade.__table__.c.cid_uf == uf)

    query = query.order_by(Estadio.__table__.c.est_nome)

    if not query:
        raise HTTPException(status_code=404, detail="Nenhum estadio encontrado.")
    
    # Serializar os estadios no formato esperado
    return [
        EstadioCidadeOut(
            est_id=estadio.est_id,
            est_nome=estadio.est_nome,
            cidade_cid_id=estadio.cidade_cid_id,
            cidade_nome=estadio.cid_nome,
            cidade_uf=estadio.cid_uf,
        )
        for estadio in query
    ]


def criar_estadio(estadio: EstadioCreate, session: Session) -> EstadioCreate:
    """Criar registro na tabela de estadio

    Args:
        estadio (EstadioCreate): Dados do estadior a ser criado.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
    Raises:
        HTTPException: Erro: 404 - Estadio já cadastrado.
        HTTPException: Erro: 404 - Cidade não encontrada.

    Returns:
        EstadioCreate: Representação do estadio criado.
    """
    buscar_estadio_nome(True, estadio.est_nome, session)  # Verifica se o nome do estadio já existe

    cidade = (
            session.query(Cidade)
            .filter(Cidade.cid_id == estadio.cidade_cid_id)
            .first()
        )
    if not cidade:
            raise HTTPException(status_code=404, detail="Cidade não encontrada.")

    novo_estadio = Estadio(
        est_nome= re.sub(r'\s+', ' ', estadio.est_nome.strip()).title(), # Remove espaços extras
        cidade_cid_id=estadio.cidade_cid_id
    )
    session.add(novo_estadio)
    session.commit()
    session.refresh(novo_estadio)
    return EstadioCreate(**novo_estadio.as_dict())


def atualizar_estadio(estadio_atualizado: EstadioUpdate, session: Session) -> EstadioUpdate:
    estadio_db = session.query(Estadio).filter(Estadio.__table__.c.est_id == estadio_atualizado.est_id).first()

    if not estadio_db:
        raise HTTPException(status_code=404, detail="Estadio não encontrado.")


    if estadio_atualizado.cidade_cid_id:
        cidade = (
            session.query(Cidade)
            .filter(Cidade.cid_id == estadio_atualizado.cidade_cid_id)
            .first()
        )
        if not cidade:
            raise HTTPException(status_code=404, detail="Cidade não encontrada.")

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
    return EstadioUpdate(**estadio_db.as_dict())


def deletar_estadio(est_id: int, session: Session):
    estadio = session.query(Estadio).filter(Estadio.__table__.c.est_id == est_id).first()
    if not estadio:
        raise HTTPException(status_code=404, detail="Estádio não encontrado.")

    estadio_rodada = buscar_estadio_rodada(est_id, session)
    if estadio_rodada:
        raise HTTPException(status_code=404, detail=f"O jogo de {estadio_rodada.rod_data} da rodada {estadio_rodada.rod_rodada} está vinculado ao estádio. Exclusão não permitida.")

    session.delete(estadio)
    session.commit()
    return "Estádio excluído com sucesso."

def buscar_estadio_nome(retorna_exception: bool, nome: str, session: Session) -> Optional[EstadioCreate]:
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

    return EstadioCreate(**estadio.as_dict()) if estadio else None

def buscar_estadio_rodada(estadio_id: int, session: Session) -> Optional[RodadaSchema] | None:
    """
    Busca um estadio pelo ID na tabela rodada.

    Args:
        estadio_id (int): ID do estadio a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Returns:
        Optional[RodadaSchema]: Representação do estadio encontrado ou None se não encontrado.
    """
    # Busca pelo estadio no banco de dados
    rodada = session.query(Rodada).filter(Rodada.__table__.c.estadio_est_id == estadio_id).first()

    if rodada:
        return RodadaSchema(**rodada.as_dict()) if rodada else None

    return None

def buscar_estadio_por_cidade_id(retorna_exception: bool, cidade_id: int, session: Session) -> EstadioCreate | None:
    """
    Busca estadios pelo ID da cidade no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso nenhum estadio seja encontrado.
        cidade_id (int): ID da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso nenhum estadio seja encontrado.

    Returns:
        List[EstadioCreate]: Lista de estadios encontrados na cidade especificada.
    """
    # Busca pelos estadios no banco de dados
    estadio = session.query(Estadio).filter(Estadio.__table__.c.cidade_cid_id == cidade_id).first()

    if not estadio and retorna_exception:
        raise HTTPException(status_code=404, detail=f"Nenhum estadio encontrado para a cidade com ID '{cidade_id}'.")

    return EstadioCreate(**estadio.as_dict()) if estadio else None

def listar_estadios_paginadas(nome_estadio: Optional[str], nome_cidade: Optional[str], uf: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> List[EstadioCidadeOut]:
    """Listar os estadios pelo nome da estadio (opcional) com paginação

    Args:
        nome_estadio (Optional[str]): Nome do estadio a ser filtrado (opcional).
        nome_cidade (Optional[str]): Nome da cidade a ser filtrada (opcional).
        uf (Optional[str]): UF da cidade a ser filtrada (opcional).
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma estadio for encontrada.

    Returns:
        List[EstadioCidadeOut]: Lista de estadios no formato esperado na API.
    """
    query = session.query(
        Estadio.__table__.c.est_id,
        Estadio.__table__.c.est_nome,
        Estadio.__table__.c.cidade_cid_id,
        Cidade.__table__.c.cid_nome.label("cid_nome"),
        Cidade.__table__.c.cid_uf.label("cid_uf"),
    ).join(Cidade, Estadio.__table__.c.cidade_cid_id == Cidade.__table__.c.cid_id)

    # Filtro opcional pelo nome do estadio
    if nome_estadio:
        query = query.filter(Estadio.__table__.c.est_nome.ilike(f"%{nome_estadio}%"))

    # Filtro opcional pela cidade
    if nome_cidade:
        query = query.filter(Cidade.__table__.c.cid_nome.ilike(f"%{nome_cidade}%"))

    # Filtro opcional pela UF
    if uf:
        query = query.filter(Cidade.__table__.c.cid_uf == uf)

    query = query.order_by(Estadio.__table__.c.est_nome)
    
    # Paginação
    estadios = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()

    # Caso nenhum estadio seja encontrado
    if not estadios:
        raise HTTPException(status_code=404, detail="Nenhum estadio encontrado.")

    # Serializar os estadios no formato esperado
    estadios_schema = [
        EstadioCidadeOut(
            est_id=estadio.est_id,
            est_nome=estadio.est_nome,
            cidade_cid_id=estadio.cidade_cid_id,
            cidade_nome=estadio.cid_nome,
            cidade_uf=estadio.cid_uf,
        )
        for estadio in estadios
    ]

    return estadios_schema