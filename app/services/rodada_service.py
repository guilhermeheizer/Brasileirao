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
from unittest import result

from requests import session
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.sql import text
from typing import Union
import re
from app.models.rodada_models import Rodada
from app.models.estadio_models import Estadio
from app.schemas.rodada_schema import CriarRodadaSchema, ResponseCriarRodadaSchema, ResponseAlterarRodadaSchema, AlterarJogoRodadaSchema
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
    
def validar_rodada(inc_alt: str, jogos_data: CriarRodadaSchema, session: Session):
    """
    Valida os dados de uma rodada antes de sua criação.

    Args:
        inc_alt (str): Indica se é inclusão ("I") ou alteração ("A").
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
    if inc_alt == "I":
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
    validar_rodada("I", rodada, session)

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

def atualizar_jogo_rodada(serie: str, ano: int, rodada_numero: int, sequencia: int, jogo: AlterarJogoRodadaSchema, session: Session):
    """
    Atualiza os dados de um jogo específico em uma rodada.
    Args:
        serie (str): Série do campeonato (A ou B).
        ano (int): Ano do campeonato.
        rodada_numero (int): Número da rodada.
        sequencia (int): Sequência do jogo na rodada.
        jogo (AlterarJogoRodadaSchema): Dados atualizados do jogo.
        session (Session): Sessão ativa do SQLAlchemy para conectar ao banco.
    Raises:        HTTPException: Erro: 404:
        - Verifica se a série é válida.
        - Verifica se as siglas dos clubes são válidas.
        - Jogo com a mesma sequência, série, rodada e ano já existe.    
        - Clube mandante e visitante são iguais.
        - Rodada não encontrada.
        - Clube mandante ou visitante não existe.
        - Estádio não existe.
    Returns:
        ResponseCriarRodadaSchema: Representação da rodada atualizada.
    """
    jogos_data: CriarRodadaSchema = CriarRodadaSchema(
        rod_serie=serie,
        rod_ano=ano,
        rod_rodada=rodada_numero,
        rod_sequencia=sequencia,
        rod_data=jogo.rod_data,
        clube_clu_sigla_mandante=jogo.clube_clu_sigla_mandante,
        clube_clu_sigla_visitante=jogo.clube_clu_sigla_visitante,
        estadio_est_id=jogo.estadio_est_id
    )
    validar_rodada("A", jogos_data, session)

    query = """
        SELECT 1
        FROM rodada
        WHERE 
            rod_serie = :serie AND
            rod_ano = :ano AND
            rod_rodada = :rodada_numero AND
            rod_sequencia = :sequencia
    """

    # Executando a query
    result = session.execute(
        text(query),
        {
            "serie": serie.upper(),
            "ano": ano,
            "rodada_numero": rodada_numero,
            "sequencia": sequencia
        }
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Rodada com série '{serie.upper()}', ano '{ano}', rodada '{rodada_numero}' e sequência '{sequencia}' não encontrada."
        )

    update_fields = []
    params = {
        "serie": serie.upper(),
        "ano": ano,
        "rodada_numero": rodada_numero,
        "sequencia": sequencia
    }

    if jogo.rod_data is not None:
        update_fields.append("rod_data = :rod_data")
        params["rod_data"] = jogo.rod_data
    if jogo.clube_clu_sigla_mandante is not None:
        update_fields.append("clube_clu_sigla_mandante = :clube_clu_sigla_mandante")
        params["clube_clu_sigla_mandante"] = jogo.clube_clu_sigla_mandante.upper()
    if jogo.rod_gols_mandante is not None:
        update_fields.append("rod_gols_mandante = :rod_gols_mandante")
        params["rod_gols_mandante"] = jogo.rod_gols_mandante
    if jogo.clube_clu_sigla_visitante is not None:
        update_fields.append("clube_clu_sigla_visitante = :clube_clu_sigla_visitante")
        params["clube_clu_sigla_visitante"] = jogo.clube_clu_sigla_visitante.upper()
    if jogo.rod_gols_visitante is not None:
        update_fields.append("rod_gols_visitante = :rod_gols_visitante")
        params["rod_gols_visitante"] = jogo.rod_gols_visitante
    if jogo.rod_pontos_mandante is not None:
        update_fields.append("rod_pontos_mandante = :rod_pontos_mandante")
        params["rod_pontos_mandante"] = jogo.rod_pontos_mandante
    if jogo.rod_pontos_visitante is not None:
        update_fields.append("rod_pontos_visitante = :rod_pontos_visitante")
        params["rod_pontos_visitante"] = jogo.rod_pontos_visitante
    if jogo.rod_calculou_classificacao is not None:
        update_fields.append("rod_calculou_classificacao = :rod_calculou_classificacao")
        params["rod_calculou_classificacao"] = jogo.rod_calculou_classificacao
    if jogo.rod_partida_finalizada is not None:
        update_fields.append("rod_partida_finalizada = :rod_partida_finalizada")
        params["rod_partida_finalizada"] = jogo.rod_partida_finalizada
    if jogo.estadio_est_id is not None:
        update_fields.append("estadio_est_id = :estadio_est_id")
        params["estadio_est_id"] = jogo.estadio_est_id

    # Gerar a query final
    if update_fields:
        update_query = f"""
            UPDATE rodada
            SET {", ".join(update_fields)}
            WHERE 
                rod_serie = :serie AND
                rod_ano = :ano AND
                rod_rodada = :rodada_numero AND
                rod_sequencia = :sequencia
        """
        # Executar a query
        try:
            session.execute(text(update_query), params)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar rodada: {str(e)}")

    # Retornar os dados atualizados
    rodada_atualizada = session.execute(
        text(query),
        {
            "serie": serie.upper(),
            "ano": ano,
            "rodada_numero": rodada_numero,
            "sequencia": sequencia
        }
    ).fetchone()

    if not rodada_atualizada:
        raise HTTPException(status_code=500, detail="Erro ao recuperar a rodada após a atualização.")
    
    retorna_rodada: ResponseAlterarRodadaSchema = ResponseAlterarRodadaSchema(
        rod_serie=serie.upper(),
        rod_ano=ano,
        rod_rodada=rodada_numero,
        rod_sequencia=sequencia,
        rod_data=jogo.rod_data,
        clube_clu_sigla_mandante=jogo.clube_clu_sigla_mandante,
        rod_gols_mandante=jogo.rod_gols_mandante,
        clube_clu_sigla_visitante=jogo.clube_clu_sigla_visitante,
        rod_gols_visitante=jogo.rod_gols_visitante,
        rod_pontos_mandante=jogo.rod_pontos_mandante,
        rod_pontos_visitante=jogo.rod_pontos_visitante,
        rod_calculou_classificacao=jogo.rod_calculou_classificacao,
        rod_partida_finalizada=jogo.rod_partida_finalizada,
        estadio_est_id=jogo.estadio_est_id
    )

    return retorna_rodada

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