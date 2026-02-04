from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.models.rodada_models import Rodada
from app.models.clube_models import Clube
from app.models.estadio_models import Estadio
from app.models.cartao_models import Cartao
from app.schemas.rodada_schema import ListaJogosRodadaFormPlacarResponse, JogoFormPlacarSchema, AtualizarRodadaPlacarSchema


def rodada_lista(
    db: Session,
    serie: str,
    ano: int,
    rodada: int,
    carrega_nao_realizados: bool = False
) -> ListaJogosRodadaFormPlacarResponse:
    """
    Carrega a lista de jogos da rodada no formato necessário para o front-end.
    Se carrega_nao_realizados=True, inclui jogos de rodadas anteriores não finalizados.

    Args:
        db (Session): Sessão ativa do banco de dados.
        serie (str): Série do campeonato (ex: 'A', 'B').
        ano (int): Ano da competição.
        rodada (int): Número da rodada.
        carrega_nao_realizados (bool): Se True, inclui jogos não finalizados das rodadas anteriores.

    Returns:
        ListaJogosRodadaFormPlacarResponse: JSON contendo detalhes da rodada e jogos.
    """
    # Garantir que a série está em maiúsculo
    serie_upper = serie.upper()

    # Validar a série
    if serie_upper not in ["A", "B"]:
        raise HTTPException(
            status_code=400,
            detail=f"Série '{serie_upper}' inválida. Use 'A' ou 'B'."
        )
   
    sql_query_str = """
        SELECT
            rodada.rod_serie AS rodada_rod_serie,
            rodada.rod_ano AS rodada_rod_ano,
            rodada.rod_rodada AS rodada_rod_rodada,
            rodada.rod_sequencia AS rodada_rod_sequencia,
            rodada.rod_data AS rodada_rod_data,
            rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
            rodada.rod_gols_mandante AS rodada_rod_gols_mandante,
            rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
            rodada.rod_gols_visitante AS rodada_rod_gols_visitante,
            rodada.rod_pontos_mandante AS rodada_rod_pontos_mandante,
            rodada.rod_pontos_visitante AS rodada_rod_pontos_visitante,
            rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao,
            rodada.rod_partida_finalidaza AS rodada_rod_partida_finalidaza,
            rodada.estadio_est_id AS rodada_estadio_est_id,
            estadio.est_nome AS est_nome,
            clube_mandante.clu_nome AS clu_nome_mandante,
            clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
            clube_visitante.clu_nome AS clu_nome_visitante,
            clube_visitante.clu_link_escudo AS clu_link_escudo_visitante,
            cartao_mandante.car_qtd_vermelho AS cartoes_vermelhos_mandante,
            cartao_mandante.car_qtd_amarelo AS cartoes_amarelos_mandante,
            cartao_visitante.car_qtd_vermelho AS cartoes_vermelhos_visitante,
            cartao_visitante.car_qtd_amarelo AS cartoes_amarelos_visitante
        FROM
            rodada
        JOIN estadio ON
            rodada.estadio_est_id = estadio.est_id
        JOIN clube AS clube_mandante ON
            rodada.clube_clu_sigla_mandante = clube_mandante.clu_sigla
        JOIN clube AS clube_visitante ON
            rodada.clube_clu_sigla_visitante = clube_visitante.clu_sigla
        LEFT OUTER JOIN cartao AS cartao_mandante ON
            rodada.rod_serie = cartao_mandante.car_serie
            AND rodada.rod_ano = cartao_mandante.car_ano
            AND rodada.clube_clu_sigla_mandante = cartao_mandante.clube_clu_sigla
        LEFT OUTER JOIN cartao AS cartao_visitante ON
            rodada.rod_serie = cartao_visitante.car_serie
            AND rodada.rod_ano = cartao_visitante.car_ano
            AND rodada.clube_clu_sigla_visitante = cartao_visitante.clube_clu_sigla
        WHERE
            rodada.rod_serie = :serie
            AND rodada.rod_ano = :ano
    """
    if carrega_nao_realizados:
        sql_query_str += " AND rodada.rod_rodada <= :rodada\n"
    else:
        sql_query_str += " AND rodada.rod_rodada = :rodada\n"
    sql_query_str += """
        ORDER BY
            rodada.rod_rodada,
            rodada.rod_data,
            rodada.rod_sequencia
    """
    sql_query = text(sql_query_str)

    # Executar a query diretamente no banco de dados
    resultados = db.execute(sql_query, {"serie": serie_upper, "ano": ano, "rodada": rodada}).fetchall()

    # Validar se há jogos correspondentes
    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="Nenhum jogo encontrado para os parâmetros fornecidos."
        )

    # Construir o JSON da resposta
    jogos_da_rodada = []
    for jogo in resultados:
        jogos_da_rodada.append(
            JogoFormPlacarSchema(
                rod_serie=jogo.rodada_rod_serie,
                rod_ano=jogo.rodada_rod_ano,
                rod_rodada=jogo.rodada_rod_rodada,
                rod_sequencia=jogo.rodada_rod_sequencia,
                est_id=jogo.rodada_estadio_est_id,
                est_nome=jogo.est_nome,
                rod_data=jogo.rodada_rod_data,
                clube_clu_sigla_mandante=jogo.rodada_clube_clu_sigla_mandante,
                clu_nome_mandante=jogo.clu_nome_mandante,
                clu_link_escudo_mandante=jogo.clu_link_escudo_mandante,
                rod_gols_mandante=jogo.rodada_rod_gols_mandante,
                clube_clu_sigla_visitante=jogo.rodada_clube_clu_sigla_visitante,
                clu_nome_visitante=jogo.clu_nome_visitante,
                clu_link_escudo_visitante=jogo.clu_link_escudo_visitante,
                rod_gols_visitante=jogo.rodada_rod_gols_visitante,
                car_qtd_vermelho_mandante=jogo.cartoes_vermelhos_mandante,
                car_qtd_amarelo_mandante=jogo.cartoes_amarelos_mandante,
                car_qtd_vermelho_visitante=jogo.cartoes_vermelhos_visitante,
                car_qtd_amarelo_visitante=jogo.cartoes_amarelos_visitante,
                rod_partida_finalidaza=jogo.rodada_rod_partida_finalidaza,
                rod_calculou_classificacao=jogo.rodada_rod_calculou_classificacao,
            )
        )

    # Retornar o JSON completo
    return ListaJogosRodadaFormPlacarResponse(
        serie=serie_upper,
        ano=ano,
        rodada=rodada,
        jogos_da_rodada=jogos_da_rodada
    )
   


def atualizar_placares_rodada(
    db: Session,
    jogos: List[AtualizarRodadaPlacarSchema]
) -> dict:
    """
    Atualiza os campos de placar e status de finalização das partidas na tabela 'rodada'.
    
    Args:
        db (Session): Sessão ativa do banco de dados.
        dados (List[AtualizarRodadaPlacarSchema]): Lista de partidas com informações de atualização.

    Returns:
        dict: Mensagem de sucesso ou erro.
    """
    pontos_mandante = 0
    pontos_visitante = 0
    # Loop para processar cada jogo individualmente
    for jogo in jogos:
        print(f" Atualizando jogo: Série {jogo.rod_serie}, Ano {jogo.rod_ano}, Rodada {jogo.rod_rodada}, Sequência {jogo.rod_sequencia}, Gols Mandante: {jogo.rod_gols_mandante}, Gols Visitante: {jogo.rod_gols_visitante}, Finalizada: {jogo.rod_partida_finalizada}")
        # Verifica se os gols estão preenchidos antes do update
        if jogo.rod_gols_mandante is not None and jogo.rod_gols_visitante is not None:
            if jogo.rod_gols_mandante == jogo.rod_gols_visitante:
                # Empate
                pontos_mandante = 1
                pontos_visitante = 1
            elif jogo.rod_gols_mandante > jogo.rod_gols_visitante:
                # Mandante vence
                pontos_mandante = 3
                pontos_visitante = 0
            else:
                # Visitante vence
                pontos_mandante = 0
                pontos_visitante = 3
            # Comando SQL para atualização do registro
            sql_update_str = """
                UPDATE rodada
                SET
                    rod_gols_mandante = :rod_gols_mandante,
                    rod_gols_visitante = :rod_gols_visitante,
                    rod_partida_finalidaza = :rod_partida_finalidaza,
                    rod_pontos_mandante = :rod_pontos_mandante,
                    rod_pontos_visitante = :rod_pontos_visitante              
                WHERE
                    rod_serie = :rod_serie AND
                    rod_ano = :rod_ano AND
                    rod_rodada = :rod_rodada AND
                    rod_sequencia = :rod_sequencia
            """
            sql_update = text(sql_update_str)

            # Executar o comando de atualização
            db.execute(sql_update, {
                "rod_gols_mandante": jogo.rod_gols_mandante,
                "rod_gols_visitante": jogo.rod_gols_visitante,
                "rod_partida_finalidaza": jogo.rod_partida_finalidaza,
                "rod_pontos_mandante": pontos_mandante,
                "rod_pontos_visitante": pontos_visitante,
                "rod_serie": jogo.rod_serie,
                "rod_ano": jogo.rod_ano,
                "rod_rodada": jogo.rod_rodada,
                "rod_sequencia": jogo.rod_sequencia
            })

    # Confirmar as alterações no banco
    db.commit()

    return {"message": f"{len(jogos)} partidas atualizadas com sucesso."}


def calcular_classificacao_brasileirao(
    db: Session,
    serie: str,
    ano: int,
    rodada: int,
    carrega_nao_realizados: bool = False
):
    """
    Calcula e atualiza a classificação do Brasileirão na tabela 'classificacao_geral' a partir dos dados da tabela 'rodada'.

    Args:
        db (Session): Sessão ativa do banco de dados.
        serie (str): Série do campeonato (ex: 'A', 'B').
        ano (int): Ano da competição.
        rodada (int): Número da rodada.
        carrega_nao_realizados (bool): Determina se jogos não finalizados de rodadas anteriores são carregados.

    Returns:
        dict: Mensagem de sucesso contendo o resultado da operação.
    """
    # Query para carregar as rodadas que atendem aos critérios
    sql_query_rodadas = """
        SELECT * FROM rodada
        WHERE rod_serie = :serie
          AND rod_ano = :ano
          AND rod_partida_finalidaza = 'S'
          AND rod_calculou_classificacao = 'N'
    """

    if carrega_nao_realizados:
        sql_query_rodadas += " AND rod_rodada <= :rodada"
    else:
        sql_query_rodadas += " AND rod_rodada = :rodada"

    rodadas = db.execute(text(sql_query_rodadas), {"serie": serie, "ano": ano, "rodada": rodada}).fetchall()

    # Se nenhuma rodada for encontrada
    if not rodadas:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma rodada encontrada que atenda aos critérios fornecidos."
        )

    for partida in rodadas:
        # Para cada partida, processamos o time mandante e visitante
        processar_time(
            db=db,
            sigla=partida.clube_clu_sigla_mandante,
            pontos=partida.rod_pontos_mandante,
            gols_pro=partida.rod_gols_mandante,
            gols_contra=partida.rod_gols_visitante,
            venceu=partida.rod_gols_mandante > partida.rod_gols_visitante,
            empatou=partida.rod_gols_mandante == partida.rod_gols_visitante
        )

        processar_time(
            db=db,
            sigla=partida.clube_clu_sigla_visitante,
            pontos=partida.rod_pontos_visitante,
            gols_pro=partida.rod_gols_visitante,
            gols_contra=partida.rod_gols_mandante,
            venceu=partida.rod_gols_visitante > partida.rod_gols_mandante,
            empatou=partida.rod_gols_mandante == partida.rod_gols_visitante
        )

        # Atualizar o registro da rodada para marcar como processado
        db.execute(
            text("""
                UPDATE rodada
                SET rod_calculou_classificacao = 'S'
                WHERE rod_serie = :serie
                  AND rod_ano = :ano
                  AND rod_rodada = :rodada
                  AND rod_sequencia = :sequencia
            """),
            {
                "serie": partida.rod_serie,
                "ano": partida.rod_ano,
                "rodada": partida.rod_rodada,
                "sequencia": partida.rod_sequencia
            }
        )

    # Salvar alterações
    db.commit()
    return {"message": "Classificação geral do Brasileirão atualizada com sucesso!"}


def processar_time(
    db: Session,
    sigla: str,
    pontos: int,
    gols_pro: int,
    gols_contra: int,
    venceu: bool,
    empatou: bool
):
    """
    Processa a classificação de um time (mandante ou visitante),
    atualizando ou criando o registro na tabela 'classificacao_geral'.

    Args:
        db (Session): Sessão ativa do banco de dados.
        sigla (str): Sigla do clube.
        pontos (int): Pontos a serem somados.
        gols_pro (int): Gols feitos (pro).
        gols_contra (int): Gols sofridos (contra).
        venceu (bool): Indicador se venceu a partida.
        empatou (bool): Indicador se empatou a partida.
    """
    # Buscar quantidade de cartões
    cartoes = db.execute(
        text("""
            SELECT car_qtd_vermelho, car_qtd_amarelo
            FROM cartao
            WHERE clube_clu_sigla = :sigla
        """),
        {"sigla": sigla}
    ).fetchone()

    # Valores iniciais
    qtd_vermelho = cartoes.car_qtd_vermelho if cartoes else 0
    qtd_amarelo = cartoes.car_qtd_amarelo if cartoes else 0

    # Verificar se o clube já está na tabela classificacao_geral
    classificacao = db.execute(
        text("""
            SELECT * FROM classificacao_geral
            WHERE clube_clu_sigla = :sigla
        """),
        {"sigla": sigla}
    ).fetchone()

    if classificacao:
        # Atualizar os valores
        db.execute(
            text("""
                UPDATE classificacao_geral
                SET clg_pontos = clg_pontos + :pontos,
                    clg_vitorias = clg_vitorias + :vitorias,
                    clg_qtd_empates = clg_qtd_empates + :empates,
                    clg_qtd_derrotas = clg_qtd_derrotas + :derrotas,
                    clg_gols_pro = clg_gols_pro + :gols_pro,
                    clg_gols_contra = clg_gols_contra + :gols_contra,
                    clg_saldo_gols = clg_saldo_gols + :saldo,
                    clg_vermelho_clube_clu_sigla = :qtd_vermelho,
                    clg_amarelo_clube_clu_sigla = :qtd_amarelo
                WHERE clube_clu_sigla = :sigla
            """),
            {
                "pontos": pontos,
                "vitorias": 1 if venceu else 0,
                "empates": 1 if empatou else 0,
                "derrotas": 1 if not venceu and not empatou else 0,
                "gols_pro": gols_pro,
                "gols_contra": gols_contra,
                "saldo": gols_pro - gols_contra,
                "qtd_vermelho": qtd_vermelho,
                "qtd_amarelo": qtd_amarelo,
                "sigla": sigla
            }
        )
    else:
        # Inserir novo registro
        db.execute(
            text("""
                INSERT INTO classificacao_geral (
                    clg_serie, clg_ano, clg_pontos, clg_vitorias, clg_saldo_gols,
                    clg_gols_pro, clg_confronto_direto, clg_vermelho_clube_clu_sigla,
                    clg_amarelo_clube_clu_sigla, clube_clu_sigla, clg_qtd_empates,
                    clg_qtd_derrotas, clg_gols_contra
                )
                VALUES (
                    :serie, :ano, :pontos, :vitorias, :saldo, :gols_pro, 0,
                    :qtd_vermelho, :qtd_amarelo, :sigla, :empates, :derrotas, :gols_contra
                )
            """),
            {
                "serie": "A",  # Por simplicidade, ajustar ao usar múltiplas séries
                "ano": 2023,   # Incrementar dinamicamente conforme necessário
                "pontos": pontos,
                "vitorias": 1 if venceu else 0,
                "saldo": gols_pro - gols_contra,
                "gols_pro": gols_pro,
                "empates": 1 if empatou else 0,
                "derrotas": 1 if not venceu and not empatou else 0,
                "qtd_vermelho": qtd_vermelho,
                "qtd_amarelo": qtd_amarelo,
                "sigla": sigla,
                "gols_contra": gols_contra
            }
        )