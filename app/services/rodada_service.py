"""
rodada_service.py

Este módulo implementa as regras de negócio e operações de serviço relacionadas às rodadas do Campeonato Brasileiro.
Fornece funções para validação, criação, atualização, deleção e consulta de rodadas, além de validações específicas de clubes e estádios.

Principais funcionalidades:
- Validação de dados de rodada e clubes
- Criação de rodadas no banco de dados
- Funções utilitárias para consistência de dados
- Estrutura para atualização, deleção e consulta de rodadas

Funções principais:
- consiste_sigla_clube_igual: Valida se mandante e visitante são diferentes
- consiste_jogo_existe_rodada: Verifica duplicidade de jogo
- criar_rodada: Cria uma nova rodada
- atualizar_rodada: Atualiza uma rodada existente
- deletar_rodada: Remove uma rodada
- obter_rodada: Consulta detalhes de uma rodada
"""
from requests import session
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Union
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

def consiste_jogo_existe_rodada_sequencia(
    session: Session,
    rodada: Union[CriarRodadaSchema, None] = None,
    serie: Union[str, None] = None,
    ano: Union[int, None] = None,
    sequencia: Union[int, None] = None,
    rodada_num: Union[int, None] = None,
    ):
    """Verificar se o jogo já existe no banco de dados com base na sequência, série, rodada e ano.
       Verificar se o jogo já existe no banco de dados com a sigla do clube mandante, visitante, série, rodada e ano.
    Args:
        db (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
        jogo: Objeto contendo os detalhes do jogo a ser verificado.
    Raises:
        HTTPException: Erro: 404: Jogo com a mesma sequência, série, rodada e ano já existe.
    """
    if rodada:
        serie = rodada.rod_serie
        ano = rodada.rod_ano
        rodada_num = rodada.rod_rodada
        sequencia = rodada.rod_sequencia

    if not (serie and ano and rodada_num and sequencia):
        raise HTTPException(
            status_code=404,
            detail="Parâmetros insuficientes fornecidos. Informe o esquema ou argumentos diretos."
        )
    
    jogo_existente = session.query(Rodada).filter(
        Rodada.__table__.c.rod_serie == serie.upper(),
        Rodada.__table__.c.rod_ano == ano,
        Rodada.__table__.c.rod_rodada == rodada_num,
        Rodada.__table__.c.rod_sequencia == sequencia
    ).first()

    if jogo_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Jogo com sequência '{sequencia}', série '{serie.upper()}', rodada '{rodada_num}', "
                    f"ano '{ano}' já existe."
        )
    
def consiste_jogo_existe_rodada_siglas(rodada: CriarRodadaSchema, session: Session):
    jogo_existente_siglas = session.query(Rodada).filter(
        Rodada.__table__.c.rod_serie == rodada.rod_serie.upper(),
        Rodada.__table__.c.rod_ano == rodada.rod_ano,
        Rodada.__table__.c.rod_rodada == rodada.rod_rodada,
        Rodada.__table__.c.clube_clu_sigla_mandante == rodada.clube_clu_sigla_mandante.upper(),
        Rodada.__table__.c.clube_clu_sigla_visitante == rodada.clube_clu_sigla_visitante.upper()
    ).first()
    
    if jogo_existente_siglas:
        raise HTTPException(
            status_code=404,
            detail=f"Jogo com siglas de clubes mandante '{rodada.clube_clu_sigla_mandante.upper()}' e visitante '{rodada.clube_clu_sigla_visitante.upper()}', "
                    f"série '{rodada.rod_serie.upper()}', rodada '{rodada.rod_rodada}', ano '{rodada.rod_ano}' já existe."
        )
    
def validar_rodada(jogos_data: CriarRodadaSchema, session: Session):
    """
    Valida os dados de uma rodada antes de sua criação.

    Args:
        jogos_data (CriarRodadaSchema): Dados da rodada a ser validada.
        session (Session): Sessão ativa do banco de dados.

    Raises:
        HTTPException: Erro de validação caso algum dado seja inválido.
    """
    consiste_serie(jogos_data.rod_serie.upper())
    consiste_sigla(jogos_data.clube_clu_sigla_mandante.upper())
    consiste_sigla(jogos_data.clube_clu_sigla_visitante.upper())
    consiste_sigla_clube_igual(jogos_data.clube_clu_sigla_mandante, jogos_data.clube_clu_sigla_visitante)

    mandante = buscar_clube_sigla(False, jogos_data.clube_clu_sigla_mandante, session)
    if not mandante:
        raise HTTPException(
            status_code=404,
            detail=f"Clube mandante com sigla '{jogos_data.clube_clu_sigla_mandante}' não encontrado."
        )

    visitante = buscar_clube_sigla(False, jogos_data.clube_clu_sigla_visitante, session)
    if not visitante:
        raise HTTPException(
            status_code=404,
            detail=f"Clube visitante com sigla '{jogos_data.clube_clu_sigla_visitante}' não encontrado."
        )
    # Validar estádio
    estadio = session.query(Estadio).filter(Estadio.est_id == jogos_data.estadio_est_id).first()
    if not estadio:
        raise HTTPException(
            status_code=404,
            detail=f"Estádio com ID '{jogos_data.estadio_est_id}' não encontrado para o jogo {jogos_data.rod_sequencia}."
        )
    
    consiste_jogo_existe_rodada_sequencia(session,jogos_data, None, None, None, None)
    consiste_jogo_existe_rodada_siglas(jogos_data, session)


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
    validar_rodada(rodada, session)

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
    """
    Atualiza os detalhes de uma rodada existente.
    (Implementação futura)
    """
    pass

# Deletar um jogo específico da rodada, ou a rodada inteira, dependendo dos requisitos do sistema.
def deletar_rodada(serie: str, ano: int, rodada_numero: int, sequencia: int, session: Session):
    """Deleta da tabela de rodada uma sequencia

    Args:
        serie (str): _description_
        ano (int): _description_
        rodada_numero (int): _description_
        sequencia (int): _description_
    """
    rodada = session.query(Rodada).filter(
        Rodada.__table__.c.rod_serie == serie.upper(),
        Rodada.__table__.c.rod_ano == ano,
        Rodada.__table__.c.rod_rodada == rodada_numero,
        Rodada.__table__.c.rod_sequencia == sequencia
    ).first()

    if not rodada:
        raise HTTPException(
            status_code=404,
            detail=f"Rodada com série '{serie.upper()}', ano '{ano}', rodada '{rodada_numero}' e sequência '{sequencia}' não encontrada."
        )

    try:
        session.delete(rodada)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e))

    return "Jogo excluído com sucesso"    

def obter_rodada(self, rodada_id: int):
    """
    Obtém os detalhes de uma rodada específica pelo ID.
    (Implementação futura)
    """
    pass
