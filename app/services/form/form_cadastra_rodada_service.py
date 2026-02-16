from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.rodada_models import Rodada
from app.models.clube_models import Clube
from app.models.estadio_models import Estadio
from app.services.clube_service import buscar_clube_sigla, consiste_serie, consiste_sigla
from typing import List, Optional
import re
from app.schemas.rodada_schema import (
    RodadaSchema,
    CriarRodadaSchema,
    AtualizarRodadaPlacarSchema,
    ResponseRodadaSchema,
    ResponseRodadasSchema,
)
from app.services.estadio_service import buscar_estadio_id
from app.services.rodada_service import consiste_jogo_existe_rodada, consiste_sigla_clube_igual


def criar_rodada(
    jogos_data: List[CriarRodadaSchema],
    session: Session
) -> ResponseRodadasSchema:
    """
    Cria uma rodada completa de jogos (10 jogos) no banco de dados.

    Args:
        db (Session): Sessão ativa do banco de dados.
        rod_serie (str): Série do campeonato (ex: 'A', 'B').
        rod_ano (int): Ano do campeonato.
        jogos_data (List[CriarRodadaSchema]): Lista com os 10 jogos da rodada.

    Returns:
        ResponseRodadasSchema: Lista de ResponseRodadaSchema com os jogos criados.

    Raises:
        HTTPException: Erro de validação ou conflito ao criar a rodada.
    """
    if len(jogos_data) != 10:
        raise HTTPException(
            status_code=404,
            detail=f"A rodada deve conter exatamente 10 jogos. Recebido: {len(jogos_data)}."
        )

    # Validar unicidade das sequências dentro da lista fornecida
    seq_set = set(j.rod_sequencia for j in jogos_data)
    if len(seq_set) != 10:
        raise HTTPException(
            status_code=404,
            detail="A lista de jogos contém sequências duplicadas."
        )

    # 2. Validar os jogos na rodada
    for jogo in jogos_data:
        consiste_serie(jogo.rod_serie.upper())
        consiste_sigla(jogo.clube_clu_sigla_mandante.upper())
        consiste_sigla(jogo.clube_clu_sigla_visitante.upper())
        consiste_sigla_clube_igual(jogo.clube_clu_sigla_mandante, jogo.clube_clu_sigla_visitante)
        buscar_clube_sigla(True, jogo.clube_clu_sigla_mandante.upper(), session) # Validar se o clube existe
        buscar_clube_sigla(True, jogo.clube_clu_sigla_visitante.upper(), session) # Validar se o clube existe
        buscar_estadio_id(True, jogo.estadio_est_id, session) # Validar estádio
        consiste_jogo_existe_rodada(jogo, session) # Verificar se o jogo já existe no banco
    
        if jogo.rod_serie.upper() != jogos_data[0].rod_serie.upper() or jogo.rod_ano != jogos_data[0].rod_ano:
            raise HTTPException(
                status_code=404,
                detail=f"Jogo com sequência {jogo.rod_sequencia} não possui série ou ano correspondentes: "
                       f"Série: {jogo.rod_serie.upper()}, Ano: {jogo.rod_ano}."
            )

    #Adicionar os jogos no banco
    rodadas = []
    sequencia = 0
    try:
        for jogo in jogos_data:
            sequencia += 10
            nova_rodada = Rodada(
                rod_serie=jogo.rod_serie.upper(),
                rod_ano=jogo.rod_ano,
                rod_rodada=jogo.rod_rodada,
                rod_sequencia=sequencia,
                rod_data=jogo.rod_data,
                clube_clu_sigla_mandante=jogo.clube_clu_sigla_mandante.upper(),
                clube_clu_sigla_visitante=jogo.clube_clu_sigla_visitante.upper(),
                rod_calculou_classificacao="N",
                rod_partida_finalizada="N",
                estadio_est_id=jogo.estadio_est_id,
            )
            session.add(nova_rodada)
            rodadas.append(nova_rodada)

        # Commitar todas as alterações no banco
        session.commit()

        # Garantir que os objetos estão atualizados com a sessão
        for rodada in rodadas:
            session.refresh(rodada)

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro ao salvar a rodada: {str(e)}"
        )

    # 4. Retornar os objetos criados no formato esperado
    return ResponseRodadasSchema(rodadas=[ResponseRodadaSchema.from_orm(jogo) for jogo in rodadas])