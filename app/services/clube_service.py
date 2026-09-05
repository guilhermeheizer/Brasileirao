from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.clube_models import Clube
from app.models.cidade_models import Cidade
from app.models.rodada_models import Rodada
from app.schemas.clube_schema import ClubeSchema, ClubeCidadeOut
from app.schemas.rodada_schema import RodadaSchema
from typing import Optional, List
import re


def listar_todos_clubes(serie: Optional[str], nome: Optional[str], session: Session) -> List[ClubeCidadeOut]:
    """Lista todos os clubes

    Args:
        serie (Optional[str]): Série do clube a ser filtrado (opcional).
        nome (Optional[str]): Nome do clube a ser filtrado (opcional).
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Erro: 404 - Nenhum clube encontrado.

    Returns:
        List[ClubeCidadeOut]: Representação dos clubes encontrados.
    """
    query = session.query(
        Clube.__table__.c.clu_sigla,
        Clube.__table__.c.clu_nome,
        Clube.__table__.c.clu_serie,
        Clube.__table__.c.clu_link_escudo,
        Clube.__table__.c.cidade_cid_id,
        Cidade.__table__.c.cid_nome.label("cid_nome"),
        Cidade.__table__.c.cid_uf.label("cid_uf"),
    ).join(Cidade, Clube.__table__.c.cidade_cid_id == Cidade.__table__.c.cid_id)

    # Filtro opcional pelo nome do clube
    if nome:
        query = query.filter(Clube.__table__.c.clu_nome.ilike(f"%{nome}%"))

    if serie:
        query = query.filter(Clube.__table__.c.clu_serie == serie.upper())

    query = query.order_by(Clube.__table__.c.clu_nome)

    if not query.all():
        raise HTTPException(status_code=404, detail="Nenhum clube encontrado.")

    clube_schema = [
        ClubeCidadeOut(
            clu_sigla=clube.clu_sigla,
            clu_nome=clube.clu_nome,
            clu_serie=clube.clu_serie,
            clu_link_escudo=clube.clu_link_escudo,
            cidade_cid_id=clube.cidade_cid_id,
            cidade_nome=clube.cid_nome,
            cidade_uf=clube.cid_uf,
        )
        for clube in query.all()
    ]

    return clube_schema
    # return [ClubeCidadeOut(**clube.as_dict()) for clube in query.all()]

def criar_clube(clube: ClubeSchema, session: Session) -> ClubeSchema:
    """Criar registro na tabela de clube

    Args:
        clube (ClubeSchema): Dados do cluber a ser criado.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
    Raises:
        HTTPException: Erro: 404 - Clube já cadastrado.
        HTTPException: Erro: 404 - Cidade não encontrada.
        HTTPException: Erro: 404 - Sigla inválida. Deve conter exatamente 3 letras maiúsculas.
        HTTPException: Erro: 404 - Série inválida. Deve ser A, B, C ou D.

    Returns:
        ClubeSchema: Representação do clube criado.
    """
    consiste_sigla(clube.clu_sigla.upper())  # Verifica se a sigla é válida
    buscar_clube_nome(True, clube.clu_nome, session)  # Verifica se a sigla já existe
    buscar_clube_sigla(True, clube.clu_sigla.upper(), session)  # Verifica se a sigla já existe
    consiste_serie(clube.clu_serie)  # Verifica se a série é válida
    cidade = (session.query(Cidade).filter(Cidade.cid_id == clube.cidade_cid_id).first())
    if not cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada.")

    novo_clube = Clube(
        clu_sigla=clube.clu_sigla.upper(),
        clu_nome= re.sub(r'\s+', ' ', clube.clu_nome.strip()).title(), # Remove espaços extras
        clu_serie=clube.clu_serie.upper(),
        clu_link_escudo=clube.clu_link_escudo.strip(),
        cidade_cid_id=clube.cidade_cid_id
    )
    session.add(novo_clube)
    session.commit()
    session.refresh(novo_clube)
    return ClubeSchema(**novo_clube.as_dict())


def atualizar_clube(clube_atualizado: ClubeSchema, session: Session) -> ClubeSchema:
    clube_db = session.query(Clube).filter(Clube.__table__.c.clu_sigla == clube_atualizado.clu_sigla.upper()).first()

    if not clube_db:
        raise HTTPException(status_code=404, detail="Clube não encontrado.")

    if clube_atualizado.clu_serie:
        consiste_serie(clube_atualizado.clu_serie)  # Ex.: verifica se a série é válida (A, B etc.)

    if clube_atualizado.cidade_cid_id:
        cidade = (
            session.query(Cidade)
            .filter(Cidade.cid_id == clube_atualizado.cidade_cid_id)
            .first()
        )
        if not cidade:
            raise HTTPException(status_code=404, detail="Cidade não encontrada.")

    # Atualização condicional dos campos (apenas os fornecidos pelo cliente)
    if clube_atualizado.clu_nome:
        # Normaliza o nome do clube (remove espaços duplicados e aplica Title Case)
        nome_normalizado = re.sub(r'\s+', ' ', clube_atualizado.clu_nome.strip()).title()

        # Verifica se já existe outro clube com o mesmo nome
        clube_existente = buscar_clube_nome(False, nome_normalizado, session)
        if clube_existente and clube_existente.clu_nome != nome_normalizado:
            raise HTTPException(status_code=404, detail=f"Já existe um clube com o nome '{nome_normalizado}.'")

        clube_db.clu_nome = nome_normalizado  # Atualiza o nome no banco

    if clube_atualizado.clu_serie:
        # Atualiza a série como maiúsculas
        clube_db.clu_serie = clube_atualizado.clu_serie.upper()

    if clube_atualizado.clu_link_escudo:
        # Remove espaços desnecessários do link do escudo
        clube_db.clu_link_escudo = clube_atualizado.clu_link_escudo.strip()

    if clube_atualizado.cidade_cid_id:
        # Atualiza o ID da cidade associada
        clube_db.cidade_cid_id = clube_atualizado.cidade_cid_id

    # Commit das alterações e atualização do estado do objeto
    if clube_atualizado:
        session.commit()
        session.refresh(clube_db)

    # Retorna o esquema atualizado
    return ClubeSchema(**clube_db.as_dict())


def deletar_clube(clu_sigla: str, session: Session):
    clube = session.query(Clube).filter(Clube.__table__.c.clu_sigla == clu_sigla).first()
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado.")

    clube_rodada = buscar_clube_rodada(clu_sigla, session)
    if clube_rodada:
        raise HTTPException(status_code=404, detail=f"O clube {clu_sigla} esta na {clube_rodada.rod_rodada} da rodada {clube_rodada.rod_data} está vinculado ao clube. Exclusão não permitida.")

    session.delete(clube)
    session.commit()
    return "Clube excluido com sucesso."

def buscar_clube_rodada(sigla: str, session: Session) -> Optional[RodadaSchema] | None:
    """
    Busca um clubew pela sigla na tabela rodada.

    Args:
        sigla (str): sigla do clube a ser buscado.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Returns:
        Optional[RodadaSchema]: Representação do estadio encontrado ou None se não encontrado.
    """
    # Busca pelo estadio no banco de dados
    rodada = session.query(Rodada).filter(Rodada.__table__.c.clube_clu_sigla_mandante == sigla or 
                                          Rodada.__table__.c.clube_clu_sigla_visitante == sigla).first()

    if rodada:
        return RodadaSchema(**rodada.as_dict()) if rodada else None

    return None

def buscar_clube_nome(retorna_exception: bool, nome: str, session: Session) -> Optional[ClubeSchema]:
    """
    Busca uma clube pelo nome no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso o clube não seja encontrado.
        nome (str): Nome do clube a ser buscado.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso o clube não seja encontrado.

    Returns:
        Optional[ClubeSchema]: Representação do clube encontrado ou None se não encontrado.
    """

    # Busca pela clube no banco de dados (ignora case com ilike)
    clube = session.query(Clube).filter(Clube.__table__.c.clu_nome.ilike(f"%{nome}%")).first()
 
    if clube:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Já existe clube com nome '{nome}' informado.")

    return ClubeSchema(**clube.as_dict()) if clube else None

def buscar_clube_sigla(retorna_exception: bool, clube_sigla: str, session: Session) -> Optional[ClubeSchema]:
    """
    Busca uma clube pelo ID no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso a clube não seja encontrado.
        clube_sigla (str): Sigla do clube a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso a clube não seja encontrado.

    Returns:
        Optional[ClubeSchema]: Representação do clube encontrado ou None se não encontrado.
    """
    # Busca pelo clube no banco de dados
    clube = session.query(Clube).filter(Clube.__table__.c.clu_sigla == clube_sigla).first()

    if clube:
        if retorna_exception:
            raise HTTPException(status_code=404, detail=f"Clube com sigla '{clube_sigla}' já existe.")
        
    return ClubeSchema(**clube.as_dict()) if clube else None

def buscar_clube_por_cidade_id(retorna_exception: bool, cidade_id: int, session: Session) -> ClubeSchema | None:
    """
    Busca clubes pelo ID da cidade no banco de dados.

    Args:
        retorna_exception (bool): Indica se deve lançar uma exceção caso nenhum clube seja encontrado.
        cidade_id (int): ID da cidade a ser buscada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Caso nenhum clube seja encontrado.

    Returns:
        List[ClubeSchema]: Lista de clubes encontrados na cidade especificada.
    """
    # Busca pelos clubes no banco de dados
    clube = session.query(Clube).filter(Clube.__table__.c.cidade_cid_id == cidade_id).first()

    if not clube and retorna_exception:
        raise HTTPException(status_code=404, detail=f"Nenhum clube encontrado para a cidade com ID '{cidade_id}'.")

    return ClubeSchema(**clube.as_dict()) if clube else None

def consiste_serie(serie: str) -> bool:
    """Consiste a série do clube.

    Args:
        serie (str): Série a ser validada.

    Raises:
        HTTPException: erro: 404 - Série inválida. Deve ser A, B, C ou D.

    Returns:
        bool: True se a série for válida.
    """
    padrao = r'^[AB]$'

    if not re.match(padrao, serie.upper()):
        raise HTTPException(status_code=404, detail=f"Série inválida: {serie}. Informar A ou B.")
    
    return bool(True)

# consiste sigla do clube 3 letras maiusculas
def consiste_sigla(sigla: str) -> bool:
    """Consiste a sigla do clube.

    Args:
        sigla (str): Sigla a ser validada.

    Raises:
        HTTPException: erro: 404 - Sigla inválida. Deve conter exatamente 3 letras maiúsculas.

    Returns:
        bool: True se a sigla for válida.
    """
    padrao = r'^[A-Z]{3}$'

    if not re.match(padrao, sigla.upper()):
        raise HTTPException(status_code=404, detail=f"Sigla inválida: {sigla}. Deve conter exatamente 3 letras maiúsculas.")
    
    return bool(True)

def listar_clubes_paginadas(serie: Optional[str], nome: Optional[str], pagina: int, tamanho_pagina: int, session: Session) -> List[ClubeCidadeOut]:
    """Listar os clubes pelo nome da clube (opcional) com paginação

    Args:
        serie (Optional[str]): Série do clube a ser filtrado (opcional).
        nome (Optional[str]): Nome do clube a ser filtrado (opcional).
        pagina (int): Número da página a ser retornada.
        tamanho_pagina (int): Tamanho da página a ser retornada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.

    Raises:
        HTTPException: Lançada se nenhuma clube for encontrada.

    Returns:
        List[ClubeCidadeOut]: Lista de clubes no formato esperado na API.
    """
    if serie:
        consiste_serie(serie)  # Verifica se a série é válida
    
    query = session.query(
        Clube.__table__.c.clu_sigla,
        Clube.__table__.c.clu_nome,
        Clube.__table__.c.clu_serie,
        Clube.__table__.c.clu_link_escudo,
        Clube.__table__.c.cidade_cid_id,
        Cidade.__table__.c.cid_nome.label("cid_nome"),
        Cidade.__table__.c.cid_uf.label("cid_uf"),
    ).join(Cidade, Clube.__table__.c.cidade_cid_id == Cidade.__table__.c.cid_id)

    # Filtro opcional pelo nome do clube
    if nome:
        query = query.filter(Clube.__table__.c.clu_nome.ilike(f"%{nome}%"))

    if serie:
        query = query.filter(Clube.__table__.c.clu_serie == serie.upper())

    query = query.order_by(Clube.__table__.c.clu_nome)

    # Paginação
    clubes = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()

    # Caso nenhum clube seja encontrado
    if not clubes:
        raise HTTPException(status_code=404, detail="Nenhum clube encontrado.")

    # Serializar os clubes no formato esperado
    return [
        ClubeCidadeOut(
            clu_sigla=clube.clu_sigla,
            clu_nome=clube.clu_nome,
            clu_serie=clube.clu_serie,
            clu_link_escudo=clube.clu_link_escudo,
            cidade_cid_id=clube.cidade_cid_id,
            cidade_nome=clube.cid_nome,
            cidade_uf=clube.cid_uf,
        )
        for clube in clubes
    ]