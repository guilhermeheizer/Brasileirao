from requests import session
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
import re
from app.models.rodada_models import Rodada
from app.models.estadio_models import Estadio
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseCriarRodadaSchema
from app.services.clube_service import buscar_clube_sigla, consiste_serie, consiste_sigla
from app.services.estadio_service import buscar_estadio_id


def consiste_sigla_clube_igual(clube_mandante: str, clube_visitante: str):
    """Verificar se as siglas dos clubes mandante e visitante são iguais
    Args:
        clube_mandante (str): Sigla do clube mandante.
        clube_visitante (str): Sigla do clube visitante.
    Raises:
        HTTPException: Erro: 404: Sigla do clube mandante e visitante são iguais.
    """
    if clube_mandante.upper() == clube_visitante.upper():
        raise HTTPException(
            status_code=404,
            detail=f"Sigla do clube mandante '{clube_mandante.upper()}' e visitante '{clube_visitante.upper()}' são iguais."
        )

def consiste_jogo_existe_rodada(rodada: CriarRodadaSchema, session: Session):
    """Verificar se o jogo já existe no banco de dados
    Args:
        db (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
        jogo: Objeto contendo os detalhes do jogo a ser verificado.
    Raises:
        HTTPException: Erro: 404: Jogo com a mesma sequência, série, rodada e ano já existe.
    """
    jogo_existente = session.query(Rodada).filter(
        Rodada.__table__.c.rod_serie == rodada.rod_serie.upper(),
        Rodada.__table__.c.rod_ano == rodada.rod_ano,
        Rodada.__table__.c.rod_rodada == rodada.rod_rodada,
        Rodada.__table__.c.rod_sequencia == rodada.rod_sequencia
    ).first()

    if jogo_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Jogo com sequência '{rodada.rod_sequencia}', série '{rodada.rod_serie.upper()}', rodada '{rodada.rod_rodada}', "
                    f"ano '{rodada.rod_ano}' já existe."
        )
    
def criar_rodada(rodada: CriarRodadaSchema, session: Session):
    """Criar registro na tabela de rodada
    Args:
        rodada (CriarRodadaSchema): Dados da rodada a ser criada.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
    Raises:
        HTTPException: Erro: 404:
        - Verifica se a série é válida.
        - Verifica se as siglas dos clubes são válidas.
        - Jogo com a mesma sequência, série, rodada e ano já existe.
        - Clube mandante e visitante são iguais.
        - Rodada já cadastrada.
        - Clube mandante ou visitante não existe.
        - Estádio não existe.
    Returns:
        ResponseCriarRodadaSchema: Representação da rodada criada.
    """
    consiste_serie(rodada.rod_serie.upper())
    consiste_sigla(rodada.clube_clu_sigla_mandante.upper())
    consiste_sigla(rodada.clube_clu_sigla_visitante.upper())
    consiste_sigla_clube_igual(rodada.clube_clu_sigla_mandante, rodada.clube_clu_sigla_visitante)
    buscar_clube_sigla(True, rodada.clube_clu_sigla_mandante.upper(), session) # Validar se o clube existe
    buscar_clube_sigla(True, rodada.clube_clu_sigla_visitante.upper(), session) # Validar se o clube existe
    buscar_estadio_id(True, rodada.estadio_est_id, session) # Validar estádio
    consiste_jogo_existe_rodada(rodada, session) # Verificar se o jogo já existe no banco

    try:
        nova_rodada = Rodada(
                rod_serie=rodada.rod_serie.upper(),
                rod_ano=rodada.rod_ano,
                rod_rodada=rodada.rod_rodada,
                rod_sequencia=rodada.rod_sequencia,
                rod_data=rodada.rod_data,
                clube_clu_sigla_mandante=rodada.clube_clu_sigla_mandante.upper(),
                clube_clu_sigla_visitante=rodada.clube_clu_sigla_visitante.upper(),
                rod_calculou_classificacao="N",
                rod_partida_finalizada="N",
                estadio_est_id=rodada.estadio_est_id,
                )
        session.add(nova_rodada)
        session.commit()
        session.refresh(nova_rodada)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e))
   
    return ResponseCriarRodadaSchema(**nova_rodada.as_dict())

def atualizar_rodada(self):
    # Lógica para atualizar os detalhes de uma rodada existente
    pass

def deletar_rodada(self):
    # Lógica para deletar uma rodada
    pass

def obter_rodada(self, rodada_id: int):
    # Lógica para obter os detalhes de uma rodada específica
    pass
