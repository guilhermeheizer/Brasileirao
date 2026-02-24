"""
form_placar_rodada_service.py

Este módulo implementa a lógica de serviço para operações de placar de rodada do Campeonato Brasileiro.
Fornece funções para:
- Listar jogos de uma rodada para preenchimento de placares
- Atualizar placares e status de jogos
- Calcular e atualizar a classificação geral
- Processar e atualizar dados de clubes na classificação
- Listar classificação geral detalhada

Utiliza SQLAlchemy para persistência, queries customizadas e integrações com modelos e schemas do projeto.
"""
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.schemas.rodada_schema import ListaJogosRodadaFormPlacarResponse, JogoFormPlacarSchema, AtualizarRodadaPlacarSchema
from app.schemas.classificacao_geral_schema import ResponseClassificacaoGeralListaSchema
from app.services.clube_service import consiste_serie

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
            status_code=404,
            detail=f"Série '{serie_upper}' inválida. Use 'A' ou 'B'."
        )
   
    sql_query_str = """
        SELECT
            rodada.rod_serie AS rodada_rod_serie,
            rodada.rod_ano AS rodada_rod_ano,
            rodada.rod_rodada AS rodada_rod_rodada,
            rodada.rod_sequencia AS rodada_rod_sequencia,
            rodada.estadio_est_id AS rodada_estadio_est_id,
            estadio.est_nome AS est_nome,
            rodada.rod_data AS rodada_rod_data,

            rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
            clube_mandante.clu_nome AS clu_nome_mandante,
            clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
            COALESCE(rodada.rod_gols_mandante, NULL) AS rodada_rod_gols_mandante,
            COALESCE(rodada.rod_pontos_mandante, NULL) AS rodada_rod_pontos_mandante,

            rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
            clube_visitante.clu_nome AS clu_nome_visitante,
            clube_visitante.clu_link_escudo AS clu_link_escudo_visitante,
            COALESCE(rodada.rod_gols_visitante, NULL) AS rodada_rod_gols_visitante,
            COALESCE(rodada.rod_pontos_visitante, NULL) AS rodada_rod_pontos_visitante,

            cartao_mandante.car_qtd_vermelho AS cartoes_vermelhos_mandante,
            cartao_mandante.car_qtd_amarelo AS cartoes_amarelos_mandante,
            cartao_visitante.car_qtd_vermelho AS cartoes_vermelhos_visitante,
            cartao_visitante.car_qtd_amarelo AS cartoes_amarelos_visitante,

            rodada.rod_partida_finalizada AS rodada_rod_partida_finalizada,
            rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao
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
                rod_gols_mandante=jogo.rodada_rod_gols_mandante if jogo.rodada_rod_gols_mandante != "" else None,
                rod_pontos_mandante=jogo.rodada_rod_pontos_mandante if jogo.rodada_rod_pontos_mandante != "" else None,
                
                clube_clu_sigla_visitante=jogo.rodada_clube_clu_sigla_visitante,
                clu_nome_visitante=jogo.clu_nome_visitante,
                clu_link_escudo_visitante=jogo.clu_link_escudo_visitante,
                rod_gols_visitante=jogo.rodada_rod_gols_visitante if jogo.rodada_rod_gols_visitante != "" else None,
                rod_pontos_visitante=jogo.rodada_rod_pontos_visitante if jogo.rodada_rod_pontos_visitante != "" else None,

                car_qtd_vermelho_mandante=jogo.cartoes_vermelhos_mandante,
                car_qtd_amarelo_mandante=jogo.cartoes_amarelos_mandante,
                car_qtd_vermelho_visitante=jogo.cartoes_vermelhos_visitante,
                car_qtd_amarelo_visitante=jogo.cartoes_amarelos_visitante,

                rod_partida_finalizada=jogo.rodada_rod_partida_finalizada,
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
                    rod_partida_finalizada = :rod_partida_finalizada,
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
                "rod_partida_finalizada": jogo.rod_partida_finalizada,
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
          AND rod_partida_finalizada = 'S'
          AND rod_calculou_classificacao = 'N'
    """

    if carrega_nao_realizados:
        sql_query_rodadas += " AND rod_rodada <= :rodada"
    else:
        sql_query_rodadas += " AND rod_rodada = :rodada"

    sql_query_rodadas += " order by rod_serie, rod_ano, rod_rodada, rod_sequencia"

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
            serie=serie,
            ano=ano,
            sigla=partida.clube_clu_sigla_mandante,
            pontos=partida.rod_pontos_mandante,
            gols_pro=partida.rod_gols_mandante,
            gols_contra=partida.rod_gols_visitante,
            qtd_jogou=1,
            venceu=partida.rod_gols_mandante > partida.rod_gols_visitante,
            empatou=partida.rod_gols_mandante == partida.rod_gols_visitante
        )

        processar_time(
            db=db,
            serie=serie,
            ano=ano,
            sigla=partida.clube_clu_sigla_visitante,
            pontos=partida.rod_pontos_visitante,
            gols_pro=partida.rod_gols_visitante,
            gols_contra=partida.rod_gols_mandante,
            qtd_jogou=1,
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
                  AND rod_partida_finalizada = 'S'
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
    serie: str,
    ano: int,
    sigla: str,
    pontos: int,
    gols_pro: int,
    gols_contra: int,
    qtd_jogou: int,
    venceu: bool,
    empatou: bool
):
    """
    Processa a classificação de um time (mandante ou visitante),
    atualizando ou criando o registro na tabela 'classificacao_geral'.

    Args:
        db (Session): Sessão ativa do banco de dados.
        serie (str): Série do campeonato (ex: 'A', 'B').
        ano (int): Ano da competição.
        sigla (str): Sigla do clube.
        pontos (int): Pontos a serem somados.
        gols_pro (int): Gols feitos (pro).
        gols_contra (int): Gols sofridos (contra).
        venceu (bool): Indicador se venceu a partida.
        empatou (bool): Indicador se empatou a partida.
    """
    # Verificar se o clube já está na tabela classificacao_geral  
    classificacao = db.execute(
        text("""
            SELECT * FROM classificacao_geral
            WHERE clg_serie = :serie 
              and clg_ano = :ano 
              and clube_clu_sigla = :sigla
        """),
        {"sigla": sigla, "serie": serie, "ano": ano}
    ).fetchone()

    if classificacao:
        # Atualizar os valores
        db.execute(
            text("""
                UPDATE classificacao_geral
                SET clg_pontos = clg_pontos + :pontos,
                    clg_qtd_jogou = clg_qtd_jogou + :qtd_jogou,
                    clg_vitorias = clg_vitorias + :vitorias,
                    clg_qtd_empates = clg_qtd_empates + :empates,
                    clg_qtd_derrotas = clg_qtd_derrotas + :derrotas,
                    clg_gols_pro = clg_gols_pro + :gols_pro,
                    clg_gols_contra = clg_gols_contra + :gols_contra,
                    clg_saldo_gols = clg_saldo_gols + :saldo
                WHERE clg_serie = :serie 
                  and clg_ano = :ano 
                  and clube_clu_sigla = :sigla
            """),
            {
                "serie": serie,
                "ano": ano,
                "pontos": pontos,
                "qtd_jogou": qtd_jogou,
                "vitorias": 1 if venceu else 0,
                "empates": 1 if empatou else 0,
                "derrotas": 1 if not venceu and not empatou else 0,
                "gols_pro": gols_pro,
                "gols_contra": gols_contra,
                "saldo": gols_pro - gols_contra,
                "sigla": sigla
            }
        )
    else:
        # Inserir novo registro para o clube
        db.execute(
            text("""
                INSERT INTO classificacao_geral (
                    clg_serie, clg_ano, clg_pontos, clg_vitorias, clg_saldo_gols,
                    clg_gols_pro, clg_confronto_direto, clube_clu_sigla, clg_qtd_jogou,clg_qtd_empates,
                    clg_qtd_derrotas, clg_gols_contra
                )
                VALUES (
                    :serie, :ano, :pontos, :vitorias, :saldo, 
                    :gols_pro, 0, :sigla, :qtd_jogou, :empates, 
                    :derrotas, :gols_contra
                )
            """),
            {
                "serie": serie,
                "ano": ano,
                "pontos": pontos,
                "vitorias": 1 if venceu else 0,
                "saldo": gols_pro - gols_contra,
                "gols_pro": gols_pro,
                "clg_confronto_direto": 0,
                "sigla": sigla,
                "qtd_jogou": qtd_jogou,
                "empates": 1 if empatou else 0,
                "derrotas": 1 if not venceu and not empatou else 0,
                "gols_contra": gols_contra
            }
        )


def lista_classificacao_geral(db: Session, serie: str, ano: int) -> list:
    """
    Retorna a lista de classificação geral com base na série e ano fornecidos.

    Args:
        db (Session): Sessão ativa do banco de dados.
        serie (str): Série do campeonato (A ou B).
        ano (int): Ano da competição.

    Returns:
        list: Lista de classificações ordenada segundo os critérios definidos.
    """
    # Garantir que a série está em maiúsculo
    serie_upper = serie.upper()
    consiste_serie(serie.upper())

    # Executar a query SQL para extrair os dados de classificação
    sql_query = """
    SELECT cg.clube_clu_sigla,
           clube.clu_nome,
           clube.clu_link_escudo,
           cg.clg_pontos,  
           cg.clg_qtd_jogou,
           cg.clg_vitorias, 
           cg.clg_qtd_empates,
           cg.clg_qtd_derrotas,
           cg.clg_gols_pro,
           cg.clg_gols_contra, 
           cg.clg_saldo_gols,  
           cartao.car_qtd_amarelo,
           cartao.car_qtd_vermelho 
    FROM classificacao_geral cg 
    JOIN cartao AS cartao ON
        cg.clg_serie = cartao.car_serie AND
        cg.clg_ano = cartao.car_ano AND
        cg.clube_clu_sigla = cartao.clube_clu_sigla 
    JOIN clube AS clube ON
        cg.clube_clu_sigla = clube.clu_sigla 	
    WHERE cg.clg_serie = :serie AND cg.clg_ano = :ano
    ORDER BY cg.clg_pontos DESC, 
             cg.clg_vitorias DESC, 
             cg.clg_saldo_gols DESC, 
             cg.clg_gols_pro DESC, 
             cartao.car_qtd_vermelho ASC,
             cartao.car_qtd_amarelo ASC
    """

    resultados = db.execute(text(sql_query), {"serie": serie_upper, "ano": ano}).fetchall()

    # Verificar se existem resultados
    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma classificação encontrada para a série '{serie_upper}' e ano '{ano}'."
        )

    # Montar a resposta em um formato de lista de dicionários
    ordem_classificacao = 0
    classificacao = []
    for resultado in resultados:
        classificacao.append(
            ResponseClassificacaoGeralListaSchema(
                ordem_classificacao=ordem_classificacao + 1,
                clube_clu_sigla=resultado.clube_clu_sigla,
                clu_nome=resultado.clu_nome,
                clu_link_escudo=resultado.clu_link_escudo,
                clg_pontos=resultado.clg_pontos,
                clg_qtd_jogou=resultado.clg_qtd_jogou,
                clg_vitorias=resultado.clg_vitorias,
                clg_qtd_empates=resultado.clg_qtd_empates,
                clg_qtd_derrotas=resultado.clg_qtd_derrotas,
                clg_gols_pro=resultado.clg_gols_pro,
                clg_gols_contra=resultado.clg_gols_contra,
                clg_saldo_gols=resultado.clg_saldo_gols,
                car_qtd_amarelo=resultado.car_qtd_amarelo,
                car_qtd_vermelho=resultado.car_qtd_vermelho
            )
        )

    return classificacao