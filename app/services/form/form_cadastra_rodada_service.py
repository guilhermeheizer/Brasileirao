"""
form_cadastra_rodada_service.py

Este módulo implementa a lógica de serviço para cadastro de rodadas completas do Campeonato Brasileiro.
Fornece função para validação e inserção de uma lista de jogos (rodada) no banco de dados.

Funcionalidade principal:
- Validar e criar uma rodada completa (10 jogos) a partir de dados recebidos do front-end

Utiliza SQLAlchemy para persistência e validações de integridade.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.rodada_models import Rodada
from app.services.rodada_service import validar_rodada
from typing import List
from app.schemas.rodada_schema import (
    CriarRodadaSchema,
    ResponseCriarRodadaSchema,
)


def criar_rodada(
    jogos_data: List[CriarRodadaSchema],
    session: Session
    ) -> List[ResponseCriarRodadaSchema]:
    """
    Cria uma rodada completa de jogos (10 jogos) no banco de dados.

    Args:
        db (Session): Sessão ativa do banco de dados.
        rod_serie (str): Série do campeonato (ex: 'A', 'B').
        rod_ano (int): Ano do campeonato.
        jogos_data (List[CriarRodadaSchema]): Lista com os 10 jogos da rodada.

    Returns:
        List[ResponseCriarRodadaSchema]: Lista de ResponseCriarRodadaSchema com os jogos criados.

    Raises:
        HTTPException: Erro de validação ou conflito ao criar a rodada.
    """
    if len(jogos_data) != 10:
        raise HTTPException(
            status_code=404,
            detail=f"A rodada deve conter exatamente 10 jogos. Recebido: {len(jogos_data)}."
        )

    for jogo in jogos_data:
        validar_rodada(jogo, session)

    #Adicionar os jogos no banco
    rodadas = []
    sequencia = 0
    try:
        for jogo in jogos_data:
            sequencia += 5
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
        print (f"Rodada criada com sucesso: Série {jogos_data[0].rod_serie.upper()}, Ano {jogos_data[0].rod_ano}, Rodada {jogos_data[0].rod_rodada}.")
        # Garantir que os objetos estão atualizados com a sessão
        for rodada in rodadas:
            session.refresh(rodada)
        print ("Limpou a sessão após criar a rodada.")
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro ao salvar a rodada: {str(e)}"
        )
    print ("Rodada salva no banco, preparando resposta...")

    rodadas_pyd = [
    ResponseCriarRodadaSchema.model_validate(jogo, from_attributes=True) for jogo in rodadas
    ]
    return rodadas_pyd